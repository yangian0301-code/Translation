from flask import Flask, request, render_template
import requests
from datetime import datetime

app = Flask(__name__)

# ========================
# 字典（中韓翻譯）
# ========================
zh_ko_dict = {
    "你好": "안녕하세요",
    "안녕하세요": "你好",
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

# ========================
# 首頁
# ========================
@app.route('/')
def index():
    return '''
    <h1>首頁</h1>
    <a href="/ask">中韓翻譯</a><br>
    <a href="/stock">查詢個股</a><br>
    <a href="/gpt">GPT頁面</a>
    '''

# ========================
# 中韓翻譯
# ========================
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    question = ""
    answer = ""

    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answer = zh_ko_dict.get(question, "抱歉，我目前沒有這個詞的韓文對應。")

    return render_template('ask.html', question=question, answer=answer)

# ========================
# 股票查詢（✅ 已修正）
# ========================
@app.route('/stock', methods=['GET', 'POST'])
def stock():
    question = ""
    answer = ""

    if request.method == 'POST':
        stock_no = request.form.get('question', '').strip()
        question = stock_no

        today = datetime.today().strftime('%Y%m%d')

        url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={today}&stockNo={stock_no}"

        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            data = res.json()

            close_prices = []

            for row in data.get('data', []):
                price = row[6].replace(',', '')
                close_prices.append(float(price))

            if close_prices:
                max_price = max(close_prices)
                min_price = min(close_prices)
                answer = f"最高收盤價: {max_price} / 最低收盤價: {min_price}"
            else:
                answer = "查無資料（可能是假日或股票不存在）"

        except:
            answer = "發生錯誤，請確認股票代號"

    return render_template('stock.html', question=question, answer=answer)

# ========================
# GPT頁面（目前用字典）
# ========================
@app.route('/gpt', methods=['GET', 'POST'])
def gpt():
    question = ""
    answer = ""

    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answer = zh_ko_dict.get(question, "目前尚未接入 GPT")

    return render_template('gpt.html', question=question, answer=answer)

# ========================
# 啟動
# ========================
if __name__ == '__main__':
    app.run(debug=True)
