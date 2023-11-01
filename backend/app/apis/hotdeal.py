from flask_restx import Resource, Namespace, reqparse
from flask import make_response
import json
from injector import inject

from ..services import HotdealService

ns = Namespace("hotdeal", description="핫딜 정보 조회 API", path="/hotdeal")

@ns.route("/<string:id>")
class Hotdeal(Resource):

    @inject
    def __init__(self, api, svc: HotdealService, *args, **kwargs):
        self.svc = svc
        super().__init__(api, *args, **kwargs)
    
    def get(self, id):
        print(id)
        hotdeal = self.svc.get_hotdeal(id)

        return make_response(json.dumps({
            "success": True,
            "id": id,
            "data": hotdeal
        }, ensure_ascii=False, indent=4).encode("utf-8"))