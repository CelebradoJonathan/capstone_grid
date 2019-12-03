from flask import Flask
import os

from src.config import app_config
from src.models import db
from src.views.FileView import file_api as file_blueprint
# from src.views.fileIdView import fileid_api as fileid_blueprint
# env_name = "development"
env_name = os.getenv('FLASK_ENV')


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    db.init_app(app)
    app.register_blueprint(file_blueprint, url_prefix='/filelog')
    @app.route('/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return 'Congratulations! Your first endpoint is working'
    return app


app = create_app(env_name)