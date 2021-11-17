import datetime
from sanic.views import HTTPMethodView
from sanic_restful_api import abort
import pandas as pd
import json
from sanic.response import json as sanic_json
from tables import df1, df2

# Merging df1 and df2 to df
df = pd.merge(left=df1, right=df2[['customer_no', 'offer']], left_on='real_id', right_on='customer_no')

# Renaming id to more relevant cardholder_id
df = df.rename(columns={'id': 'cardholder_id'})

# Offer Classes

class OfferFilterByID(HTTPMethodView):
    async def get(self, request, cardholder_id):
        filtered_data = df.loc[df['cardholder_id']==cardholder_id]
        result = json.loads(filtered_data[['cardholder_id', 'fname', 'lname', 'gender', 'offer']].to_json(orient='records', date_format='iso'))
        if not result:
            abort(404, message=f"Could not find Cardholder with id: {cardholder_id}")
        return sanic_json(result)


class OfferFilterByDays(HTTPMethodView):
    async def get(self, request, days):
        end = pd.to_datetime(datetime.date.today())
        start = end - datetime.timedelta(days=days)
        filtered_data = df.loc[(df['created_at']<=end) & (df['created_at']>=start)]
        results = json.loads(filtered_data[['cardholder_id', 'fname', 'lname', 'gender', 'offer']].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find CardHolders created in last {days} days.")
        return sanic_json(results)


class OfferFilterLastN(HTTPMethodView):
    async def get(self, request, last_n_holder):
        filtered_data = df.tail(last_n_holder)
        results = json.loads(filtered_data[['cardholder_id', 'fname', 'lname', 'gender', 'offer']].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any CardHolders")
        return sanic_json(results)


class OfferSearchName(HTTPMethodView):
    async def get(self, request, search_name):
        filtered_data = df.loc[(df['fname'].str.contains(search_name, case=False)) | df['lname'].str.contains(search_name, case=False)]
        results = json.loads(filtered_data[['cardholder_id', 'fname', 'lname', 'gender', 'offer']].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any CardHolders that contains '{search_name}'")
        return sanic_json(results)


class OfferCreatedToday(HTTPMethodView):
    async def get(self, request):
        today = pd.to_datetime(datetime.date.today())
        filtered_data = df.loc[df['created_at']>=today]
        results = json.loads(filtered_data[['cardholder_id', 'fname', 'lname', 'gender', 'offer']].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any CardHolders created today")
        return sanic_json(results)

class OfferAll(HTTPMethodView):
    async def get(self, request):
        results = json.loads(df[['cardholder_id', 'fname', 'lname', 'gender', 'offer']].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"No Data Found")
        return sanic_json(results)
