import html

import scraps.auth as auth
from scraps.Db import MySQLDatabase


class User:
    def __init__(self, user_data: dict):
        self.credentials = {
            'user_email': html.escape(user_data['user-email']),
            'user_password': html.escape(user_data['user-password'])
        }
        self.is_logged_in = False
        self.db = MySQLDatabase()
        self.table = 'users'
        self.make_model()

    def make_model(self):
        self.db.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {table} (id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT, user_email VARCHAR(255), user_password VARCHAR(255), created_at DATETIME DEFAULT CURRENT_TIMESTAMP)".format(table=self.table))
        self.db.dbconn.commit()

    def register_user(self):
        self.credentials['user_password'] = auth.hash_password(
            self.credentials['user_password'])
        try:
            self.db.insert_single(self.table, self.credentials)
            return True
        except:
            return False

    def is_registered_user(self):
        user_columns = []
        user_values = []
        for key, value in self.credentials.items():
            user_columns.append(key)
            user_values.append(value)

        user_row = self.db.fetch_single(
            self.table, user_columns[0], user_values[0])

        if not user_row:
            return False
        else:
            return True

    def log_in_user(self):
        user_columns = []
        user_values = []
        for key, value in self.credentials.items():
            user_columns.append(key)
            user_values.append(value)

        user_row = self.db.fetch_single(
            self.table, user_columns[0], user_values[0])

        if user_row:
            is_user_password = auth.check_hashed_password(
                self.credentials['user_password'], user_row[2])

            if user_row and self.credentials['user_email'] == user_row[1] and is_user_password:
                self.is_logged_in = True
                self.id = user_row[0]
                self.join_date = user_row[3]
                return True
            else:
                return False
        else:
            return False

    def update_user(self, id: int):
        self.credentials['user_password'] = auth.hash_password(
            self.credentials['user_password'])
        try:
            self.db.update_single(self.table, self.credentials, id)
            return True
        except:
            return False

    def delete_user(self, id: int):
        try:
            self.db.delete_single(self.table, id)
            return True
        except:
            return False
