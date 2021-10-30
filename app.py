from flask import render_template, url_for, redirect
from tables import api, app

from cardholder import (
    CardHolderFilterByID,
    CardHolderFilterByRealID,
    CardHolderFilterByDays,
    CardHolderFilterLastN,
    CardHolderSearchName,
    CardHolderCreatedToday,
    CardHolderAll
)

from customer import (
    CustomerFilterByID,
    CustomerFilterByCustomerNo,
    CustomerFilterByDays,
    CustomerFilterLastN,
    CustomerSearchName,
    CustomerCreatedToday,
    CustomerAll
)


# Create tables: Run it once
# db.create_all()
# db.session.commit()


# Cardholder Routes
api.add_resource(CardHolderFilterByID, "/cardholder/id/<int:cardholder_id>")
api.add_resource(CardHolderFilterByRealID, "/cardholder/real_id/<int:cardholder_real_id>")
api.add_resource(CardHolderFilterByDays, "/cardholder/created_last_n_days/<int:days>")
api.add_resource(CardHolderFilterLastN, "/cardholder/last_n_person/<int:last_n_holder>")
api.add_resource(CardHolderSearchName, "/cardholder/search/<string:search_name>")
api.add_resource(CardHolderCreatedToday, "/cardholder/created_today")
api.add_resource(CardHolderAll, "/cardholder/full_data")

# Customer Routes
api.add_resource(CustomerFilterByID, "/customer/id/<int:customer_id>")
api.add_resource(CustomerFilterByCustomerNo, "/customer/customer_no/<int:customer_customer_no>")
api.add_resource(CustomerFilterByDays, "/customer/created_last_n_days/<int:days>")
api.add_resource(CustomerFilterLastN, "/customer/last_n_person/<int:last_n_customer>")
api.add_resource(CustomerSearchName, "/customer/search/<string:search_name>")
api.add_resource(CustomerCreatedToday, "/customer/created_today")
api.add_resource(CustomerAll, "/customer/full_data")

@app.route('/')
def index():
    return render_template('home.html', title="Home")

@app.route('/home')
def home():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)