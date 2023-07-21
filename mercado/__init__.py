from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mercado.db'
app.config['SECRET_KEY'] = '489814ef972b7399d5de9af9'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "entrar_conta"
login_manager.login_message_category= "info"
login_manager.login_message = "Por favor, entre na sua conta antes de acessar esse recurso"
from mercado import routes