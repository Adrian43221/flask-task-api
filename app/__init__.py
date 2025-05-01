from flask import Flask
from .extensions import db, migrate
from .routes import main
from app.models import user, task

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)

    return app
