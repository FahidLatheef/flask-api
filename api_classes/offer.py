import datetime
from flask_restx import Resource, fields, marshal_with, abort
from tables import TABLE1

# OFFER MARSHALL STRUCTURE

resource_fields_offer = {
    'id': fields.Integer,
    'fname': fields.String,
    'lname': fields.String,
    'gender':fields.String,
    'customer.offer': fields.Integer,
}

# Offer Classes

class OfferFilterByID(Resource):
    @marshal_with(resource_fields_offer)
    def get(self, cardholder_id):
        result = TABLE1.query.filter_by(id=cardholder_id).first()
        if not result:
            abort(404, message=f"Could not find Cardholder with id: {cardholder_id}")
        return result


class OfferFilterByDays(Resource):
    @marshal_with(resource_fields_offer)
    def get(self, days):
        end = datetime.date.today()
        start = end - datetime.timedelta(days=days)
        results = TABLE1.query.filter(TABLE1.created_at <= end).filter(TABLE1.created_at >= start).all()
        if not results:
            abort(404, message=f"Could not find CardHolders created in last {days} days.")
        return results


class OfferFilterLastN(Resource):
    @marshal_with(resource_fields_offer)
    def get(self, last_n_holder):
        results = TABLE1.query.filter(TABLE1.id).order_by(TABLE1.id.desc()).limit(last_n_holder).all()
        if not results:
            abort(404, message=f"Could not find any CardHolders")
        return results


class OfferSearchName(Resource):
    @marshal_with(resource_fields_offer)
    def get(self, search_name):
        results = TABLE1.query.filter(TABLE1.fname.like(f'%{search_name}%') | TABLE1.lname.like(f'%{search_name}%')).all()
        if not results:
            abort(404, message=f"Could not find any CardHolders that contains '{search_name}'")
        return results


class OfferCreatedToday(Resource):
    @marshal_with(resource_fields_offer)
    def get(self):
        today = datetime.date.today()
        results = TABLE1.query.filter(TABLE1.created_at >= today).all()
        if not results:
            abort(404, message=f"Could not find any CardHolders created today")
        return results


class OfferAll(Resource):
    @marshal_with(resource_fields_offer)
    def get(self):
        results = TABLE1.query.order_by(TABLE1.id.desc()).all()
        if not results:
            abort(404, message=f"No Data Found")
        return results
