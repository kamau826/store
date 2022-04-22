from app import db,login_manager
from flask_login import UserMixin
from datetime import datetime,date


@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone=db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    type=db.Column(db.String(50),default="normal")

    def __repr__(self):
        return '<User {}>'.format(self.username)



class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    location=db.Column(db.String(255))
    products=db.relationship('Product',backref='store')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    model=db.Column(db.String(255))
    serial=db.Column(db.String(255))
    price=db.Column(db.Integer)
    quantity=db.Column(db.Integer)
    status=db.Column(db.String(30))
    store_id=db.Column(db.Integer,db.ForeignKey('store.id'))
    sales=db.relationship('Sale',backref='product')

class Sale(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    product_id=db.Column(db.Integer,db.ForeignKey('product.id'))
    created_on=db.Column(db.Date,default=date.today())


