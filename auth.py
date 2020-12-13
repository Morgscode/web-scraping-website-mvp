import bcrypt

from flask import session


def bind_user_to_session(user: object):
    if user:
        session.clear()
        user_dict = {
            'email': user.credentials['user_email'],
            'password': user.credentials['user_password'],
            'id': user.id,
            'is_logged_in': 1,
            'member_since': user.join_date
        }
        session["user"] = user_dict
        session.modified = True


def bind_data_to_session_credentials(data: list):
    user_credentials = {
        'user-email': session['user']['email'],
        'user-password': session['user']['password']
    }

    if data['new-password'] != '':
        session['user']['password'] = data['new-password']
        user_credentials['user-password'] = data['new-password']
    if data['user-email'] != '':
        session['user']['email'] = data['user-email']
        user_credentials['user-email'] = data['user-email']
    session.modified = True

    return user_credentials


def hash_password(password: str):
    salt = bcrypt.gensalt(rounds=16)
    hased_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hased_pw


def check_hashed_password(password: str, hashed_password: str):
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False
