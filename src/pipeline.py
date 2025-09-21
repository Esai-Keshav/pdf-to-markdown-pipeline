from pathlib import Path
import logging

import time
import re

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling_core.types.doc import ImageRefMode


def fix_nested_lists(md: str) -> str:
    """
    Fix nested list formatting in Markdown by replacing '  - ...'
    with proper indented levels (2 spaces per depth).
    Example:
        '  - Item'   -> '  - Item'
        '    -    Item' -> '    - Item'
    """

    def replacer(match):
        dashes = match.group(0).split()
        depth = len(dashes) - 1  # first '-' is level 1
        return " " * depth + "- "

    return re.sub(r"(?:- )+", replacer, md)


def convert_pdf_with_nested_lists(pdf_path: str, output_dir: str):
    logging.basicConfig(level=logging.INFO)

    input_path = Path(pdf_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Pipeline options
    pipeline_options = PdfPipelineOptions()
    pipeline_options.images_scale = 2.0
    pipeline_options.generate_page_images = True
    pipeline_options.generate_picture_images = True

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    start_time = time.time()
    result = converter.convert(input_path)
    doc = result.document

    # Markdown with external image refs (nested lists preserved)
    md_ref = out_dir / (input_path.stem + "-nested-ref.md")
    # md_ref.replace("  -", "  -")
    text_ref = doc.export_to_markdown(
        image_mode=ImageRefMode.REFERENCED,
        # indent=4,  # spaces for nested list indentation
    )

    # pprint(text_ref)
    # md_ref.write_text(text_ref, encoding="utf-8")

    # Markdown with embedded images (base64)
    md_emb = out_dir / (input_path.stem + "-nested-embedded.md")
    text_emb = doc.export_to_markdown(image_mode=ImageRefMode.EMBEDDED, indent=4)
    text_emb = text_emb.replace("- -", "  - ")
    md_emb.write_text(text_emb, encoding="utf-8")

    logging.info(f"Converted in {time.time() - start_time:.2f} seconds.")
    # print("✅ Markdown with refs:", md_ref)
    print("✅ Markdown with embedded images:", md_emb)


if __name__ == "__main__":
    # input_file = "../examples/img.pdf"
    # output_dir = "../output"

    input_file = "../examples/Esai Keshav.pdf"
    output_dir = "../output"

    # convert_pdf_with_nested_lists("./Esai Keshav.pdf", "output")
    convert_pdf_with_nested_lists(input_file, output_dir)
