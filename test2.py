#test2.py

import streamlit as st
import pandas as pd

st.title("Keyword Mining ✨")

### 파일 업로드 위젯
uploaded_file = st.file_uploader("", type=["csv", "xlsx"])
if uploaded_file is not None:
    # 업로드된 파일을 DataFrame으로 읽기
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(uploaded_file, engine='openpyxl')


    ### 초기 데이터 가공
        
    df['선택'] = False  
    df['메모'] = ''
    df['쇼핑탭'] = "https://search.shopping.naver.com/search/all?where=all&frm=NVSCTAB&query=" + df['키워드']

    # '총검색수'와 '상품수' 열의 값을 정수로 변경
    df['총 검색수'] = pd.to_numeric(df['총 검색수'], errors='coerce').fillna(0).astype(int)
    df['상품수'] = pd.to_numeric(df['상품수'], errors='coerce').fillna(0).astype(int)



    ### 1번 데이터프레임

    edited_df = st.data_editor(
        df,
        hide_index=True,
        #use_container_width=True,
        column_order=("선택", "키워드", "총 검색수", "상품수", "경쟁강도", "쇼핑탭"),
        column_config={
            "선택": st.column_config.CheckboxColumn(width="small"),
            "키워드": st.column_config.TextColumn(width="medium"),
            "쇼핑탭": st.column_config.LinkColumn(display_text="쇼핑탭"),
            },  
        )


    # 2번 데이터 프레임
    selected_data = edited_df[edited_df["선택"]]
    st.caption(f"선택된 키워드: {selected_data.shape[0]}")
    st.data_editor(
        selected_data,
        hide_index=True,
        #use_container_width=True,
        column_order=("키워드", "총 검색수", "상품수", "경쟁강도", "쇼핑탭","메모"),
        column_config={
            "키워드": st.column_config.TextColumn(width=""),
            "쇼핑탭": st.column_config.LinkColumn(display_text="쇼핑탭"),
            "메모" : st.column_config.TextColumn(width="medium")
            },  
        )


    # 선택된 키워드
    selected_keyword = st.multiselect(
        '',
        selected_data['키워드'].tolist(),
        selected_data['키워드'].tolist())

    # 키워드 입력란
    keyword_input = st.text_input("")

    # 글자수 표시
    character_count = len(keyword_input)
    st.caption(f"상품명길이: {character_count}")


