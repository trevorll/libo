import os
from passlib.hash import sha256_crypt
import os
from flask_mail import Message,Mail
import re
from flask_migrate import Migrate
from flask import Flask,render_template,redirect,request,flash,session,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from models import *




app = Flask(__name__,template_folder='templates')
app.secret_key = 'godwill65'
POSTGRES = {
    'user': 'godwill',
    'pw': 'godwill63',
    'db': 'godwill',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)
app.config.update(
        DEBUG=True,
        MAIL_SERVER= 'smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='gtreksolution@gmail.com',
        MAIL_PASSWORD='godwill8764'

        )

mail=Mail(app)

@app.route('/', methods=['POST','GET'])
def login():
    if request.method=='POST':
        if not request.form["name"] or not request.form["password"]:
            flash('please fill all fields')
            return render_template('login.html')
        user=genius.query.filter(genius.name==request.form['name']).first()
        pas = request.form['password']
        if not user:
            flash('sign up first')
        elif not sha256_crypt.verify(pas, user.password):
                flash('please enter the correct credetials')
        else:
            session['user']=user.name
            return render_template('success.html', user=session['user'], image=user.image)
    return render_template('login.html')

@app.route('/success', methods=['POST','GET'])
def success():
    if 'user' in session:
        return render_template('success.html',user=session['user'])

    return render_template('test.html')
@app.route('/signup',methods=['POST','GET'])
def test():
    if request.method == 'POST':

        newuser=genius(fname=request.form['fname'],lname=request.form['lname'],oname=request.form['oname'], name=request.form["name"],password=request.form["password"],image=request.form["image"],reg_date=dt.now(), email=request.form['email'])
        if not request.form['fname'] or not request.form['lname'] or not request.form['oname'] or not request.form['name'] or not request.form["password"] or not request.form['rep_pass']or not request.form['email']:
            flash("please fill all fiels")
        elif request.form['password'] != request.form['rep_pass']:
            flash('passwords don\'t match')
        elif genius.query.filter(genius.name==request.form['name']).first():
            flash("user already exists")
        else:
            msg = Message('trial mail',
            sender = 'godwillsolutions@noreply.com',
            recipients=[request.form['email']])
            msg.body='Hello '+request.form['name'] +' you have successfully signed in to GTREK solutions there are so many things you can do welcome'
            mail.send(msg)
            newuser.save()
            session['user']=newuser.name
            user =genius.query.filter(genius.name==request.form['name']).first()
            flash('thank you very much, '+ request.form['name'] +' we have sent you an email')
            return render_template('success.html',user=session['user'],image=user.image)
    return render_template('test.html')
@app.route('/users', methods=['GET','POST'])
def users():
    return render_template('all.html',users=genius.query.all())



@app.route('/search_user', methods=['GET','POST'])
def search_user():
    if request.method== 'POST':
        #name=booked_hostel.query.filter(booked_hostel.name==request.form['search']).first()
        user = genius.query.filter_by(name=request.form['search']).first()
        if not user:
            flash('user does not exist')
            return redirect(url_for('users'))
        else:
            books=borrowed_books.query.filter_by(name=request.form['search']).first()
            return render_template('user.html',user=user.name,password=user.password,image=user.image,name=booked_hostel.query.filter(booked_hostel.name==request.form['search']).first(),books=books)
    return render_template('all.html')

@app.route('/superadmin',methods=['POST','GET'] )
def superadmin():
    if request.method=='POST':
        user = request.form['username']
        if not request.form['username'] or not request.form['password']:
            flash("please fill all fields")
        elif request.form['username'] != "Godwill" or request.form['password']!= "trevor":
            flash("wrong details")
        else:
            return render_template("superadmin.html", user=user)
    return render_template('superadminlogin.html')


@app.route('/add_admin', methods =[ 'POST','GET'])
def add_admin():
    if request.method == 'POST':
        newadmin=Admin(username=request.form['username'],password=request.form['password'])
        if not request.form['username'] or not request.form['password']:
            flash("please fill all the fields")
        elif Admin.query.filter(Admin.username==request.form['username']).first():
            flash('admin already exists')
        else:
            newadmin.save()
            flash('admin successfully added')
            return render_template('superadmin.html')
    return render_template('add_admin.html')
@app.route('/admin', methods = ['POST','GET'])
def admin():
    if request.method=='POST':
        if not request.form['username'] or not request.form['password']:
            flash('please fill all fields')
        admin=Admin.query.filter(Admin.username==request.form['username']).first()
        if not admin:
            flash('Sorry you are not an admin please contact the super admin')
        elif not sha256_crypt.verify(request.form['password'], admin.password):
            flash('Wrong password please check the password')
        else:
            session['admin']=admin.username
            return render_template('admin_loggedin.html',user=session['admin'])
    return render_template('admin.html')
@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method=='POST':
        user=genius.query.filter(genius.name==request.form['name']).first()
        if not user:
            flash('the user does not exist')
        else:
            db.session.delete(user)
            db.session.commit()
            flash('user successfully deleted')
            return redirect(url_for('users'))
    return redirect(url_for('users'))
@app.route('/user_logout')
def user_logout():
    session.pop('user')
    return redirect(url_for('login'))

@app.route('/change_password',methods=['GET','POST'])
def changepass():
    if 'user' in session:
        user=genius.query.filter(genius.name==session['user']).first()
        if request.method=='POST':
            if not request.form['name'] or not request.form['prev_pass']:
                flash('please fill all fields')
            # elif not user.name== request.form['name']:
            #     flash('please provide the name you registered with')
            elif not sha256_crypt.verify(request.form['prev_pass'], user.password):
                flash('The user password you have entered is wrong')
            else:
                msg = Message('Changed password',
                sender = 'godwillsolutions@noreply.com',
                recipients=[user.email])
                msg.body='Hello '+request.form['name'] +' you have successfully changed your password'
                mail.send(msg)
                user.password=sha256_crypt.encrypt(request.form['new_pass'])
                user.save()
                flash('password successfully changed')
                session['user']=user.name
                return redirect(url_for('success'))
        return render_template('changepass.html')
    return redirect(url_for('success'))

