from db import db
from datetime import datetime

class CarModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(255), nullable=False, unique = False)
    model = db.Column(db.String(255), nullable=False, unique = False)
    transmission = db.Column(db.String(255), nullable=False, unique = False)
    price = db.Column(db.Float(precision=2), nullable=False, unique = False)
    release_year = db.Column(db.DateTime, default=datetime.utcnow, unique = False)


