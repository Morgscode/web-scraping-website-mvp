import html
from urllib.parse import urlparse

from scraps.Db import MySQLDatabase
import scraps.app.services.file_service as file_service
import scraps.app.services.web_scraper as web_scraper_service
import scraps.app.services.location_service as location_service


class CrawlInstance:
    def __init__(self, user_data: dict, user_id: int):
        self.table = 'user_crawls'
        self.db = MySQLDatabase()
        self.make_model()
        self.user_id = user_id
        if user_data:
            self.user_crawl_options = {
                'webpage_url': location_service.manage_domain_scheme(
                    html.escape(user_data['webpage-url'])),
                'crawl_option': html.escape(user_data['crawl-option']),
                'content_option': html.escape(user_data['content-option'])
            }
        self.urls = []
        self.formatted_hrefs = []
        self.pages_crawled = 0
        self.crawl_errors = 0
        self.download_location = ''

    def make_model(self):
        self.db.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {table} (id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT, webpage_url VARCHAR(255), crawl_option VARCHAR(255), content_option VARCHAR(255), pages_crawled INTEGER, crawl_errors INTEGER,user_id INTEGER, download_location VARCHAR(255), created_at DATETIME DEFAULT CURRENT_TIMESTAMP)".format(table=self.table))
        self.db.dbconn.commit()

    def is_valid_url(self, url: str):
        response = location_service.validate_web_url(url)
        if response:
            return True
        else:
            return False

    def retrieve_and_parse_url(sefl, url: str):

        formatted_target_url = location_service.manage_domain_scheme(
            url)
        parsed_target_url = urlparse(formatted_target_url)

        return parsed_target_url

    def prepare_data_dir(self):
        # we'll also need a parse version of the full url
        parsed_target_url = self.retrieve_and_parse_url(
            self.user_crawl_options['webpage_url'])
        # lets create a dirctory for data
        self.download_location = file_service.setup_data_directory(
            parsed_target_url, self.user_id)

    def index_initial_page_as_soup(self, url: str):

        data = web_scraper_service.get_webpage_html(
            self.user_crawl_options['webpage_url'])

        if data.status_code != 200:
            return False
        data_soup = web_scraper_service.convert_html_to_soup_obj(data)

        return data_soup

    def index_webpage_content_by_url(self, url: str, index: int):
        # let's grab the html response from the server
        page_html = web_scraper_service.get_webpage_html(url)

        response_is_text_or_json = web_scraper_service.assess_content_type_for_text_or_json(
            page_html)

        if not response_is_text_or_json:
            # we dont really want to index anything that
            # isn't plain text or json
            return False

        # let's convert it to some tasty soup
        page_html_soup = web_scraper_service.convert_html_to_soup_obj(
            page_html)

        if self.user_crawl_options['content_option'] == 'page-title':
            # extract the page title
            page_html_text_content = web_scraper_service.extract_page_title_as_text(
                page_html_soup)

        elif self.user_crawl_options['content_option'] == 'main-content':
            # extract the page's main content
            page_html_text_content = web_scraper_service.extract_and_format_main_content_as_text(
                page_html_soup)

        elif self.user_crawl_options['content_option'] == 'all-content':
            # extract all the text from this page
            page_html_text_content = web_scraper_service.convert_soup_to_text(
                page_html_soup)

        # let's generate a formatted path in our file system for this webpage
        formatted_path = location_service.format_path_as_file_location(url)

        # let's write the retieved text to a file and store it's location
        # the index will be 0 or more, this will order the files in the directory
        parsed_target_url = urlparse(self.user_crawl_options['webpage_url'])

        new_file_loaction = file_service.write_text_to_file(
            page_html_text_content, formatted_path, index, parsed_target_url, self.user_id)

        # let's strip all of the unneeded whitespace, and tidy it up
        formatted_text = file_service.strip_whitespace_from_file(
            new_file_loaction)

        # let's rewrite the cleaned text to the file
        file_service.write_text_to_file(
            formatted_text, formatted_path, index, parsed_target_url, self.user_id)

    def grab_internal_page_links(self):
        data = web_scraper_service.get_webpage_html(
            self.user_crawl_options['webpage_url'])

        soup = web_scraper_service.convert_html_to_soup_obj(data)
        internal_page_links = web_scraper_service.get_internal_links_from_webpage(
            soup, self.user_crawl_options['webpage_url'])

        for webpage_link in internal_page_links:
            webpage_link_href = location_service.format_href_as_url(
                webpage_link, self.user_crawl_options['webpage_url'])

            self.urls.append(webpage_link_href)

    def grab_internal_navigation_links(self):

        data = web_scraper_service.get_webpage_html(
            self.user_crawl_options['webpage_url'])

        soup = web_scraper_service.convert_html_to_soup_obj(data)

        internal_page_links = web_scraper_service.get_valid_webpage_link_hrefs_in_navs(
            soup)

        for webpage_link in internal_page_links:
            webpage_link_href = location_service.format_href_as_url(
                webpage_link, self.user_crawl_options['webpage_url'])
            self.urls.append(webpage_link_href)

    def index_webpage_by_url_list(self):

        if len(self.urls) > 0:

            # if there are no links in a nav, just index the content on that page
            self.index_webpage_content_by_url(
                self.user_crawl_options['webpage_url'], 0)
            for index, link in enumerate(self.urls):
                try:
                    self.index_webpage_content_by_url(
                        link, index + 1)
                    # lets sleep for a second to introduce a crawl delay
                    self.pages_crawled += 1
                except:
                    self.crawl_errors += 1

            return self

    def compress_data_directory(self):
        file_service.compress_directory(self.download_location)

    def log_crawl_to_db(self, user_id):

        crawl = {
            "webpage_url": self.user_crawl_options["webpage_url"],
            "crawl_option": self.user_crawl_options["crawl_option"],
            "content_option": self.user_crawl_options["content_option"],
            "pages_crawled": self.pages_crawled,
            "crawl_errors": self.crawl_errors,
            "user_id": user_id,
            "download_location": self.download_location,
        }

        self.db.insert_single(self.table, crawl)
