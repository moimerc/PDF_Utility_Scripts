import pymupdf
import os
from tqdm import tqdm

def extract_original_images(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"PDF 문서를 엽니다: {pdf_path}")
    doc = pymupdf.open(pdf_path)
    
    total_images = 0

    # tqdm을 적용하여 진행률 표시줄 생성
    for page_index in tqdm(range(len(doc)), desc="원본 직접 추출 진행률", unit="페이지"):
        page = doc[page_index]
        images = page.get_images(full=True)
        
        for img_index, img in enumerate(images):
            xref = img[0]
            
            # 픽셀로 변환(Pixmap)하지 않고 원본 바이트(Raw Bytes) 데이터를 그대로 가져옴
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]  # 원본 확장자 (예: 'jpeg', 'png' 등)
            
            # 원본 확장자를 그대로 유지하여 저장
            output_filename = os.path.join(output_dir, f"page_{page_index+1:03d}_img_{img_index+1}.{image_ext}")
            
            with open(output_filename, "wb") as f:
                f.write(image_bytes)
                
            total_images += 1

    print(f"\n작업 완료! 총 {total_images}개의 이미지가 '{output_dir}'에 저장되었습니다.")

# 파일 경로 설정
pdf_file = r"sample.pdf"
output_folder = r"./Extracted_Images"

extract_original_images(pdf_file, output_folder)