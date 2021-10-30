from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_restful import Api

path1 = 'sqlite:///' + 'DB1.db'
path2 = 'sqlite:///' + 'DB2.db'

# print(path1) 
# print(path2)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = path1
app.config['SQLALCHEMY_BINDS'] = {'DB2' : path2}

db = SQLAlchemy(app)
api = Api(app)


class TABLE1(db.Model):
    __tablename__ = 'table1'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(40), nullable=False)
    lname = db.Column(db.String(40), nullable=False)
    real_id = db.Column(db.Integer)
    status = db.Column(db.String(40), nullable=True, default = "ACTIVE")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now())
    gender = db.Column(db.String(20))

    def __repr__(self):
        return f"Cardholder Table: {self.fname} {self.lname}"



class TABLE2(db.Model):
    __bind_key__ = 'DB2'
    __tablename__ = 'table2'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(40), nullable=False)
    lname = db.Column(db.String(40), nullable=False)
    customer_no = db.Column(db.Integer)
    status = db.Column(db.String(40), nullable=True, default = "ACTIVE")
    offer = db.Column(db.Integer, default=50000)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now())

    def __repr__(self):
        return f"Customer Table: {self.fname} {self.lname}"
