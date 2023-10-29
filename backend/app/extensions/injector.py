from injector import Module, singleton, Injector
from flask_injector import FlaskInjector

class AppModule(Module):
    def __init__(self, app, db):
        self.app = app
        self.db = db
    
    def configure(self, binder):
        from flask_sqlalchemy.session import Session
        binder.bind(Session, to=self.db.session, scope=singleton)

def _configure_injector(app, db):

    injector = Injector([AppModule(app, db)])

    return FlaskInjector(app=app, injector=injector)