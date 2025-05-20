# Putusan MK Extractor

Alat untuk ekstraksi dan pemformatan putusan Mahkamah Konstitusi dengan OCR berbasis GPU menggunakan EasyOCR dan PyMuPDF.

---

## Persyaratan Sistem (Ubuntu)

- Python >= 3.7
- GPU NVIDIA dengan driver dan CUDA Toolkit (jika ingin pakai OCR GPU)
- `pip` dan `virtualenv` (disarankan)

---

## Instalasi Driver & CUDA (Opsional - untuk GPU)

1. **Cek apakah GPU dan driver NVIDIA sudah terpasang:**

```bash
nvidia-smi
```

2. **Pasang driver NVIDIA dan CUDA Toolkit**

Ikuti panduan resmi:  
- [NVIDIA Driver Ubuntu](https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html)  
- [CUDA Toolkit Installer](https://developer.nvidia.com/cuda-downloads)

---

## Setup Virtual Environment

```bash
sudo apt update
sudo apt install python3-pip python3-venv -y

python3 -m venv venv
source venv/bin/activate
```

---

## Instalasi Proyek

```bash
# Upgrade pip
pip install --upgrade pip

# Instal proyek dan semua dependensinya
pip install .
```

### 🔥 Instal Torch GPU (Opsional)

Jika ingin menggunakan GPU, install versi PyTorch yang cocok dengan CUDA:

```bash
# Contoh untuk CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

Jika tidak pakai GPU:

```bash
pip install torch torchvision
```

---

## Cara Menggunakan

Setelah di-install, kamu bisa menjalankan alat ini melalui terminal:

```bash
putusan-extract path/to/file.pdf -o output.txt
```

Atau secara programatik di Python:

```python
from putusan_mk_extractor.extractor import PDFTextExtractor

extractor = PDFTextExtractor("contoh.pdf")
extractor.extract_grouped_content().format_content().save_to("hasil.txt")
```

---

## Struktur Proyek

```
putusan_mk_extractor/
├── __init__.py
├── __main__.py
├── extractor.py
setup.py
README.md
```

---

## Lisensi

MIT License

---

## Kontak

Hidayat  
[dayat@rumahlogic.com]
