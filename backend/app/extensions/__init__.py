from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()
api = Api(version="1.0", title="API 문서", description="Swagger 문서", doc="/api-docs", prefix="/api")

from .injector import _configure_injector

from flask import url_for