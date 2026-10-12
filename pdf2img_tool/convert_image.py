import os
import subprocess
from multiprocessing import Pool, cpu_count
from glob import glob
from tqdm import tqdm

# =========================================================================
# ⚙️ 변환 설정 (원하는 확장자로 변경하여 사용)
# =========================================================================
INPUT_EXT = ".jpx"   # 원본 파일 확장자 (예: .webp, .jpg)
OUTPUT_EXT = ".png"  # 변환할 파일 확장자 (예: .png, .jpeg)

def convert_image(file_path):
    # 지정한 출력 확장자로 경로 생성
    output_path = os.path.splitext(file_path)[0] + OUTPUT_EXT
    
    # FFmpeg 명령어 구성 (-y: 덮어쓰기, -v error: 불필요한 로그 생략)
    command = ['ffmpeg', '-y', '-v', 'error', '-i', file_path, output_path]
    subprocess.run(command)
    
    # 변환 완료 후 원본 파일을 삭제하려면 아래 주석을 해제하세요.
    # os.remove(file_path)
    
    return output_path

if __name__ == '__main__':
    # 타겟 파일들이 위치한 폴더 경로 (현재 폴더 기준 상대 경로)
    folder_path = r"./Extracted_Images"
    
    # 폴더 내의 지정된 입력 확장자 파일 목록 가져오기
    target_files = glob(os.path.join(folder_path, f"*{INPUT_EXT}"))
    
    if not target_files:
        print(f"⚠️ '{folder_path}' 폴더에서 '{INPUT_EXT}' 파일을 찾을 수 없습니다.")
    else:
        cores = cpu_count()
        print(f"총 {len(target_files)}개의 '{INPUT_EXT}' 파일을 '{OUTPUT_EXT}'(으)로 변환합니다. (활성 코어: {cores}개)")
        
        # 멀티프로세싱 병렬 처리 및 tqdm 진행률 표시
        with Pool(cores) as p:
            list(tqdm(p.imap_unordered(convert_image, target_files), total=len(target_files), desc="변환 진행률", unit="파일"))
            
        print("\n모든 변환 작업이 완료되었습니다.")