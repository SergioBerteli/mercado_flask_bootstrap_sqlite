from mercado import app, db
from mercado.models import Produto, Usuario
from mercado.forms import FormularioDeRegistro, FormularioLogin, ComprarProduto, VenderProduto, CriaProduto
from flask_login import login_user, login_required, logout_user, current_user
from flask import request

from flask import render_template, redirect, url_for, flash, get_flashed_messages
@app.route("/")
@app.route("/home")
def pagina_inicial():
    return render_template("index.html")            

@app.route("/produtos", methods=['GET', 'POST'])
@login_required
def lista_produtos():
    compra_produto = ComprarProduto()
    vende_produto = VenderProduto()
    if request.method == "POST":
        produto_comprado = request.form.get("produto_comprado")
        p_comprado_obj = Produto.query.filter_by(nome=produto_comprado).first()
        
        produto_vendido = request.form.get("produto_vendido")
        p_vendido_obj = Produto.query.filter_by(id=produto_vendido).first()
        
        if p_vendido_obj:
            if current_user.pode_vender(p_vendido_obj):
                p_vendido_obj.volta_ao_mercado(current_user)
                flash(f"Você acabou de vender o {p_vendido_obj.nome} por ${p_vendido_obj.preco}", category="success")
            else:
                flash(f"Atualmente você não adquiriu o {p_vendido_obj.nome}.", category="danger")
        
        if p_comprado_obj:
            if current_user.pode_comprar(p_comprado_obj):
                if current_user.esta_disponivel(p_comprado_obj):
                    p_comprado_obj.atribui_dono(current_user)                
                    flash(f"Você acabou de adquirir um {p_comprado_obj.nome}!", category="success")
                else:
                    flash(f"O {p_comprado_obj.nome} não está disponivel atualmente", category="danger")
            else:
                flash(f"Você não possui dinheiro o suficiente", category="danger")
        return redirect(url_for('lista_produtos'))
    if request.method == "GET":
        produtos = Produto.query.filter_by(dono=None)    
        produtos_adquiridos = Produto.query.filter_by(dono=current_user.id)
        return render_template("produtos.html", produtos=produtos, compra_produto=compra_produto, produtos_adquiridos=produtos_adquiridos, vende_produto=vende_produto)

@app.route("/registar", methods=['GET', 'POST'])
def cria_conta():
    form = FormularioDeRegistro()
    if form.validate_on_submit():
        usuario_criado = Usuario(username=form.username.data, senha=form.senha1.data, endereco_email=form.email.data)
        db.session.add(usuario_criado)
        db.session.commit()
        login_user(usuario_criado)
        flash(f"Conta criada com sucesso!, você agora está logado como {usuario_criado.username}", category="success")
        return redirect(url_for('lista_produtos'))
    
    if form.errors != {}:
        for erro in form.errors.values():
            flash(f"Ocorreu um erro: {erro.pop()}", category="danger")
    return render_template('nova_conta.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def entrar_conta():
    form = FormularioLogin()
    if form.validate_on_submit():
        usuario_inserido = Usuario.query.filter_by(username=form.username.data).first()
        if usuario_inserido and usuario_inserido.checar_senha(form.senha.data):
            login_user(usuario_inserido)
            flash(f"Sucesso! Você entrou como {usuario_inserido.username}", category="success")
            return redirect(url_for("lista_produtos"))
        else:
            flash("Usuário e/ou senha incorretos!", category="danger")
            
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta", category="info")
    return redirect(url_for('pagina_inicial'))

@app.route('/registra_produto', methods=['GET', 'POST'])
@login_required
def registra_produto():
    form = CriaProduto()
    if form.validate_on_submit():
        produto_criado = Produto(nome=form.nome.data, descricao=form.descricao.data, preco=form.preco.data)
        db.session.add(produto_criado)
        db.session.commit()
        flash(f"Produto criado com sucesso!", category="success")
        return redirect(url_for("registra_produto"))
    
    if form.errors != {}:
        for erro in form.errors.values():
            flash(f"Ocorreu um erro: {erro.pop()}", category="danger")
        
    return render_template("registros.html", form=form)