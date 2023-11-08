import asyncio
from typing import List
from bs4 import BeautifulSoup
import re

from .base import HotdealUpdateServiceBase

from ...repositories import HotdealRepository
from ...entity import Hotdeal
from ...data import Source
from ...utils.class_from_args import class_from_args

class QuasarzoneHotdealUpdateService(HotdealUpdateServiceBase):

    _source = Source.quasarzone

    def update(self, repo: HotdealRepository):
        
        hotdeal_urls = self._get_hotdeal_urls_from_hotdeal_board()

        for url in hotdeal_urls:
            hotdeal = self._get_hotdeal_entity_with_parsing_from_hotdeal_url(url)
            self._add_or_update_with_repository(hotdeal, repo)
    
    def _get_hotdeal_urls_from_hotdeal_board(self) -> List[str]:
        
        hotdeal_urls = []

        max_page = 1
        categories = ["PC/하드웨어", "노트북/모바일", "가전/TV"]
        board_urls = [f"https://quasarzone.com/bbs/qb_saleinfo?page={page}&category={category}" for category in categories for page in range(max_page, 0, -1)]

        boards = asyncio.run(self._client.get_many(board_urls))

        for board in boards:
            bs = BeautifulSoup(board, "html.parser")
            heads = bs.find("tbody").find_all("tr")

            for head in heads:
                code = re.search('views/(.+?)?category', head.select_one("a.subject-link").attrs["href"]).group(1)[:-1]
                hotdeal_urls.append(f"https://quasarzone.com/bbs/qb_saleinfo/views/{code}")
        
        return hotdeal_urls

    def _get_hotdeal_entity_with_parsing_from_hotdeal_url(self, url: str) -> Hotdeal:
        r = asyncio.run(self._client.get(url))
        bs = BeautifulSoup(r, "html.parser")

        d = {}

        d["code"] = url.split("views/")[-1]
        d["id"] = self._create_hotdeal_id(d["code"])
        d["source_link"] = url

        if "블라인드 처리된 글입니다" in str(bs):
            d["is_blind"] = True
            d["title"] = None
            d["original_price"] = None
            d["price_to_krw"] = None
            d["currency_type"] = None
            d["store_link"] = None
            d["is_done"] = None
        else:
            d["is_blind"] = False

            d["title"] = bs.find("title").text.split(" >")[0]

            info_table = bs.select_one("table.market-info-view-table")
            info_trs = info_table.find_all("tr")

            d["original_price"] = float(re.sub(r'[^0-9.]', '', info_trs[2].find("span").text))
            d["price_to_krw"] = 0
            d["currency_type"] = info_trs[2].find("span").text.split("(")[1][:3]
            d["store_link"] = info_trs[0].find("a").text

            if "종료" in bs.select_one("h1.title").text:
                d["is_done"] = True
            else:
                d["is_done"] = False

        return class_from_args(Hotdeal, d)