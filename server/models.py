from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash


from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(200))
    bio = db.Column(db.String(255))
    recipes = db.relationship('Recipe', backref='author', lazy=True)

    @property
    def password_hash(self):
        raise AttributeError('password_hash is not readable')

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

    

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.String(255), nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('recipes', lazy=True))

    def __init__(self, title, instructions, minutes_to_complete, user_id):
        self.title = title
        self.instructions = instructions
        self.minutes_to_complete = minutes_to_complete
        self.user_id = user_id
    