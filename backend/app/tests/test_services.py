from ..services import HotdealService

def test_hotdeal_services(session):
    hotdeal_service = HotdealService(session=session)

    