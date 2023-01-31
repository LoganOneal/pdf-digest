from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian
from flask_cors import CORS
from grobid.client import GrobidClient

db = SQLAlchemy()
guard = Praetorian()
cors = CORS()

grobidClient = GrobidClient("localhost", "8070")
