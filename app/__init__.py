from flask import Flask
from flask.ext.mongoengine import MongoEngine

import logging

# Start a flask application context.
app = Flask(__name__)

# Load configuration from file.
app.config.from_object('config')

# Setup Db object.
db = MongoEngine(app)

# Setup logging.
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

# Import auth module and register blueprint.
from app.mod_auth.controller import auth
app.register_blueprint(auth, url_prefix='/auth')

# Import budget module and register blueprint.
from app.mod_budget.controller import budget
app.register_blueprint(budget, url_prefix='/budget')