@app.route('/admin_loggedin', methods=['POST','GET'])
def admin_loggedin():
    return render_template('admin_loggedin.html',user=session['admin'])

@app.route('/add_hostel', methods=['POST','GET'])
def add_hostel():
     if 'admin' in session:
        if request.method == 'POST':
            hoste=hostel(name=request.form['name'])
            if not request.form['name']:
                flash('input a valid hostel name')
            elif hostel.query.filter(hostel.name==request.form['name']).first():
                flash('hostel already added')
            else:
                hoste.save()
                flash('hostel successfully added')
                return redirect(url_for('admin_loggedin'))
     return render_template('add_hostel.html')



@app.route('/book_hostel', methods=['GET','POST'])
def book_hostel():
    if 'user' in session:
        user=genius.query.filter(genius.name==session['user']).first()
        if request.method == 'POST':
            booked=booked_hostel(bookeddate=dt.now(),username=request.form['username'],name=session['user'],hostel=request.form['hostel'])
            if not request.form['hostel']:
                flash('please enter the name of the hostel you want to book')

            elif not  hostel.query.filter(hostel.name==request.form['hostel']):
                flash('enter a name that is in hostels')
            elif booked_hostel.query.filter(booked_hostel.name==session['user']).first():
                flash('sorry you have already booked your hostel')
            else:
                msg = Message('Changed password',
                sender = 'godwillsolutions@noreply.com',
                recipients=[user.email])
                msg.body='Hello '+ user.name +' you have successfully booked '+request.form['hostel'] +' hostel'
                mail.send(msg)
                booked.hostel=request.form['hostel']
                booked.save()
                session['user']=user.name
                flash('congradulation! you have successfully booked the hostel')
                return redirect(url_for('success',image=user.image))
    return render_template('hostels.html',hostels=hostel.query.all())

@app.route('/add_book', methods=['GET','POST'])
def add_book():
    if 'admin' in session:
        if request.method=='POST':
            book=books(datein=dt.now(),serialno=request.form['serialno'],name=request.form['name'],author=request.form['author'],quantity=request.form['quantity'], section=request.form['section'],addedby=session['admin'])
            if not request.form['serialno'] or not request.form['name'] or not request.form['author'] or not request.form['quantity'] or not request.form['section']:
                flash('please fill all fields')
            elif books.query.filter(books.serialno==request.form['serialno']).first() or books.query.filter(books.name==request.form['name']).first():
                flash('That book already exists')
            else:
                book.save()
                flash('The book has been successfully saved')
                return redirect(url_for('admin_loggedin'))
    return render_template('addbook.html')
@app.route('/borrowbook',methods=['GET','POST'])
def borrowbook():
    if 'user' in session:

        if request.method=='POST':

            book=borrowed_books(serialno=request.form['serialno'],name=session['user'],borrowed_date=dt.now())
            if not request.form['serialno']:
                flash('fill all fields')
            elif not books.query.filter(books.serialno==request.form['serialno']):
                flash('the book is not in stock')
            elif books.query.filter(books.serialno==request.form['serialno']).first().quantity==0:
                flash('all of these books have already been borrowed')
            elif borrowed_books.query.filter(borrowed_books.serialno==request.form['serialno']).first() and borrowed_books.query.filter(borrowed_books.name==session['user']).first():
                flash('oops! you cannot borrow the same book twice')
            else:
                user= genius.query.filter(genius.name==session['user']).first()
                msg = Message('borrowed books',
                sender = 'godwillsolutions@noreply.com',
                recipients=[user.email])
                msg.body='Hello '+ session['user'] +' you have successfully borrowed a book by the name '+ books.query.filter(books.serialno==request.form['serialno']).first().name
                mail.send(msg)
                book.save()
                flash('successfully borrowed the book')
                book=books.query.filter(books.serialno==request.form['serialno']).first()
                book.quantity=book.quantity-1
                book.save()
                return redirect(url_for('success'))

    return render_template('borrowbook.html')


@app.route('/returnbook',methods=['GET','POST'])
def returnbook():
    if 'user' in session:
        if request.method=='POST':
            book=borrowed_books.query.filter(borrowed_books.serialno==request.form['serialno']).first()
            if not request.form['serialno']:
                flash('fill all fields')
            if not book:
                flash('you never borrowed this book')
            else:
                user= genius.query.filter(genius.name==session['user']).first()
                msg = Message('Acceptance of returned book',
                sender = 'godwillsolutions@noreply.com',
                recipients=[user.email])
                msg.body='Hello '+ session['user'] +' you have successfully returned a book by the name '+ books.query.filter(books.serialno==request.form['serialno']).first().name
                mail.send(msg)
                db.session.delete(book)
                db.session.commit()
                flash('successfully returned the book')
                book=books.query.filter(books.serialno==request.form['serialno']).first()
                book.quantity=book.quantity+1
                book.save()
                return redirect(url_for('success'))

    return render_template('returnbook.html')

@app.route('/availablebooks', methods=['GET','POST'])
def availablebooks():
    return render_template('availablebooks.html',books=books.query.all())

@app.route('/borrowedbooks', methods=['GET','POST'])
def borrowedbooks():
    return render_template('borrowedbooks.html',books=borrowed_books.query.all())

if __name__== "__main__":
    app.config['DEBUG']=True
    app.run(port=5432)
