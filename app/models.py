# CPR MP FOR W2OL-PY-R4 2021 A.R.R.
from app import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String(120))
    isDone = db.Column(db.Boolean)
    ddl = db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.now)
    def __repr__(self):
        return '<title:{}>'.format(self.title)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.now)
    def __repr__(self):
        return '<id:{}>'.format(self.id)