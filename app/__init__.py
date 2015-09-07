from flask import Flask
from flask.ext.mongoengine import MongoEngine

# Start a flask application context.
app = Flask(__name__)

# Load configuration from file.
app.config.from_object('config')

# Setup Db object.
db = MongoEngine(app)

# Import auth module and register blueprint.
from app.mod_auth.controller import auth
app.register_blueprint(auth, url_prefix='/auth')
