from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.tef1s.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


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


@app.route('/info', methods=["GET"])
def index():
    return render_template("detail.html")

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
