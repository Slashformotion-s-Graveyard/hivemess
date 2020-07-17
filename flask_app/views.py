from flask_app import app
from flask import render_template, url_for, make_response, request, redirect, session
from .hive_db.users import Current_HiveUserDB
from .hive_db.users.user import account_exists

@app.errorhandler(404)
def error_handler_404(error):
    # print(error)
    return render_template("public/404.html", error=error)

@app.errorhandler(500)
def error_handler_500(error):
    # print(error)
    return render_template("public/500.html", error=error)

@app.route("/")
def index():
    return render_template("public/index.html")


@app.route("/tokens")
def tokens():
    return render_template('public/nada.html', page_name="tokens")


@app.route("/user/", methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        username = request.form["username"]
        if account_exists(username):
            return redirect(url_for("user_infos", username=username))
        else:
            context_user_form = {
                "wrong_username": True,
                "state": "warning",
                "last_username": username
            }
            return render_template('public/user/user_form.html', **context_user_form)
    else:
        if "wrong_username" in session.keys():
            context_user_form = {
                    "wrong_username": True,
                    "state": "warning",
                    "last_username": session.get('wrong_username', 'null')
                }
            session.pop('wrong_username')
        else:
            context_user_form = {
                    "wrong_username": False,
                    "state": False,
                    "last_username": "null"
                }
        return render_template('public/user/user_form.html', **context_user_form)

@app.route("/user/<string:username>")
def user_infos(username):
    if not 'username' in session.keys() or session['username'] != username:
        if account_exists(username):
            session['username'] = username
            session['user_data'] = Current_HiveUserDB.get_user(username)
        
            context = {
            'username': username

            }

            return render_template("public/user/overview_user.html", **context)
        else:
            session['wrong_username'] = username
            return redirect(url_for('user'))
            