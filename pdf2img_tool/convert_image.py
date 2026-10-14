import os
import subprocess
from multiprocessing import Pool, cpu_count
from glob import glob
from tqdm import tqdm

# =========================================================================
# ⚙️ Conversion Settings (Change to desired extensions)
# =========================================================================
INPUT_EXT = ".jpx"   # Original file extension (e.g., .webp, .jpg)
OUTPUT_EXT = ".png"  # Target file extension (e.g., .png, .jpeg)

# -------------------------------------------------------------------------
# Bit depth (pixel format) for the output. Applied only when set.
#
# Leave empty ("") to preserve the source's bit depth (FFmpeg default).
# -------------------------------------------------------------------------
# PS Vita custom theme requires 8-bit PNG:
#   - No transparency  → "rgb24"   (8-bit RGB)
#   - With transparency → "rgba"   (8-bit RGBA)
# -------------------------------------------------------------------------
# Other common values (for reference):
#   PNG : rgb24, rgba, rgb48be (16-bit), rgba64be (16-bit + alpha),
#         gray (8-bit gray), gray16be (16-bit gray), monob (1-bit)
#   JPEG: yuvj420p, yuvj422p, yuvj444p  (JPEG only supports 8-bit)
#   WEBP: yuva420p, bgra                (WEBP only supports 8-bit)
# -------------------------------------------------------------------------
PIX_FMT = ""         # <-- Set to "rgb24" for PS Vita custom theme

def convert_image(file_path):
    # Generate output path with the specified extension
    output_path = os.path.splitext(file_path)[0] + OUTPUT_EXT
    
    # Base command
    command = ['ffmpeg', '-y', '-v', 'error', '-i', file_path]
    
    # Only apply pixel format when explicitly set
    if PIX_FMT:
        command += ['-pix_fmt', PIX_FMT]
    
    command.append(output_path)
    subprocess.run(command)
    
    # Uncomment the line below to delete the original file after conversion
    # os.remove(file_path)
    
    return output_path

if __name__ == '__main__':
    # Directory containing the target files (relative path)
    folder_path = r"./Extracted_Images"
    
    # Get a list of files with the specified input extension
    target_files = glob(os.path.join(folder_path, f"*{INPUT_EXT}"))
    
    if not target_files:
        print(f"⚠️ Could not find any '{INPUT_EXT}' files in '{folder_path}'.")
    else:
        cores = cpu_count()
        print(f"Converting {len(target_files)} '{INPUT_EXT}' files to '{OUTPUT_EXT}'. (Active cores: {cores})")
        print(f"Pixel format: {PIX_FMT if PIX_FMT else 'source default (unchanged)'}")
        
        # Multiprocessing parallel execution with tqdm progress bar
        with Pool(cores) as p:
            list(tqdm(p.imap_unordered(convert_image, target_files), total=len(target_files), desc="Conversion Progress", unit="files"))
            
        print("\nAll conversion tasks completed successfully.")