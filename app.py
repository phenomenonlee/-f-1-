from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.u2fmd2o.mongodb.net/?retryWrites=true&w=majority ')
db = client.dbsparta


app = Flask(__name__)


@app.route('/main')
def index():
    return render_template("song.html")


@app.route('/detail', methods=["post"])
def project_detail_post():

    return jsonify({'msg':'작성완료'})
    return render_template("detail.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
