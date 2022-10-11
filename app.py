import email
# from multiprocessing.sharedctypes import Value
import random as rand
from sqlite3 import connect
from traceback import print_tb
# from turtle import title
from dateutil import parser
from unicodedata import name
from wsgiref.validate import validator
from flask import Flask, flash, redirect, render_template, url_for, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_mail import Mail, Message
from itsdangerous.serializer import Serializer
from sqlalchemy import Integer, false, null
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LOGIN_MESSAGE, LoginManager, UserMixin, login_required, login_user, logout_user, current_user

# -----MISC-----
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tradeJournalProject2022'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tjp.db'

app.config['SQLALCHEMY_BINDS'] = {
    'tjpdata': 'sqlite:///tjpdata.db', 'tjp': 'sqlite:///tjp.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# -----GMAIL-----
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tjp.app22@gmail.com'
app.config['MAIL_PASSWORD'] = 'htslsutatpzdnuai'

# #-----YAHOO-----
# app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TSL'] =True
# app.config['MAIL_USERNAME'] = 'tjp.app@yahoo.com'
# app.config['MAIL_PASSWORD'] = 'tjpTJP#2k22'

# #-----OUTLOOK-----
# app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TSL'] =True
# app.config['MAIL_USERNAME'] = 'tjp.app@outlook.com'
# app.config['MAIL_PASSWORD'] = 'tjpTJP#2k22'

mail = Mail(app)


# -----Classes-----
class UserTable(UserMixin, db.Model):
    __bind_key__ = 'tjp'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False, unique=False)
    lastname = db.Column(db.String(20), nullable=False, unique=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    cityto = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(150), nullable=True)
    phonenumber = db.Column(db.String(13), nullable=False, unique=True)
    zipcode = db.Column(db.String(6), nullable=False, unique=False)
    userid = db.Column(db.String(8), nullable=False, unique=True)

    def get_token(self):
        serial = Serializer(app.config['SECRET_KEY'])
        return serial.dumps({'user_id': self.id})

    @staticmethod
    def verify_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return UserTable.query.get(user_id)


class DataTableCr(db.Model):
    __bind_key__ = 'tjpdata'
    sno = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(8), nullable=False, unique=False)
    securityname = db.Column(db.String(50), nullable=False, unique=False)
    buyprice = db.Column(db.Float, nullable=True, unique=False)
    sellprice = db.Column(db.Float, nullable=True, unique=False)
    quantity = db.Column(db.Integer, nullable=False, unique=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    buy_date = db.Column(db.DateTime, nullable=True)
    sell_date = db.Column(db.DateTime, nullable=True)
    no_of_lot = db.Column(db.Integer, nullable=True, unique=False)
    lot_size = db.Column(db.Integer, nullable=True, unique=False)
    profit = db.Column(db.Float, nullable=True, unique=False)
    profit_percent = db.Column(db.Float, nullable=True, unique=False)
    trade_type = db.Column(db.String(10), nullable=False, unique=False)
    instrument = db.Column(db.String(10), nullable=False, unique=False)
    trade_state = db.Column(db.String(10), nullable=False, unique=False)
    isOpen = db.Column(db.Boolean, nullable=False, unique=False)
    # When isOpen == True, that means the Trade State is 'OPEN'.

    def __repr__(self):
        return '<Task %r>' % self.sno


@login_manager.user_loader
def load_user(user_id):
    return UserTable.query.get(int(user_id))


# -----Forms-----
class LoginForm(FlaskForm):
    __bind_key__ = 'tjp'
    userid = StringField('user id', validators=[
        InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=90)])
    remember = BooleanField('Remember me')


class ChangePasswordForm(FlaskForm):
    __bind_key__ = 'tjp'
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=90)])
    confirmpassword = PasswordField('confirm password', validators=[
        InputRequired(), Length(min=8, max=90)])


