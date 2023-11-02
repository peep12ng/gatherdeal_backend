from flask_restx import Namespace, Resource, marshal

from http import HTTPStatus

from .models import (
    hotdeal_model,
    pagination_model,
    pagination_links_model,
)

from .parsers import (
    pagination_parser,
)

from .utils import (
    _pagination_nav_links,
    _pagination_nav_header_links,
)

from flask import jsonify

from injector import inject

from ...services import HotdealService

hotdeal_ns = Namespace(name="hotdeals", description="핫딜 다중/단일 조회, 갱신을 위한 API", path="/hotdeals", validate=True)
hotdeal_ns.models[hotdeal_model.name] = hotdeal_model
hotdeal_ns.models[pagination_links_model.name] = pagination_links_model
hotdeal_ns.models[pagination_model.name] = pagination_model

@hotdeal_ns.route("", endpoint="hotdeal_list")
class HotdealList(Resource):

    @inject
    def __init__(self, api, svc: HotdealService, *args, **kwargs):
        self.svc = svc
        super().__init__(api, *args, **kwargs)
    
    # @hotdeal_ns.doc(security="Bearer")
    @hotdeal_ns.response(int(HTTPStatus.OK), "Ok", pagination_model)
    @hotdeal_ns.expect(pagination_parser)
    def get(self):

        request_data = pagination_parser.parse_args()
        page = request_data.get("page")
        per_page = request_data.get("per_page")
        pagination = self.svc.get_hotdeal_list(page, per_page)
        response_data = marshal(pagination, pagination_model)
        response_data["links"] = _pagination_nav_links(pagination)
        response = jsonify(response_data)
        response.headers["Link"] = _pagination_nav_header_links(pagination)
        response.headers["Total_Count"] = pagination.total
        return response

@hotdeal_ns.route("/update")
class HotdealUpdate(Resource):

    @inject
    def __init__(self, api, svc: HotdealService, *args, **kwargs):
        self.svc = svc
        super().__init__(api, *args, **kwargs)
    
    def post(self):

        self.svc.update_all_hotdeal_update_services()