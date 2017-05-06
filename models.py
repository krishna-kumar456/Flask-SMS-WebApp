from app import db
from sqlalchemy.dialects.postgresql import JSON


class Contacts(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    phone_no = db.Column(db.String())
    

    def __init__(self, name, phone_no):
        self.name = name
        self.phone_no = phone_no
        

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    message = db.Column(db.String())
    time = db.Column(db.DateTime())
    

    def __init__(self, name, phone_no, time):
        self.name = name
        self.phone_no = phone_no
        self.time = time

        

    def __repr__(self):
        return '<id {}>'.format(self.id)