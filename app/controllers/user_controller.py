from scraps.app.models.User import User
from flask import request, render_template, session, redirect, url_for, flash


def user_register(user_data: list):
    user = User(user_data)
    is_registered = user.is_registered_user()

    if is_registered:
        flash("email address is already registered, login instead", "danger")
        return render_template("register.jinja.html")
    else:
        user.register_user()
        flash('successful scraps registration', 'info')
        return render_template("register-success.jinja.html", user=user)


def user_login(data: list):
    user = User(data)
    user.log_in_user()

    if not user.is_logged_in:
        flash("incorrect login, try again", "danger")
        return render_template("login.jinja.html")
    else:
        session.clear()
        user_dict = {
            'email': user.email[1],
            'password': user.password[1],
            'id': user.id,
            'is_logged_in': 1,
            'member_since': user.join_date
        }
        session["user"] = user_dict
        flash('successfully logged in as {user}'.format(
            user=session['user']['email']), "info")
        return redirect(url_for("crawl"))


def user_logout():
    session.clear()
    flash("successfully logged out from scraps", "info")
    return redirect(url_for("login"))


def user_update(id: int, data: dict):

    if data['user-password'] == session['user']['password']:

        if data['new-password'] != '':
            session['user']['password'] = data['new-password']

        if data['user-email'] != '':
            session['user']['email'] = data['user-email']

        user_credentials = {
            'user-email': session['user']['email'],
            'user-password': session['user']['password']
        }

        user = User(user_credentials)
        user.update_user(id)
        session.modified = True
        return redirect(url_for('users', id=id))
    else:
        flash("invalid form submission", "danger")
        return redirect(url_for('users', id=id))


def user_delete(id):
    user_credentials = {
        'user-email': session['user']['email'],
        'user-password': session['user']['password']
    }
    user = User(user_credentials)
    user.delete_user(id)
    session.clear()
    return redirect(url_for('show_app_index'))
