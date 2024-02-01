import streamlit as st
import pandas as pd

st.title('MY STORE APP')

# Excel 파일 경로
file_path = 'test-rowdata.xlsx'

# Excel 파일을 읽어와서 데이터프레임으로 변환
df = pd.read_excel(file_path)

# 변수로 받은 상품 ID 값
target_product_id = st.text_input("상품 ID를 입력하세요")

# 상품ID 열을 텍스트로 변환
df['상품ID'] = df['상품ID'].astype(str)

# 변수로 받은 값과 상품ID 값이 일치하는 데이터만 필터링
filtered_df = df[df['상품ID'] == target_product_id]


st.dataframe(df)

st.dataframe(filtered_df)