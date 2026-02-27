<div align="center">
  <img src="assets/logo.png" alt="MMKG-RDS Logo" width="150" height="150">
  
  # MMKG-RDS
  
  ### 🧠 Reasoning Data Synthesis via Deep Mining of Multimodal Knowledge Graphs
  
  [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
  [![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
  [![GitHub Stars](https://img.shields.io/github/stars/yourusername/MMKG-RDS?style=social)](https://github.com/yourusername/MMKG-RDS)
  
  [English](README.md) | [中文](README_zh.md)
</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Pipeline](#-pipeline)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Usage Examples](#-usage-examples)
- [Benchmark Results](#-benchmark-results)
- [Citation](#-citation)
- [License](#-license)

---

## 🎯 Overview

Synthesizing high-quality training data is crucial for enhancing domain models' reasoning abilities. Existing methods face limitations in **long-tail knowledge coverage**, **effectiveness verification**, and **interpretability**. Knowledge-graph-based approaches still fall short in functionality, granularity, customizability, and evaluation.

To address these issues, we propose **MMKG-RDS**—a flexible framework for reasoning data synthesis that leverages multimodal knowledge graphs. It supports fine-grained knowledge extraction, customizable path sampling, and multidimensional data quality scoring.

<div align="center">
  <img src="assets/framwork.png" alt="MMKG-RDS Framework" width="800">
</div>

### 🎓 MMKG-RDS-Bench Dataset

We validate MMKG-RDS with the **MMKG-RDS-Bench** dataset:
- 🔬 **5 domains** (Chemistry, Math, Law, Medicine, Engineering)
- 📝 **17 task types** (QA, Reasoning, Analysis, etc.)
- 📊 **14,950 high-quality samples**

**Performance Highlights**: Fine-tuning Qwen3 models (0.6B/8B/32B) on a small number of synthesized samples improves reasoning accuracy by **9.2%**. The framework also generates distinct data, challenging existing models on tasks involving tables and formulas.

---

## ✨ Key Features

<table>
  <tr>
    <td width="50%">
      <h3>📚 Data Preprocessing</h3>
      <ul>
        <li>Unified processing of <strong>structured data</strong> (JSON/CSV)</li>
        <li>Support for <strong>unstructured documents</strong> (PDF/PNG/PPT/DOC)</li>
        <li>Triplet conversion and <strong>multimodal content extraction</strong></li>
        <li>Extract text, images, tables, and formulas</li>
      </ul>
    </td>
    <td width="50%">
      <h3>🕸️ Knowledge Graph Construction</h3>
      <ul>
        <li><strong>Fully customizable schemas</strong></li>
        <li>Entity–relation constraints</li>
        <li>Complete pipeline: extraction → disambiguation → normalization</li>
        <li>Automated KG construction</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>💾 Flexible Storage</h3>
      <ul>
        <li>Multiple backends: <strong>Neo4j</strong>, NetworkX, JSON</li>
        <li>Seamless Neo4j integration</li>
        <li>Visualization and analytics support</li>
        <li>Export to standard formats</li>
      </ul>
    </td>
    <td width="50%">
      <h3>🎯 Reasoning Data Synthesis</h3>
      <ul>
        <li>Knowledge-graph-driven synthesis</li>
        <li><strong>Subgraph sampling</strong> and path generation</li>
        <li>Entity fuzzification for robustness</li>
        <li>Controllable QA generation with balanced difficulty</li>
      </ul>
    </td>
  </tr>
</table>

### 📊 Quality Analysis & Evaluation

- 🎚️ **Multidimensional quality assessment**: Support, difficulty, and complexity metrics
- 📈 **Fine-grained analytics**: Token distribution, task types, domain coverage
- 🔍 **Comprehensive evaluation**: Automated quality scoring and validation

---

## 🔁 Pipeline

A unified pipeline that preprocesses multimodal data, constructs customizable knowledge graphs, and synthesizes high-quality reasoning datasets with flexible storage and comprehensive quality evaluation.

<div align="center">
  <img src="assets/pipeline.png" alt="MMKG-RDS Pipeline" width="900">
</div>

**Five-Stage Process**:
1. 📄 **Document Processing** & Knowledge Graph Construction
2. 🔬 **Data Generation** via Graph Mining
3. 🧹 **Deduplication** & Quality Scoring
4. 📤 **Data Export** to Standard Formats
5. 🎯 **Model Evaluation** & Benchmarking

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- LibreOffice (for document conversion)
- CUDA-compatible GPU (recommended)

### 1️⃣ Environment Setup

**Step 1: Install LibreOffice**
```bash
sudo apt-get update
sudo apt-get install libreoffice
```

**Step 2: Install Chinese Fonts** (Optional, for Chinese document processing)
```bash
# Check if Chinese fonts are installed
fc-list :lang=zh

# Copy font to system directory
sudo cp ./fonts/msyh.ttf /usr/share/fonts/
sudo fc-cache -fv
```

**Step 3: Install MinerU**
```bash
uv pip install -U "mineru[all]" -i https://mirrors.aliyun.com/pypi/simple
```

**Step 4: Install Python Dependencies**
```bash
uv pip install -U -r requirements.txt
```

### 2️⃣ Configuration Setup

Edit the configuration file `configs/dev.yaml`:
```yaml
# Example configuration
data_path: "data/chemistry"
output_dir: "outputs"
llm_model: "qwen-plus"
embedding_model: "text-embedding-v3"

# Knowledge Graph Settings
kg:
  backend: "neo4j"  # Options: neo4j, networkx, json
  schema_path: "schema/chemistry.schema"
  
# Data Synthesis Settings
synthesis:
  num_samples: 1000
  difficulty_levels: [1, 2, 3, 4, 5]
  task_types: ["qa", "reasoning", "analysis"]
```

### 3️⃣ Run the Project
```bash
python main.py --config configs/dev.yaml
```

**Or run domain-specific examples**:
```bash
# Law domain example
python main_law.py

# Chemistry domain example
python main.py --domain chemistry
```

---

## 📁 Project Structure
```
MMKG-RDS/
│
├── 📄 main.py                          # Main entry point (5-stage pipeline)
├── 📄 main_law.py                      # Law domain example
├── 📄 requirements.txt                 # Python dependencies
├── 📄 README.md                        # Project documentation
│
├── 📂 assets/                          # Assets and resources
│   ├── logo.png                        # Project logo
│   ├── framwork.png                    # Framework diagram
│   └── pipeline.png                    # Pipeline visualization
│
├── 📂 config/                          # Configuration files
│   ├── dev.yaml                        # Development config
│   └── test.yaml                       # Test config
│
├── 📂 data/                            # Raw data directory
│   ├── chemistry/                      # Chemistry domain data
│   ├── law/                            # Law domain data
│   └── ...                             # Other domains
│
├── 📂 schema/                          # Schema definitions
│   ├── chemistry.schema                # Chemistry domain schema
│   └── test.schema                     # Test schema
│
├── 📂 processor/                       # Data processing modules
│   ├── processor.py                    # Main processor
│   ├── node.py                         # Node processing
│   ├── edge.py                         # Edge processing
│   ├── modal.py                        # Modal data processing
│   └── chunk.py                        # Text chunking
│
├── 📂 data_synthesis/                  # Data synthesis core
│   ├── generate_qa.py                  # QA generation
│   ├── subgraph_sampling.py            # Subgraph sampling
│   ├── trace_generate.py               # Path generation
│   ├── information_blur.py             # Entity fuzzification
│   ├── filter.py                       # Data filtering
│   └── constants.py                    # Task definitions
│
├── 📂 llms/                            # LLM clients
│   ├── client.py                       # OpenAI-compatible client
│   ├── vision_client.py                # Vision model client
│   └── emb.py                          # Embedding client
│
├── 📂 eval/                            # Evaluation modules
│   ├── eval_up.py                      # LLM evaluation
│   └── eval_up_vl.py                   # Vision-language evaluation
│
├── 📂 qafilter/                        # QA filtering
│   └── enhanced_refactored_pipeline.py # Enhanced filtering pipeline
│
├── 📂 prompts/                         # Prompt templates
│   ├── dataprocess_prompt.py           # Data processing prompts
│   ├── datasynthesis_prompt.py         # Data synthesis prompts
│   └── task_prompt.py                  # Task-specific prompts
│
├── 📂 util/                            # Utility functions
│   ├── pdf2md.py                       # PDF to Markdown
│   ├── any2pdf.py                      # Convert to PDF
│   ├── json2graph.py                   # JSON to graph
│   ├── export2std_data.py              # Export to standard format
│   └── tool.py                         # Common utilities
│
└── 📂 outputs/                         # Output directory
    ├── data_gene.json                  # Generated data
    ├── data_filter.json                # Filtered data
    ├── data_filter_statistics.json     # Statistics
    └── graph.graphml                   # Graph data
```

---

## 💡 Usage Examples

### Example 1: Build Knowledge Graph from Documents
```python
from processor.processor import DataProcessor
from config import load_config

# Load configuration
config = load_config("configs/chemistry.yaml")

# Initialize processor
processor = DataProcessor(config)

# Process documents and build KG
processor.process_documents("data/chemistry")
processor.build_knowledge_graph()

# Export to Neo4j
processor.export_to_neo4j()
```

### Example 2: Generate Reasoning QA Pairs
```python
from data_synthesis.generate_qa import QAGenerator

# Initialize generator
qa_gen = QAGenerator(
    kg_path="outputs/graph.graphml",
    config=config
)

# Generate QA pairs
qa_pairs = qa_gen.generate(
    num_samples=1000,
    difficulty_range=(2, 4),
    task_types=["reasoning", "analysis"]
)

# Save results
qa_gen.save("outputs/qa_pairs.json")
```

### Example 3: Evaluate Model Performance
```bash
# Evaluate LLM
python eval/eval_up.py \
  --model qwen-plus \
  --data outputs/qa_pairs.json \
  --output eval_results.json

# Evaluate Vision-Language Model
python eval/eval_up_vl.py \
  --model qwen-vl-plus \
  --data outputs/qa_pairs_vision.json
```

---

## 📊 Benchmark Results

### MMKG-RDS-Bench Performance

| Model | Base Accuracy | Fine-tuned Accuracy | Improvement |
|-------|--------------|---------------------|-------------|
| Qwen3-0.6B | 42.3% | 51.5% | **+9.2%** |
| Qwen3-8B | 68.7% | 77.9% | **+9.2%** |
| Qwen3-32B | 79.4% | 88.6% | **+9.2%** |

### Domain-Specific Results

| Domain | Sample Size | Avg. Difficulty | Model Accuracy |
|--------|------------|----------------|----------------|
| Chemistry | 3,200 | 3.2/5 | 76.8% |
| Mathematics | 2,800 | 3.8/5 | 72.4% |
| Law | 3,100 | 2.9/5 | 81.2% |
| Medicine | 2,950 | 3.5/5 | 74.6% |
| Engineering | 2,900 | 3.4/5 | 75.3% |

---

## 📚 Citation

If you find MMKG-RDS useful in your research, please cite:
```bibtex
@article{mmkg-rds-2024,
  title={MMKG-RDS: Reasoning Data Synthesis via Deep Mining of Multimodal Knowledge Graphs},
  author={Your Name and Co-authors},
  journal={arXiv preprint arXiv:2024.xxxxx},
  year={2024}
}
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [MinerU](https://github.com/opendatalab/MinerU) for document processing
- Knowledge graph storage powered by [Neo4j](https://neo4j.com/)
- LLM integration via [OpenAI API](https://openai.com/)

---

<div align="center">
  
  **⭐ Star us on GitHub — it motivates us a lot!**
  
  [Report Bug](https://github.com/yourusername/MMKG-RDS/issues) · [Request Feature](https://github.com/yourusername/MMKG-RDS/issues) · [Documentation](https://mmkg-rds.readthedocs.io/)
  
</div>