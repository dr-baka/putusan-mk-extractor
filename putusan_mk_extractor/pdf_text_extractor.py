import fitz  # PyMuPDF
import easyocr
from PIL import Image
import io
import re


class PDFTextExtractor:
    def __init__(self, pdf_path: str, use_gpu=True, is_putusan=False):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.reader = easyocr.Reader(['id'], gpu=use_gpu)  # Gunakan GPU
        self.grouped = []
        self.formatted_text = ""
        self.is_putusan = is_putusan

    def _extract_text_or_ocr(self, page):
        """Gunakan teks langsung jika tersedia, jika tidak gunakan EasyOCR dengan GPU + grayscale."""
        text = page.get_text("text").strip()
        if text:
            return text

        # Render halaman ke gambar (pixmap), konversi ke PIL Image
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # ✅ Konversi ke grayscale
        img_gray = img.convert("L")  # mode "L" = grayscale

        # ✅ Konversi ke NumPy array untuk EasyOCR
        import numpy as np
        img_np = np.array(img_gray)

        # OCR dengan EasyOCR
        results = self.reader.readtext(img_np, detail=0)
        return "\n".join(results).strip()
    
    
    def extract_grouped_content(self):
        for page in self.doc:
            page_text = self._extract_text_or_ocr(page)
            lines = page_text.splitlines()
            header, content, footer = [], [], []
            state = "header"

            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue

                if state == "header":
                    header.append(stripped)
                    if "putusan.mahkamahagung.go.id" in stripped.lower():
                        state = "content"
                        self.is_putusan = True
                elif state == "content":
                    if "disclaimer" in stripped.lower():
                        footer.append(stripped)
                        state = "footer"
                    else:
                        content.append(stripped)
                else:
                    footer.append(stripped)

            self.grouped.append({
                "header": header,
                "content": content,
                "footer": footer
            })
        return self

    def format_content(self):
        all_content = []
        for page in self.grouped:
            if self.is_putusan:
                all_content.extend(page["content"])
            else:
                # Jika bukan putusan, ambil semua konten
                all_content.extend(page["header"])
                

        result = []
        buffer = []
        inside_identity_block = False

        for line in all_content:
            stripped = line.strip()
            if not stripped:
                continue

            if stripped.startswith("Terdakwa 1") or stripped.startswith("Terdakwa 2"):
                if buffer:
                    result.append("\n".join(buffer))
                    buffer = []
                inside_identity_block = True
                buffer.append(stripped)
                continue

            if inside_identity_block:
                if (
                    re.match(r"^\d+\.\s", stripped) or
                    stripped.startswith(":") or
                    re.match(r"^(Kecamatan|Provinsi|: )", stripped) or
                    re.match(r"^[A-Z][a-z]+(?: [A-Z][a-z]+)* :", stripped)
                ):
                    buffer.append(stripped)
                    continue
                else:
                    result.append("\n".join(buffer))
                    buffer = []
                    inside_identity_block = False

            if not inside_identity_block:
                result.append(stripped)

        if buffer:
            result.append("\n".join(buffer))

        self.formatted_text = "\n\n".join(result)
        return self

    def save_to(self, output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(self.formatted_text)
        print(f"✅ Formatted content saved to: {output_path}")
        return self
