import datetime

from ..extensions import db
from ..entity import Hotdeal

class HotdealModel(Hotdeal, db.Model):

    serialize_rules = ["scrape_at"]
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