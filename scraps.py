import datetime
import scraps.app.controllers.user_controller as user_controller
import scraps.app.controllers.crawl_controller as crawl_controller

from flask import Flask, request, redirect, url_for, render_template, session, flash
from flask_wtf.csrf import CSRFProtect

app = Flask("scraps")
app.config["SECRET_KEY"] = 'dev'
app.config["FLASK_ENV"] = 'development'
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=30)
csrf = CSRFProtect(app)

time = datetime.datetime.now()
current_year = time.year


@app.before_request
def check_csrf():
    csrf.protect()


@app.route("/")
@csrf.exempt
def show_app_index():
    if 'user' in session and 'is_logged_in' in session['user']:
        return redirect(url_for('crawl'))
    else:
        return render_template("index.jinja.html", year=current_year)


@app.route("/users", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form["user-email"] and request.form["user-password"]:
            return user_controller.user_register(request.form)
        else:
            flash("Invalid form submission - try again", 'danger')
            return render_template("register.jinja.html", year=current_year)
    else:
        return render_template("register.jinja.html", year=current_year)


@app.route("/users/<int:id>", methods=["GET", "POST"])
def users(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        if request.form['action'] == "_update":
            return render_template("user-update.jinja.html", year=current_year)
        elif request.form['action'] == "_patch" and request.form['user-password']:
            return user_controller.user_update(session['user']['id'], request.form)
        elif request.form['action'] == "_delete":
            return user_controller.user_delete(session['user']['id'])
        else:
            flash("invalid request", "danger")
            return render_template("user.jinja.html", year=current_year)
    else:
        return render_template("user.jinja.html", year=current_year)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["user-email"] and request.form["user-password"]:
            return user_controller.user_login(request.form)
        else:
            flash("Invalid login attempt", "danger")
            return render_template("login.jinja.html", year=current_year)
    else:
        return render_template("login.jinja.html", year=current_year)


@app.route("/logout", methods=["GET"])
def logout():
    return user_controller.user_logout()


@app.route("/crawl", methods=["GET", "POST"])
def crawl():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        print(request)
        return crawl_controller.process_user_crawl_request()
    else:
        return render_template("crawl-form.jinja.html", year=current_year)
