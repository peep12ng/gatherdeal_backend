from flask import Flask
from flask_cors import CORS
import os

from . import config as Config
from .config import get_config
from .extensions import db, migrate, scheduler, api, _configure_injector

from .tasks import hotdeal_update_task

from .apis import hotdeal_ns

NAMESPACES = [
    hotdeal_ns,
]

def create_app(app_name=None, config=None) -> Flask:

    if app_name is None:
        app_name = Config.DefaultConfig.PROJECT

    app = Flask(app_name)
    configure_app(app, config)
    configure_extensions(app)

    return app

def configure_app(app: Flask, config=None):

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(Config.DefaultConfig)

    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(get_config(os.getenv("CONFIG")))
    print(os.getenv("CONFIG"))

def configure_extensions(app):

    # flask_sqlalchemy
    db.init_app(app)

    # flask_migrate
    migrate.init_app(app, db)

    # flask_apshceduler
    scheduler.init_app(app)

    # flask_restx
    api.init_app(app)

    for ns in NAMESPACES:
        api.add_namespace(ns)
    
    from . import tasks
    from . import models
    scheduler.add_job(
        func=hotdeal_update_task,
        id="hotdeal_update",
        trigger="interval",
        seconds=10800,
        max_instances=1,
        start_date="2000-01-01 12:19:00",
    )
    scheduler.start()

    # flask_injector
    _configure_injector(app, db)