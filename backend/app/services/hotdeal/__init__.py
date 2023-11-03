from flask_restx import marshal

from injector import inject

from ...repositories import HotdealRepository
from .quasarzone import QuasarzoneHotdealUpdateService

class HotdealService:

    @inject
    def __init__(self,
                hotdeal_repo: HotdealRepository=None,
                session=None):
        if session:
            self._hotdeal_repo = HotdealRepository(session)
        else:
            self._hotdeal_repo = hotdeal_repo

        self._hotdeal_update_services = [
            QuasarzoneHotdealUpdateService(),
        ]

    def update_all_hotdeal_update_services(self):
        hotdeals = []

        for s in self._hotdeal_update_services:
            hotdeals.extend(s.update(self._hotdeal_repo))
            self._hotdeal_repo.commit()
            self._hotdeal_repo.close()
        
        return hotdeals
    
    def get_hotdeal_list(self, page, per_page):
        pagination = self._hotdeal_repo.paginate(page, per_page)
        return pagination
    
    def get_hotdeal(self, id: str):

        _hotdeal = self._hotdeal_repo.get_by_id(id)

        hotdeal = _hotdeal.serialize()

        return hotdeal