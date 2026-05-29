from flask import render_template,request,redirect,url_for,make_response
from main import app
from db import *
from models.usuario_model import *
from models.chamado_model import *
import io
from fpdf import *

@app.route('/usuario/cadastro', methods=['GET'])
def cadastrar_usuario():
    if request.method == 'GET':
        return render_template('usuarios/cadastrar_usuario.html')

@app.route('/usuario/salvar',methods=['POST'])
def salvar_usuario():
    if request.method == 'POST':
        db = Session()
        nome = request.form.get('nome_usuario')
        email = request.form.get('email_usuario')
        departamento = request.form.get('departamento_usuario')
        ramal = request.form.get('ramal_usuario')
        senha = request.form.get('senha_usuario')
        senha_confirm = request.form.get('senha_usuario_confirm')
        status = request.form.get('status')
        if senha == senha_confirm:
            usuario = Usuario(
                nome=nome,
                email=email,
                departamento=departamento,
                ramal=ramal,
                senha=senha,
                status=status
            )
            db.add(usuario)
            db.commit()
            db.close()
            print('USUARIO CRIADO')
            return redirect(url_for('listar_usuario'))
        else:
            print('Senha diferentes')
            return redirect(url_for('cadastrar_usuario'))

@app.route('/usuario/listar')
def listar_usuario():
    db = Session()
    users = db.query(Usuario).all()
    return render_template('usuarios/listar_usuario.html',users=users)

@app.route('/usuario/permissoes')
def permissoes_usuario():
    return render_template('usuarios/permissoes_usuario.html')

@app.route('/usuario/historico')
def historico_usuario():
    db = Session()
    users = db.query(Usuario).all()
    if not users:
        print("Usuarios vazio!")
        return render_template('chamados/historico.html', users=[])
    else:
        return render_template('usuarios/historico_usuario.html', users=users)

@app.route('/usuario/historico/relatorio/<int:id>')
def relatorioUsuario(id):
    db = Session()
    try:    
        usuario = db.query(Usuario).filter_by(id=id).first()
        if not usuario:
            return "Usuario não encontrado", 404
        
        chamados = db.query(Chamado).filter_by(id_usuario=id).all()
    
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()

        pdf.set_font("Helvetica", style="B", size=20)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 12, txt=f"FICHA DO USUÁRIO #{usuario.id}", align="R", new_x="LMARGIN", new_y="NEXT")
        
        pdf.ln(5)

        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, txt=f"Nome: {usuario.nome}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, txt=f"Email: {usuario.email}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, txt=f"Departamento: {usuario.departamento}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, txt=f"Status: {usuario.status}", new_x="LMARGIN", new_y="NEXT")

        pdf.ln(10)
        
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 10, txt=f"Histórico de Chamados ({len(chamados)})", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

        pdf.set_font("Helvetica", "", 10)
        
        dados_tabela = [
            ["Título / Descrição", "Status", "Prioridade", "Categoria", "Abertura"]
        ]
        
        for chamado in chamados:
            
            data_str = chamado.data_abertura.strftime('%d/%m/%Y %H:%M') if chamado.data_abertura else ""
            
            
            info_chamado = f"{chamado.titulo}\nDesc: {chamado.descricao}"
            
            dados_tabela.append([
                info_chamado,
                str(chamado.status),
                str(chamado.prioridade),
                str(chamado.categoria),
                data_str
            ])

        with pdf.table(col_widths=(65, 25, 25, 30, 45), text_align="LEFT") as tabela:
            for linha in dados_tabela:
                row = tabela.row()
                for celula in linha:
                    row.cell(celula)

        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=usuario_{id}.pdf'
        
        return response

    except Exception as e:
        return f"Erro ao gerar relatório: {str(e)}", 500

    finally:
        db.close()
