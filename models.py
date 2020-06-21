from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from passlib.hash import sha256_crypt

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class genius(db.Model):
    __tablename__= "fixed"
    fname=db.Column(db.String)
    lname=db.Column(db.String)
    oname=db.Column(db.String)
    name = db.Column((db.String), primary_key = True)
    password = db.Column((db.String))
    image = db.Column(db.String)
    reg_date = db.Column(db.DateTime)
    email = db.Column(db.String)

    def __init__(self,fname,lname,oname,name,password,image,reg_date,email):
        self.fname=fname
        self.lname=lname
        self.oname=oname
        self.name=name
        self.password= sha256_crypt.encrypt(password)
        self.image= image
        self.reg_date=reg_date
        self.email=email

    def save(self):
        db.session.add(self)
        db.session.commit()


class Admin(db.Model):
    __tablename__="admins"
    username= db.Column((db.String), primary_key=True)
    password= db.Column(db.String)

    def __init__(self, username,password):
        # super(Admin, self).__init__()
        self.username = username
        self.password= sha256_crypt.encrypt(password)


    def save(self):
        db.session.add(self)
        db.session.commit()

class hostel(db.Model):
    __tablename__="hostel"
    name = db.Column((db.String), primary_key = True)

    def __init__(self, name):
        self.name= name


    def save(self):
        db.session.add(self)
        db.session.commit()


class booked_hostel(db.Model):
    __tablename__="booked_hostel"
    bookeddate=db.Column(db.DateTime)
    username=db.Column((db.String), primary_key=True)
    name= db.Column(db.String, db.ForeignKey('fixed.name'),nullable=False)
    fixed=db.relationship('genius',backref=db.backref('booked_hostel',cascade='all,delete'))
    hostel = db.Column(db.String)

    def __init__(self,bookeddate,username,name,hostel):
        self.bookeddate=bookeddate
        self.username=username
        self.name=name
        self.hostel=hostel

    def save(self):
        db.session.add(self)
        db.session.commit()

class books(db.Model):
    __tablename__='books'
    serialno=db.Column((db.Integer),primary_key=True)
    name= db.Column((db.String),unique=True,nullable=False )
    author = db.Column(db.String)
    quantity= db.Column(db.Integer)
    section = db.Column(db.String)
    datein=db.Column(db.DateTime)
    addedby=db.Column(db.String)

    def __init__(self,datein,serialno,name,author,quantity,section,addedby):
        self.datein=datein
        self.serialno=serialno
        self.name=name
        self.author=author
        self.quantity=quantity
        self.section=section
        self.addedby=addedby

    def save(self):
        db.session.add(self)
        db.session.commit()

class number(db.Model):
    __tablename__="number"
    name = db.Column(db.String, db.ForeignKey('fixed.name'),primary_key=True,nullable=False)
    number = db.Column(db.Integer)
    fixed=db.relationship('genius',backref=db.backref('number',cascade='all,delete'))

    def __init__(self, name,number):
        self.name = name
        self.number = number


    def save(self):
        db.session.add(self)
        db.session.commit()



class borrowed_books(db.Model):
    __tablename__= 'borrowed_books'
    serialno=db.Column((db.Integer),db.ForeignKey('books.serialno'),primary_key=True,nullable=False)
    books=db.relationship('books',backref=db.backref('books',cascade = 'all,delete'))
    name=db.Column((db.String),db.ForeignKey('fixed.name'),nullable=False)
    fixed=db.relationship('genius',backref=db.backref('fixed',cascade='all,delete'))
    borrowed_date=db.Column(db.DateTime)

    def __init__(self, serialno,name,borrowed_date):
        self.serialno=serialno
        self.name=name
        self.borrowed_date=borrowed_date

    def save(self):
        db.session.add(self)
        db.session.commit()



class search_object():
    Users=list()

    def __init__(self, Users,query):
        self.Users=users
        self.query=None
