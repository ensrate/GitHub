from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = '예시 페이지 초안'
    # 동적인 컨텐츠 생성
    items = [
        {'name': '아이템1', 'description': '아이템1의 설명입니다.', 'link': '/item/1'},
        {'name': '아이템2', 'description': '아이템2의 설명입니다.', 'link': '/item/2'},
        {'name': '아이템3', 'description': '아이템3의 설명입니다.', 'link': '/item/3'}
    ]
    return render_template('index.html', title=title, items=items)

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    # 여기서는 아이템의 ID에 따라 상세 정보를 보여줄 수 있습니다.
    # 예를 들어, item_id를 기반으로 데이터베이스에서 해당 아이템의 정보를 가져와서 보여줄 수 있습니다.
    # 이 예시에서는 단순히 아이템의 ID를 출력합니다.
    return f'아이템 {item_id}의 상세 정보입니다.'

if __name__ == '__main__':
    app.run(debug=True)