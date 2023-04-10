from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from apps.grobid_client import Client

db = SQLAlchemy()
login_manager = LoginManager()
grobid_client = Client(base_url="http://localhost:8070/api")

