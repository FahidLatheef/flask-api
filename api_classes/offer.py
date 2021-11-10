import datetime
from flask_restx import Resource, fields, marshal_with, abort
import pandas as pd
import json
from tables import df1, df2

# Merging df1 and df2 to df
df = pd.merge(left=df1, right=df2[['customer_no', 'offer']], left_on='real_id', right_on='customer_no')

# Renaming id to more relevant cardholder_id
df = df.rename(columns={'id': 'cardholder_id'})

# OFFER MARSHALL STRUCTURE

resource_fields_offer = {
    'cardholder_id': fields.Integer,
    'fname': fields.String,
    'lname': fields.String,
    'gender': fields.String,
    'offer': fields.Integer,
}

# Offer Classes

class OfferFilterByID(Resource):
    @marshal_with(resource_fields_offer)
    def get(self, cardholder_id):
        result = json.loads(df.loc[df['cardholder_id']==cardholder_id].to_json(orient='records', date_format='iso'))
        if not result:
            abort(404, message=f"Could not find Cardholder with id: {cardholder_id}")
        return result[0]


class OfferFilterByDays(Resource):
    @marshal_with(resource_fields_offer)
    def get(self, days):
        end = pd.to_datetime(datetime.date.today())
        start = end - datetime.timedelta(days=days)
        results = json.loads(df.loc[(df['created_at']<=end) & (df['created_at']>=start)].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find CardHolders created in last {days} days.")
        return results


class OfferFilterLastN(Resource):
    @marshal_with(resource_fields_offer)
    def get(self, last_n_holder):
        results = json.loads(df.tail(last_n_holder).to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any CardHolders")
        return results


class OfferSearchName(Resource):
    @marshal_with(resource_fields_offer)
    def get(self, search_name):
        results = json.loads(df.loc[(df['fname'].str.contains(search_name, case=False)) | df['lname'].str.contains(search_name, case=False)].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any CardHolders that contains '{search_name}'")
        return results


class OfferCreatedToday(Resource):
    @marshal_with(resource_fields_offer)
    def get(self):
        today = pd.to_datetime(datetime.date.today())
        results = json.loads(df.loc[df['created_at']>=today].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any CardHolders created today")
        return results


class OfferAll(Resource):
    @marshal_with(resource_fields_offer)
    def get(self):
        results = json.loads(df.to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"No Data Found")
        return results
