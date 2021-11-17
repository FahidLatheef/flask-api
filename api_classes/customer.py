import datetime
from sanic_restful_api import abort
from sanic.views import HTTPMethodView
import pandas as pd
import json
from sanic.response import json as sanic_json
from tables import df2 as df  # Importing table2 dataframe as dfß

# Customer Classes

class CustomerFilterByID(HTTPMethodView):
    async def get(self, request, customer_id):
        result = json.loads(df.loc[df['id']==customer_id].to_json(orient='records', date_format='iso'))
        if not result:
            abort(404, message=f"Could not find Customer with id: {customer_id}")
        return sanic_json(result)


class CustomerFilterByCustomerNo(HTTPMethodView):
    async def get(self, request, customer_customer_no):
        result = json.loads(df.loc[df['customer_no']==customer_customer_no].to_json(orient='records', date_format='iso'))
        if not result:
            abort(404, message=f"Could not find Customer with customer_no: {customer_customer_no}")
        return sanic_json(result)


class CustomerFilterByDays(HTTPMethodView):
    async def get(self, request, days):
        end = pd.to_datetime(datetime.date.today())
        start = end - datetime.timedelta(days=days)
        results = json.loads(df.loc[(df['created_at']<=end) & (df['created_at']>=start)].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find Customers created in last {days} days.")
        return sanic_json(results)


class CustomerFilterLastN(HTTPMethodView):
    async def get(self, request, last_n_customer):
        results = json.loads(df.tail(last_n_customer).to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any Customers")
        return sanic_json(results)


class CustomerSearchName(HTTPMethodView):
    async def get(self, request, search_name):
        results = json.loads(df.loc[(df['fname'].str.contains(search_name, case=False)) | df['lname'].str.contains(search_name, case=False)].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any Customer that contains '{search_name}'")
        return sanic_json(results)


class CustomerCreatedToday(HTTPMethodView):
    async def get(self, request):
        today = pd.to_datetime(datetime.date.today())
        results = json.loads(df.loc[df['created_at']>=today].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any Customers created today")
        return sanic_json(results)


class CustomerAll(HTTPMethodView):
    async def get(self, request):
        results = json.loads(df.to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"No Data Found")
        return sanic_json(results)
