from flask_restx.reqparse import RequestParser
from flask_restx.inputs import positive

pagination_parser = RequestParser(bundle_errors=True)
pagination_parser.add_argument("page", type=positive, required=False, default=1)
pagination_parser.add_argument("per_page", type=positive, required=False, choices=[5, 10, 25, 50, 100], default=10)