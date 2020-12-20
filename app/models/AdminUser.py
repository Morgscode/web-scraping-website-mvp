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

    # def is_verified_admin(self):
    #     # get user row
    #     # check by user creds (user and pass)
    #     # assess admin status

    # def clean_data_dir(self):
    #     # bring in file service
    #     # bring in db
    #     # get all rows id, download locations WHERE
    #     # `files_deleted` is false and older
    #     # than 30 mins
    #     # update row to files deleted
