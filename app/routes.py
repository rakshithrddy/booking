import time
from datetime import datetime
from os import abort

import stripe
from flask import render_template, redirect, url_for, request, flash, session, jsonify
from flask_api import status
from flask_login import logout_user, login_user, login_required, current_user

from app import app
from app import helper
from app.forms import LoginForm, RegistrationForm, TripForm, DriverDetailsForm, BookingForm
from app.models import User, Bookings, Driver

prepopulate_user = {'username': 'test', 'email': 'test@test.com',
                    'phone_number': '9876543210'}
stripe.api_key = app.config['STRIPE_SECRET_KEY']
operationally_optimized = True
data, cities = helper.get_city_coordinates()


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Index aka Home page for the application.
    The home page takes trip details like depart from, depart to, departure date, type of trip(one way by default)
    redirects to driver details if successful.
    """
    form = TripForm()
    if form.is_submitted():
        try:
            depart_date = form.departure_date.data  # get departure date from form
            present = datetime.now()
            if depart_date < present.date():
                flash("Please select the future booking date")
                return render_template('index.html', form=form, current_user=current_user, locations=cities)

            # Calculate total distance
            total_distance = helper.get_distance(source=request.form.get('depart_from'),
                                                 destination=request.form.get('depart_to'),
                                                 operational_optimize=operationally_optimized)
            # append all the details into session
            session['booking_details'] = {'trip_type': form.trip_type.data,
                                          'depart_from': request.form.get('depart_from'),
                                          'depart_to': request.form.get('depart_to'),
                                          'departure_date': time.mktime(depart_date.timetuple()),
                                          'total_distance': total_distance
                                          }
            # redirect to driver selection
            return redirect(url_for('select_driver'))
        except AttributeError:
            flash('All the fields are required')
            return render_template('index.html', form=form, current_user=current_user, locations=cities)
    return render_template('index.html', form=form, current_user=current_user, locations=cities)


@app.route('/maps', methods=['POST'])
def maps():
    languages = helper.get_languages()
    try:
        driver_to_cost_map, language_to_driver_map = helper.create_maps(languages)
        data__ = {'driver_to_cost_map': driver_to_cost_map, 'language_to_driver_map': language_to_driver_map}
        return jsonify(data__)
    except Exception as e:
        print(e)


@app.route('/select_driver', methods=['GET', 'POST'])
def select_driver():
    form = DriverDetailsForm(car_name='Nano')
    languages = helper.get_languages()
    driver_to_cost_map, language_to_driver_map = helper.create_maps(languages)
    if form.is_submitted():
        try:
            booking_details = session['booking_details']
            booking_details['driver_name'] = request.form.get('drivername')
            booking_details['cost_per_km'] = driver_to_cost_map[request.form.get('drivername')]
            booking_details['car_name'] = form.car_name.data
            booking_details['language'] = request.form.get('language')
            booking_details['total_cost'] = helper.cost(distance=booking_details['total_distance'],
                                                        cost_per_km=driver_to_cost_map[request.form.get('drivername')],
                                                        operational_optimized=True)
            session['booking_details'] = booking_details
            return redirect(url_for('book'))
        except (AttributeError, Exception):
            flash("All the fields are required")
            return render_template('select_driver.html', form=form, languages=languages,
                                   driver_to_cost_map=jsonify(driver_to_cost_map),
                                   language_to_driver_map=jsonify(language_to_driver_map))
    return render_template('select_driver.html', form=form, languages=languages,
                           driver_to_cost_map=jsonify(driver_to_cost_map),
                           language_to_driver_map=jsonify(language_to_driver_map))


@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = BookingForm()
    if form.is_submitted():
        d = datetime.strptime(form.pickup_time.data, "%H:%M")
        time_ = d.strftime('%I:%M %p')
        try:
            booking_details = session['booking_details']
            booking_details['pickup_address'] = form.pickup_address.data
            booking_details['pickup_time'] = time_
            booking_details['user_id'] = current_user.get_id()
            try:
                date_ = datetime.fromtimestamp(booking_details['departure_date'])
                booking_details['departure_date'] = date_.strftime("%m/%d/%Y")
            except TypeError:
                pass
            session['booking_details'] = booking_details
            return redirect(url_for('confirm'))
        except AttributeError:
            flash("All fields are required")
            render_template('book.html', form=form, current_user=current_user)
    return render_template('book.html', form=form, current_user=current_user)


@app.route('/confirm')
@login_required
def confirm():
    return render_template('confirm_booking.html', booking_details=session['booking_details'])


@app.route('/thanks')
@login_required
def thanks():
    booking_details = session['booking_details']
    ticket = helper.generate_ticket(current_user.get_id())
    booking_details['ticket'] = ticket
    book_obj = Bookings(**booking_details)
    book_obj.add_booking_details(booking_obj=book_obj)
    book_obj.commit_booking_details()
    return render_template('thanks.html', ticket=ticket)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(data=prepopulate_user)
    if form.is_submitted():
        user_ = User.get_user_by_username(form.username.data)
        if not user_:
            flash('Invalid Username or password or register')
            return redirect(url_for('login'))
        login_user(user_)
        try:
            next_page = request.referrer.split('next=%2F')[1]
            if next_page:
                return redirect(url_for(next_page))
        except:
            return redirect(url_for('index'))
    return render_template('login.html', form=form, title='Sign In', current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm(data=prepopulate_user)
    if form.validate_on_submit():
        user_ = User(username=form.username.data,
                     email=form.email.data,
                     phone_number=form.phone_number.data)
        user_.add_user(user_)
        flash('Congrats you registered successfully')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register', current_user=current_user)


@app.route('/payments', methods=['POST', 'GET'])
@login_required
def payments():
    details = session['booking_details']
    session_ = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Cab Booking',
                },
                'unit_amount': int(details['total_cost'] * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return {
        'checkout_session_id': session_['id'],
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }


# ########################  API ##########################

@app.route('/api/driver/<int:id>', methods=['GET'])
def get_driver(id):
    return jsonify(Driver.query.get_or_404(id).to_dict())


@app.route('/api/driver', methods=['POST'])
def create_driver():
    driver = Driver()
    data = request.get_json() or {}
    if 'name' not in data:
        return 'Name key not found', status.HTTP_400_BAD_REQUEST
    driver.from_dict(data, method='POST')
    driver.add_driver(driver)
    response = jsonify(driver.to_dict())
    response.status_code = 201
    return response


@app.route('/api/driver/<int:id>', methods=['PUT'])
def update_driver(id):
    driver = Driver.query.get_or_404(id)
    data = request.get_json() or {}
    if driver is None:
        return 'Record not found', status.HTTP_400_BAD_REQUEST
    if 'name' in data:
        return 'Record name cant be altered', status.HTTP_400_BAD_REQUEST
    driver.from_dict(data, method='PUT')
    driver.commit_driver()
    return jsonify(driver.to_dict())
