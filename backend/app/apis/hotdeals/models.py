from flask_restx import Model
from flask_restx.fields import String, Float, DateTime, Boolean, Nested, Integer, List

hotdeal_model = Model(
    "Hotdeal",
    {
        "id": String,
        "title": String,
        "original_price": Float,
        "price_to_krw": Float,
        "currency_type": String,
        "store_link": String,
        "source_link": String,
        "scrape_at": DateTime,
        "is_done": Boolean,
        "is_blind": Boolean,
    },
)

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)

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
        "items": List(Nested(hotdeal_model)),
    },
)