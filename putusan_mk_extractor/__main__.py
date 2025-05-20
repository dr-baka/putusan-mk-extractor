import argparse
from pathlib import Path
from putusan_mk_extractor.pdf_text_extractor import PDFTextExtractor
from putusan_mk_extractor.text_cleaner import TextCleaner

def main():
    parser = argparse.ArgumentParser(description="Ekstraksi & pembersihan teks dari PDF putusan MA/MK.")
    parser.add_argument("--input", required=True, help="Path ke file PDF input.")
    parser.add_argument("--output", required=True, help="Path ke file teks output yang telah dibersihkan.")

    args = parser.parse_args()

    input_pdf = args.input
    cleaned_output = args.output
    intermediate_output = Path(cleaned_output).with_name("raw.txt")

    # Langkah 1: Ekstraksi teks mentah dari PDF
    (
        PDFTextExtractor(input_pdf)
        .extract_grouped_content()
        .format_content()
        .save_to(intermediate_output)
    )

    # Langkah 2: Pembersihan dan formatting teks
    (
        TextCleaner.from_file(intermediate_output)
        .clean_newlines_and_bullets()
        .join_sentences()
        .fix_ordering()
        .fix_page_headers()
        .to_file(cleaned_output)
    )

    print(f"✅ Berhasil! Hasil akhir disimpan di: {cleaned_output}")

if __name__ == "__main__":
    main()
