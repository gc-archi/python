import json
from datetime import datetime
from flask import Fask, render_template, request, redirect, Markup, escape

application = Flask(__name__)

DATA_FILE = 'norilog.json'

def save_data(start, finish, memo, created_at):
    try:
        #Get Data from Database and Perse by JSON format
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []

    database.insert(0,{
        "start" : start,
        "finish" : finish,
        "memo" : memo,
        "created_at" : created_at.strftime("%Y-%m-%d %H:%M")
    })

    json.dump(database, open(DATA_FILE, mode="w", encoding="utf-8"), indent=4, ensure_ascii=False)

def load_data():
    """
    save_data関数で出力されたnorilog.jsonからデータを取得する
    """
    try:
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []
    return database

def main():
    application.run('127.0.0.1', 8000)

@application.route("/")
def index():
    """
    Top Page templateを利用して出力
    """
    ride = load_data()
    return render_template('index.html', rides=ride)
    #index.html側で、reides変数としてload_dataの結果を渡す。

@application.route('/save', methods=['POST'])
def save():
    """データsave用URL"""
    #記録されたデータを取得する
    start = request.form.get('start')
    finish = request.form.get('finish')
    memo = request.form.get('memo')
    create_at = datetime.now()
    save_data(start, finish, memo, create_at)
    #データ保存後は、トップページへリダイレクト
    return redirect('/')

@application.template_filter('nl2br')
def nl2br_filter(s):
    """改行文字をbrタグに置き換えるテンプレートフィルター"""
    return escape(s).replace('\n', Markup('<br>'))

if __name__ == '__main__':
    #ListenするIPアドレスとポート番号を指定
    application.run('0.0.0.0', 8000, debug=True)