from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian
from flask_cors import CORS
from grobid_client import Client

db = SQLAlchemy()
guard = Praetorian()
cors = CORS()

grobidClient = Client(base_url="http://localhost:8070/api")
