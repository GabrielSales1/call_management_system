from flask import Flask, render_template,request
from db import Session



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

from controllers.chamado_controller import *
from controllers.usuario_controller import *

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)