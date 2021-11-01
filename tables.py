from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_restx import Api
from flask_migrate import Migrate

path1 = 'sqlite:///' + 'databases/DB1.db'
path2 = 'sqlite:///' + 'databases/DB2.db'

# print(path1) 
# print(path2)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = path1
app.config['SQLALCHEMY_BINDS'] = {'DB2' : path2}

db = SQLAlchemy(app)

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/docs/')
app.register_blueprint(blueprint)
# api = Api(app, prefix="/api")

migrate = Migrate(app, db)

class TABLE1(db.Model):
    __tablename__ = 'table1'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(40), nullable=False)
    lname = db.Column(db.String(40), nullable=False)
    real_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(40), nullable=True, default = "ACTIVE")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now())
    gender = db.Column(db.String(20))
    customer = db.relationship('TABLE2', backref='table1', uselist=False)
    def __repr__(self):
        return f"Cardholder Table: {self.fname} {self.lname}"



class TABLE2(db.Model):
    __bind_key__ = 'DB2'
    __tablename__ = 'table2'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(40), nullable=False)
    lname = db.Column(db.String(40), nullable=False)
    customer_no = db.Column(db.Integer, db.ForeignKey('table1.real_id'))
    status = db.Column(db.String(40), nullable=True, default = "ACTIVE")
    offer = db.Column(db.Integer, default=50000)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now())

    def __repr__(self):
        return f"Customer Table: {self.fname} {self.lname}"
