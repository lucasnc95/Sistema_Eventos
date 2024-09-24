# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    __tablename__ = 'Usuario'
    IDUser = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(255), nullable=False)
    Senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.Senha, password)

    def get_id(self):
        return str(self.IDUser)


class Docente(db.Model):
    __tablename__ = 'Docente'
    IDUser = db.Column(db.Integer, db.ForeignKey('Usuario.IDUser'), primary_key=True)
    SIAPE = db.Column(db.String(20), nullable=False)


class Discente(db.Model):
    __tablename__ = 'Discente'
    IDUser = db.Column(db.Integer, db.ForeignKey('Usuario.IDUser'), primary_key=True)
    Matricula = db.Column(db.String(20), nullable=False)


class Externo(db.Model):
    __tablename__ = 'Externo'
    IDUser = db.Column(db.Integer, db.ForeignKey('Usuario.IDUser'), primary_key=True)
    CPF = db.Column(db.String(20), nullable=False)


class Evento(db.Model):
    __tablename__ = 'Evento'
    IDEvento = db.Column(db.Integer, primary_key=True)
    IDUserDocente = db.Column(db.Integer, db.ForeignKey('Usuario.IDUser'))
    Titulo = db.Column(db.String(255), nullable=False)
    Descricao = db.Column(db.String(255), nullable=False)
    Data = db.Column(db.Date, nullable=False)
    Horario = db.Column(db.Time, nullable=False)
    Vagas = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.String(20), nullable=False)


class Inscricao(db.Model):
    __tablename__ = 'Inscritos'
    IDUser = db.Column(db.Integer, db.ForeignKey('Usuario.IDUser'), primary_key=True)
    IDEvento = db.Column(db.Integer, db.ForeignKey('Evento.IDEvento'), primary_key=True)
    Presente = db.Column(db.Boolean, default=False)
    evento = db.relationship('Evento', backref='inscricoes')
    usuario = db.relationship('User', backref='inscricoes')
