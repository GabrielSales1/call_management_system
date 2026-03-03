from flask import Flask, render_template,request

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)