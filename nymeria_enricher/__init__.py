from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from nymeria_enricher.config import Config

import logging

logger = logging.getLogger(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.auth'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Set logger Configuration
    formatter = logging.Formatter(Config.APP_LOG_FORMAT)
    file_handler = logging.FileHandler(Config.APP_LOG_LOCATION)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log_level = logging.getLevelName(Config.APP_LOG_LEVEL)
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    db.init_app(app)
    login_manager.init_app(app)

    from nymeria_enricher.enrichment.routes import csv_enrich_blueprint
    from nymeria_enricher.auth.routes import auth_blueprint
    app.register_blueprint(csv_enrich_blueprint)
    app.register_blueprint(auth_blueprint)

    with app.app_context():
        db.create_all()
    return app
