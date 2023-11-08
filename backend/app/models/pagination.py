from flask_restx import Model
from flask_restx.fields import String, Nested, Boolean, Integer, List

from .hotdeal import hotdeal_model

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)

# pagination_model = Model(
#     "Pagination",
#     {
#         "links": Nested(pagination_links_model, skip_none=True),
#         "has_prev": Boolean,
#         "has_next": Boolean,
#         "page": Integer,
#         "total_pages": Integer(attribute="pages"),
#         "items_per_page": Integer(attribute="per_page"),
#         "total_items": Integer(attribute="total"),
#         "items": List(Nested(hotdeal_model)),
#     },
# )

def create_pagination_model(model: Model) -> Model:
    pagination_model = Model(
        "Pagination",
        {
            "links": Nested(pagination_links_model, skip_none=True),
            "has_prev": Boolean,
            "has_next": Boolean,
            "page": Integer,
            "total_pages": Integer(attribute="pages"),
            "items_per_page": Integer(attribute="per_page"),
            "total_items": Integer(attribute="total"),
            "items": List(Nested(model)),
        },
    )
    return pagination_model