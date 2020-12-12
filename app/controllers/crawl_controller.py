import scraps.app.services.file_service as file_service
import scraps.app.services.web_scraper as web_scraper_service
import scraps.app.services.location_service as location_service


def process_user_crawl_request(data: dict):
    return {
        "status": "success",
        "statusCode": 200,
        "message": "winning",
    }
