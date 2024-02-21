from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np
import tensorflow as tf

app = Flask(__name__)

model = tf.keras.models.load_model('./model/mnist_model.h5')

# 이미지 전처리 함수 (흑백 변환)
def preprocess_image(image):
    try:
        img = Image.open(image).convert('L')  # 흑백 변환
        img = img.resize((28, 28))  # 이미지 크기를 모델에 맞게 조정
        img_array = np.array(img)  # 이미지를 배열로 변환
        img_array = img_array / 255.0  # 이미지를 정규화
        img_array = np.expand_dims(img_array, axis=0)  # 배치 차원 추가
        return img_array
    except Exception as e:
        return str(e)

# index 페이지 렌더링
@app.route('/')
def index():
    # index.html을 렌더링할 때 필요한 CSS 및 JavaScript 파일을 함께 전달
    return render_template('index.html', css_files=[
        'main.css',
    ])

# 모델 서비스 페이지 렌더링
@app.route('/playlist')
def playlist():
    return render_template('playlist.html', css_files=[
        'default.css',
        'playlist.css',
        'ProjectView.css'
    ], js_files=[
        'playlist.js',
        'ProjectView.js',
        'data.js',
    ])

# 예측 엔드포인트
# Flask 애플리케이션에서 /predict 엔드포인트에 대한 POST 요청을 처리하는 부분
# 데코레이터를 사용하여 특정 URL 경로(/predict)와 HTTP 메서드(POST)에 대한 요청을 처리
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 이미지 파일 가져오기
        file = request.files['file']
        # 이미지 전처리
        image = preprocess_image(file)
        if isinstance(image, str):
            return jsonify({'error': image}), 400  # 전처리 오류 응답
        # 모델 예측
        prediction = model.predict(image)
        # 예측 결과를 소프트맥스 확률에서 가장 높은 확률을 가진 클래스로 변환
        predicted_class = np.argmax(prediction)
        # 예측 결과 반환
        # 만약 상태 코드를 명시하지 않는다면, 기본적으로 200이 반환되지만, 명시적으로 상태 코드를 지정하는 것이 코드의 가독성과 명확성을 높일 
        return jsonify({'prediction': int(predicted_class)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # 서버 오류 응답

if __name__ == '__main__':
    app.run(debug=True)
