import datetime
from flask_restx import Resource, abort
import pandas as pd
import json
from tables import df1 as df  # Importing table1 dataframe as df


# Cardholder Classes

class CardHolderFilterByID(Resource):
    def get(self, cardholder_id):
        result = json.loads(df.loc[df['id']==cardholder_id].to_json(orient='records', date_format='iso'))
        if not result:
            abort(404, message=f"Could not find CardHolder with id: {cardholder_id}")
        return result[0]


class CardHolderFilterByRealID(Resource):
    def get(self, cardholder_real_id):
        result = json.loads(df.loc[df['real_id']==cardholder_real_id].to_json(orient='records', date_format='iso'))
        if not result:
            abort(404, message=f"Could not find CardHolder with real_id: {cardholder_real_id}")
        return result[0]


class CardHolderFilterByDays(Resource):
    def get(self, days):
        end = pd.to_datetime(datetime.date.today())
        start = end - datetime.timedelta(days=days)
        results = json.loads(df.loc[(df['created_at']<=end) & (df['created_at']>=start)].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find CardHolders created in last {days} days.")
        return results


class CardHolderFilterLastN(Resource):
    def get(self, last_n_holder):
        results = json.loads(df.tail(last_n_holder).to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any CardHolders")
        return results


class CardHolderSearchName(Resource):
    def get(self, search_name):
        results = json.loads(df.loc[(df['fname'].str.contains(search_name, case=False)) | df['lname'].str.contains(search_name, case=False)].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any CardHolders that contains '{search_name}'")
        return results


class CardHolderCreatedToday(Resource):
    def get(self):
        today = pd.to_datetime(datetime.date.today())
        results = json.loads(df.loc[df['created_at']>=today].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any CardHolders created today")
        return results


class CardHolderAll(Resource):
    def get(self):
        results = json.loads(df.to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"No Data Found")
        return results
