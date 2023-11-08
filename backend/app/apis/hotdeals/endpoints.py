from flask_restx import Namespace, Resource
from http import HTTPStatus
from injector import inject

from .parsers import (
    pagination_parser,
)

from ..paginate import pagination_to_response

from ...models.hotdeal import hotdeal_model
from ...models.pagination import pagination_links_model, create_pagination_model
from ...services import HotdealService

hotdeal_ns = Namespace(name="hotdeals", description="핫딜 다중/단일 조회, 갱신을 위한 API", path="/hotdeals", validate=True)
hotdeal_ns.models[hotdeal_model.name] = hotdeal_model
hotdeal_ns.models[pagination_links_model.name] = pagination_links_model

pagination_model = create_pagination_model(hotdeal_model)
hotdeal_ns.models[pagination_model.name] = pagination_model

@hotdeal_ns.route("/", endpoint="hotdeal_list")
class HotdealList(Resource):

    @inject
    def __init__(self, api, svc: HotdealService, *args, **kwargs):
        self.svc = svc
        super().__init__(api, *args, **kwargs)
    
    # @hotdeal_ns.doc(security="Bearer")
    @hotdeal_ns.response(int(HTTPStatus.OK), "Ok", pagination_model)
    @hotdeal_ns.expect(pagination_parser)
    def get(self):

        # parsing
        request_data = pagination_parser.parse_args()
        page = request_data.get("page")
        per_page = request_data.get("per_page")

        # get pagination from services
        pagn = self.svc.get_hotdeal_list_pagination(page, per_page)

        return pagination_to_response(pagn, pagination_model, "hotdeal_list")

@hotdeal_ns.route("/<string:id>", endpoint="hotdeal")
@hotdeal_ns.param("id", "Hotdeal id")
class Hotdeal(Resource):

    @inject
    def __init__(self, api, svc: HotdealService, *args, **kwargs):
        self.svc = svc
        super().__init__(api, *args, **kwargs)
    
    @hotdeal_ns.response(int(HTTPStatus.OK), "Ok", hotdeal_model)
    @hotdeal_ns.marshal_with(hotdeal_model)
    def get(self, id):
        return self.svc.get_hotdeal(id)

@hotdeal_ns.route("/update")
class HotdealUpdate(Resource):

    @inject
    def __init__(self, api, svc: HotdealService, *args, **kwargs):
        self.svc = svc
        super().__init__(api, *args, **kwargs)
    
    def post(self):

        self.svc.update_all_hotdeal_update_services()