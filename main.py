import os
import datetime

from app.controllers.user_controller import *
from app.controllers.crawl_controller import *
from Db import MySQLDatabase

from flask import Flask, request, redirect, url_for, render_template, session, g, flash, send_from_directory
from flask_wtf.csrf import CSRFProtect

app = Flask("scraps")
app.config["FLASK_APP"] = os.environ.get("FLASK_APP")
app.config["FLASK_ENV"] = os.environ.get("FLASK_ENV")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=30)

csrf = CSRFProtect(app)

time = datetime.datetime.now()
current_year = time.year


@app.before_request
def check_csrf():
    csrf.protect()


@app.before_request
def set_app_globals():
    g.year = current_year


@app.route("/")
@csrf.exempt
def show_app_index():
    if 'user' in session and 'is_logged_in' in session['user']:
        return redirect(url_for('crawl'))
    else:
        return render_template("index.jinja.html")


@app.route("/users", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form["user-email"] and request.form["user-password"]:
            return user_register(request.form)
        else:
            flash("Invalid form submission - try again", 'danger')
            return render_template("register.jinja.html")
    else:
        return render_template("register.jinja.html")


@app.route("/users/<int:id>", methods=["GET", "POST"])
def users(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        if request.form['action'] == "_update":
            return render_template("user-update.jinja.html")
        elif request.form['action'] == "_patch" and request.form['user-password']:
            return user_update(session['user']['id'], request.form)
        elif request.form['action'] == "_delete":
            return user_delete(session['user']['id'])
        else:
            flash("invalid request", "danger")
            return render_template("user.jinja.html")
    else:
        user_crawls = get_all_user_crawls()
        return render_template("user.jinja.html", crawls=user_crawls)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["user-email"] and request.form["user-password"]:
            return user_login(request.form)
        else:
            flash("Invalid login attempt", "danger")
            return render_template("login.jinja.html")
    else:
        return render_template("login.jinja.html")


@app.route("/logout", methods=["GET"])
def logout():
    return user_logout()


@app.route("/crawl", methods=["GET", "POST"])
def crawl():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        if request.is_json:
            json = request.get_json(request)
            return process_user_crawl_request(json)
        else:
            flash(
                "that request wasn't quite what we were expecting. try using the form", "danger")
            return render_template("crawl-form.jinja.html")
    else:
        return render_template("crawl-form.jinja.html")


@app.route('/public/<path:filename>', methods=["GET"])
def download(filename):
    if 'user' not in session:
        return {
            "status": "failed",
            "statusCode": 401,
            "message": "not authorized"
        }, 401
    else:
        return send_from_directory(directory="public/", filename=filename, as_attachment=True)
