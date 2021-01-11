#!/usr/bin/env python python2.7
# coding:utf-8
"""
文件上传
"""
import logging
import requests
import os
import subprocess
import time
import redis
import hashlib
from datetime import datetime
from uncompase import config, REDIS_HOST, UPLOAD_SUCCESS_CNT
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="run.log",
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [line:%(lineno)d] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

rds = redis.Redis(host=REDIS_HOST)
# 特殊字符列表
SIGN = [' ', '$', '&', '*', '|', "(", ")", '~', "'", '"']
# 上传失败文件存放路径
PATH = "/test_zhanlun/ce"
# 文件循环时间
UPLOAD_TIME = 10

def get_date():
    # 获取时间
    return datetime.now().strftime("%Y%m%d")

def get_file_type(fname):
    """
    获得文件类型
    :param fname: 包含文件名的绝对路径
    :return: 文件类型
    """
    cmd = "file %s | awk '{print $2}'" % (fname)
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc.wait()
        file_type = proc.stdout.read().strip()
        return file_type
    except Exception as e:
        logging.exception('get_type {} failed')
        
def get_md5(file_path):
    md5_obj = hashlib.md5()
    with open(file_path, 'rb')as f:
        while True:
            d = f.read(8096)
            if not d:
                break
            md5_obj.update(d)
    hash_code = md5_obj.hexdigest()
    md5 = str(hash_code).lower()
    return md5
    
def escape(filepath):
    """
    对含有特殊符号的文件夹进行转义
    :param filepath: 文件路径
    :return: 文件路径
    """
    for i in SIGN:
        if i in filepath:
            filepath = filepath.replace(i, "\%s" % i)
    return filepath
    
def copy_file(thepath, path, type_resouce):
    """
    将PE文件复制到指定目录
    :param thepath: 文件原始路径
    :param PATH: 文件复制路径
    :return: 
    """
    file_md5 = os.path.split(thepath)[-1]
    m_file_name = "".join([type_resouce,"__",file_md5])
    tpath = os.path.join(PATH, m_file_name)
    if os.path.exists(tpath):
        return ""
    try:
        thepath = escape(thepath)
        cmd = 'cp %s %s' % (thepath, tpath)
        proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
        if (PATH and proc):
            proc.communicate()
            isfailed = proc.returncode
            if (isfailed):
                logger.warning(" copy %s failed !" % (thepath))
    except Exception, e:
        logger.warning(e)
        
def upload_one_file(fpath):
    """
    将文件上传
    :param fpath: 文件保存路径
    :return:
    """
    date = get_date()
    fname = os.path.split(fpath[0])[-1]
    logging.info("begin upload {}".format(fname))
    file_type = get_file_type(fpath[0])
    
    if file_type.startswith("PE"):
        type_code = 2
    elif file_type.startswith("ELF"):
        type_code = 18
    else:
        return
    try:
        f = open(fpath[0], 'rb')
        md5 = get_md5(fpath[0])
        data = {'md5': md5, 'attr': 1, 'source_type': fpath[1], 'operator': 'zhanlun', 'desc': '',
                'file_type': type_code}
        # url = 'http://172.29.71.21:8000/api/v1/sample_upload'
        url = 'http://filecld-taskdb-update-1.novalocal:8000/api/v1/sample_upload'
        file = {'file': (fname, f)}
        res = requests.post(url, data=data, files=file)
        logging.info("upload {} result is{}".format(fname, res.content))
        rds.incr(UPLOAD_SUCCESS_CNT.format(date=date, source=fpath[1]))
        copy_file(fpath[0], PATH, fpath[1])
    except Exception:
        copy_file(fpath, PATH, fpath[1])
        logging.exception("upload {} failed".format(fpath[0]))
    finally:
        f.close()

def mutliprocess_unload_file(file_path, source_type):
    """
    多进程上传
    :param file_path: 文件路径
    :param source_type: 文件源
    :return:
    """
    files = os.listdir(file_path)
    file_list = []
    # 封装数据格式用于传递参数
    for name in files:
        path = os.path.join(file_path, name)
        file_list.append([path, source_type])

    with ProcessPoolExecutor() as pool:
        pool.map(upload_one_file, file_list)

def run():
    while True:
        config_dic = config()
        for type_resouce in config_dic:
            mutliprocess_unload_file(config_dic[type_resouce]["fin_path"], type_resouce)
        time.sleep(UPLOAD_TIME)


if __name__ == "__main__":
    run()


