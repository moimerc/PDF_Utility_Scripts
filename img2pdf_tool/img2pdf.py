import os
from PIL import Image
import pymupdf

# =========================================================================
# ⚙️ Execution Control Section
# =========================================================================
# Directory containing images to convert (relative to current script)
TARGET_DIR = r"./Input_Images/"

# File prefix (leave empty to search in order: 1.png, 2.png...)
FILE_PREFIX = ""      

# Supported image extensions (e.g., "png", "jpg", "webp", "bmp")
EXTENSION = "png"         

# Grayscale conversion option (True: grayscale, False: original colors)
FORCE_GRAYSCALE = True

# Output PDF save path
OUTPUT_FILE = os.path.join(TARGET_DIR, "Compiled_Score.pdf")
# =========================================================================

def build_score_pdf(base_dir, file_prefix, ext, output_pdf, force_grayscale=True):
    """
    Compiles a sequential list of images in a designated directory into a single PDF.
    Utilizes the Pillow library, supporting various formats including PNG, JPG, WebP, and BMP.
    
    :param base_dir: Path to the directory containing image files
    :param file_prefix: Prefix of the filenames (e.g., leave empty for 1, 2, 3...)
    :param ext: File extension (e.g., 'png', 'jpg', 'webp')
    :param output_pdf: Final PDF filename or full path
    :param force_grayscale: Enables grayscale conversion if True
    """
    converted_images = []
    i = 1
    
    # Automatically search in sequence until no more files are found
    while True:
        filename = f"{file_prefix}{i}.{ext}"
        full_path = os.path.join(base_dir, filename)
        
        # Stop searching if the file does not exist
        if not os.path.exists(full_path):
            if i == 1:
                print(f"❌ [Error] Could not find the first file ({filename}). Please check the path and filename.")
                return
            break
            
        print(f"📂 Loading file: {filename}")
        img = Image.open(full_path)
        
        # Grayscale conversion
        if force_grayscale:
            img = img.convert('L')
        else:
            img = img.convert('RGB')
            
        converted_images.append(img)
        i += 1
        
    if not converted_images:
        return

    # Step 1: Merge and save images as PDF using Pillow
    first_page = converted_images[0]
    remaining_pages = converted_images[1:]
    
    first_page.save(
        output_pdf,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=remaining_pages
    )
    
    # Step 2: Force default viewer layout to Single Page (Continuous Scrolling OFF) using PyMuPDF
    doc = pymupdf.open(output_pdf)
    
    # Overwrite PDF metadata: SinglePage (single page view, disable scrolling)
    doc.set_pagelayout("SinglePage")
    
    # In-place save without creating temporary files
    doc.saveIncr()
    doc.close()
    
    print(f"\n[Success] A total of {len(converted_images)} images have been merged into the PDF.")
    print(f"💾 Final PDF path: {os.path.abspath(output_pdf)}")

if __name__ == "__main__":
    build_score_pdf(
        base_dir=TARGET_DIR,
        file_prefix=FILE_PREFIX,
        ext=EXTENSION,
        output_pdf=OUTPUT_FILE,
        force_grayscale=FORCE_GRAYSCALE
    )