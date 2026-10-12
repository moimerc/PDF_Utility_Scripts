# PDF Utility Scripts

## Script Overview
This repository contains Python utility scripts for specific PDF and image processing tasks: extracting raw image bytes from PDFs, and compiling sequential image files into a single grayscale PDF.

## Primary Use Cases
- **Raw Image Extraction**: Extracting unaltered original images from PDF documents without re-encoding.
- **Grayscale PDF Compilation**: Converting and merging scanned images or screenshots into a grayscale PDF. It can be used to bind multi-page music scores.

## Tool Descriptions

### `pdf2img.py`
Uses `PyMuPDF` to extract embedded images from PDF files in their original format.

### `convert_image.py`
A multiprocessing batch converter that uses `FFmpeg` to convert image formats. It can be easily modified to support other formats by changing the input and output extension variables.

### `png2pdf.py`
Compiles a sequential list of images into a single PDF document. It applies a grayscale conversion (`convert('L')` via `Pillow`) to the images before merging them.

## Requirements

- Python 3.x
- `PyMuPDF` (for `pdf2img.py`)
- `Pillow` (for `png2pdf.py`)
- `FFmpeg` installed and added to system PATH (for `convert_image.py`)

```bash
pip install pymupdf Pillow
```

## Usage

Before running the scripts, open them in a text editor and update the directory paths in the configuration sections to point to your local files.

1. **`pdf2img.py`**: Update `pdf_file` (input PDF path) and `output_folder` (where extracted images will be saved).
2. **`convert_image.py`**: Update `INPUT_EXT`, `OUTPUT_EXT`, and `folder_path` to point to the directory containing your target images.
3. **`png2pdf.py`**: Update `TARGET_DIR` (directory containing your images), `FILE_PREFIX` (e.g., "page"), `TOTAL_PAGES`, `EXTENSION` (e.g., "png"), and `OUTPUT_FILE` (final PDF path).

Run the desired script from the terminal:

**To extract raw images from a PDF:**
```bash
python pdf2img.py
```

**To batch convert image formats:**
```bash
python convert_image.py
```

**To compile images into a grayscale PDF:**
```bash
python png2pdf.py
```