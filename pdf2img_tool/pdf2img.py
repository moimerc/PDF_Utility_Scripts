import pymupdf
import os
from tqdm import tqdm

def extract_original_images(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Opening PDF document: {pdf_path}")
    doc = pymupdf.open(pdf_path)
    
    total_images = 0

    # Create progress bar using tqdm
    for page_index in tqdm(range(len(doc)), desc="Extraction Progress", unit="pages"):
        page = doc[page_index]
        images = page.get_images(full=True)
        
        for img_index, img in enumerate(images):
            xref = img[0]
            
            # Extract raw bytes without converting to Pixmap
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]  # Original extension (e.g., 'jpeg', 'png')
            
            # Save while maintaining the original extension
            output_filename = os.path.join(output_dir, f"page_{page_index+1:03d}_img_{img_index+1}.{image_ext}")
            
            with open(output_filename, "wb") as f:
                f.write(image_bytes)
                
            total_images += 1

    print(f"\nTask complete! A total of {total_images} images have been saved to '{output_dir}'.")

# File path configuration
pdf_file = r"sample.pdf"
output_folder = r"./Extracted_Images"

extract_original_images(pdf_file, output_folder)