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
    
    def get_hotdeals(self, page=1):
        per_page = 10
        offset = 10*(page-1)

        _hotdeals = self._hotdeal_repo.list(per_page, offset, is_blind=False, is_done=False)

        hotdeals = {h.id:h.serialize() for h in _hotdeals}

        return hotdeals
    
    def get_hotdeal(self, id: str):

        _hotdeal = self._hotdeal_repo.get_by_id(id)

        hotdeal = _hotdeal.serialize()

        return hotdeal