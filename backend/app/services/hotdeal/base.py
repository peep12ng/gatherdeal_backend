from abc import abstractmethod, abstractproperty

from ...entity import Hotdeal
from ...repositories import HotdealRepository
from ...data import Source

from .client import ClientObject

class HotdealUpdateServiceBase:

    _client = ClientObject()

    @abstractproperty
    def _source(self) -> Source:
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        raise NotImplementedError()
    
    def _update(self, hotdeal: Hotdeal, repo: HotdealRepository):
        _hotdeal = repo.new(**hotdeal.__dict__)

        if repo.exists(_hotdeal.id):
            repo.update(_hotdeal, ["is_blind", "is_done"])
        else:
            print("add")
            repo.add(_hotdeal)
        
        print(f"update complete id{_hotdeal.id}")

        return _hotdeal
    
    @abstractmethod
    def get_hotdeal(self) -> Hotdeal:
        raise NotImplementedError()
    
    def _create_hotdeal_id(self, code:str) -> str:
        return self._source.hotdeal_id_header + f"_{code}"