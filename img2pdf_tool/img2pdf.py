import os
from PIL import Image
import pymupdf

# =========================================================================
# ⚙️ 실행 제어 공간
# =========================================================================
# 변환할 이미지들이 위치한 폴더 (현재 스크립트 위치 기준)
TARGET_DIR = r"./Input_Images/"

# 파일명 접두사 (비워두면 1.png, 2.png... 순서대로 탐색합니다)
FILE_PREFIX = ""      

# 지원하는 이미지 확장자 (예: "png", "jpg", "webp", "bmp" 등)
EXTENSION = "png"         

# 흑백 변환 옵션 (True: 흑백, False: 원본 색상)
FORCE_GRAYSCALE = True

# 최종 결과물 PDF 저장 경로
OUTPUT_FILE = os.path.join(TARGET_DIR, "Compiled_Score.pdf")
# =========================================================================

def build_score_pdf(base_dir, file_prefix, ext, output_pdf, force_grayscale=True):
    """
    지정된 디렉토리 내의 이미지를 순서대로 묶어 하나의 PDF를 생성합니다.
    Pillow 라이브러리를 사용하므로 PNG뿐만 아니라 JPG, WebP, BMP 등 다양한 포맷을 지원합니다.
    
    :param base_dir: 이미지 파일들이 위치한 폴더의 경로
    :param file_prefix: 파일명의 앞부분 (예: 비워두면 1, 2, 3...)
    :param ext: 파일 확장자 (예: 'png', 'jpg', 'webp')
    :param output_pdf: 최종 저장될 PDF 파일명 또는 전체 경로
    :param force_grayscale: True일 경우 흑백 변환 가동
    """
    converted_images = []
    i = 1
    
    # 파일이 더 이상 없을 때까지 순서대로 자동 탐색합니다.
    while True:
        filename = f"{file_prefix}{i}.{ext}"
        full_path = os.path.join(base_dir, filename)
        
        # 파일이 존재하지 않으면 탐색 종료
        if not os.path.exists(full_path):
            if i == 1:
                print(f"❌ [오류] 첫 번째 파일({filename})을 찾을 수 없습니다. 경로와 파일명을 확인하십시오.")
                return
            break
            
        print(f"📂 파일 로드 중: {filename}")
        img = Image.open(full_path)
        
        # 흑백(Grayscale) 변환
        if force_grayscale:
            img = img.convert('L')
        else:
            img = img.convert('RGB')
            
        converted_images.append(img)
        i += 1
        
    if not converted_images:
        return

    # 1차 작업: Pillow를 이용하여 이미지들을 PDF로 병합 저장
    first_page = converted_images[0]
    remaining_pages = converted_images[1:]
    
    first_page.save(
        output_pdf,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=remaining_pages
    )
    
    # 2차 작업: PyMuPDF를 이용해 뷰어 기본값을 Single Page(Continuous Scrolling OFF)로 강제 설정
    doc = pymupdf.open(output_pdf)
    
    # PDF 메타데이터 속성 덮어쓰기: SinglePage (단면 보기, 스크롤 비활성화)
    doc.set_pagelayout("SinglePage")
    
    # 임시 파일 없이 제자리(In-place)에 덮어쓰기 저장
    doc.saveIncr()
    doc.close()
    
    print(f"\n[성공] 총 {len(converted_images)}장의 이미지가 PDF로 병합되었습니다.")
    print(f"💾 최종 PDF 경로: {os.path.abspath(output_pdf)}")

if __name__ == "__main__":
    build_score_pdf(
        base_dir=TARGET_DIR,
        file_prefix=FILE_PREFIX,
        ext=EXTENSION,
        output_pdf=OUTPUT_FILE,
        force_grayscale=FORCE_GRAYSCALE
    )