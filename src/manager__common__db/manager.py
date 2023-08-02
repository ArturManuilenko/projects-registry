from flask import Flask
from flask_migrate import Migrate
from db_utils.modules.db import db
from db_utils.modules.db import attach_to_flask_app
import src.manager__common__db.models.models as models
from src.conf.manager__common__db import db_config

app = Flask(__name__)

attach_to_flask_app(app, db_config)

migrate = Migrate(compare_type=True)
migrate.init_app(app, db)

__all__ = (
    'models',
    'app',
    'db',
)
