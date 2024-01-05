import streamlit as st
from PIL import Image
import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.efficientnet import preprocess_input
from streamlit_option_menu import option_menu


skin_disease_model = tf.keras.models.load_model('/Users/choejong-gyu/Downloads/project/EfficientNetB3-skin disease-83.17.h5')

class_labels = {
    1: 'Eczema',
    2: 'Melanoma',
    3: 'Atopic Dermatitis',
    4: 'Basal Cell Carcinoma',
    5: 'Melanocytic Nevi',
    6: 'Benign Keratosis-like Lesions',
    7: 'Psoriasis pictures Lichen Planus and related diseases',
    8: 'Seborrheic Keratoses and other Benign Tumors',
    9: 'Tinea Ringworm Candidiasis and other Fungal Infections',
    10: 'Warts Molluscum and other Viral Infections',
}

# Streamlit 애플리케이션 타이틀 설정
st.set_page_config(
    page_title="피부질환 케어 서비스",
    layout="wide",
    initial_sidebar_state="expanded",
)


with st.sidebar:
    choice = option_menu("Menu", ["피부질환 판별", "정보", "서비스 페이지"],
                         icons=['house', 'kanban', 'bi bi-robot'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#08c7b4"},
    }
    )

def add_bg_from_url(url):
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url({url});
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# 배경 이미지 추가
add_bg_from_url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAADICAMAAAA9W+hXAAAAA1BMVEXb8Pn2e0wOAAAANElEQVR4nO3BMQEAAADCoPVP7WsIoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAeAN1+AABVhDU2QAAAABJRU5ErkJggg==")

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
        background-color: #45A049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# 메뉴에 따른 동작
if choice == "피부질환 판별":
    # 피부질환 판별 페이지에 대한 코드를 작성합니다.
    st.subheader("피부질환 판별 페이지")
    
    # 딥러닝 모델 정확성에 대한 정보 표시
    st.info("주의: 이 딥러닝 모델은 정확하지 않을 수 있습니다. 결과에 대해 신뢰성이 없을 수 있으니 주의해야하며 전문의의 상담이 필요합니다.")
    
    # 동의 체크박스
    agreed = st.checkbox("동의합니다.")
    
    # 동의한 경우에만 사진 업로드 버튼을 활성화
    if agreed:
        uploaded_image = st.file_uploader("피부 사진 업로드", type=["jpg", "jpeg", "png"])
    else:
        uploaded_image = None
    
    if uploaded_image:
        # 이미지 전처리
        img = Image.open(uploaded_image)
        img = img.resize((300, 300))
        img = np.array(img)
        img = preprocess_input(img)  # EfficientNetB3에 맞게 이미지 전처리
        
        # 모델을 사용한 예측
        predictions = skin_disease_model.predict(np.expand_dims(img, axis=0))
        class_index = np.argmax(predictions)
        predicted_label = class_labels[class_index]  # 클래스 라벨 찾기
        probability = np.max(predictions)
    
        # 예측 결과 표시
        st.subheader("피부질환 판별 결과")
        st.image(uploaded_image, caption="업로드한 이미지", use_column_width=True)
        st.write(f"예측된 피부질환: {predicted_label}")
        st.write(f"예측 확률: {probability:.2f}")
