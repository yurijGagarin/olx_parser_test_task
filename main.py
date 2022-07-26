import os

from flask import Flask, render_template, request, abort, redirect, jsonify

from parser import parse_all_data

app = Flask(__name__)

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']


@app.route("/about")
def about():
    is_user = request.cookies.get('username')
    return render_template('about.html', is_user=is_user)


@app.route("/")
def index():
    username = request.cookies.get('username')
    if username:
        return render_template('user.html', is_user=True)
    return render_template('guest.html')


@app.route('/login', methods=['POST'])
def login():
    payload = request.form.to_dict()

    username = payload.get('username')
    password = payload.get('password')

    if username and password and username == USERNAME and password == PASSWORD:
        resp = redirect("/", code=302)
        resp.set_cookie('username', username, secure=True, httponly=True)
        return resp

    return abort(403)


@app.route('/data', methods=['GET'])
def get_data():
    username = request.cookies.get('username')
    if not username:
        return redirect("/", code=302)

    return jsonify(parse_all_data())


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    resp = redirect("/", code=302)
    resp.delete_cookie('username')
    return resp


if __name__ == '__main__':
    app.run()
