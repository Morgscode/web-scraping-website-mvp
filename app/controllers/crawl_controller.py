from scraps import app
from scraps.app.models.Crawl import CrawlInstance

from flask import session


def process_user_crawl_request(data: str):
    crawl = CrawlInstance(data, session['user']['id'])
    is_valid_crawl_reqeust = crawl.is_valid_url()

    if not is_valid_crawl_reqeust:
        return {
            "status": "failed",
            "stausCode": 400,
            "message": "Invalid url requested"
        }, 400
    else:
        return {
            "status": "success",
            "statusCode": 200,
            "message": "That url is valid!"
        }
