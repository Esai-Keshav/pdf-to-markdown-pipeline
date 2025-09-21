import fitz  # PyMuPDF
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from PIL import Image
import os
import camelot

# ------------------------ OCR Model ------------------------
ocr_model = ocr_predictor(pretrained=True)


# ------------------------ Extract Tables with Camelot ------------------------
def extract_tables(pdf_path, page_num):
    """
    Extract tables from a PDF page using Camelot and return Markdown string
    """
    tables_md = []
    try:
        # Camelot uses 1-based page numbers
        tables = camelot.read_pdf(pdf_path, pages=str(page_num + 1), flavor="stream")

        for table in tables:
            df = table.df.fillna("")  # replace None
            md_table = "| " + " | ".join(df.iloc[0]) + " |"
            md_table += "\n| " + " | ".join(["---"] * len(df.iloc[0])) + " |"

            for row in df.iloc[1:].values:
                row_str = [str(cell) if cell else "" for cell in row]
                md_table += "\n| " + " | ".join(row_str) + " |"

            tables_md.append(md_table)
    except Exception as e:
        print(f"⚠️  Table extraction failed on page {page_num + 1}: {e}")
        tables_md.append("```\n# Table extraction failed - please inspect\n```")

    return "\n\n".join(tables_md)


# ------------------------ Extract Figures ------------------------
def extract_figures(pdf_path, page_num, out_dir="figures"):
    """Extract images from PDF page and save as PNG"""
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    page = doc[page_num]

    figs = []
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)

        # Convert to RGB if necessary
        if pix.n > 3:
            pix = fitz.Pixmap(fitz.csRGB, pix)

        img_path = os.path.join(out_dir, f"page{page_num}_img{img_index}.png")
        pix.save(img_path)
        figs.append(img_path)

    return figs


# ------------------------ Extract Text with Doctr OCR ------------------------
def extract_text_with_ocr(pdf_path, page_num):
    """Extract text from PDF page using Doctr OCR"""
    doc = DocumentFile.from_pdf(pdf_path)
    page = doc[page_num : page_num + 1]  # single page
    result = ocr_model(page)
    text = result.render()
    return text


# ------------------------ PDF to Markdown ------------------------
def pdf_to_md(pdf_path, md_path):
    doc = fitz.open(pdf_path)
    md_output = []

    for i in range(len(doc)):
        md_output.append(f"# Page {i + 1}\n")

        # 1. Text (OCR)
        text = extract_text_with_ocr(pdf_path, i)
        if text.strip():
            md_output.append(text)

        # 2. Tables
        tables = extract_tables(pdf_path, i)
        if tables:
            md_output.append("## Tables\n" + tables)

        # 3. Figures
        figs = extract_figures(pdf_path, i)
        if figs:
            md_output.append("## Figures")
            for fig in figs:
                md_output.append(f"![figure]({fig})")

    # Save final Markdown
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(md_output))

    print(f"✅ Markdown exported to {md_path}")


# ------------------------ Run ------------------------
if __name__ == "__main__":
    pdf_to_md("./test.pdf", "output.md")
