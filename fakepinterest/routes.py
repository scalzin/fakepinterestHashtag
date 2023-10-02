# criar as rotas do site
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.forms import FormCriarConta, FormLogin, FormFoto
from fakepinterest.models import User, Post
from flask_login import login_required, login_user, logout_user, current_user
import os
from werkzeug.utils import secure_filename



@app.route('/', methods=['get', 'post'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        user = User.query.filter_by(email = formlogin.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, formlogin.senha.data):
            login_user(user)
            return redirect(url_for('perfil', id_user = user.id))
    return render_template('homepage.html', form=formlogin)

@app.route('/criarconta', methods=['get', 'post'])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        user = User(username= formcriarconta.username.data, 
                    email= formcriarconta.email.data, 
                    senha= senha)
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('perfil', id_user = user.id))
    return render_template('criarconta.html', form=formcriarconta)


@app.route('/perfil/<id_user>', methods=['get', 'post'])
@login_required 
def perfil(id_user):
    if int(id_user) == int(current_user.id):
        # vendo o próprio perfil
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # salvar o arquivo na pasta fotos_post
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo.save(caminho)
            # registrar o arquivo no bd
            foto = Post(imagem= nome_seguro, id_user= current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template('perfil.html', user= current_user, form= formfoto)
    else:
        user = User.query.get(int(id_user))
        return render_template('perfil.html', user=user, form = None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/feed')
@login_required
def feed():
    fotos= Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template('feed.html', fotos=fotos)