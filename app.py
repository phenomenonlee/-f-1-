from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta
import hashlib
import jwt
import requests

app = Flask(__name__)

from pymongo import MongoClient

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb+srv://test:sparta@cluster0.tef1s.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


# 라우터들
@app.route("/")
def main():
    return render_template('index.html')


@app.route("/", methods=["POST"])
def insert_contents_post():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])#{'id': 'gwonyeong', 'exp': 1657768562}
                                                                            # {'id': 'gwonyeong', 'pw': 'eca38cd8f32bd60d105845c50acc190bbf0657df89253d3bf18438463f701d0d'}
        print(payload)
        user_id = db.users.find_one({"id": payload["id"]},{'_id': False})
        print(user_id)
        idx_list = list(db.contents.find({}, {'_id': False}))
        idx = len(idx_list) + 1

        artist_receive = request.form['artist_give']
        title_receive = request.form['title_give']
        desc_receive = request.form['desc_give']
        url_receive = request.form['url_give']
        doc = {'index': idx,
               'artist': artist_receive,
               'title': title_receive,
               'desc': desc_receive,
               'url': url_receive,
               'id': user_id['id']}
        db.contents.insert_one(doc)

        return jsonify({'msg': '공유되었습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template('login.html',msg = '로그인이 필요합니다.')


@app.route("/con", methods=["GET"])
def insert_contents_get():
    contents = list(db.contents.find({}, {'_id': False}))
    return jsonify({'contents': contents})


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/detail?<index>')
def detail(index):
    return render_template('detail.html')


@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

@app.route("/mypage", methods=["POST"])
def mypage_info():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    all_users = list(db.contents.find({"id": payload['id']}, {'_id': False}))
    print(all_users)
    return jsonify({'contents': all_users})


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


# login&signup

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "id": username_receive,  # 아이디
        "pw": password_hash,  # 비밀번호
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': username_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/')
def index():
    return render_template("detail.html")

    
@app.route("/info", methods=["POST"])
def ripple_post():
    ripple_receive = request.form['ripple_give']
    print(ripple_receive)
    doc = {
        'ripple': ripple_receive,
    }
    db.info.insert_one(doc)

    return jsonify({'msg': '작성 완료!'})


@app.route('/contents', methods=["GET"])
def desc_get():
    desc_list = list(db.contents.find({}, {'_id': False}))
    return jsonify({'desc': desc_list})


@app.route('/info', methods=["GET"])
def ripple_get():
    ripple_list = list(db.info.find({}, {'_id': False}))
    return jsonify({'ripple': ripple_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
