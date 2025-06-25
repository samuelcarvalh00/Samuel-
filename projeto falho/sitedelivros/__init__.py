# sitedelivros/__init__.py
print("DEBUG: __init__.py está sendo carregado.") # Linha de depuração

from flask import Flask
from sitedelivros.database import create_tables
import logging
import os
from flask_login import LoginManager, current_user
from sitedelivros.models import User

def create_app():
    print("DEBUG: Função create_app() iniciada.") # Linha de depuração
    app = Flask(__name__,
                static_folder='static',
                static_url_path='/static',
                template_folder='templates')

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-muito-segura-e-unica-aqui-2025'

    app.config['DB_CONFIG'] = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',
        'database': 'biblioteca'
    }

    # ... (restante do seu código __init__.py, incluindo a parte com 'raise e' no bloco try/except) ...

    # Garanta que esta linha esteja lá com o 'raise e'
    try:
        app.logger.info("Tentando criar tabelas do banco de dados...")
        with app.app_context():
            create_tables(app.config['DB_CONFIG'])
        app.logger.info("Tabelas do banco de dados verificadas/criadas com sucesso.")
    except Exception as e:
        app.logger.error(f"ERRO CRÍTICO: Não foi possível conectar ou criar tabelas no banco de dados: {e}")
        raise e # <--- Mantenha esta linha para forçar o traceback

    print("DEBUG: create_app() retornando a instância do Flask.") # Linha de depuração
    return app# sitedelivros/__init__.py
print("DEBUG: __init__.py está sendo carregado.") # Linha de depuração

from flask import Flask
from sitedelivros.database import get_db_connection # Importar get_db_connection
import logging
import os
from flask_login import LoginManager, current_user
from sitedelivros.models import User
from sitedelivros.database import create_tables # Manter import de create_tables

