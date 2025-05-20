from putusan_mk_extractor.pdf_text_extractor import PDFTextExtractor
from pathlib import Path


input_pdf = "berkas_3TAHUN2025.pdf"
# cleaned_output = args.output
# intermediate_output = Path(cleaned_output).with_name("raw.txt")

# Langkah 1: Ekstraksi teks mentah dari PDF
(
    PDFTextExtractor(input_pdf)
    .extract_grouped_content()
    .format_content()
    .save_to("raw.txt")
)