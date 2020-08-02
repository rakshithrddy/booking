from flask_login import UserMixin

from app import db, engine
from app import login
from datetime import datetime
from sqlalchemy.orm import sessionmaker

session_orm = sessionmaker(bind=engine)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120))
    phone_number = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    bookings = db.relationship('Bookings', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def add_user(cls, user_obj):
        db.session.add(user_obj)
        cls.commit_user()

    @classmethod
    def commit_user(cls):
        db.session.commit()


@login.user_loader
def load_user(id_):
    return User.query.get(int(id_))


class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    car_name = db.Column(db.String(20))
    cost_per_km = db.Column(db.Integer)
    depart_from = db.Column(db.String(50))
    depart_to = db.Column(db.String(50))
    departure_date = db.Column(db.String(50))
    driver_name = db.Column(db.String(50))
    language = db.Column(db.String(20))
    total_cost = db.Column(db.Integer)
    total_distance = db.Column(db.Integer)
    trip_type = db.Column(db.String(30))
    pickup_address = db.Column(db.String(20))
    pickup_time = db.Column(db.String(30))
    ticket = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<car_name: {self.car_name} cost_per_km: {self.cost_per_km} depart_from: {self.depart_from}" \
               f"depart_to: {self.depart_to} departure_date: {self.departure_date} driver_name: {self.driver_name}" \
               f"language: {self.language} total_cost: {self.total_cost} total_distance: {self.total_distance}>" \
               f"trip_type: {self.trip_type} pickup_address: {self.pickup_address} User_id: {self.user_id}"

    @classmethod
    def add_booking_details(cls, booking_obj):
        db.session.add(booking_obj)

    @classmethod
    def commit_booking_details(cls):
        db.session.commit()

    @classmethod
    def get_booking_details_by_userid(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.timestamp.desc()).first()


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    name = db.Column(db.String(40))
    about = db.Column(db.String(140))
    language = db.Column(db.String(30))
    cost_per_km = db.Column(db.Integer)

    @classmethod
    def get_driver_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_driver_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def add_driver(cls, driver_obj):
        db.session.add(driver_obj)
        cls.commit_driver()

    @classmethod
    def commit_driver(cls):
        db.session.commit()

    @staticmethod
    def jsonify_drivers():
        driver_data = {}
        records = db.session.query(Driver).all()
        for record in records:
            driver_data[record.name] = {"languages": record.language.split(','),
                                        "cost_per_km": record.cost_per_km}
        return driver_data

    @staticmethod
    def get_driver_names():
        records = db.session.query(Driver.name).all()
        records = [value for value, in records]
        return records

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'language': self.language,
            'cost_per_km': self.cost_per_km
        }
        return data

    def from_dict(self, data, method):
        global fields
        if method == 'POST':
            fields = ['name', 'about', 'language', 'cost_per_km']
        elif method == 'PUT':
            fields = ['about', 'language', 'cost_per_km']
        for field in fields:
            if field in data.keys():
                if field == 'language':
                    languages = data[field]
                    languages = languages.replace(" ", '')
                    data[field] = languages
                setattr(self, field, data[field])
