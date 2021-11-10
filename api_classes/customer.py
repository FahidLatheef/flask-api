import datetime
from flask_restx import Resource, abort
import pandas as pd
import json

# df is table2
df = pd.read_csv("databases/table2.csv")

# Function to convert time string to datetime format
def date_convert(date_to_convert):
    try:
        return datetime.datetime.strptime(str(date_to_convert), f'%Y-%m-%d %X.%f')
    except:
        return float('nan')
# Converting time string to datetime format
df['created_at'] = df['created_at'].apply(date_convert)
df['updated_at'] = df['updated_at'].apply(date_convert)

# Customer Classes

class CustomerFilterByID(Resource):
    def get(self, customer_id):
        result = json.loads(df.loc[df['id']==customer_id].to_json(orient='records', date_format='iso'))
        if not result:
            abort(404, message=f"Could not find Customer with id: {customer_id}")
        return result[0]


class CustomerFilterByCustomerNo(Resource):
    def get(self, customer_customer_no):
        result = json.loads(df.loc[df['customer_no']==customer_customer_no].to_json(orient='records', date_format='iso'))
        if not result:
            abort(404, message=f"Could not find Customer with customer_no: {customer_customer_no}")
        return result[0]


class CustomerFilterByDays(Resource):
    def get(self, days):
        end = pd.to_datetime(datetime.date.today())
        start = end - datetime.timedelta(days=days)
        results = json.loads(df.loc[(df['created_at']<=end) & (df['created_at']>=start)].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find Customers created in last {days} days.")
        return results


class CustomerFilterLastN(Resource):
    def get(self, last_n_customer):
        results = json.loads(df.tail(last_n_customer).to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any Customers")
        return results


class CustomerSearchName(Resource):
    def get(self, search_name):
        results = json.loads(df.loc[(df['fname'].str.contains(search_name, case=False)) | df['lname'].str.contains(search_name, case=False)].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any Customer that contains '{search_name}'")
        return results


class CustomerCreatedToday(Resource):
    def get(self):
        today = pd.to_datetime(datetime.date.today())
        results = json.loads(df.loc[df['created_at']>=today].to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"Could not find any Customers created today")
        return results


class CustomerAll(Resource):
    def get(self):
        results = json.loads(df.to_json(orient='records', date_format='iso'))
        if not results:
            abort(404, message=f"No Data Found")
        return results
