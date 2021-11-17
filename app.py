# from flask import render_template, redirect
from sanic.response import redirect
from tables import app, jinja

from api_classes.cardholder import (
    CardHolderFilterByID,
    CardHolderFilterByRealID,
    CardHolderFilterByDays,
    CardHolderFilterLastN,
    CardHolderSearchName,
    CardHolderCreatedToday,
    CardHolderAll
)

from api_classes.customer import (
    CustomerFilterByID,
    CustomerFilterByCustomerNo,
    CustomerFilterByDays,
    CustomerFilterLastN,
    CustomerSearchName,
    CustomerCreatedToday,
    CustomerAll
)

from api_classes.offer import (
    OfferFilterByID,
    OfferFilterByDays,
    OfferFilterLastN,
    OfferSearchName,
    OfferCreatedToday,
    OfferAll
)

# Cardholder Routes
app.add_route(CardHolderFilterByID.as_view(), "/cardholder/id/<cardholder_id:int>", methods=['GET'])
app.add_route(CardHolderFilterByRealID.as_view(), "/cardholder/real_id/<cardholder_real_id:int>", methods=['GET'])
app.add_route(CardHolderFilterByDays.as_view(), "/cardholder/created_last_n_days/<days:int>", methods=['GET'])
app.add_route(CardHolderFilterLastN.as_view(), "/cardholder/last_n_person/<last_n_holder:int>", methods=['GET'])
app.add_route(CardHolderSearchName.as_view(), "/cardholder/search/<search_name:str>", methods=['GET'])
app.add_route(CardHolderCreatedToday.as_view(), "/cardholder/created_today", methods=['GET'])
app.add_route(CardHolderAll.as_view(), "/cardholder/full_data", methods=['GET'])

# Customer Routes
app.add_route(CustomerFilterByID.as_view(), "/customer/id/<customer_id:int>", methods=['GET'])
app.add_route(CustomerFilterByCustomerNo.as_view(), "/customer/customer_no/<customer_customer_no:int>", methods=['GET'])
app.add_route(CustomerFilterByDays.as_view(), "/customer/created_last_n_days/<days:int>", methods=['GET'])
app.add_route(CustomerFilterLastN.as_view(), "/customer/last_n_person/<last_n_customer:int>", methods=['GET'])
app.add_route(CustomerSearchName.as_view(), "/customer/search/<search_name:str>", methods=['GET'])
app.add_route(CustomerCreatedToday.as_view(), "/customer/created_today", methods=['GET'])
app.add_route(CustomerAll.as_view(), "/customer/full_data", methods=['GET'])

# Offer Routes
app.add_route(OfferFilterByID.as_view(), "/offer/id/<cardholder_id:int>", methods=['GET'])
app.add_route(OfferFilterByDays.as_view(), "/offer/created_last_n_days/<days:int>", methods=['GET'])
app.add_route(OfferFilterLastN.as_view(), "/offer/last_n_person/<last_n_holder:int>", methods=['GET'])
app.add_route(OfferSearchName.as_view(), "/offer/search/<search_name:str>", methods=['GET'])
app.add_route(OfferCreatedToday.as_view(), "/offer/created_today", methods=['GET'])
app.add_route(OfferAll.as_view(), "/offer/full_data", methods=['GET'])

@app.route('/')
async def index(request):
    return jinja.render('home.html', request=request, title="Sanic API Home ")

@app.route('/home')
async def home(request):
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
