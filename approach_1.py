from pathlib import Path
import logging
import time

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling_core.types.doc import ImageRefMode


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
    text_ref = doc.export_to_markdown(
        image_mode=ImageRefMode.REFERENCED,
        indent=4,  # spaces for nested list indentation
    )
    md_ref.write_text(text_ref, encoding="utf-8")

    # Markdown with embedded images (base64)
    md_emb = out_dir / (input_path.stem + "-nested-embedded.md")
    text_emb = doc.export_to_markdown(image_mode=ImageRefMode.EMBEDDED, indent=4)
    md_emb.write_text(text_emb, encoding="utf-8")

    logging.info(f"Converted in {time.time() - start_time:.2f} seconds.")
    print("✅ Markdown with refs:", md_ref)
    print("✅ Markdown with embedded images:", md_emb)


if __name__ == "__main__":
    input_file = "./test.pdf"
    output_dir = "output"
    # convert_pdf_with_nested_lists("./Esai Keshav.pdf", "output")
    convert_pdf_with_nested_lists(input_file, output_dir)
