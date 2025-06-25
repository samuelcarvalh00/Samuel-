# sitedelivros/views.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from sitedelivros.models import User, Book
# Importe as funções do Flask-Login
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/catalogo')
@login_required  # Agora o catálogo requer login
def catalogo():
    # Busca apenas os livros do usuário logado
    books = Book.get_all_by_user(current_user.id)
    for book in books:
        if book and book['cover_url'] and (book['cover_url'].startswith('http://') or book['cover_url'].startswith('https://')):
            book['cover_url_full'] = book['cover_url']
        elif book and book['cover_url']:
            book['cover_url_full'] = url_for('static', filename=f"img/{book['cover_url']}")
        else:
            book['cover_url_full'] = current_app.config['DEFAULT_COVER_URL']
    return render_template('catalogo.html', books=books)

@main.route('/livro/<int:book_id>')
@login_required  # Requer login para ver detalhes
def livro_detalhe(book_id):
    # Busca o livro apenas se pertencer ao usuário logado
    book = Book.get_by_id_and_user(book_id, current_user.id)
    if not book:
        flash('Livro não encontrado ou você não tem permissão para visualizá-lo.', 'error')
        return redirect(url_for('main.catalogo'))
    
    if book['cover_url'] and (book['cover_url'].startswith('http://') or book['cover_url'].startswith('https://')):
        book['cover_url_full'] = book['cover_url']
    elif book['cover_url']:
        book['cover_url_full'] = url_for('static', filename=f"img/{book['cover_url']}")
    else:
        book['cover_url_full'] = current_app.config['DEFAULT_COVER_URL']
    return render_template('detalhe_livro.html', book=book)

@main.route('/quemsomos')
def quemsomos():
    return render_template('quemsomos.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    # Se já logado, redireciona
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = User.get_by_email(email)

        if user and check_password_hash(user.password_hash, senha):
            login_user(user) # Usa a função login_user do Flask-Login
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Email ou senha inválidos.', 'error')
    return render_template('login.html')

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    # Se já logado, redireciona
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if User.get_by_email(email):
            flash('Este email já está cadastrado.', 'error')
        elif senha != confirmar_senha:
            flash('As senhas não coincidem.', 'error')
        else:
            User.create(email, senha)
            flash('Registro realizado com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('main.login'))
    return render_template('registro.html')

@main.route('/logout')
@login_required # Garante que só usuários logados possam fazer logout
def logout():
    logout_user() # Usa a função logout_user do Flask-Login
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.index'))

@main.route('/cadastrar', methods=['GET', 'POST'])
@login_required # Protege esta rota
def cadastrar():
    # Busca apenas os livros do usuário logado
    books = Book.get_all_by_user(current_user.id)
    for book in books:
        if book and book['cover_url'] and (book['cover_url'].startswith('http://') or book['cover_url'].startswith('https://')):
            book['cover_url_full'] = book['cover_url']
        elif book and book['cover_url']:
            book['cover_url_full'] = url_for('static', filename=f"img/{book['cover_url']}")
        else:
            book['cover_url_full'] = current_app.config['DEFAULT_COVER_URL']

    if request.method == 'POST':
        title = request.form['titulo_do_livro']
        author = request.form['autor']
        year = request.form.get('ano')
        cover_url = request.form.get('cover_image_url')
        description = request.form.get('description')

        if not year:
            year = None # Garante que seja None se estiver vazio
        if not cover_url:
            cover_url = None
        if not description:
            description = None

        # Cria o livro associado ao usuário logado
        Book.create(title, author, current_user.id, year, cover_url, description)
        flash('Livro cadastrado com sucesso!', 'success')
        return redirect(url_for('main.cadastrar')) # Redireciona para atualizar a lista

    return render_template('cadastrar.html', books=books)

@main.route('/editar_livro/<int:book_id>', methods=['GET', 'POST'])
@login_required # Protege esta rota
def editar_livro(book_id):
    # Busca o livro apenas se pertencer ao usuário logado
    book = Book.get_by_id_and_user(book_id, current_user.id)
    if not book:
        flash('Livro não encontrado ou você não tem permissão para editá-lo.', 'error')
        return redirect(url_for('main.cadastrar'))

    if request.method == 'POST':
        book['title'] = request.form['titulo_do_livro']
        book['author'] = request.form['autor']
        book['year'] = request.form.get('ano')
        book['cover_url'] = request.form.get('cover_image_url')
        book['description'] = request.form.get('description')

        if not book['year']:
            book['year'] = None
        if not book['cover_url']:
            book['cover_url'] = None
        if not book['description']:
            book['description'] = None

        # Atualiza o livro garantindo que pertence ao usuário
        Book.update(book_id, book['title'], book['author'], current_user.id, book['year'], book['cover_url'], book['description'])
        flash('Livro atualizado com sucesso!', 'success')
        return redirect(url_for('main.cadastrar'))

    # Lógica para popular o campo de input de capa na edição
    if book['cover_url'] and (book['cover_url'].startswith('http://') or book['cover_url'].startswith('https://')):
        book['cover_url_for_input'] = book['cover_url']
    elif book['cover_url']:
        book['cover_url_for_input'] = book['cover_url']
    else:
        book['cover_url_for_input'] = '' # Campo vazio se não houver capa

    # Lógica para exibir a capa na pré-visualização na edição (usa cover_url_full)
    if book['cover_url'] and (book['cover_url'].startswith('http://') or book['cover_url'].startswith('https://')):
        book['cover_url_display'] = book['cover_url']
    elif book['cover_url']:
        book['cover_url_display'] = url_for('static', filename=f"img/{book['cover_url']}")
    else:
        book['cover_url_display'] = current_app.config['DEFAULT_COVER_URL']

    return render_template('editor_livro.html', book=book)

@main.route('/deletar_livro/<int:book_id>', methods=['POST'])
@login_required # Protege esta rota
def deletar_livro(book_id):
    # Deleta o livro apenas se pertencer ao usuário logado
    if Book.delete(book_id, current_user.id):
        flash('Livro deletado com sucesso!', 'success')
    else:
        flash('Erro ao deletar livro ou você não tem permissão.', 'error')
    return redirect(url_for('main.cadastrar'))