import datetime
from sanic_restful_api import abort
from sanic.views import HTTPMethodView
import pandas as pd
import json
from sanic.response import json as sanic_json
from tables import df1 as df  # Importing table1 dataframe as df

# Cardholder Classes

class CardHolderFilterByID(HTTPMethodView):
    async def get(self, request, cardholder_id):
        result = json.loads(df.loc[df['id']==cardholder_id].to_json(orient='records', date_format='iso'))
        if not result:
            abort(404, message=f"Could not find CardHolder with id: {cardholder_id}")
        return sanic_json(result)


class CardHolderFilterByRealID(HTTPMethodView):
    def get(self, request, cardholder_real_id):
        result = json.loads(df.loc[df['real_id']==cardholder_real_id].to_json(orient='records', date_format='iso'))
        if not result:
            abort(404, message=f"Could not find CardHolder with real_id: {cardholder_real_id}")
        return sanic_json(result)


class CardHolderFilterByDays(HTTPMethodView):
    async def get(self, request, days):
        end = pd.to_datetime(datetime.date.today())
        start = end - datetime.timedelta(days=days)
        results = json.loads(df.loc[(df['created_at']<=end) & (df['created_at']>=start)].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find CardHolders created in last {days} days.")
        return sanic_json(results)


class CardHolderFilterLastN(HTTPMethodView):
    async def get(self, request, last_n_holder):
        results = json.loads(df.tail(last_n_holder).to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any CardHolders")
        return sanic_json(results)


class CardHolderSearchName(HTTPMethodView):
    def get(self, request, search_name):
        results = json.loads(df.loc[(df['fname'].str.contains(search_name, case=False)) | df['lname'].str.contains(search_name, case=False)].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any CardHolders that contains '{search_name}'")
        return sanic_json(results)


class CardHolderCreatedToday(HTTPMethodView):
    async def get(self, request):
        today = pd.to_datetime(datetime.date.today())
        results = json.loads(df.loc[df['created_at']>=today].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any CardHolders created today")
        return sanic_json(results)


class CardHolderAll(HTTPMethodView):
    async def get(self, request):
        results = json.loads(df.to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"No Data Found")
        return sanic_json(results)
