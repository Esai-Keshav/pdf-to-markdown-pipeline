# PDF-to-Markdown Conversion Report

## 1. Architecture Overview

The project provides **two approaches** for converting PDFs to Markdown:

### 1.1 Docling-based Pipeline (`pipeline.py`)

- **Core Engine:** [Docling](https://github.com/DS4SD/docling)
- **Responsibilities:**

  - Text extraction
  - Heading inference (via font-size quantization)
  - Nested list detection
  - Table extraction
  - Image extraction (page-level or picture-level)

- **Output:** Markdown files with either referenced images or embedded Base64 images.
- **Advantages:** Quick setup, robust for machine-generated PDFs.

### 1.2 Custom-built Pipeline (`approach_2.py`)

- **Core Components:**

  - OCR: [python-doctr](https://github.com/mindee/doctr)
  - PDF processing: [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
  - Table extraction: [Camelot](https://camelot-py.readthedocs.io/en/master/)
  - Image processing: [Pillow](https://pillow.readthedocs.io/en/stable/)

- **Responsibilities:**

  - Full OCR on scanned PDFs
  - Custom text block and table detection
  - Fine-grained image extraction and embedding

- **Output:** Markdown with embedded or referenced images, custom table formatting.
- **Advantages:** Fully customizable, suitable for scanned or complex PDFs.

---

## 2. Pipeline Stages

| Stage                          | Docling Pipeline                                   | Custom Pipeline                                               |
| ------------------------------ | -------------------------------------------------- | ------------------------------------------------------------- |
| **Input**                      | PDF file                                           | PDF file                                                      |
| **Pre-processing**             | Optional page scaling, image generation            | PDF page extraction, image preprocessing                      |
| **Text Extraction**            | Font-size quantization for headings, text blocks   | OCR via Doctr                                                 |
| **List & Structure Detection** | Detect nested lists, indentation                   | Custom parsing of bullet/numbered lists                       |
| **Table Extraction**           | Tables via Docling parser                          | Tables via Camelot (lattice/stream)                           |
| **Image Extraction**           | Page images, figure images                         | Extracted via PyMuPDF & Pillow, optionally embedded as Base64 |
| **Markdown Export**            | `export_to_markdown()` with `ImageRefMode` options | Custom Markdown generation script                             |
| **Output**                     | Markdown files with referenced or embedded images  | Markdown files with referenced or embedded images             |

---
