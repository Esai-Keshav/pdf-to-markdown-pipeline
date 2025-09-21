# PDF-to-Markdown Conversion Pipeline

## Overview

`pdf-to-markdown-pipeline` : this project aims to develop a system that automatically converts any PDF file into a well-
structured Markdown file (.md). The output must preserve headings, paragraphs, lists, figures,
tables, and document hierarchy.

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/pdf-to-markdown-pipeline.git
   cd pdf-to-markdown-pipeline

   ```

2. **Install PyTorch**

   Follow the official installation instructions based on your OS, Python version, and whether you want CPU or GPU support:

   [PyTorch Installation Guide](https://pytorch.org/get-started/locally/)

   Example (CPU-only):

   ```bash
   pip install torch torchvision torchaudio

   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

This project provides **two approaches** to convert PDFs to Markdown:

### 1. `pipeline.py` – Docling-based pipeline

- Uses [Docling](https://github.com/DS4SD/docling) as the base engine.
- Handles:
  - Nested lists
  - Image extraction (referenced or embedded)
  - PDF page/image scaling

**Run the pipeline:**

```bash
python pipeline.py

```

### 2. `approach_2.py` – Custom-built pipeline

- Fully **built from scratch** without Docling.
- Allows more control over:

  - OCR (via `doctr`)
  - Table extraction (via `camelot`)
  - Image processing (via `Pillow` and `PyMuPDF`)

- Useful for custom PDF layouts or specialized workflows.

**Run the custom pipeline:**

```bash
python approach_2.py

```
