from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_restful import Api, Resource, fields, marshal_with, abort
from sqlalchemy.sql.expression import func

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

# Create tables: Run it once
# db.create_all()
# db.session.commit()


# TABLE 1 API ENDPOINTS

resource_fields_table1 = {
    'id': fields.Integer,
    'fname': fields.String,
    'lname': fields.String,
    'real_id': fields.Integer,
    'status': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

class CardHolderFilterByID(Resource):
    @marshal_with(resource_fields_table1)
    def get(self, cardholder_id):
        result = TABLE1.query.filter_by(id=cardholder_id).first()
        if not result:
            abort(404, message=f"Could not find CardHolder with id: {cardholder_id}")
        return result

api.add_resource(CardHolderFilterByID, "/cardholder/id/<int:cardholder_id>")


class CardHolderFilterByRealID(Resource):
    @marshal_with(resource_fields_table1)
    def get(self, cardholder_real_id):
        result = TABLE1.query.filter_by(real_id=cardholder_real_id).first()
        if not result:
            abort(404, message=f"Could not find CardHolder with real_id: {cardholder_real_id}")
        return result

api.add_resource(CardHolderFilterByRealID, "/cardholder/real_id/<int:cardholder_real_id>")


class CardHolderFilterByDays(Resource):
    @marshal_with(resource_fields_table1)
    def get(self, days):
        end = datetime.date.today()
        start = end - datetime.timedelta(days=days)
        results = TABLE1.query.filter(TABLE1.created_at <= end).filter(TABLE1.created_at >= start).all()
        if not results:
            abort(404, message=f"Could not find CardHolders created in last {days} days.")
        return results

api.add_resource(CardHolderFilterByDays, "/cardholder/created_last_n_days/<int:days>")


class CardHolderFilterLastN(Resource):
    @marshal_with(resource_fields_table1)
    def get(self, last_n_holder):
        results = TABLE1.query.filter(TABLE1.id).order_by(TABLE1.id.desc()).limit(last_n_holder).all()
        if not results:
            abort(404, message=f"Could not find any CardHolders")
        return results

api.add_resource(CardHolderFilterLastN, "/cardholder/last_n_person/<int:last_n_holder>")


class CardHolderSearchName(Resource):
    @marshal_with(resource_fields_table1)
    def get(self, search_name):
        results = TABLE1.query.filter(TABLE1.fname.like(f'%{search_name}%') | TABLE1.lname.like(f'%{search_name}%')).all()
        if not results:
            abort(404, message=f"Could not find any CardHolders that contains '{search_name}'")
        return results

api.add_resource(CardHolderSearchName, "/cardholder/search/<string:search_name>")

class CardHolderCreatedToday(Resource):
    @marshal_with(resource_fields_table1)
    def get(self):
        today = datetime.date.today()
        results = TABLE1.query.filter(TABLE1.created_at >= today).all()
        if not results:
            abort(404, message=f"Could not find any CardHolders created today")
        return results

api.add_resource(CardHolderCreatedToday, "/cardholder/created_today")

class CardHolderAll(Resource):
    @marshal_with(resource_fields_table1)
    def get(self):
        results = TABLE1.query.order_by(TABLE1.id.desc()).all()
        if not results:
            abort(404, message=f"No Data Found")
        return results

api.add_resource(CardHolderAll, "/cardholder/full_data")

# TABLE 2 API ENDPOINTS

resource_fields_table2 = {
    'id': fields.Integer,
    'fname': fields.String,
    'lname': fields.String,
    'customer_no': fields.Integer,
    'status': fields.String,
    'offer': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}


class CustomerFilterByID(Resource):
    @marshal_with(resource_fields_table2)
    def get(self, customer_id):
        result = TABLE2.query.filter_by(id=customer_id).first()
        if not result:
            abort(404, message=f"Could not find Customer with id: {customer_id}")
        return result

api.add_resource(CustomerFilterByID, "/customer/id/<int:customer_id>")


class CustomerFilterByCustomerNo(Resource):
    @marshal_with(resource_fields_table2)
    def get(self, customer_customer_no):
        result = TABLE2.query.filter_by(customer_no=customer_customer_no).first()
        if not result:
            abort(404, message=f"Could not find Customer with customer_no: {customer_customer_no}")
        return result

api.add_resource(CustomerFilterByCustomerNo, "/customer/customer_no/<int:customer_customer_no>")


class CustomerFilterByDays(Resource):
    @marshal_with(resource_fields_table2)
    def get(self, days):
        end = datetime.date.today()
        start = end - datetime.timedelta(days=days)
        results = TABLE2.query.filter(TABLE2.created_at <= end).filter(TABLE2.created_at >= start).all()
        if not results:
            abort(404, message=f"Could not find Customers created in last {days} days.")
        return results

api.add_resource(CustomerFilterByDays, "/customer/created_last_n_days/<int:days>")


class CustomerFilterLastN(Resource):
    @marshal_with(resource_fields_table2)
    def get(self, last_n_customer):
        results = TABLE2.query.filter(TABLE2.id).order_by(TABLE2.id.desc()).limit(last_n_customer).all()
        if not results:
            abort(404, message=f"Could not find any Customers")
        return results

api.add_resource(CustomerFilterLastN, "/customer/last_n_person/<int:last_n_customer>")


class CustomerSearchName(Resource):
    @marshal_with(resource_fields_table2)
    def get(self, search_name):
        results = TABLE2.query.filter(TABLE2.fname.like(f'%{search_name}%') | TABLE2.lname.like(f'%{search_name}%')).all()
        if not results:
            abort(404, message=f"Could not find any Customer that contains '{search_name}'")
        return results

api.add_resource(CustomerSearchName, "/customer/search/<string:search_name>")


class CustomerCreatedToday(Resource):
    @marshal_with(resource_fields_table2)
    def get(self):
        today = datetime.date.today()
        results = TABLE2.query.filter(TABLE2.created_at >= today).all()
        if not results:
            abort(404, message=f"Could not find any Customers created today")
        return results

api.add_resource(CustomerCreatedToday, "/customer/created_today")


class CustomerAll(Resource):
    @marshal_with(resource_fields_table2)
    def get(self):
        results = TABLE2.query.order_by(TABLE2.id.desc()).all()
        if not results:
            abort(404, message=f"No Data Found")
        return results

api.add_resource(CustomerAll, "/customer/full_data")


@app.route('/')
def index():
    return render_template('home.html', title="Home")

@app.route('/home')
def home():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)