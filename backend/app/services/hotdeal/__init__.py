from injector import inject

from .quasarzone import QuasarzoneHotdealUpdateService
from .fmkorea import FmkoreaHotdealUpdateService

from ...repositories import HotdealRepository

class HotdealService:

    @inject
    def __init__(self,
                hotdeal_repo: HotdealRepository=None,
                session=None):
        '''
        의존성 주입을 위한 @inject 데코레이터, hotdeal_repo 인수
        db.session을 부여해 서비스 직접 생성(task, test에서 사용)

        :param hotdeal_repo (HotdealRepository): HotdealRepository
        :param session (Session): SQLAlchemy.Session
        '''
        if session:
            self._hotdeal_repo = HotdealRepository(session)
        else:
            self._hotdeal_repo = hotdeal_repo

        self._hotdeal_update_services = [
            QuasarzoneHotdealUpdateService(),
            FmkoreaHotdealUpdateService(),
        ]
    
    def update_all_hotdeal_update_services(self):

        for s in self._hotdeal_update_services:
            s.update(self._hotdeal_repo)
            self._hotdeal_repo.commit()
            self._hotdeal_repo.close()

    def get_hotdeal_list_pagination(self, page, per_page):
        pagination = self._hotdeal_repo.paginate(page, per_page)
        return pagination
    
    def get_hotdeal(self, id: str):

        _hotdeal = self._hotdeal_repo.get_by_id(id)

        hotdeal = _hotdeal.__dict__

        return hotdeal