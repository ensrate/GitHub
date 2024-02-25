from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import io

app = Flask(__name__)

# 숫자 데이터셋 로드
digits = datasets.load_digits()
X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2, random_state=42)

# 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

@app.route('/')
def home():
    return render_template('index.html')

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

@app.route('/predict', methods=['POST'])
def predict():
    # 업로드된 이미지 가져오기
    file = request.files['file']
    
    # 이미지를 8x8 크기로 변환하고 배열로 변환
    img = Image.open(io.BytesIO(file.read()))
    img = img.resize((8, 8))
    img = np.array(img.convert('L'))
    
    # 이미지를 1차원 배열로 펼쳐서 예측을 위해 모델에 전달
    img = img.reshape(1, -1)
    
    # 모델로 예측 수행
    prediction = model.predict(img)[0]
    
    return jsonify({'prediction': int(prediction)})

if __name__ == '__main__':
    app.run(debug=True)
