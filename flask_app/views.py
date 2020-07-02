from flask_app import app
from flask import render_template, url_for, make_response, request, redirect, session



@app.route("/")
def index():
    return "hello johann et jean-robert"