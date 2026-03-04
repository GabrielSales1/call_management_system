from flask import Flask, render_template,request

app = Flask(__name__)

#login "auth"
@app.route('/login',methods=['GET','POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    if email == 'admin@gmail.com' and senha == 'admin':
        return render_template('/index.html')
    else:
        return render_template('/login.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/abrir-chamado')
def abrirChamado():
    return render_template('chamados/abrir_chamado.html')

@app.route('/atribuir')
def atribuirChamado():
    return render_template('chamados/atribuir_chamado.html')

@app.route('/encerrar')
def encerrarChamado():
    return render_template('chamados/encerrar.html')

@app.route('/historico')
def historicoChamado():
    return render_template('chamados/historico.html')

@app.route('/listar-chamado')
def listarChamado():
    return render_template('chamados/listar_chamado.html')

@app.route('/status')
def statusChamado():
    return render_template('chamados/status.html')


if __name__ == '__main__':
    app.run(debug=True)