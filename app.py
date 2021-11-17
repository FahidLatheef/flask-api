# from flask import render_template, redirect
from sanic.response import file, redirect, text
from tables import api, app, jinja

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

# Create tables: Run it once
# db.create_all()
# db.session.commit()

# Cardholder Routes
app.add_route(CardHolderFilterByID, "/cardholder/id/<int:cardholder_id>")
app.add_route(CardHolderFilterByRealID, "/cardholder/real_id/<int:cardholder_real_id>")
app.add_route(CardHolderFilterByDays, "/cardholder/created_last_n_days/<int:days>")
app.add_route(CardHolderFilterLastN, "/cardholder/last_n_person/<int:last_n_holder>")
app.add_route(CardHolderSearchName, "/cardholder/search/<string:search_name>")
app.add_route(CardHolderCreatedToday, "/cardholder/created_today")
app.add_route(CardHolderAll, "/cardholder/full_data")

# Customer Routes
app.add_route(CustomerFilterByID.as_view(), "/customer/id/<int:customer_id>")
app.add_route(CustomerFilterByCustomerNo, "/customer/customer_no/<int:customer_customer_no>")
app.add_route(CustomerFilterByDays, "/customer/created_last_n_days/<int:days>")
app.add_route(CustomerFilterLastN, "/customer/last_n_person/<int:last_n_customer>")
app.add_route(CustomerSearchName, "/customer/search/<string:search_name>")
app.add_route(CustomerCreatedToday, "/customer/created_today")
app.add_route(CustomerAll.as_view(), "/customer/full_data")

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