class ResetRequestForm(FlaskForm):
    __bind_key__ = 'tjp'
    email = StringField('email', validators=[
                        InputRequired(), Length(min=4, max=100)])


class RegistrationForm(FlaskForm):
    __bind_key__ = 'tjp'
    firstname = StringField('First Name *', validators=[
                            InputRequired(), Length(min=1, max=30)])
    lastname = StringField('Last Name *', validators=[
                           InputRequired(), Length(min=1, max=30)])
    email = StringField('Email *', validators=[InputRequired(), Email(
        message='Invalid Email,\nPlease Try Again!'), Length(max=100)])
    password = PasswordField('Password *', validators=[
                             InputRequired(), Length(min=8, max=90)])
    confirmpassword = PasswordField('Confirm Password *', validators=[
                                    InputRequired(), Length(min=8, max=90)])
    cityto = StringField('City *', validators=[
                         InputRequired(), Length(min=3, max=35)])
    zipcode = StringField('Zipcode *', validators=[
                          InputRequired(), Length(min=0, max=6)])
    address = StringField('Address', validators=[Length(min=0, max=150)])
    state = StringField('State *', validators=[
                        InputRequired(), Length(min=3, max=35)])
    phonenumber = StringField('Phone Number', validators=[
                              Length(min=10, max=12)])


