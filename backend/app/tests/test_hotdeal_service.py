from ..services import HotdealService

def test_hotdeal_service_init(app, db, session):
    hotdeal_service = HotdealService(session=session)

    assert hotdeal_service

def test_hotdeal_service_update(session):
    hotdeal_service = HotdealService(session=session)

    hotdeals = hotdeal_service.update_all_hotdeal_update_services()
    print(len(hotdeals))

    assert hotdeals