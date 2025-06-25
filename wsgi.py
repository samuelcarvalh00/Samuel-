# wsgi.py
import sys
import os

# Adiciona o diretório do seu projeto ao PYTHONPATH.
# MUDE 'seu_usuario' para o seu nome de usuário exato no PythonAnywhere.
# MUDE 'seu_projeto' para o nome da pasta raiz do seu projeto no PythonAnywhere
# (por exemplo, se você clonou seu repositório em /home/seu_usuario/meu_site_de_livros, então use 'meu_site_de_livros').
project_home = '/home/sam2498/neolibres'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Importa sua aplicação Flask.
# Assumimos que a instância do Flask se chama 'app' e está no arquivo 'app.py'
# na raiz do seu diretório de projeto.
from app import app as application

# Se você tiver variáveis de ambiente específicas para o seu ambiente de produção
# que não são gerenciadas pelo PythonAnywhere (o que é raro para o plano gratuito),
# você poderia carregá-las aqui. Mas para o MySQL, o PythonAnywhere já lida com isso.