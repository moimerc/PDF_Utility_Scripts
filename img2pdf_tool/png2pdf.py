import os
from PIL import Image

def build_score_pdf(base_dir, file_prefix, total_pages, ext, output_pdf, force_grayscale=True):
    """
    지정된 디렉토리 내의 page1부터 pageN까지의 이미지를 순서대로 묶어 하나의 흑백 PDF를 생성합니다.
    
    :param base_dir: 이미지 파일들이 위치한 폴더의 절대 경로
    :param file_prefix: 파일명의 앞부분 (예: 'page')
    :param total_pages: 총 페이지 수 (예: 8)
    :param ext: 파일 확장자 (예: 'png')
    :param output_pdf: 최종 저장될 PDF 파일명 또는 전체 경로
    :param force_grayscale: True일 경우 강제 흑백 변환 가동
    """
    converted_images = []
    
    # 1부터 total_pages(8)까지 순서대로 파일 경로를 자동 생성합니다.
    for i in range(1, total_pages + 1):
        filename = f"{file_prefix}{i}.{ext}"  # 'page1.png', 'page2.png' ... 순으로 빌드
        full_path = os.path.join(base_dir, filename)
        
        # 하드웨어 디스크 내 파일 존재 여부 실시간 검증
        if not os.path.exists(full_path):
            print(f"⚠️ [경고] 파일을 찾을 수 없어 건너뜁니다: {full_path}")
            continue
            
        print(f"📂 파일 로드 중 ({i}/{total_pages}): {filename}")
        img = Image.open(full_path)
        
        # 강제 흑백 픽셀 포맷 변환 제어
        if force_grayscale:
            img = img.convert('L')  # 8-bit Grayscale 변환으로 그림자 및 색상 잔상 필터링
        else:
            img = img.convert('RGB')
            
        converted_images.append(img)
        
    if not converted_images:
        print("❌ 변환할 수 있는 이미지 파일이 존재하지 않습니다. 경로를 재확인하십시오.")
        return

    # 첫 페이지를 기준으로 나머지 페이지들을 하드웨어 메모리 상에서 병합하여 PDF로 일괄 저장
    first_page = converted_images[0]
    remaining_pages = converted_images[1:]
    
    first_page.save(
        output_pdf,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=remaining_pages
    )
    print(f"\n🎉 [성공] 8장의 악보가 완벽하게 변환되었습니다.")
    print(f"💾 최종 PDF 경로: {os.path.abspath(output_pdf)}")


# =========================================================================
# ⚙️ 실행 제어 공간
# =========================================================================
if __name__ == "__main__":
    
    # 사용자님께서 제시해주신 절대 경로를 원본 그대로 할당합니다.
    # (파이썬에서 윈도우 경로 내 역슬래시 정렬 문제를 방지하기 위해 일반 슬래시(/) 구조를 유지합니다.)
    TARGET_DIR = "./Input_Images/"
    
    FILE_PREFIX = "page"      # 파일명 접두사
    TOTAL_PAGES = 8          # 파일 총 개수
    EXTENSION = "png"         # 확장자 명
    
    # 최종 결과물 PDF가 저장될 경로와 이름을 지정합니다.
    # 이미지 폴더와 같은 위치에 'BraveHeart_Suite.pdf'라는 이름으로 저장되도록 설정했습니다.
    OUTPUT_FILE = os.path.join(TARGET_DIR, "Compiled_Score.pdf")
    
    # 함수 실행 (강제 흑백 변환 옵션 가동)
    build_score_pdf(
        base_dir=TARGET_DIR,
        file_prefix=FILE_PREFIX,
        total_pages=TOTAL_PAGES,
        ext=EXTENSION,
        output_pdf=OUTPUT_FILE,
        force_grayscale=True
    )