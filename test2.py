#test2.py

import streamlit as st
import pandas as pd

# 파일 업로드 위젯
uploaded_file = st.file_uploader("파일 업로드", type=["csv", "xlsx"])
if uploaded_file is not None:
    # 업로드된 파일을 DataFrame으로 읽기
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(uploaded_file, engine='openpyxl')

    # 선택한 열만 남기기
    selected_columns = ["키워드", "총 검색수", "상품수", "경쟁강도"]
    df_selected = df[selected_columns]

    # 첫 번째 열에 체크박스 추가
    checkbox_col = st.checkbox("Select All", key="select_all")
    if checkbox_col:
        df_selected.insert(0, "Select", True)
    else:
        df_selected.insert(0, "Select", False)

    # 새로운 데이터프레임 출력
    edited_df = st.data_editor(df_selected, hide_index=True, use_container_width=True)

    # 선택된 행만 추출
    selected_rows = edited_df[edited_df["Select"]]
    st.write("선택된 키워드:")
    st.data_editor(selected_rows, hide_index=True, use_container_width=True)

    # 선택된 키워드
    selected_keyword = st.multiselect(
        '키워드 선택',
        selected_rows['키워드'].tolist(),
        selected_rows['키워드'].tolist())

    # 키워드 입력란
    keyword_input = st.text_input("상품명")

    # 글자수 표시
    character_count = len(keyword_input)
    st.text(f"상품명길이: {character_count}")
