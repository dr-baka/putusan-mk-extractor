from pathlib import Path
import re


class TextCleaner:
    bullet_regex = re.compile(r"""^(
        (\d{1,3}[\.\)])|              # 1. or 1)
        ([a-zA-Z][\.\)])|             # a. or A. or a) or A)
        ([ivxlcdmIVXLCDM]{1,5}[\.\)])|  # i. or iv)
        ([-•*])                       # -, •, *
    )\s+""", re.VERBOSE)

    halaman_pattern = re.compile(r"^Halaman \d+ dari \d+(?: Halaman)? Putusan Nomor .+")
    halaman_inline_pattern = re.compile(r"(?!^)(Halaman \d+ dari \d+(?: Halaman)? Putusan Nomor .+)")
    halaman_exact_pattern = re.compile(
        r"(Halaman \d+ dari \d+(?: Halaman)? Putusan Nomor .+?)(?=(Halaman \d+ dari \d+(?: Halaman)? Putusan Nomor |$))"
    )

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def from_file(cls, path: Path | str):
        if isinstance(path, str):
            path = Path(path) 
        with path.open("r", encoding="utf-8") as f:
            return cls(f.read())

    def to_file(self, path: Path | str):
        if isinstance(path, str):
            path = Path(path)
        with path.open("w", encoding="utf-8") as f:
            f.write(self.text)
        return self

    def remove_spaces(self):
        lines = self.text.splitlines()
        cleaned = [" ".join(word for word in line.split() if word.strip()) for line in lines]
        self.text = "\n".join(cleaned)
        return self

    def clean_newlines_and_bullets(self):
        lines = [line.strip() for line in self.text.splitlines()]
        cleaned_lines = []

        bullet = False
        for line in lines:
            if line:
                line = " ".join(word for word in line.split() if word.strip())
                if self.halaman_exact_pattern.search(line):
                    cleaned_lines.append(line)
                else:
                    if line == "-":
                        bullet = True
                    else:
                        cleaned_lines.append(f"- {line}" if bullet else line)
                        bullet = False

        self.text = "\n".join(cleaned_lines)
        return self

    def join_sentences(self):
        lines = self.text.splitlines()
        joined_lines = []
        sentence = ""

        for line in lines:
            if line and \
               line[-1] not in [".", "!", "?", ":", ";"] and \
               not self.bullet_regex.match(line) and \
               not self.halaman_exact_pattern.search(line) and \
               not line.startswith(": "):
                sentence += line.strip() + " "
            else:
                sentence += line.strip()
                joined_lines.append(sentence)
                sentence = ""

        self.text = "\n".join(joined_lines)
        return self

    def fix_ordering(self):
        lines = self.text.splitlines()
        ordered_lines = []

        for line in lines:
            if line:
                if line.startswith(": ") and ordered_lines and \
                   ordered_lines[-1] and not ordered_lines[-1].startswith("Halaman "):
                    ordered_lines[-1] += " " + line.strip()
                else:
                    ordered_lines.append(line)
            else:
                ordered_lines.append(line)

        self.text = "\n".join(ordered_lines)
        return self

    def fix_page_headers(self):
        lines = self.text.splitlines()
        output = []

        for line in lines:
            if self.halaman_inline_pattern.search(line):
                line = self.halaman_inline_pattern.sub(r"\n\n\1", line)
                output.extend(line.splitlines())
            elif self.halaman_pattern.match(line):
                if output and output[-1].strip():
                    output.append("")
                output.append(line)
            else:
                output.append(line)

        self.text = "\n".join(output)
        return self


"""
Contoh penggunaan
input_path = Path("content_only_formatted.txt")
output_path = Path("content_cleaned_no_enters2.txt")

(
    TextCleaner.from_file(input_path)
    .clean_newlines_and_bullets()
    .join_sentences()
    .fix_ordering()
    .fix_page_headers()
    .to_file(output_path)
)

print(f"✅ Teks sudah dibersihkan dan disimpan ke {output_path}")
"""