import html

import auth as auth
from Db import MySQLDatabase


class AdminUser:
    def __init__(self, user_data: dict):
        self.credentials = {
            'user_email': user_data['email'],
            'user_password': user_data['password']
        }
        self.is_admin = False
        self.db = MySQLDatabase()
        self.user_table = 'users'
        self.crawl_table = 'user_crawls'
