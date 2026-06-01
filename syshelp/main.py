from flask import Flask, render_template,request
from db import Session
from flask_login import LoginManager,login_user,login_required
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

@lm.user_loader
def carregar_usuario(user_id):
    db = Session()
    usuario = db.query(Usuario).get(int(user_id))
    db.close()
    return usuario

#login "auth"
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        db = Session()
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = db.query(Usuario).filter_by(email=email).first()
        
        if user.email == email and user.senha == senha:
            login_user(user)
            return render_template('/index.html')
    return render_template('/login.html')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

from controllers.chamado_controller import *
from controllers.usuario_controller import *

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)