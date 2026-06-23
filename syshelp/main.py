from flask import Flask, render_template,request,session
from db import Session as db_session
from datetime import timedelta
from flask_login import LoginManager,login_user,login_required
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

@lm.user_loader
def carregar_usuario(user_id):
    db = db_session()
    usuario = db.query(Usuario).get(int(user_id))
    db.close()
    return usuario

#login "auth"
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        db = db_session()
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = db.query(Usuario).filter_by(email=email).first()

        if user is None or user.senha != senha:
            msg = 'Email ou senha incorretos'
            return render_template('/login.html',msg=msg)
        
        if user.email == email and user.senha == senha:
            login_user(user,remember=True)
            session.permanent = True
            return redirect('/')
    return render_template('/login.html')

@app.route('/')
@login_required
def index():
    db = db_session()
    chamados_totais = db.query(Chamado).count()
    chamados = db.query(Chamado).order_by(Chamado.data_abertura.desc()).limit(5).all()
    usuarios_ativos = db.query(Usuario).filter(Usuario.status=='ativo').count()
    return render_template('index.html', user=current_user, chamados_totais=chamados_totais, chamados=chamados, usuarios_ativos=usuarios_ativos)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

from controllers.chamado_controller import *
from controllers.usuario_controller import *

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)