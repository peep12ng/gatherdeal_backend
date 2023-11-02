from flask import url_for
from flask_sqlalchemy.pagination import Pagination

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

def _pagination_nav_header_links(pagination: Pagination):
    url_dict = _pagination_nav_links(pagination)
    link_header = ""
    for rel, url in url_dict.items():
        link_header += f'<{url}>; rel="{rel}", '
    return link_header.strip().strip(",")