import datetime

from flask import Flask
from flask import flash, render_template, request, url_for, session, redirect

from auth import Auth
from call import Call
from customer import Customer

app = Flask(__name__)
app.secret_key = b'J.;0ajk>,m8jkLIn89hans*jkj90($'


def check_for_logged_in():
    '''Check if there is a user currently logged in.
    If not, redirect to the login page. Otherwise do nothing.'''
    auth = Auth()
    if auth.is_logged_in():
        return True
    else:
        return False


def check_for_valid_customer_id(customer_id):

    '''Check if the given customer ID matches up to an 
    actual customer record. If not, redirect to the /customers/
    page.'''
    customers = Customer.get_all()
    for customer in customers:
        if customer_id == customer['customer_id']:
            return True
        else:
            return False


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        auth = Auth()
        if auth.login(username, password):
            return redirect(url_for('show_customers'))
        else:
            flash('Could not log you in')
    return render_template('auth/login.html')


@app.route("/logout/")
def logout():
    auth = Auth()
    auth.logout()
    return redirect(url_for('login'))


@app.route("/")
@app.route("/customers/")
def show_customers():
    if check_for_logged_in() == True:
        customers = Customer.get_all()
        return render_template('customer/show-list.html', customers=customers)
    else:
        return redirect(url_for('login'))


@app.route("/customers/add/", methods=['GET', 'POST'])
def add_customer():
    '''Check for logged in.
    If GET, show the page to add a customer.
    If POST, do the following:
    1. Get data from the POST request.
    2. Also get the current user's ID.
    3. Create a new Customer object with all the above data.
    4. Save it to the database.
    5. Redirect to the /customers/ page.'''
    if check_for_logged_in() == True:
    
        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            address1 = request.form.get('address1')
            address2 = request.form.get('address2')
            postal_code = request.form.get('postal_code')
            city = request.form.get('city')
            country = request.form.get('country')
            customer_id = None

            auth = Auth()
            current_user = auth.get_current_user()
            user_id = current_user['user_id']
            c = Customer(first_name, last_name, email, phone, address1, address2, postal_code, city, country, customer_id, user_id)
            c.save()
            return redirect(url_for('show_customers'))

        return render_template('customer/add.html')
    
    else:
        return redirect(url_for('login'))

@app.route("/customers/<int:customer_id>/edit/", methods=['GET', 'POST'])
def edit_customer(customer_id):
    '''Check for logged in customer. Check for valid customer id.
    If GET, show the page to edit the given customer.
    If POST, do the following:
    1. Get data from the POST request.
    2. Get a Customer object from the Customer class, that matches the
       given customer_id. This object will contain the OLD data.
    3. Set the values for the customer object - use the data you got
       from the POST request.
    4. Save the customer object.
    5. Redirect to /customers/ page.'''
    if check_for_logged_in() == True:

        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            address1 = request.form.get('address1')
            address2 = request.form.get('address2')
            postal_code = request.form.get('postal_code')
            city = request.form.get('city')
            country = request.form.get('country')
            customer_id = customer_id
            auth = Auth()
            current_user = auth.get_current_user()
            user_id = current_user['user_id']

            customer = Customer(first_name, last_name, email, phone, address1, address2, postal_code, city, country, customer_id, user_id)
            customer.save()
            return redirect(url_for('show_customers')) 
        
        customer = Customer.get(customer_id)
        return render_template('customer/edit.html', customer=customer)

    else:
        return redirect(url_for('login'))
    


@app.route("/customers/<int:customer_id>/")
def show_customer(customer_id):
    '''Check for logged in user. Check for valid customer id.
    Get customer object that matches the given customer id.
    Get a list of calls that are associated with the given customer id.
    Render the 'customer/show-one.html' template with the above data.'''
    if check_for_logged_in() == True:
        customer = Customer.get(customer_id)
        auth = Auth()
        current_user = auth.get_current_user()
        user_id = current_user['user_id']
        calls = Call.get_for_customer(customer_id, user_id)
        return render_template('customer/show-one.html', customer=customer, calls=calls)
    else:
        return redirect(url_for('login'))



@app.route("/calls/<int:customer_id>/add/", methods=['POST'])
def add_call(customer_id):
    '''Check for logged in user. Check for valid customer id.
    Get customer object that matches the given customer id.
    Get the user_id of the currently logged-in user.
    Get the current date-time.
    Get the notes from the POST request.
    Use the above data to create a new Call object. Save it.
    Redirect to the /customers/<customer_id>/ page.'''
    if check_for_logged_in() == True:
        if check_for_valid_customer_id(customer_id) == True:
            customer_id = customer_id
            c = Customer.get(customer_id)

            auth = Auth()
            current_user = auth.get_current_user()
            user_id = current_user['user_id']

            current_dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            note = request.form.get('note')
            call_id = None

            new_call = Call(current_dt, note, call_id, customer_id, user_id)
            new_call.save()
            return redirect(url_for('show_customer', customer_id=customer_id))
        else:
            return redirect(url_for('show_customers'))
    else:
        return redirect(url_for('login'))

