from flask import Flask
from flask_cors import CORS
from src.conf.projects_registry__api import API__VERSION
from src.conf.manager__common__db import db_config
from src.service__api.utils.uuid_route_validate import UUID4Converter
from src.utils.jira import Jira
from src.utils.tempo import Tempo
from src.utils.conflience import Confluence
from src.validators.main import Validator
from db_utils.modules.db import attach_to_flask_app


app = Flask(__name__)
app.config.from_object('src.conf.service__api.Config')
attach_to_flask_app(app, db_config)
app.url_map.converters['uuid'] = UUID4Converter
cors = CORS(app)
jira = Jira()
tempo = Tempo()
confluence = Confluence()
validator = Validator()

from src.service__api.routes import api_bp  # noqa: F401
app.register_blueprint(api_bp, url_prefix=f'/api/{API__VERSION}')
import src.service__api.routes as routes  # noqa: F401


__all__ = (
    "api_bp",
    "app",
    "routes"
)
