from flask import Flask, render_template,request
from db import Session
from models.chamado_model import *
from models.usuario_model import *


app = Flask(__name__)

#login "auth"
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session = Session()
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = session.query(Usuario).filter_by(email=email).first()
        
        if user.email == email and user.senha == senha:
            return render_template('/index.html')
    return render_template('/login.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)