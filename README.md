# PDF Utility Scripts

## Overview
Python utilities for PDF and image processing: extracting embedded images from PDFs without re-encoding (`pdf2img.py`), batch-converting image formats via FFmpeg (`convert_image.py`), and compiling sequential images into a grayscale PDF (`img2pdf.py`).

## Use Cases
- **Raw image extraction**: Pull original images out of a PDF.
- **Batch image conversion**: Convert a folder of images from one format to another (e.g. JPX → PNG).
- **Grayscale PDF compilation**: Merge scanned images or screenshots into a single grayscale PDF, useful for assembling multi-page sheet music.

## Scripts

### `pdf2img.py`
Extracts embedded images from PDF files in their original format using `PyMuPDF`.

### `convert_image.py`
A multiprocessing batch converter built on `FFmpeg`. Change the input/output extension variables to support other formats. An optional `PIX_FMT` setting controls the output bit depth (e.g. `rgb24` for 8-bit PNG).

### `img2pdf.py`
Compiles a sequential list of images into a single PDF, converting to grayscale (`convert('L')` via `Pillow`) before merging. Also sets the default viewer layout to 'Single Page' (continuous scrolling off) via `PyMuPDF`, which works well for reading sheet music page-by-page on a tablet.

## Requirements
- Python 3.x
- `PyMuPDF` (for `pdf2img.py`, `img2pdf.py`)
- `Pillow` (for `img2pdf.py`)
- `FFmpeg` in PATH (for `convert_image.py`)

Install the Python dependencies:

```bash
pip install pymupdf Pillow
```

## Usage

Edit the configuration block at the top of each script to point to your local files.

1. **`pdf2img.py`** — set `pdf_file` and `output_folder`.
2. **`convert_image.py`** — set `INPUT_EXT`, `OUTPUT_EXT`, and `folder_path`. Optionally set `PIX_FMT` (leave empty to keep the source bit depth).
3. **`img2pdf.py`** — set `TARGET_DIR`, `FILE_PREFIX` (leave empty for 1, 2, 3...), `EXTENSION` (e.g. `"png"`), and `OUTPUT_FILE`.

Then run:

```bash
python pdf2img.py        # Extract raw images from a PDF
python convert_image.py  # Batch-convert image formats
python img2pdf.py        # Compile images into a grayscale PDF
```