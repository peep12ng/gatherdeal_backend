import asyncio
from bs4 import BeautifulSoup
import re

from .base import HotdealUpdateServiceBase

from ...repositories import HotdealRepository
from ...entity import Hotdeal
from ...data import Source

class QuasarzoneHotdealUpdateService(HotdealUpdateServiceBase):

    _source = Source.quasarzone

    def update(self, repo: HotdealRepository):

        result = []

        max_page = 1
        categories = ["PC/하드웨어", "노트북/모바일", "가전/TV"]
        urls = [f"https://quasarzone.com/bbs/qb_saleinfo?page={page}&category={category}" for category in categories for page in range(max_page, 0, -1)]

        pages = asyncio.run(self._client.get_many(urls))

        for p in pages:
            bs = BeautifulSoup(p, "html.parser")
            heads = bs.find("tbody").find_all("tr")

            for head in heads:
                hotdeal = self.get_hotdeal(head)
                result.append(self._update(hotdeal, repo))
        
        return result
    
    def get_hotdeal(self, head) -> Hotdeal:

        _code = re.search('views/(.+?)?category', head.select_one("a.subject-link").attrs["href"]).group(1)[:-1]

        id = self._create_hotdeal_id(_code)

        _url = f"https://quasarzone.com/bbs/qb_saleinfo/views/{_code}"

        source_link = _url

        _bs = self._get_hotdeal_bs(_url)

        title = _bs.find("title").text.split(" >")[0]

        _table = _bs.select_one("table.market-info-view-table")
        _trs = _table.find_all("tr")

        first_price = float(re.sub(r'[^0-9.]', '', _trs[2].find("span").text))
        last_price = 0
        currency_type = _trs[2].find("span").text.split("(")[1][:3]
        store_link = _trs[0].find("a").text

        if "종료" in _bs.select_one("h1.title").text:
            is_done = True
        else:
            is_done = False
        is_blind = False

        hotdeal = Hotdeal(id, title, first_price, currency_type, last_price, store_link,
                          source_link, is_done, is_blind)

        return hotdeal
    
    def _get_hotdeal_bs(self, url: str) -> BeautifulSoup:
        r = asyncio.run(self._client.get(url))
        bs = BeautifulSoup(r, "html.parser")

        return bs