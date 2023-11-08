from flask_restx import marshal, Model
from flask_sqlalchemy.pagination import Pagination
from flask import url_for, jsonify, Response

def pagination_to_response(pagination: Pagination, pagination_model: Model, endpoint: str) -> Response:

    # marshal(data, fields): data를 fields의 형태로 변환?
    data = marshal(pagination, pagination_model)
    data["links"] = _pagination_nav_links(pagination, endpoint)
    resp = jsonify(data)
    resp.headers["Link"] = _pagination_nav_header_links(pagination, endpoint)
    resp.headers["Total_Count"] = pagination.total
    return resp

def _pagination_nav_links(pagination: Pagination, endpoint: str):

    nav_links = {}

    per_page = pagination.per_page
    this_page = pagination.page
    last_page = pagination.pages

    nav_links["self"] = url_for(endpoint, page=this_page, per_page=per_page)
    nav_links["first"] = url_for(endpoint, page=1, per_page=per_page)
    if pagination.has_prev:
        nav_links["prev"] = url_for(endpoint, page=this_page-1, per_page=per_page)
    if pagination.has_next:
        nav_links["next"] = url_for(endpoint, page=this_page+1, per_page=per_page)
    nav_links["last"] = url_for(endpoint, page=last_page, per_page=per_page)

    return nav_links

def _pagination_nav_header_links(pagination: Pagination, endpoint: str):
    url_dict = _pagination_nav_links(pagination, endpoint)
    link_header = ""
    for rel, url in url_dict.items():
        link_header += f'<{url}>; rel="{rel}", '
    return link_header.strip().strip(",")