from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://text:sparta@cluster0.3wkhjck.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# 라우터들
@app.route('/')
def main():
    song_info = list(db.songinfo.find({},{'_id':False}))
    return render_template('index.html', song_infos=song_info)


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
    song_title_receive = request.form['song_title_give']
    song_artist_receive = request.form['song_artist_give']
    song_des_receive = request.form['song_des_give']
    song_genre_receive = request.form['song_genre_give']

    doc = {
        'song_title': song_title_receive,
        'song_artist': song_artist_receive,
        'song_des': song_des_receive,
        'song_genre': song_genre_receive
    }
    db.songinfo.insert_one(doc)
    return jsonify({'msg': '보내기 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
