import os
from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="putusan_mk_extractor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyMuPDF>=1.22.0",
        "Pillow>=10.0.0",
        "easyocr>=1.7.1",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "numpy>=1.19.0"
    ],
    entry_points={
        "console_scripts": [
            "putusan-extract=putusan_mk_extractor.__main__:main"
        ]
    },
    author="Hidayat",
    description="putusan_mk_extractor adalah alat bantu berbasis Python untuk mengekstrak dan membersihkan teks dari dokumen putusan Mahkamah Konstitusi (atau Mahkamah Agung), termasuk PDF hasil pindai tanpa teks asli. Ekstraksi dilakukan dengan kombinasi antara pembacaan teks langsung dan OCR (EasyOCR + GPU).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    url="https://github.com/dr-baka/putusan-mk-extractor",
    license="MIT",
)
