# Sistema de Gestão de Chamados Técnicos (Help Desk)

Descrição
---------
Sistema web simples para registrar, acompanhar e gerenciar chamados técnicos abertos por colaboradores da empresa. Permite registrar chamados, atribuí-los a técnicos, acompanhar status, gerar relatórios em PDF e gerenciar usuários.

Objetivo do projeto
-------------------
Desenvolver um sistema para registrar, acompanhar e gerenciar chamados técnicos abertos por colaboradores da empresa relacionados a problemas técnicos, dúvidas ou solicitações de suporte. O sistema deve permitir o registro completo do chamado, o controle do seu andamento, a atribuição a técnicos responsáveis e a análise de tempos de resolução, contribuindo para a melhoria da eficiência do suporte técnico interno.

Funcionalidades principais
--------------------------
- Autenticação de usuários (login / logout).
- Cadastro e listagem de usuários.
- Upload de foto de perfil para usuários.
- Abertura de chamados com título, descrição, categoria, prioridade, técnico responsável e datas.
- Listagem e alteração de status / dados do chamado.
- Exclusão de chamados.
- Histórico de chamados (filtragem por finalizados).
- Geração de relatórios em PDF:
  - Relatório individual de chamado (ficha do chamado).
  - Relatório de histórico por usuário (lista de chamados do usuário).
- UI baseada em templates (pasta templates) e assets estáticos (pasta static).

Estrutura do repositório
------------------------
- syshelp/
  - main.py                 — aplicação Flask (rotas gerais e configuração de sessão/login).
  - db.py                   — configuração do SQLAlchemy e engine (MySQL).
  - requirements.txt        — dependências do projeto.
  - controllers/            — controllers/responsáveis pelas rotas (chamado_controller.py, usuario_controller.py).
  - models/                 — modelos SQLAlchemy (chamado_model.py, usuario_model.py).
  - templates/              — templates HTML (views).
  - static/                 — arquivos estáticos (CSS, imagens, JS, etc).

Modelos (resumo)
----------------
- Usuario
  - id, nome, email, senha, departamento, ramal, status, foto
  - relacionamento: um usuário pode ter muitos chamados

- Chamado
  - id, titulo, descricao, data_abertura, data_fechamento, status, prioridade, categoria, id_usuario (FK)
  - relacionamento: chamado.usuario → usuário responsável

Rotas principais
----------------
- Autenticação:
  - GET, POST /login — formulário e processamento de login
  - GET /logout — logout

- Chamados:
  - GET /chamado/abrir-chamado — formulário para abrir chamado
  - POST /chamado/salvar — salva novo chamado
  - GET /chamado/listar — lista todos os chamados
  - GET /chamado/status — visualização do status
  - GET /chamado/status/alterar/<id> — formulário para alterar chamado
  - POST /chamado/status/salvar/<id> — salva alterações do chamado
  - POST /chamado/status/deletar/<id> — deleta chamado
  - GET /chamado/historico — histórico de chamados finalizados
  - GET /chamado/historico/relatorio/pdf/<id> — gera PDF do chamado

- Usuários:
  - GET, POST /usuario/perfil — perfil do usuário e upload de foto
  - GET /usuario/cadastro — formulário de cadastro de usuário
  - POST /usuario/salvar — salva novo usuário
  - GET /usuario/listar — lista usuários
  - GET /usuario/permissoes — página de permissões (placeholder)
  - GET /usuario/historico — histórico de usuários
  - GET /usuario/historico/relatorio/<id> — gera PDF com histórico de chamados do usuário

Requisitos
---------
- Python 3.8+
- Banco de dados MySQL (ou ajuste a URI para outro SGDB compatível)
- Dependências (instalar via pip):
  - Flask
  - Flask-Login
  - SQLAlchemy
  - pymysql
  - python-dotenv
  - fpdf
  - werkzeug
  - outras listadas em `syshelp/requirements.txt`

Instalação e execução (local)
-----------------------------
1. Clone o repositório:
   git clone https://github.com/GabrielSales1/call_management_system.git
2. Acesse a pasta do projeto:
   cd call_management_system
3. Crie e ative um ambiente virtual:
   python -m venv .venv
   - Windows: .venv\Scripts\activate
   - macOS/Linux: source .venv/bin/activate
4. Instale as dependências:
   pip install -r syshelp/requirements.txt
5. Configure as variáveis de ambiente:
   - crie um arquivo `.env` ou exporte as variáveis necessárias.
   - Exemplo mínimo para `.env`:
     SECRET_KEY=uma_chave_secreta_long_e_segura
   Observação: atualmente a URI do banco está definida diretamente em `syshelp/db.py` como:
     mysql+pymysql://root:@localhost:3306/syshelp
   Recomenda-se:
   - Criar o banco MySQL:
     CREATE DATABASE syshelp CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
   - Criar um usuário com permissões ou ajustar a URI para usar um usuário/senha seguros.
   - (Melhoria recomendada) alterar `db.py` para obter a URI do ambiente, por exemplo:
     DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:@localhost:3306/syshelp')
6. Inicialize/crie as tabelas:
   - O projeto usa SQLAlchemy com Base.metadata.create_all(engine) — as tabelas são criadas automaticamente ao importar os modelos.
7. Execute a aplicação:
   python syshelp/main.py
8. Acesse no navegador:
   http://127.0.0.1:5000/

Contato
-------
Desenvolvedor: GabrielSales1

---
Obrigado por usar/avaliar este projeto! Se quiser, eu posso ajudar a transformar estas instruções em um arquivo README.md pronto para commitar no repositório.
