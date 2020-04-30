import datetime
from index import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resume = db.Column(db.String(140), nullable=False)
    titre =  db.Column(db.String(140), nullable=False)
    content = db.Column(db.String(140), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)