# -----Routes-----
@app.route('/')
def index():

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserTable.query.filter_by(userid=form.userid.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid user-id or password :(</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('login.html', title='Login', form=form)


def send_mail(user):
    token = user.get_token()
    msg = Message('Password Reset Request', recipients=[
                  user.email], sender='noreply@tjp.com')
    msg.body = f'''To reset your password, please follow the link below:
                
    {url_for('reset_token', token=token, _external=True)}'''

    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = ResetRequestForm()

    if form.validate_on_submit():
        user = UserTable.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
            print('Reset link has been sent!')
            flash("A URL has been sent to your email", "info")
            # info is a built in category for flash()
            return redirect(url_for('login'))

    return render_template('reset_request.html', title='Reset Request', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = UserTable.verify_token(token)
    if user is None:
        print('Invalid token, please try again')
        return redirect(url_for('reset_request'))

    form = ChangePasswordForm()
    if form.validate_on_submit():
        if form.password.data == form.confirmpassword.data:
            hashed_pass = generate_password_hash(
                form.password.data, method='sha256')
        user.password = hashed_pass
        db.session.commit()
        print('Password has been changed')
        return redirect(url_for('login'))

    return render_template('change_password.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data == form.confirmpassword.data:

            cityFirst = form.cityto.data[0]
            stateFirst = form.state.data[0]
            userid = form.firstname.data[0].upper() + form.lastname.data[0].upper() + cityFirst.upper(
            ) + stateFirst.upper() + form.zipcode.data[4] + form.zipcode.data[5] + f'{rand.randint(10, 99)}'
            print(userid)

            # if (id + 1) < 10 :
            #     idVar += firstTwo + '000' + (UserTable.id+1)
            #     print(idVar)

            hashed_pass = generate_password_hash(
                form.password.data, method='sha256')
            new_user = UserTable(email=form.email.data, password=hashed_pass, cityto=form.cityto.data, state=form.state.data,
                                 zipcode=form.zipcode.data, phonenumber=form.phonenumber.data, address=form.address.data,
                                 firstname=form.firstname.data, lastname=form.lastname.data, userid=userid)

            db.session.add(new_user)
            db.session.commit()

            return render_template('prompt.html', userid=userid)
        else:
            return "<h1>Passwords Don't Match, kindly change</h1>"
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data +'</h1>'
    return render_template('signup.html', form=form)


# def aslidate(year, month, day):
#     year1=int(year)
#     if month[0] == '0':
#         month1=month[1]
#         if day[0] == '0':
#             day1 = day[1]
#             return (datetime(int(year1), int(month1), int(day1) ))
#         else:
#             return (datetime(int(year1), int(month1), int(day[0:1]) ))
    
#     else:
#         month1=month[0:1]
#         if day[0] == '0':
#             day1 = day[1]
#             return (datetime(int(year1), int(month1), int(day1) ))
#         else:
#             return (datetime(int(year1), int(month1), int(day[0:1]) ))


@app.route('/delete/<int:sno>')
def delete(sno):
    OpenTrade = DataTableCr.query.filter_by(sno=sno).first()
    db.session.delete(OpenTrade)
    db.session.commit()
    
    

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
@login_required
def update(sno):
    current_trade = DataTableCr.query.filter_by(sno=sno).first()
    State = current_trade.trade_state
    TradeType = current_trade.trade_type
    checkbox_stats_OPENBUY=False
    checkbox_stats_OPENSELL=False
    new_buydate = ""
    new_selldate = ""
    if (State == "OPEN"):
        if (TradeType == "Buy"):
            new_buydate=current_trade.buy_date.strftime("%Y-%m-%d")
            checkbox_stats_OPENBUY=True
        if (TradeType == "Sell"):
            new_selldate=current_trade.sell_date.strftime("%Y-%m-%d")
            checkbox_stats_OPENSELL=True
    elif (State == "CLOSED"):
        new_selldate=current_trade.sell_date.strftime("%Y-%m-%d")
        new_buydate=current_trade.buy_date.strftime("%Y-%m-%d")



    # new_buydate=current_trade.buy_date.strftime("%Y-%m-%d")
    # new_selldate=current_trade.sell_date.strftime("%Y-%m-%d")
    print("New_Buydate", new_buydate)

    
    # final_buy_date = datetime.strptime(new_buydate, '%Y-%m-%d')
    # print("FINAL SHIT", final_buy_date)

    if request.method=='POST':
        trade_type_backend = request.form['trade_type']

        # buy ya phir sell

        trade_instrument = request.form['trade_instrument']
        
        # equity, futures, call ya put

        security_name = request.form['stockname']
        lotsize = request.form['lotsize']
        nolot = request.form['nolot']
        quantity= request.form['quantity']
        buy_date_initial = request.form['buydate']
        
        buy_price = request.form['buyprice']
        
        
        sell_date_initial = request.form['selldate']
        sell_price = request.form['sellprice']
        
        sell_date2_initial = request.form['selldate2']

        

        sell_price2=request.form['sellprice2']

        open_buy_default= request.form['openBuyfirst_defaultcheck']
        open_sell_default=request.form['openSELLfirst_defaultcheck']
        

        
        buy_date2_initial = request.form['buydate2']
        

        buy_price2=request.form['buyprice2']
        net_profit_num= request.form['profit']
        profit_percent=request.form['profitpercent']
        
        if open_sell_default == "OPENSELL_ye" and open_buy_default == "OPENBUY_no":
            # open_sell=request.form['openSell'].value
            print("OPEN TRADE SELL")
            # sell_DATE_format = sell_date2
            sell_date2 = parser.parse(sell_date2_initial)
            isOpen=True
            tradeState="OPEN"
            new_trade = DataTableCr(userid=current_user.userid, trade_type=trade_type_backend, instrument=trade_instrument,  securityname=security_name,
                               lot_size=lotsize, no_of_lot=nolot, quantity=quantity, sell_date=sell_date2, sellprice=sell_price2, trade_state=tradeState, isOpen=isOpen)
            print("security_name", security_name)
            delete(sno)
            print("New Trade", new_trade)

            print("zero")
            db.session.add(new_trade)
            print("hello ", new_trade)
            print("ONE")
            db.session.commit()
            print("two")
            name = current_user.firstname
            user_for_pass = current_user.userid
            tasks = DataTableCr.query.order_by(DataTableCr.date_created).all()
            return render_template('dashboard.html',  tasks=tasks, name=name, user_for_pass=user_for_pass)

        if open_buy_default == "OPENBUY_ye" and open_sell_default == "OPENSELL_no":
            open_buy= request.form['openBuy']
            print("OPEN TRADE BUY")
            # buy_DATE_format = buy_date
            buy_date = parser.parse(buy_date_initial)
            isOpen=True
            tradeState="OPEN"
            new_trade = DataTableCr(userid=current_user.userid, trade_type=trade_type_backend, instrument=trade_instrument,  securityname=security_name,
                               lot_size=lotsize, no_of_lot=nolot, quantity=quantity, buy_date=buy_date, buyprice=buy_price, trade_state=tradeState, isOpen=isOpen)
            print("security_name", security_name)
            delete(sno)
            print("New Trade", new_trade)

            print("zero")
            db.session.add(new_trade)
            print("hello ", new_trade)
            print("ONE")
            db.session.commit()
            print("two")
            name = current_user.firstname
            user_for_pass = current_user.userid
            tasks = DataTableCr.query.order_by(DataTableCr.date_created).all()
            return render_template('dashboard.html',  tasks=tasks, name=name, user_for_pass=user_for_pass)

        if open_buy_default == "OPENBUY_no" and open_sell_default == "OPENSELL_no":
            tradestate2="CLOSED"
            isOPEN=False
            if trade_type_backend == "Buy":
                # buy_DATE_format = buy_date
                # sell_DATE_format = sell_date
                buy_date = parser.parse(buy_date_initial)
                sell_date = parser.parse(sell_date_initial)
                new_trade = DataTableCr(userid=current_user.userid, trade_type=trade_type_backend, instrument=trade_instrument,  securityname=security_name,
                               lot_size=lotsize, no_of_lot=nolot, quantity=quantity, buy_date=buy_date, buyprice=buy_price, sell_date=sell_date, sellprice=sell_price, profit=net_profit_num, profit_percent=profit_percent, trade_state="CLOSED", isOpen=False)
                
                # current_trade.userid = current_user.userid
                

                print("security_name", security_name)
                delete(sno)
                print("New Trade", new_trade)

                print("zero")
                db.session.add(new_trade)
                print("hello ", new_trade)
                print("ONE")
                db.session.commit()
                print("two")
                name = current_user.firstname
                user_for_pass = current_user.userid
                tasks = DataTableCr.query.order_by(DataTableCr.date_created).all()
                return render_template('dashboard.html',  tasks=tasks, name=name, user_for_pass=user_for_pass)
                
            else:
                # buy_DATE_format = buy_date2
                # sell_DATE_format = sell_date2
                buy_date2 = parser.parse(buy_date2_initial)
                sell_date2 = parser.parse(sell_date2_initial)
                new_trade = DataTableCr(userid=current_user.userid, trade_type=trade_type_backend, instrument=trade_instrument,  securityname=security_name,
                               lot_size=lotsize, no_of_lot=nolot, quantity=quantity, buy_date=buy_date2, buyprice=buy_price2, sell_date=sell_date2, sellprice=sell_price2, profit=net_profit_num, profit_percent=profit_percent, trade_state="CLOSED", isOpen=False)
                print("security_name", security_name)

                print("New Trade", new_trade)
                delete(sno)
                print("zero")
                db.session.add(new_trade)
                print("hello ", new_trade)
                print("ONE")
                db.session.commit()
                print("two")
                name = current_user.firstname
                user_for_pass = current_user.userid
                tasks = DataTableCr.query.order_by(DataTableCr.date_created).all()
                return render_template('dashboard.html',  tasks=tasks, name=name, user_for_pass=user_for_pass)
        
    selldate=new_selldate
    buydate =new_buydate
    print("SELL DATE == ", selldate)
    print("Buy DATE == ", buydate)
    Task = DataTableCr.query.filter_by(sno=sno).first()
    return render_template('update.html', Task=Task, buydate=buydate, selldate=selldate, checkbox_stats_OPENBUY=checkbox_stats_OPENBUY, checkbox_stats_OPENSELL=checkbox_stats_OPENSELL)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        trade_type_backend = request.form['trade_type']

        # buy ya phir sell

        trade_instrument = request.form['trade_instrument']
        
        # equity, futures, call ya put

        security_name = request.form['stockname']
        lotsize = request.form['lotsize']
        nolot = request.form['nolot']
        quantity= request.form['quantity']

        # buy_date = datetime.strptime(request.form['buydate'], '%Y-%m-%d')
        buy_date_initial = request.form['buydate']
        print(buy_date_initial)
        # buy_date = datetime.strptime(buy_date_initial, '%Y-%m-%d')
        # buy_date = parser.parse(buy_date_initial)
        # print(buy_date)
        buy_price = request.form['buyprice']
        
        # agar open hai buy type trade then open_buy="OPENBUY"
        # sell_date = datetime.strptime(request.form['selldate'], '%Y-%m-%d')
        sell_date_initial = request.form['selldate']
        print(sell_date_initial)
        # sell_date = datetime.strptime(sell_date_initial, '%Y-%m-%d')
        # sell_date = parser.parse(sell_date_initial)
        # print(sell_date)
        sell_price = request.form['sellprice']
        sell_date2_initial = request.form['selldate2']
        print(sell_date2_initial)
        # sell_date2 = datetime.strptime(sell_date2_initial, '%Y-%m-%d')
        # sell_date2 = parser.parse(sell_date2_initial)
        # print(sell_date2)

        # sell_year2 = sell_date2[0:4]
        # sell_month2= sell_date2[5:7]
        # sell_day2=sell_date2[8:10]

        sell_price2=request.form['sellprice2']

        open_buy_default= request.form['openBuyfirst_defaultcheck']
        open_sell_default=request.form['openSELLfirst_defaultcheck']
        
        buy_date2_initial = request.form['buydate2']
        print(buy_date2_initial)
        # buy_date2 = datetime.strptime(buy_date2_initial, '%Y-%m-%d')
        # buy_date2 = parser.parse(buy_date2_initial)
        # print(buy_date2)

        # buy_year2 = buy_date2[0:4]
        # buy_month2 = buy_date2[5:7]
        # buy_day2= buy_date2[8:10]

        buy_price2=request.form['buyprice2']
        net_profit_num= request.form['profit']
        profit_percent=request.form['profitpercent']

        # buy_year = buy_date[0:4]
        # buy_month = buy_date[5:7]
        # buy_day= buy_date[8:10]

        # sell_year = sell_date[0:4]
        # sell_month= sell_date[5:7]
        # sell_day=sell_date[8:10]


        if open_buy_default == "OPENBUY_ye" and open_sell_default == "OPENSELL_no":
            open_buy= request.form['openBuy']
            print("OPEN TRADE BUY")
            # buy_DATE_format = buy_date
            buy_date = parser.parse(buy_date_initial)
            isOpen=True
            tradeState="OPEN"
            new_trade = DataTableCr(userid=current_user.userid, trade_type=trade_type_backend, instrument=trade_instrument,  securityname=security_name,
                               lot_size=lotsize, no_of_lot=nolot, quantity=quantity, buy_date=buy_date, buyprice=buy_price, trade_state=tradeState, isOpen=isOpen)
            print("security_name", security_name)
            print("New Trade", new_trade)

            print("zero")
            db.session.add(new_trade)
            print("hello ", new_trade)
            print("ONE")
            db.session.commit()
            print("two")
            name = current_user.firstname
            user_for_pass = current_user.userid
            tasks = DataTableCr.query.order_by(DataTableCr.buy_date).all()
            return render_template('dashboard.html',  tasks=tasks, name=name, user_for_pass=user_for_pass)


        if open_sell_default == "OPENSELL_ye" and open_buy_default == "OPENBUY_no":
            # open_sell=request.form['openSell'].value
            print("OPEN TRADE SELL")
            # sell_DATE_format = sell_date2
            sell_date2 = parser.parse(sell_date2_initial)
            isOpen=True
            tradeState="OPEN"
            new_trade = DataTableCr(userid=current_user.userid, trade_type=trade_type_backend, instrument=trade_instrument,  securityname=security_name,
                               lot_size=lotsize, no_of_lot=nolot, quantity=quantity, sell_date=sell_date2, sellprice=sell_price2, trade_state=tradeState, isOpen=isOpen)
            print("security_name", security_name)
            print("New Trade", new_trade)

            print("zero")
            db.session.add(new_trade)
            print("hello ", new_trade)
            print("ONE")
            db.session.commit()
            print("two")
            name = current_user.firstname
            user_for_pass = current_user.userid
            tasks = DataTableCr.query.order_by(DataTableCr.sell_date).all()
            return render_template('dashboard.html',  tasks=tasks, name=name, user_for_pass=user_for_pass)


        if open_buy_default == "OPENBUY_no" and open_sell_default == "OPENSELL_no":
            tradestate2="CLOSED"
            isOPEN=False
            if trade_type_backend == "Buy":
                # buy_DATE_format = buy_date
                # sell_DATE_format = sell_date
                buy_date = parser.parse(buy_date_initial)
                sell_date = parser.parse(sell_date_initial)
                new_trade = DataTableCr(userid=current_user.userid, trade_type=trade_type_backend, instrument=trade_instrument,  securityname=security_name,
                               lot_size=lotsize, no_of_lot=nolot, quantity=quantity, buy_date=buy_date, buyprice=buy_price, sell_date=sell_date, sellprice=sell_price, profit=net_profit_num, profit_percent=profit_percent, trade_state=tradestate2, isOpen=isOPEN)
                print("security_name", security_name)
                print("New Trade", new_trade)

                print("zero")
                db.session.add(new_trade)
                print("hello ", new_trade)
                print("ONE")
                db.session.commit()
                print("two")
                name = current_user.firstname
                user_for_pass = current_user.userid
                tasks = DataTableCr.query.order_by(DataTableCr.buy_date).all()
                return render_template('dashboard.html',  tasks=tasks, name=name, user_for_pass=user_for_pass)
                
            else:
                # buy_DATE_format = buy_date2
                # sell_DATE_format = sell_date2
                sell_date2 = parser.parse(sell_date2_initial)
                buy_date2 = parser.parse(buy_date2_initial)
                new_trade = DataTableCr(userid=current_user.userid, trade_type=trade_type_backend, instrument=trade_instrument,  securityname=security_name,
                               lot_size=lotsize, no_of_lot=nolot, quantity=quantity, buy_date=buy_date2, buyprice=buy_price2, sell_date=sell_date2, sellprice=sell_price2, profit=net_profit_num, profit_percent=profit_percent, trade_state=tradestate2, isOpen=isOPEN)
                print("security_name", security_name)
                print("New Trade", new_trade)

                print("zero")
                db.session.add(new_trade)
                print("hello ", new_trade)
                print("ONE")
                db.session.commit()
                print("two")
                name = current_user.firstname
                user_for_pass = current_user.userid
                tasks = DataTableCr.query.order_by(DataTableCr.sell_date).all()
                return render_template('dashboard.html',  tasks=tasks, name=name, user_for_pass=user_for_pass)

        # try:
        #     print("zero")
        #     db.session.add(new_task)
        #     print( "hello ",new_task)
        #     print("ONE")
        #     db.session.commit()
        #     print("two")
        #     return redirect('/dashboard', current_user.username)
        # except:
        #     return 'There was an issue adding your task'
    else:
        name = current_user.firstname
        user_for_pass = current_user.userid
        tasks = DataTableCr.query.order_by(DataTableCr.date_created).all()
        return render_template('dashboard.html',  tasks=tasks, name=name, user_for_pass=user_for_pass)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
