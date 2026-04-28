
from flask import Flask, request, render_template

app = Flask(__name__)

# 建立題庫
zh_ko_dict = {
    "你好": "안녕하세요",
    "안녕하세요" : "你好",
    "謝謝": "감사합니다",
    "對不起": "죄송합니다",
    "早安": "좋은 아침",
    "晚安": "안녕히 주무세요",
    "老師": "선생님",
    "學生": "학생",
    "朋友": "친구",
    "家人": "가족",
    "愛": "사랑"
}




# homepage process
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        # 2. 讀取學生的問題###^#@#Q%#@
        question = request.form.get('question', '').strip()
        # 3. 查詢題庫的對應答案
        answer = zh_ko_dict.get(question, "抱歉，我目前沒有這個詞的韓文對應。")
        # 4. 回傳答案給學生
        return render_template('ask.html', question=question, answer=answer)
    # GET 時給空白欄位
    return render_template('ask.html', question="", answer="")


@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        # 2. 讀取使用者輸入的股票號碼
        question = request.form.get('question', '').strip()
        # 3. 查詢股票號碼的收盤價
        answer = zh_ko_dict.get(question, "抱歉，我目前沒有這個股票號碼。")
        # 4. 回傳答案給使用者
        return render_template('stock.html', question=question, answer=answer)
    # GET 時給空白欄位
    return render_template('stock.html', question="", answer="")













@app.route('/gpt', methods=['GET', 'POST'])
def gpt():
    if request.method == 'POST':
        # 2. 讀取學生的問題
        question = request.form.get('question', '').strip()
        # 3. 查詢題庫的對應答案
        answer = zh_ko_dict.get(question, "抱歉，我目前沒有這個詞的韓文對應。")
        # 4. 回傳答案給學生
        return render_template('gpt.html', question=question, answer=answer)
    # GET 時給空白欄位
    return render_template('gpt.html', question="", answer="")



if __name__ == '__main__':
    # 開發用；部署用 gunicorn（見下方）
    app.run(host='0.0.0.0', debug=False)
    from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>首頁</h1><a href="/stock">查詢個股</a>'

@app.route('/stock', methods=['GET', 'POST'])
def stock():
    question = ""
    answer = ""

    if request.method == 'POST':
        stock_no = request.form['question']
        question = stock_no

        today = datetime.today().strftime('%Y%m%d')

        url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={today}&stockNo={stock_no}"

        res = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0"
        })

        data = res.json()

        try:
            close_prices = []

            for row in data['data']:
                price = row[6].replace(',', '')
                close_prices.append(float(price))

            if close_prices:
                max_price = max(close_prices)
                min_price = min(close_prices)
                answer = f"最高收盤價: {max_price} / 最低收盤價: {min_price}"
            else:
                answer = "查無資料"

        except:
            answer = "輸入錯誤或查無此股票"

    return render_template("stock.html", question=question, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)

