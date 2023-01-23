""" database dependencies to support sqliteDB examples """
from random import randrange
import os, base64
import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Post(db.Model):
    __tablename__ = 'posts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, image):
        self.userID = id
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": str(file_encode)
        }


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _firstName = db.Column(db.String(255), unique=False, nullable=False)
    _lastName = db.Column(db.String(255), unique=False, nullable=False)
    _extracurricular = db.Column(db.String(255), unique=False, nullable=False)
    _hoursPerWeek = db.Column(db.String(255), unique=False, nullable=False)
    _coachName = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, firstName, lastName, extracurricular, hoursPerWeek, coachName):
        self._firstName = firstName    # variables with self prefix become part of the object, 
        self._lastName= lastName
        self._extracurricular= extracurricular 
        self._hoursPerWeek = hoursPerWeek
        self._coachName = coachName

    # a name getter method, extracts name from object
    @property
    def firstName(self):
        return self._firstName
    
    # first name setter 
    @firstName.setter
    def firstName(self, firstName):
        self._firstName = firstName
    
    # last name getter 
    @property
    def lastName(self):
        return self._lastName
    
    # last name setter 
    @lastName.setter
    def lastName(self, lastName):
        self._lastName = lastName
    
    #extracurricular getter 
    @property
    def extracurricular(self):
        return self._extracurricular
    
    #extracurricular setter
    @extracurricular.setter
    def extracurricular(self, extracurricular):
        self._extracurricular = extracurricular
    
    #hours per week getter    
    @property
    def hoursPerWeek(self):
        return self._hoursPerWeek
    
    # hoursPerWeek setter
    @hoursPerWeek.setter
    def hoursPerWeek(self, hoursPerWeek):
        self._hoursPerWeek = hoursPerWeek
        
    #coach name getter    
    @property
    def coachName(self):
        return self._coachName
    
    # coach name setter
    @coachName.setter
    def coachName(self,coachName):
        self._coachName = coachName

    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts user to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "extracurricular": self.extracurricular,
            "hoursPerWeek": self.hoursPerWeek,
            "coachName": self.coachName,
            "posts": [post.read() for post in self.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, firstName="", lastName="", extracurricular="", hoursPerWeek="", coachName=""):
        """only updates values with length"""
        if len(firstName) > 0:
            self.firstName = firstName
        if len(lastName) > 0:
            self.lastName = lastName
        if len(extracurricular) > 0:
            self.extracurricular = extracurricular
        if len(hoursPerWeek) > 0:
            self.hoursPerWeek = hoursPerWeek
        if len(coachName) > 0:
            self.coachName = coachName
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = User(firstName='Kaylee', lastName='Hou', extracurricular='Guitar', hoursPerWeek='5', coachName='N/A')
    u2 = User(firstName='Theo', lastName='Huntalas', extracurricular='Skateboarding', hoursPerWeek='3', coachName='N/A')
    u3 = User(firstName='Ellie', lastName='Pang', extracurricular='Soccer', hoursPerWeek='8', coachName='Coach Robby')
    u4 = User(firstName='Haeryn', lastName='Yu', extracurricular='Kickboxing', hoursPerWeek='2', coachName='Coach Burr')

    users = [u1, u2, u3, u4]

    """Builds sample user/note(s) data"""
    for user in users:
        try:
            '''add a few 1 to 4 notes per user'''
            for num in range(randrange(1, 4)):
                note = "#### " + user.firstName + " note " + str(num) + ". \n Generated by test data."
                user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
            '''add user/post data to table'''
            user.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {user.firstName}")
            