from flask_app import app
from flask import render_template, url_for, make_response, request, redirect, session

@app.errorhandler(404)
def error_handler_404(error):
    # print(error)
    return render_template("public/404.html", error=error)

@app.route("/")
def index():
    return render_template("public/index.html")


@app.route("/tokens")
def token():
    return render_template('public/nada.html', page_name="tokens")


@app.route("/user/", methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        username = request.form["username"]
        return render_template("public/user/overview.html", username=username)
    else:
        return render_template('public/user/user_form.html')

@app.route("/user/<string:username>")
def user_infos(username):
    return "sss"