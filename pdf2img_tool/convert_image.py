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

def convert_image(file_path):
    # Generate output path with the specified extension
    output_path = os.path.splitext(file_path)[0] + OUTPUT_EXT
    
    # Construct FFmpeg command (-y: overwrite, -v error: suppress unnecessary logs)
    command = ['ffmpeg', '-y', '-v', 'error', '-i', file_path, output_path]
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
        
        # Multiprocessing parallel execution with tqdm progress bar
        with Pool(cores) as p:
            list(tqdm(p.imap_unordered(convert_image, target_files), total=len(target_files), desc="Conversion Progress", unit="files"))
            
        print("\nAll conversion tasks completed successfully.")