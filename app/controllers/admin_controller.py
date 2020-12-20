from app.models.AdminUser import AdminUser

from app.services.file_service import delete_data_directory


def get_all_active_crawls(user):
    print(user)
