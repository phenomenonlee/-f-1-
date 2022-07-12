from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.tef1s.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


# 라우터들
@app.route("/")
def main():

    return render_template('index.html')

@app.route("/" , methods=["POST"])
def insert_contents_post():
    try:
        idx = request.form['index']
    except:
        idx = 0
    artist_receive =request.form['artist_give']
    title_receive = request.form['title_give']
    desc_receive = request.form['desc_give']
    url_receive = request.form['url_give']
    doc = {'index':idx,
        'artist':artist_receive,
           'title':title_receive,
           'desc':desc_receive,
           'url':url_receive }
    db.contents.insert_one(doc)

    return jsonify({'msg': '데이터 POST'})


@app.route("/con", methods=["GET"])
def insert_contents_get():
    contents = list(db.contents.find({}, {'_id': False}))

    return jsonify({'contents' : contents})


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/detail')
def detail():
    return render_template('detail.html')


@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


# 헤더 및 푸터
@app.route('/header')
def header():
    return render_template('header.html')


@app.route('/footer')
def footer():
    return render_template('footer.html')


# 여기부터 기능들
@app.route('/detail', methods=["POST"])
def detail_post():


    return jsonify({'msg': '보내기 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
