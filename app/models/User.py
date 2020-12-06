import html
from scraps.Db import Database


class User():
    def __init__(self, data: list):
        self.email = ('user_email', html.escape(data['user-email']))
        self.password = ('user_password', html.escape(data['user-password']))
        self.is_logged_in = False

        self.db = Database('scraps_local')
        self.table = 'users'
        self.make_model()

    def make_model(self):
        self.db.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {table} (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, user_email text, user_password text, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)".format(table=self.table))
        self.db.conn.commit()

    def is_registered_user(self):
        (user_column, username) = self.email
        user_row = self.db.fetch_single(self.table, user_column, username)

        if not user_row:
            return False
        else:
            return True

    def register_user(self):
        registrant = [self.email, self.password]
        try:
            self.db.insert_single(self.table, registrant)
            return True
        except:
            return False

    def log_in_user(self):
        (email_column_key, username) = self.email
        (password_column_key, password) = self.password
        user_row = self.db.fetch_single(self.table, email_column_key, username)

        if user_row and username == user_row[1] and password == user_row[2]:
            self.is_logged_in = True
            self.id = user_row[0]
            self.join_date = user_row[3]
            return True
        else:
            return False

    def get_user_email(self):
        return self.email

    def get_user_password(self):
        return self.password

    def update_user(self, id: int):
        try:
            user = [self.email, self.password]
            self.db.update_single(self.table, user, id)
            return True
        except:
            return False

    def delete_user(self, id: int):
        try:
            self.db.delete_single(self.table, id)
            return True
        except:
            return False
