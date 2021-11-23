from fastapi import APIRouter, HTTPException, status
from database import df2 as df
import pandas as pd
import datetime
import json


router = APIRouter(
    prefix="/customer",
    tags=['Customers']
)


@router.get("/id/{id}")
def filter_by_id(id:int):
    result = json.loads(df.loc[df['id']==id].to_json(orient='records', date_format='iso'))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find Customer with id: {id}")
    return result

@router.get("/customer_no/{customer_no}")
def filter_by_customer_no(customer_no:int):
    result = json.loads(df.loc[df['customer_no']==customer_no].to_json(orient='records', date_format='iso'))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find Customer with customer_no: {customer_no}")
    return result

@router.get("/days/{days}")
def filter_by_days(days:int):
    end = pd.to_datetime(datetime.date.today())
    start = end - datetime.timedelta(days=days)
    results = json.loads(df.loc[(df['created_at']<=end) & (df['created_at']>=start)].to_json(orient='records', date_format='iso'))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find Customers created in last {days} days.")
    return results

@router.get("/last_n_user/{last_n_user}")
def filter_by_last_n_created_users(last_n_user:int):
    results = json.loads(df.tail(last_n_user).to_json(orient='records', date_format='iso'))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find any Customers")
    return results

@router.get("/search_name/{search_name}")
def filter_by_search_string(search_name:str):
    results = json.loads(df.loc[(df['fname'].str.contains(search_name, case=False)) | df['lname'].str.contains(search_name, case=False)].to_json(orient='records', date_format='iso'))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find any Customer that contains '{search_name}'")
    return results

@router.get("/today")
def users_created_today():
    today = pd.to_datetime(datetime.date.today())
    results = json.loads(df.loc[df['created_at']>=today].to_json(orient='records', date_format='iso'))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find any Customers created today")
    return results

@router.get("/full_data")
def full_data():
    results = json.loads(df.to_json(orient='records', date_format='iso'))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Data Found")
    return results
