import os
import glob
import unicodedata
import msoffcrypto
import io
import pandas as pd

def normalize_filename(filename):
    """
    파일명을 NFC 형태로 정규화합니다.
    """
    return unicodedata.normalize('NFC', filename)

def get_latest_excel_info(folder_path, file_pattern):
    """
    지정된 폴더에서 특정 파일 패턴을 갖는 가장 최근의 엑셀 파일 정보를 반환합니다.

    Parameters:
        folder_path (str): 엑셀 파일을 찾을 폴더의 경로.
        file_pattern (str): 찾을 파일명 패턴.

    Returns:
        tuple: 최신 엑셀 파일의 경로와 NFC 형태로 정규화된 파일명.
    """
    files = glob.glob(os.path.join(folder_path, file_pattern), recursive=True)

    if files:
        files.sort(key=os.path.getmtime, reverse=True)
        latest_file_path = files[0]
        latest_file_name = os.path.basename(latest_file_path)

        # NFC 형태로 파일명 정규화
        normalized_file_name = normalize_filename(latest_file_name)

        return latest_file_path, normalized_file_name
    else:
        return None, None

def get_df_from_password_excel(excelpath, password):
    """
    비밀번호가 설정된 엑셀 파일에서 데이터프레임을 반환합니다.

    Parameters:
        excelpath (str): 엑셀 파일 경로.
        password (str): 엑셀 파일의 비밀번호.

    Returns:
        pandas.DataFrame: 비밀번호가 설정된 엑셀 파일의 데이터프레임.
    """
    df = pd.DataFrame()
    temp = io.BytesIO()
    with open(excelpath, 'rb') as f:
        excel = msoffcrypto.OfficeFile(f)
        excel.load_key(password)
        excel.decrypt(temp)
        df = pd.read_excel(temp)

        # 모든 숫자 데이터를 텍스트로 변환하고 .0 제거
        df = df.applymap(lambda x: str(x).rstrip('.0') if isinstance(x, (int, float)) else str(x))
        
        del temp
    return df

# 사용 예시
if __name__ == "__main__":
    # 다운로드 폴더 경로 설정
    download_folder_path = "/Users/chanhee/Downloads"

    # 파일명 패턴 설정
    file_pattern = '스마트스토어_**주문발주발송관리_*'

    # 최신 엑셀 파일 정보 얻기
    latest_file_path, normalized_file_name = get_latest_excel_info(download_folder_path, file_pattern)

    # 최신 파일 정보 출력 또는 변수에 담기
    if latest_file_path:
        print("가장 최근 엑셀 파일 (NFC 형태):", normalized_file_name)

        # 엑셀 파일 비밀번호 설정
        excel_password = '1111'

        # 데이터프레임 얻기
        df = get_df_from_password_excel(latest_file_path, excel_password)


# '주문번호'를 int64로 변환
df['주문번호'] = pd.to_numeric(df['주문번호'], errors='coerce').fillna(0).astype(int)

# zentrade_df와 smartstore_df 병합
merged_df = pd.merge(smartstore_df, df, how='inner', left_on='주문번호', right_on='주문번호', suffixes=('_스마트스토어', '_젠트레이드'))

# 필요한 열만 선택
result_df = merged_df[['주문번호_스마트스토어', '송장번호_젠트레이드']]

# 결과 데이터프레임을 엑셀로 저장
output_excel_path = '/Users/chanhee/Desktop/lch/python/result_output.xlsx'
result_df.to_excel(output_excel_path, index=False)

print(f"결과가 {output_excel_path}로 저장되었습니다.")

# 추가 코드: merged_df를 엑셀 파일로 저장
merged_excel_path = '/Users/chanhee/Desktop/lch/python/merged_output.xlsx'
merged_df.to_excel(merged_excel_path, index=False)
print(f"Merged 결과가 {merged_excel_path}로 저장되었습니다.")
