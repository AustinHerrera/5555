
from app import db, app
from hashlib import md5
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from . import lm

class machinetype(db.Model):
    Machineid = db.Column(db.Integer, primary_key=True)
    Machinetype = db.Column(db.String(20))
    machines = db.relationship('machine', backref='Machineid',lazy='dynamic')

    def __init__(self,Machineid, Machinetype):
        self.Machineid = Machineid
        self.Machinetype = Machinetype

    def __repr__(self):
        return '<machineid %r>' % self.Machineid

class contracts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Contractname = db.Column(db.String(10))
    contract = db.relationship('machine', backref='contractid', lazy='dynamic')
    def __init__(self,id, Contractname):
        self.id = id
        self.Contractname = Contractname
    def __repr__(self):
        return '<id %r>' % self.id


class machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Machinetypeid = db.Column(db.Integer, db.ForeignKey('machinetype.Machineid'))
    Machineip = db.Column(db.String(12))
    Machinename = db.Column(db.String(20))
    Contractid = db.Column(db.Integer, db.ForeignKey('contracts.id'))

    def __repr__(self):
        return '<id %r>' % self.id

class actions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    Action = db.Column(db.String(25))

    def __repr__(self):
        return '<Action %r>' % self.Action


    def __init__(self, Action):
        self.Action = Action

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#    username= db.Column(db.String(25), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.String(25))
    password_hash = db.Column(db.String(128))

    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, email, password):
        self.password = password
        self.email = email

    def __repr__(self):
        return '<user %r>' % self.email
    
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.email)


@lm.user_loader
def load_user(email):
    return User.query.filter_by(email = email).first()
