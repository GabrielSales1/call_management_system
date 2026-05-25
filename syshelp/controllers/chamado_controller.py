from flask import render_template,request,redirect, url_for,make_response
from main import app
import io
from db import *
from models.chamado_model import *
from models.usuario_model import *
from datetime import datetime
from fpdf import * 

@app.route('/chamado/abrir-chamado', methods=['GET'])
def abrirChamado():
    session = Session()
    users = session.query(Usuario).all()
    return render_template('chamados/abrir_chamado.html',users=users)

@app.route('/chamado/salvar',methods=['POST'])
def salvar():
    session = Session()

    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    status = request.form.get('status')
    prioridade = request.form.get('prioridade')
    categoria = request.form.get('categoria')
    tecnico = request.form.get('tecnico')

    #PEGANDO AS DATAS
    data_abertura_str = request.form.get('data_abertura')
    data_fechamento_str = request.form.get('data_fechamento')

    #CONVERTENDO
    data_abertura = None
    if data_abertura_str:
        data_abertura = datetime.strptime(data_abertura_str, "%Y-%m-%d")

    data_fechamento = None
    if data_fechamento_str:
        data_fechamento = datetime.strptime(data_fechamento_str, "%Y-%m-%d")

    chamado = Chamado(
        titulo=titulo,
        descricao=descricao,
        status=status,
        prioridade=prioridade,
        categoria=categoria,
        data_abertura=data_abertura,
        data_fechamento=data_fechamento,
        id_usuario=tecnico
    )
    session.add(chamado)
    session.commit()
    return redirect(url_for('listarChamado'))

@app.route('/chamado/listar')
def listarChamado():
    db = Session()
    chamados = db.query(Chamado).all()
    return render_template('chamados/listar_chamado.html',chamados=chamados)

@app.route('/chamado/status')
def statusChamado():
    db = Session()
    chamados = db.query(Chamado).all()
    return render_template('chamados/status.html',chamados=chamados)

@app.route('/chamado/status/alterar/<int:id>', methods=['GET'])
def alterarChamado(id):
    db = Session()
    chamado = db.query(Chamado).filter_by(id=id).first()
    usuario = db.query(Usuario).all()
    return render_template('chamados/alterar_chamado.html',chamado=chamado, usuario=usuario)

@app.route('/chamado/status/salvar/<int:id>',methods=['POST'])
def salvarAlteracao(id):
    db = Session()
    chamado = db.query(Chamado).filter_by(id=id).first()
    chamado.titulo = request.form.get('titulo')
    chamado.descricao = request.form.get('descricao')
    chamado.status = request.form.get('status')
    chamado.prioridade = request.form.get('prioridade')
    chamado.categoria = request.form.get('categoria')
    chamado.id_usuario = request.form.get('tecnico')

    data_abertura_str = request.form.get('data_abertura')
    data_fechamento_str = request.form.get('data_fechamento')

    chamado.data_abertura = datetime.strptime(data_abertura_str, "%Y-%m-%d") if data_abertura_str else None
    chamado.data_fechamento = datetime.strptime(data_fechamento_str, "%Y-%m-%d") if data_fechamento_str else None

    db.commit()
    db.close()
    return redirect(url_for('listarChamado'))

@app.route('/chamado/status/deletar/<int:id>', methods=['POST'])
def deletarChamado(id):
    db = Session()
    
    chamado = db.query(Chamado).filter(Chamado.id == id).first()

    if not chamado:
        return "Chamado não encontrado", 404

    db.delete(chamado)
    db.commit()
    return redirect(url_for('statusChamado'))

@app.route('/chamado/historico')
def historicoChamado():
    db = Session()
    chamados = db.query(Chamado).filter(Chamado.data_fechamento != None, Chamado.status.in_(['resolvido','fechado'])).all()
    if not chamados:
        print("Chamado vazio!")
        return render_template('chamados/historico.html', chamados=[])
    else:
        return render_template('chamados/historico.html', chamados=chamados)

@app.route('/chamado/historico/relatorio/pdf/<int:id>')
def relatorioChamado(id):
    db = Session()
    try:
        chamado = db.query(Chamado).filter_by(id=id).first()
        if not chamado:
            return "Chamado não encontrado", 404

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()
        
        pdf.set_font("Helvetica", style="B", size=20)
        pdf.set_text_color(44, 62, 80) # Azul escuro corporativo
        pdf.cell(0, 12, txt=f"FICHA DO CHAMADO #{chamado.id}", align="R", new_x="LMARGIN", new_y="NEXT")

        pdf.set_draw_color(52, 152, 219) # Azul claro
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(8)
        
        txt_titulo = str(chamado.titulo or "Sem Título")
        txt_desc = str(chamado.descricao or "Sem Descrição")
        txt_abertura = chamado.data_abertura.strftime('%d/%m/%Y') if chamado.data_abertura else "-"
        txt_fechamento = chamado.data_fechamento.strftime('%d/%m/%Y') if chamado.data_fechamento else "Em aberto"
        txt_status = str(chamado.status or "-").upper()
        txt_prioridade = str(chamado.prioridade or "-").upper()
        txt_categoria = str(chamado.categoria or "-").upper()
        txt_tecnico = str(chamado.usuario.nome or "Não atribuído")

        def criar_bloco(label, valor, largura_total=190, multi=False):
            pdf.set_font("Helvetica", style="B", size=10)
            pdf.set_text_color(127, 140, 141) # Cinza médio
            pdf.cell(largura_total, 5, label, new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font("Helvetica", size=11)
            pdf.set_text_color(44, 62, 80) # Azul escuro
            
            if multi:
                pdf.set_fill_color(248, 249, 250)
                pdf.set_draw_color(220, 224, 230)
                pdf.multi_cell(largura_total, 7, valor, border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.cell(largura_total, 7, valor, new_x="LMARGIN", new_y="NEXT")
            
            pdf.ln(4)

        criar_bloco("TÍTULO DO CHAMADO", txt_titulo)
        
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.set_text_color(127, 140, 141)
        
        pdf.cell(95, 5, "STATUS")
        pdf.cell(95, 5, "PRIORIDADE", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", size=11)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(95, 7, txt_status)
        pdf.cell(95, 7, txt_prioridade, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
       
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.set_text_color(127, 140, 141)
        pdf.cell(95, 5, "DATA DE ABERTURA")
        pdf.cell(95, 5, "DATA DE FECHAMENTO", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", size=11)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(95, 7, txt_abertura)
        pdf.cell(95, 7, txt_fechamento, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

        pdf.set_font("Helvetica", style="B", size=10)
        pdf.set_text_color(127, 140, 141)
        pdf.cell(95, 5, "CATEGORIA")
        pdf.cell(95, 5, "TÉCNICO ENCARREGADO", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", size=11)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(95, 7, txt_categoria)
        pdf.cell(95, 7, txt_tecnico, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)
        
        criar_bloco("DESCRIÇÃO DETALHADA", txt_desc, largura_total=190, multi=True)
            
    finally:
        db.close()
    
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=chamado_{id}.pdf'
    
    return response
