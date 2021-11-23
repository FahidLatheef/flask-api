from fastapi import HTTPException, status, APIRouter
import pandas as pd
from database import df1, df2
import json
import datetime

router = APIRouter(
    prefix="/offer",
    tags=['Offer']
)

# Merging df1 and df2 to df
df = pd.merge(left=df1, right=df2[['customer_no', 'offer']], left_on='real_id', right_on='customer_no')
# Renaming id to more relevant cardholder_id
df = df.rename(columns={'id': 'cardholder_id'})


@router.get("/cardholder_id/{cardholder_id}")
def filter_by_id(cardholder_id:int):
    filtered_data = df.loc[df['cardholder_id']==cardholder_id]
    result = json.loads(filtered_data[['cardholder_id', 'fname', 'lname', 'gender', 'offer']].to_json(orient='records', date_format='iso'))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find Cardholder with id: {cardholder_id}")
    return result

@router.get("/days/{days}")
def created_last_n_days(days:int):
    end = pd.to_datetime(datetime.date.today())
    start = end - datetime.timedelta(days=days)
    filtered_data = df.loc[(df['created_at']<=end) & (df['created_at']>=start)]
    results = json.loads(filtered_data[['cardholder_id', 'fname', 'lname', 'gender', 'offer']].to_json(orient='records', date_format='iso'))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find Cardholders created in last {days} days.")
    return results

@router.get("/last_n_user/{last_n_user}")
def filter_by_last_n_created_users(last_n_user:int):
    filtered_data = df.tail(last_n_user)
    results = json.loads(filtered_data[['cardholder_id', 'fname', 'lname', 'gender', 'offer']].to_json(orient='records', date_format='iso'))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find any Cardholders")    
    return results

@router.get("/search_name/{search_name}")
def filter_by_search_string(search_name:str):
    filtered_data = df.loc[(df['fname'].str.contains(search_name, case=False)) | df['lname'].str.contains(search_name, case=False)]
    results = json.loads(filtered_data[['cardholder_id', 'fname', 'lname', 'gender', 'offer']].to_json(orient='records', date_format='iso'))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find any Cardholder that contains '{search_name}'")
    return results

@router.get("/today")
def users_created_today():
    today = pd.to_datetime(datetime.date.today())
    filtered_data = df.loc[df['created_at']>=today]
    results = json.loads(filtered_data[['cardholder_id', 'fname', 'lname', 'gender', 'offer']].to_json(orient='records', date_format='iso'))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find any Cardholders created today")
    return results

@router.get("/full_data")
def full_data():
    results = json.loads(df[['cardholder_id', 'fname', 'lname', 'gender', 'offer']].to_json(orient='records', date_format='iso'))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Data Found")
    return results
