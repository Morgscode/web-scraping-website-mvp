from scraps import app
from scraps.app.models.Crawl import CrawlInstance

from flask import session


def process_user_crawl_request(data: dict):
    crawl = CrawlInstance(data, session['user']['id'])
    is_valid_crawl_reqeust = crawl.is_valid_url(
        crawl.user_crawl_options['webpage_url'])

    if not is_valid_crawl_reqeust:
        return {
            "status": "failed",
            "stausCode": 400,
            "message": "Invalid url requested"
        }, 400

    crawl.prepare_data_dir()

    if crawl.user_crawl_options['crawl_option'] == "single-page":
        crawl.index_webpage_content_by_url(
            crawl.user_crawl_options['webpage_url'], 0)

    if crawl.user_crawl_options['crawl_option'] == "internal-links":
        crawl.grab_internal_page_links()
        crawl.index_webpage_by_url_list()

    if crawl.user_crawl_options['crawl_option'] == "nav-links":
        crawl.grab_internal_navigation_links()
        crawl.index_webpage_by_url_list()

    crawl.compress_data_directory()

    crawl.log_crawl_to_db(session['user']['id'])

    return {
        "status": "success!",
        "statusCode": 200,
        "message": "Successfully crawled {url}... scraped {pgcount} pages into text files with {errcount} errors".format(url=crawl.user_crawl_options['webpage_url'], pgcount=crawl.pages_crawled, errcount=crawl.crawl_errors),
        "downloadUrl": '{download}.zip'.format(download=crawl.download_location)
    }