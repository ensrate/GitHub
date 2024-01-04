import pandas as pd 
import streamlit as st 
import pickle

##############################
# global 변수 정의 영역
##############################

btn_nl = None
man = pregnant = plasma = pressure = thickness = insulin = bmi = pedigree = age = None

##############################
# sidebar 영역
##############################
def show_sidebar():
    global btn_ml
    global man, pregnant, plasma, pressure, thickness, insulin, bmi, pedigree, age
    
    st.sidebar.title('Good Health (건강지키미)')
    
    st.sidebar.markdown(':arrow_right:당뇨병 여부를 확인 할 수 있습니다. (머신러닝)')
    st.sidebar.markdown('---')
    
    st.sidebar.markdown('<h4 style="color:orange;">정보를 입력하세요</h>', unsafe_allow_html=True)
    man = st.sidebar.radio('성별', ('남성', '여성'))
    age = st.sidebar.slider('나이(age)', 0, 99, 29)
    pregnant = st.sidebar.slider('과거 임신 횟수 (pregnant)', 0, 20, 3)
    plasma = st.sidebar.slider('포도당 부하 검사 2시간 후 공복 혈당 농도 (nm Hg)', 0, 200, 117)
    pressure = st.sidebar.slider('확장기 혈압 (nm Hg) (pressure)', 0, 130, 72)
    thickness = st.sidebar.slider('혈청 인슐린 (2-hour, mu U.nl)(insulin)', 0, 1000, 30)
    bmi = st.sidebar.slider('BMI지수 (bmi)', 0.0, 70.0, 32.0, step=0.1)
    pedigree = st.sidebar.slider('당뇨병 가족력 (pedigree)', 0.0, 30.0, 0.3725, step=0.001)
    st.sidebar.markdown('---')
    
    btn_ml = st.sidebar.button(':part_alternation_mark:당뇨병확인 머신러닝을 시작합니다.')  # 당뇨병 예측을 위한 머신러닝 버튼
    
##############################
# 참고 테이블 영역
##############################
def showDiabetes():
    df = pd.read_csv('./diabetes.csv', names=['pregnant', 'plasma', 'pressure', 'thickness', 'Insulin', 'BMI', \
        'pedigree', 'Age'], encoding='utf-8')
    st.markdown('<h4 stle="color:white;> 당뇨병 데이터 (참고) : 머신러닝 학습 데이터 </h4>', unsafe_allow_html=True)
    
    st.dataframe(df)
##############################
# 머신러닝 영역
##############################
def ml_Diabetes(features):
    # Model 불러오기
    load_clf = pickle.load(open('diabetes_model (1).pkl', 'rb'))
    
    # 예측
    prediction = load_clf.predict(features)  # 1 : 당뇨, 2 : 당뇨아님
    # prediction_proba = load_clf.predict_proba(features)  # 확률로 예측 (ex : 0.4)
    st.write("")
    st.write("")

    # 예측 결과 보여주기
    if prediction > 0.5:
        st.markdown("<h3 style='color:gold; text-align:center;'>머신러닝 검사 결과 당뇨일 가능성이 높습니다.</h3>", \
            unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; text-align:center;'>병원방문이 필요해 보입니다.</h3>", \
            unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color:gold; text-align:center;'>머신러닝 검사 결과 당뇨가 아닙니다.</h3>", \
            unsafe_allow_html=True)
        
    st.write("")
    st.write("")
    
    st.markdown('---')
    # Test data 보여주기
    st.write('예측 (Prediction)')
    
    st.dataframe(features)
    
    st.write(prediction)
    st.markdown('---')
    showDiabetes()
    
##############################
# Main 영역
##############################

def main():
    global age, man, btn_nl
    global pregnant, plasma, pressure, thickness, insulin, bmi, pedigree
    
    st.set_page_config()
    show_sidebar()
    
    if btn_ml:
        # Machine Learning 학습 데이터
        input_data = {
            'pregnant': pregnant,
            'plasma': plasma,
            'pressure': pressure,
            'thickness': thickness,
            'BMI': bmi,
            'pedigree': pedigree,
            'Age': age,
        }
    
        features = pd.DataFrame(input_data, index=[0])
        st.markdown('<h5 style="text_align:center; color:orange;">현재의 건강 상태를 표시하고 좋은 건강 상태를 유지하기 위한 조언\
            하겠습니다. </h5>', unsafe_allow_html=True)

        ml_Diabetes(features.to_numpy())
        btn_nl = False
        
main()