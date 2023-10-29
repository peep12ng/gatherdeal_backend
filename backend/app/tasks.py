from .services import HotdealService
from .extensions import db

def hotdeal_update_task():
    hotdeal_service = HotdealService()
    hotdeal_service.update_all()