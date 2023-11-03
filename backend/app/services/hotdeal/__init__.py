from flask import url_for, jsonify
from flask_sqlalchemy.pagination import Pagination
from flask_restx import marshal

from injector import inject

from .quasarzone import QuasarzoneHotdealUpdateService

from ...repositories import HotdealRepository
from ...models.pagination import pagination_model

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

        for s in self._hotdeal_update_services:
            s.update(self._hotdeal_repo)
            self._hotdeal_repo.commit()
            self._hotdeal_repo.close()

    def get_hotdeal_list_response(self, page, per_page):
        pagination = self._hotdeal_repo.paginate(page, per_page)

        response_data = marshal(pagination, pagination_model)
        response_data["links"] = self._pagination_nav_links(pagination)
        response = jsonify(response_data)
        response.headers["Link"] = self._pagination_nav_header_links(pagination)
        response.headers["Total_Count"] = pagination.total
        return response
    
    def _pagination_nav_links(pagination: Pagination):
        nav_links = {}
        per_page = pagination.per_page
        this_page = pagination.page
        last_page = pagination.pages
        nav_links["self"] = url_for("hotdeal_list", page=this_page, per_page=per_page)
        nav_links["first"] = url_for("hotdeal_list", page=1, per_page=per_page)
        if pagination.has_prev:
            nav_links["prev"] = url_for(
                "hotdeal_list", page=this_page - 1, per_page=per_page
            )
        if pagination.has_next:
            nav_links["next"] = url_for(
                "hotdeal_list", page=this_page + 1, per_page=per_page
            )
        nav_links["last"] = url_for("hotdeal_list", page=last_page, per_page=per_page)
        return nav_links

    def get_hotdeal(self, id: str):

        _hotdeal = self._hotdeal_repo.get_by_id(id)

        hotdeal = _hotdeal.__dict__

        return hotdeal
    
    def _pagination_nav_header_links(self, pagination: Pagination):
        url_dict = self._pagination_nav_links(pagination)
        link_header = ""
        for rel, url in url_dict.items():
            link_header += f'<{url}>; rel="{rel}", '
        return link_header.strip().strip(",")