import html

from urllib.parse import urlparse


from scraps.Db import Database
import scraps.app.services.file_service as file_service
import scraps.app.services.web_scraper as web_scraper_service
import scraps.app.services.location_service as location_service


class CrawlInstance:
    def __init__(self, user_data: dict, user_id: int):
        self.table = 'user_crawls'
        self.db = Database('scraps_local')
        self.make_model()
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
        self.download_location = ''

    def make_model(self):
        self.db.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {table} (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, webpage_url text, crawl_option text, content_option text, pages_crawled INTEGER, user_id INTEGER, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)".format(table=self.table))
        self.db.conn.commit()

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
        # we'll also need a parse version of the full url
        parsed_target_url = self.retrieve_and_parse_url(url)
        # lets create a dirctory for data
        self.download_location = file_service.setup_data_directory(
            parsed_target_url, self.user_id)
        # let's generate a formatted path in our file system for this webpage
        formatted_path = location_service.format_path_as_file_location(url)
        # let's write the retieved text to a file and store it's location
        # the index will be 0 or more, this will order the files in the directory
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
            pages_indexed = 0
            indexing_errors = 0
            # if there are no links in a nav, just index the content on that page
            self.index_webpage_content_by_url(
                self.user_crawl_options['webpage_url'], 0)
            for index, link in enumerate(self.urls):
                try:
                    self.index_webpage_content_by_url(
                        link, index + 1)
                    # lets sleep for a second to introduce a crawl delay
                    time.sleep(1)
                except:
                    indexing_errors += 1
                else:
                    pages_indexed += 1
