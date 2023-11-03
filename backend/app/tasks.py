from .services import HotdealService
from .extensions import db

def hotdeal_update_task():
    hotdeal_service = HotdealService(session=db.session)
    hotdeal_service.update_all_hotdeal_update_services()