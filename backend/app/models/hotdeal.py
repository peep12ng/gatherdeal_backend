from flask_restx import Model
from flask_restx.fields import String, Float, DateTime, Boolean
import datetime

from ..extensions import db
from ..entity import Hotdeal

class HotdealModel(Hotdeal, db.Model):
    
    _now = datetime.datetime.now()

    id = db.Column(db.VARCHAR(30), primary_key=True)
    title = db.Column(db.TEXT)
    original_price = db.Column(db.DOUBLE)
    price_to_krw = db.Column(db.DOUBLE)
    currency_type = db.Column(db.VARCHAR(30))
    store_link = db.Column(db.TEXT)
    source_link = db.Column(db.TEXT)
    scrape_at = db.Column(db.DATETIME, default=_now)
    is_done = db.Column(db.BOOLEAN)
    is_blind = db.Column(db.BOOLEAN)

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