def create_app():
    print("DEBUG: Função create_app() iniciada.") # Linha de depuração
    app = Flask(__name__,
                static_folder='static',
                static_url_path='/static',
                template_folder='templates')

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-muito-segura-e-unica-aqui-2025'

    app.config['DB_CONFIG'] = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',
        'database': 'biblioteca'
    }

    app.config['DEFAULT_COVER_URL'] = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjUwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDI1MCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyNTAiIGhlaWdodD0iMzAwIiBmaWxsPSIjMjUzQzRGZCIvPgo8cGF0aCBkPSJNMTA0LjY1MiAxMzkuMjEzQzEwNC42NTIgMTMwLjcwNiAxMTAuNDYyIDEyNS44MDUgMTE1LjcxNiAxMjUuODA1SDE0Ni4yODRDMTUxLjU1NyAxMjUuODA1IDE1Ny4zNTIgMTMwLjcwNiAxNTcuMzUyIDEzOS4yMTNWMjAxLjI5NkMxNTcuMzUyIDIwOS44MDQgMTUxLjU1NyAyMTQuNzA0IDE0Ni4yODQgMjE0LjcwNEgxMTUuNzE2QzExMC40NjIgMjE0LjcwNCAxMDQuNjUyIDIwOS44MDQgMTA0LjY1MiAyMDEuMjk2VjEzOS4yMTNaIiBmaWxsPSIjRkY1RTVEIi8+CjxwYXRoIGQ9Ik0xMjguMDM3IDE4Ny41NjhMMTI4LjAzNyAxNTIuMjI0TDE1Ny4xMTUgMTUxLjk1M0wxNTcuMTE1IDE1OS42MzZMMTM3LjE4MyAxNTkuNjM2TDEzNy4xODMgMTcyLjM4N0wxNTQuNDg4IDE3Mi42MzFMMTU0LjQ4OCAxODAuNDQxTDEzNy4xODMgMTgwLjE2TDEzNy4xODMgMTg3LjU2OEwxMjguMDM3IDE4Ny41NjhZIiBpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik0xMTUuNjU3IDE4Ny41NjhMMTE1LjY1NyAxNTIuMjI0TDEyNC44MDIgMTUyLjIyNExxMjQuODAyIDE4Ny41NjhMMTE1LjY1NyAxODcuNTY4WiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTY1Ljg4OCAxNzAuMjE2QzY1Ljg4OCAxNTkuNDI4IDYyLjA0NCAxNTAuNjMxIDUyLjgzNCAxNTAuNjMxS DM0LjMyNUNyMjUuMDYgMTUwLjYzMSAyMS4yNTggMTU5LjQ3MyAyMS4yNTggMTcwLjE2MVYxODkuNzAzQzIxLjI1OCAyMDAuNDE1IDI1LjA2IDIwOC44NDUgMzQuMzI1IDIwOC44NDVINTIuODM0QzYyLjA0NCAyMDguODQ1IDY1Ljg4OCAyMDAuMzExIDY1Ljg4OCAxODkuNDI4VjE3MC4yMTZaTTM1LjI1NSAxODMuNDUxQzM1LjI1NSAxODYuNjk4IDM2LjgyIDE4OC4zMTIgMzkuMzUgMTg4LjMxMkg0OC44MTlDNTEuMzYzIDE4OC4zMTIgNTIuODQ5IDE4Ni42NTQgNTIuODQ5IDE4My4zMTJWMTU1LjkyQzUyLjg0OSAxNTIuNTc4IDUxLjM2MyAxNTAuOTY0IDQ4LjgxOSAxNTAuOTY0S DM5LjM1QzM2LjgyIDE1MC45NjQgMzUuMjU1IDE1Mi41MzUgMzUuMjU1IDE1NS44MjZWMTgzLjQ1MVoiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik0yMzIuMjI4IDE3MC4yMTZDMTkyLjY5NyAxNjAuMjQzIDE5Mi43MjYgMTUwLjY2MiAxOTIuNzQ4IDE0MC41ODhDMTkyLjY5NyAxMzkuNDE4IDE5Mi42NTcgMTM4LjU5NyAxOTIuNjU3IDEzOC41OTdWMTA1LjYzMVY1Ni41NzJDMTkyLjY1NyA1Ni41NzIgMjAyLjIxNyA2MC4yNjUgMjE5LjY3NiA36.3MTJDMjQ3LjMwNiAxMTAuNTMyIDI1Mi4wNjUgMTM4LjQyOCAyNDcuMjYyIDE3My43NjRDMjQ3LjA2NyAxNzYuMDQgMjM3LjEyOSAxNzguMDY2IDIzMi4yMjggMTcwLjIxNloiIGZpbGw9IndoaXRlIi8+Cjwvc3ZnPgo='

    # Inicializa Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login' # Define a rota para onde o usuário será redirecionado se não estiver logado

    # Função user_loader do Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        app.logger.info(f"Tentando carregar usuário com ID: {user_id}")
        try:
            user = User.get_by_id(int(user_id))
            if user:
                app.logger.info(f"Usuário {user.email} carregado com sucesso.")
            else:
                app.logger.warning(f"Usuário com ID {user_id} não encontrado.")
            return user
        except Exception as e:
            app.logger.error(f"Erro ao carregar usuário via load_user: {e}")
            return None


    # Context Processor para injetar current_user em todos os templates
    @app.context_processor
    def inject_current_user():
        return dict(current_user=current_user)

    # Registra o Blueprint 'main'
    from sitedelivros.views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Configuração de logging
    logging.basicConfig(level=logging.INFO)
    app.logger.info("Aplicativo Flask inicializado.")

    # Tenta criar as tabelas do banco de dados dentro do contexto da aplicação
    print("DEBUG: Antes do bloco try/except para create_tables.") # Nova linha de depuração
    try:
        app.logger.info("Tentando criar tabelas do banco de dados...")
        with app.app_context():
            # AQUI ESTÁ A CHAVE: Adicione um print ANTES de chamar create_tables
            print("DEBUG: Chamando create_tables...") # Nova linha de depuração
            create_tables(app.config['DB_CONFIG'])
            print("DEBUG: create_tables executado com sucesso.") # Nova linha de depuração
        app.logger.info("Tabelas do banco de dados verificadas/criadas com sucesso.")
    except Exception as e:
        app.logger.error(f"ERRO CRÍTICO: Não foi possível conectar ou criar tabelas no banco de dados: {e}")
        print(f"DEBUG: EXCEÇÃO CAPTURADA no __init__.py: {e}") # Nova linha de depuração
        raise e # <--- Mantenha esta linha para forçar o traceback

    print("DEBUG: create_app() retornando a instância do Flask.") # Linha de depuração
    return app