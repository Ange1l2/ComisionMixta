from datetime import datetime
from src import bcrypt, db, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

# AQUI FALTA LA LIBRERÍA: ITSDANGEROUS: es una biblioteca que permite pasar datos por entornos no confiables, como cookies HTTP, de forma segura. Para ello, firma los datos de forma criptográfica para garantizar que no se hayan alterado.

from time import time
import jwt


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    nombre =  db.Column(db.String, nullable=False)
    apellidos =  db.Column(db.String, nullable=False)
    genero =  db.Column(db.String, nullable=False)
    fechaNacimiento =  db.Column(db.Date, nullable=False)
    telefono = db.Column(db.Numeric, nullable=False)
    tipoUsuario =  db.Column(db.String, nullable=False)
    
        
    def __init__(self, email, password, nombre, apellidos, genero, fechaNacimiento, telefono, tipoUsuario):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        #self.is_admin = is_admin
        self.nombre = nombre
        self.apellidos = apellidos
        self.genero = genero
        self.fechaNacimiento = fechaNacimiento
        self.telefono = telefono
        self.tipoUsuario = tipoUsuario


    def __repr__(self):
        return f"<email {self.email}>"


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256'
        )


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return db.session.get(User, id)
