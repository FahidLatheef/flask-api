import datetime
from flask_restx import Resource, fields, marshal_with, abort
from tables import TABLE2


# TABLE 2 MARSHALL STRUCTURE

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

# Customer table2 Classes

class CustomerFilterByID(Resource):
    @marshal_with(resource_fields_table2)
    def get(self, customer_id):
        result = TABLE2.query.filter_by(id=customer_id).first()
        if not result:
            abort(404, message=f"Could not find Customer with id: {customer_id}")
        return result


class CustomerFilterByCustomerNo(Resource):
    @marshal_with(resource_fields_table2)
    def get(self, customer_customer_no):
        result = TABLE2.query.filter_by(customer_no=customer_customer_no).first()
        if not result:
            abort(404, message=f"Could not find Customer with customer_no: {customer_customer_no}")
        return result


class CustomerFilterByDays(Resource):
    @marshal_with(resource_fields_table2)
    def get(self, days):
        end = datetime.date.today()
        start = end - datetime.timedelta(days=days)
        results = TABLE2.query.filter(TABLE2.created_at <= end).filter(TABLE2.created_at >= start).all()
        if not results:
            abort(404, message=f"Could not find Customers created in last {days} days.")
        return results


class CustomerFilterLastN(Resource):
    @marshal_with(resource_fields_table2)
    def get(self, last_n_customer):
        results = TABLE2.query.filter(TABLE2.id).order_by(TABLE2.id.desc()).limit(last_n_customer).all()
        if not results:
            abort(404, message=f"Could not find any Customers")
        return results


class CustomerSearchName(Resource):
    @marshal_with(resource_fields_table2)
    def get(self, search_name):
        results = TABLE2.query.filter(TABLE2.fname.like(f'%{search_name}%') | TABLE2.lname.like(f'%{search_name}%')).all()
        if not results:
            abort(404, message=f"Could not find any Customer that contains '{search_name}'")
        return results


class CustomerCreatedToday(Resource):
    @marshal_with(resource_fields_table2)
    def get(self):
        today = datetime.date.today()
        results = TABLE2.query.filter(TABLE2.created_at >= today).all()
        if not results:
            abort(404, message=f"Could not find any Customers created today")
        return results


class CustomerAll(Resource):
    @marshal_with(resource_fields_table2)
    def get(self):
        results = TABLE2.query.order_by(TABLE2.id.desc()).all()
        if not results:
            abort(404, message=f"No Data Found")
        return results
