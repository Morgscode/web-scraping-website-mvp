import html

from scraps.Db import Database
import scraps.app.services.file_service as file_service
import scraps.app.services.web_scraper as web_scraper_service
import scraps.app.services.location_service as location_service


class CrawlInstance:
    def __init__(self, user_data: dict, user_id: int):
        self.table = 'user_crawls'
        self.user_id = user_id
        self.user_crawl_options = {
            'webpage_url': location_service.manage_domain_scheme(
                html.escape(user_data['webpage-url'])),
            'crawl_option': html.escape(user_data['crawl-option']),
            'content_option': html.escape(user_data['content-option'])
        }
        self.urls = []
        self.formatted_hrefs = []
        self.pages_crawled = 0
        self.db = Database('scraps_local')
        self.make_model()

    def make_model(self):
        self.db.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {table} (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, webpage_url text, pages_crawled INTEGER, user_id INTEGER, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)".format(table=self.table))
        self.db.conn.commit()

    def is_valid_url(self):
        response = location_service.validate_web_url(
            self.user_crawl_options['webpage_url'])

        if response:
            return True
        else:
            return False
