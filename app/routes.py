from app import app,db
from flask import render_template,redirect,url_for,flash,request
from app.forms import LoginForm,RegisterForm,AddProduct,AddStore
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,Product,Store,Sale
from datetime import datetime,date
from app import login_manager

login_manager.login_view='login'



@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user,remember=form.remember_me.data)
                return redirect(url_for('store'))
            flash("invalid username or password")
            return redirect(url_for('login'))
    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        password=generate_password_hash(form.password.data)
        user=User(username=form.username.data,email=form.email.data,phone=form.phone.data,password_hash=password,type='normal')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/store',methods=['GET','POST'])
@login_required
def store():
    form = AddProduct()
    products=Product.query.all()
    stores=Store.query.all()
    num = Product.query.filter_by(name="cover",status="not sold").count()
    num_glass = Product.query.filter_by(name="glass",status="not sold").count()
    num_sale = Sale.query.filter_by(created_on=date.today()).count()
    if current_user.is_authenticated:
      return render_template('store.html',products=products,form=form,stores=stores,num=num,glass=num_glass,num_sale=num_sale)




@app.route('/add_product',methods=['GET','POST'])
@login_required
def add_product():
    form=AddProduct()
    if form.validate_on_submit():



        product=Product(name=form.name.data,model=form.model.data,serial=form.serial.data,price=form.price.data,quantity=form.quantity.data,status="not sold")
        product.store_id=1
        db.session.add(product)
        db.session.commit()
        flash("product added successfully")
    return redirect(url_for("store"))


@app.route('/edit_product/<int:id>',methods=['GET','POST'])
@login_required
def edit_product(id):
    product = Product.query.get(id)
    if request.method=='POST':

        product.name=request.form['name']
        product.serial=request.form['serial']
        product.price=request.form['price']
        product.quantity=request.form['quantity']
        product.store_id=1
        # db.session.add(product)
        db.session.commit()
        flash("product updated successfully")
        return redirect(url_for('store'))
    return render_template('edit_product.html',product=product)

@app.route('/sell_product/<int:id>',methods=['GET','POST'])
@login_required
def sell_product(id):
    product = Product.query.get(id)
    product.status = "SOLD"
    sale = Sale(product_id=id)
    db.session.add(sale)
    db.session.commit()
    return redirect(url_for('store'))

@app.route('/sales',methods=['GET','POST'])
@login_required
def sales():
    sales=Sale.query.all()


    sales_today=Sale.query.filter_by(created_on=date.today())
    num_sale=Sale.query.filter_by(created_on=date.today()).count()
    if current_user.is_authenticated:
      return render_template('sales.html',sales=sales,sales_today=sales_today,num=num_sale)

@app.route('/delete_sale/<int:id>',methods=['GET','POST'])
def delete_sale(id):
    sale=Sale.query.get(id)
    db.session.delete(sale)
    db.session.commit()
    return redirect(url_for('sale'))

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        name=request.form['search']
        searched_products=Product.query.filter_by(name=name)

    return render_template('store.html',results=searched_products)




@app.route('/add_store',methods=['GET','POST'])
@login_required
def add_store():
    form=AddStore()
    if form.validate_on_submit():
        store=Store(name=form.name.data,location=form.location.data)
        db.session.add(store)
        db.session.commit()
        flash("store added successfully")
        return redirect(url_for('store'))
    return render_template('addstore.html',form=form)

@app.route('/delete_product/<int:id>',methods=['POST','GET'])
def delete_product(id):
    product=Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('store'))
