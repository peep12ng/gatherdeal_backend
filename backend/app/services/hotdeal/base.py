from abc import abstractmethod, abstractproperty
from typing import List

from .client import ClientObject

from ...entity import Hotdeal
from ...repositories import HotdealRepository
from ...data import Source

class HotdealUpdateServiceBase:

    # 수집 모듈
    _client = ClientObject()

    # 핫딜 게시판 구분 코드
    _categories: str = None

    # 핫딜 게시판 주소 리스트
    _board_urls: list[str] = None

    @abstractproperty
    def _source(self) -> Source:
        '''
        타겟 웹사이트 Source\n
        웹사이트 별 ID 생성을 위해 사용.
        '''
        raise NotImplementedError()

    @abstractproperty
    def _categories(self) -> List[str]:
        '''
        핫딜 게시판 구분 코드 리스트
        '''
        raise NotImplementedError()
    
    @abstractproperty
    def _board_urls(self) -> List[str]:
        '''
        핫딜 게시판 코드 구분 주소 리스트
        '''
        raise NotImplementedError()

    @abstractmethod
    def update(self, repo: HotdealRepository):
        '''
        상위 HotdealService에서 사용하는 함수.\n
        필수적으로 _add_or_update_with_repository를 가져야 함.\n
        타겟으로 하는 웹사이트 별 핫딜 게시판 수집 구문 로직의 위치.
        
        :param repo (HotdealRepository): 상위 HotdealService의 HotdealRepository
        '''
        raise NotImplementedError()

    @abstractmethod
    def _get_board_urls(self):
        raise NotImplementedError()
    
    @abstractmethod
    def _get_hotdeal_urls_from_hotdeal_board(self) -> List[str]:
        '''
        핫딜 게시판에서 핫딜 url들을 반환\n
        Source별 수집 로직 구분

        :return hotdeal_urls (List[str]): 핫딜 정보 url 리스트
        '''
    
    @abstractmethod
    def _get_hotdeal_entity_with_parsing_from_hotdeal_url(self, url: str) -> Hotdeal:
        '''
        핫딜 정보 웹페이지에서 파싱

        :param url (str): 핫딜 정보 url

        :return hotdeal (Hotdeal): 파싱 결과 엔티티
        '''
        raise NotImplementedError()
    
    def _add_or_update_with_repository(self, hotdeal: Hotdeal, repo: HotdealRepository):
        '''
        Hotdeal 엔티티를 입력 받아 중복 여부 검사. 결과에 따라 추가 혹은 갱신

        :param hotdeal (Hotdeal): 추가/갱신 할 hotdeal 엔티티
        :param repo (HotdealRepository): 상위 HotdealService의 HotdealRepository
        '''
        _hotdeal = repo.new(**hotdeal.__dict__)

        if repo.exists(_hotdeal.id):
            repo.update(_hotdeal, ["is_blind", "is_done"])
        else:
            print("add")
            repo.add(_hotdeal)
        
        print(f"update complete id{_hotdeal.id}")
    
    def _create_hotdeal_id(self, code:str) -> str:
        '''
        Source별 핫딜 id 생성 함수

        :param code (str): 핫딜 고유 code

        :return id (str): 핫딜 고유 id(헤더_코드)
        '''
        return self._source.hotdeal_id_header + f"_{code}"