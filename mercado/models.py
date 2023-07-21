from mercado import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    senha_hash = db.Column(db.String(length=60), nullable=False)
    endereco_email = db.Column(db.String(length=50), nullable=False, unique=True)
    saldo = db.Column(db.Integer(), nullable=False, default=2000)
    produtos_adquiridos = db.relationship('Produto', backref='dono_do_produto', lazy=True)
    
    @property
    def senha(self):
        return self.senha
    
    @senha.setter
    def senha(self, senha_em_texto):
        self.senha_hash = bcrypt.generate_password_hash(senha_em_texto).decode('utf-8')
        
    def checar_senha(self, senha_inserida):
        return bcrypt.check_password_hash(pw_hash=self.senha_hash, password=senha_inserida)
    
    @property
    def saldo_mais_bonito(self):
        novo_saldo = [(','+digito) if index%3 == 0 and index != 0 else digito for index, digito in enumerate(str(self.saldo)[::-1])]
        return ''.join(novo_saldo)[::-1]
    
    def pode_comprar(self, prod):
        return self.saldo>=prod.preco
    
    def esta_disponivel(self, prod):
        return not prod.dono
    
    def pode_vender(self, prod):
        return prod in self.produtos_adquiridos

class Produto(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(length=20), nullable=False)
    preco = db.Column(db.Float(), nullable=False)
    descricao = db.Column(db.String(length=1024), nullable=False)
    dono = db.Column(db.Integer(), db.ForeignKey('usuario.id'))
    
    def __repr__(self):
        return self.nome
    
    def atribui_dono(self, user):
        self.dono = user.id
        user.saldo -= self.preco
        db.session.commit()
    
    def volta_ao_mercado(self, user):
        self.dono = None
        user.saldo += self.preco
        db.session.commit()
        
    
