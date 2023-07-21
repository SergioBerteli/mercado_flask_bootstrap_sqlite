from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField, FloatField
from wtforms.validators import Length, DataRequired, EqualTo, Email
from mercado.models import Usuario, Produto

class FormularioDeRegistro(FlaskForm):
    
    def validate_username(self, username_to_check):
        usuario = Usuario.query.filter_by(username=username_to_check.data).first()
        if usuario:
            raise ValidationError("Esse nome de usuario já existe")
    
    def validate_email(self, email_to_check):
        email = Usuario.query.filter_by(endereco_email=email_to_check.data).first()
        if email:
            raise ValidationError("Esse email já está sendo usado")
    
    username = StringField(label="Insira o seu nome de usuário", validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField(label="Insira o seu e-mail", validators=[DataRequired(), Email(message="Endereço de e-mail invalido")])
    senha1 = PasswordField(label="Insira a sua senha", validators=[DataRequired(), Length(min=6)])
    senha2 = PasswordField(label="Confirme a sua senha", validators=[DataRequired(), EqualTo("senha1", message="As senhas não correspondem.")])
    submit = SubmitField(label="Criar a conta")
    
class FormularioLogin(FlaskForm):
    username = StringField(label="Nome de usuário", validators=[DataRequired()])
    senha = PasswordField(label="Senha", validators=[DataRequired()])
    submit = SubmitField(label="Entrar")
    
class ComprarProduto(FlaskForm):
    submit = SubmitField(label="Sim, eu quero")

class VenderProduto(FlaskForm):
    submit = SubmitField(label="Sim, eu quero vender.")
    
class CriaProduto(FlaskForm):
    nome = StringField(label="Insira o nome do produto", validators=[DataRequired()])
    preco = FloatField(label="O preço do produto", validators=[DataRequired()])
    descricao = StringField(label="Descreva o seu produto", validators=[DataRequired(), Length(max=1024, message="Não são aceitas descrições com mais de 1024 caracteres")])
    submit = SubmitField(label="Botar à venda")
    
    def validate_nome(self, nome_para_checar):
        p_existente = Produto.query.filter_by(nome=nome_para_checar.data).first()
        if p_existente:
            raise ValidationError("Um produto com esse nome já existe")
        
    def validate_preco(self, preco_para_checar):
        if preco_para_checar.data < 0:
            raise ValidationError("Por favor insira um valor positivo.")