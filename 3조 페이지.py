from PIL import Image
import streamlit as st

# Streamlit 애플리케이션 타이틀 설정
st.title("피부질환 케어 서비스")

# 스타일 설정
st.markdown(
    """
    <style>
    .stButton > button {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 사이드바 메뉴 설정
menu = st.sidebar.selectbox("메뉴 선택", ["피부질환 판별", "주변 병원 찾기", "서비스 페이지"])

# 각 메뉴에 따른 동작
if menu == "피부질환 판별":
    # 피부질환 판별 페이지에 대한 코드를 작성합니다.
    st.subheader("피부질환 판별 페이지")
    uploaded_image = st.file_uploader("피부 사진 업로드", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        # 딥러닝 모델로 피부질환 판별 수행
        st.image(uploaded_image, caption="업로드한 이미지", use_column_width=True)
        # 판별 결과 표시

elif menu == "주변 병원 찾기":
    # 주변 병원 찾기 페이지에 대한 코드를 작성합니다.
    st.subheader("주변 병원 찾기 페이지")
    
    # 지도 서비스 이미지를 추가합니다.
    st.image("kakaomap_img.png", caption="KakaoMap", width=550)  # 이미지의 너비를 700px로 조절

    # KakaoMap API를 사용한 지도 표시 및 주변 병원 검색
    st.write("주변 병원 찾기 서비스를 이용하려면 아래 버튼을 클릭하세요.")
    
    # 개인 페이지로 이동하는 버튼을 스타일리시하게 디자인합니다.
    personal_page_url = "http://host240102.dothome.co.kr/map/kakao_map (search).html"  # 서비스 페이지 URL을 여기에 입력
    button_text = "카카오맵 페이지로 이동"
    button_code = f'<a href="{personal_page_url}" target="_blank"><button style="width: 100%; padding: 10px; font-size: 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; transition: background-color 0.3s ease;">{button_text}</button></a>'
    st.markdown(button_code, unsafe_allow_html=True)
    

elif menu == "서비스 페이지":
    # 개인 페이지로 이동하는 버튼을 스타일리시하게 디자인합니다.
    st.subheader("외부 서비스 페이지에서 이용하기")
    personal_page_url = "http://host240102.dothome.co.kr/web/index.html"  # 서비스 페이지 URL을 여기에 입력
    button_text = "서비스 페이지로 이동"
    button_code = f'<a href="{personal_page_url}" target="_blank"><button style="width: 100%; padding: 10px; font-size: 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; transition: background-color 0.3s ease;">{button_text}</button></a>'
    st.markdown(button_code, unsafe_allow_html=True)