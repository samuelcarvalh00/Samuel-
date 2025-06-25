from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """
    Decorator que verifica se o usuário está logado.
    Se não estiver, redireciona para a página de login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'error')
            return redirect(url_for('main.login'))  # Corrigido para usar o blueprint
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """
    Retorna o ID do usuário atual da sessão, se estiver logado.
    """
    return session.get('user_id')

def is_logged_in():
    """
    Verifica se há um usuário logado na sessão.
    """
    return 'user_id' in session