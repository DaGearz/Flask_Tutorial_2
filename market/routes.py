from market import app
from flask import render_template, redirect, url_for, request, flash
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm
from . import db
from flask_login import current_user, login_user, logout_user, login_required
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', method =["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    items = Item.query.all()

    return render_template('market.html', items=items, purchase_form=purchase_form)

@app.route('/register', methods =["GET", "POST"])
def register_page():

    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account creted successfully! You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #if there are not errors
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a use:{err_msg}', category='danger')


    return render_template('register.html', form=form)

@app.route('/login', methods =["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(form.password.data):
            login_user(attempted_user)
            flash(f'Success! Your are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match', category='danger')



    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    user = current_user.username
    logout_user()

    flash(f'You are logged out {user}', category='info')
    return(redirect(url_for('home_page')))
