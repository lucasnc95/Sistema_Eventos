# app.py
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from config import Config
from models import db, User, Evento, Inscricao, Docente, Discente, Externo  # Certifique-se de importar os modelos

app = Flask(__name__)
app.config.from_object(Config)

# Inicializando as extensões com a aplicação
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(Nome=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciais inválidas', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        tipo_usuario = request.form['tipo_usuario']
        siape = request.form.get('siape', None)
        matricula = request.form.get('matricula', None)
        cpf = request.form.get('cpf', None)

        if tipo_usuario == 'docente' and not siape:
            flash('Docentes devem fornecer o SIAPE.', 'danger')
            return render_template('register.html')
        elif tipo_usuario == 'discente' and not matricula:
            flash('Discentes devem fornecer a matrícula.', 'danger')
            return render_template('register.html')
        elif tipo_usuario == 'externo' and not cpf:
            flash('Usuários externos devem fornecer o CPF.', 'danger')
            return render_template('register.html')

        new_user = User(Nome=nome, Senha=password, tipo=tipo_usuario)
        db.session.add(new_user)
        db.session.commit()
        
        if tipo_usuario == 'docente':
            docente = Docente(IDUser=new_user.IDUser, SIAPE=siape)
            db.session.add(docente)
        elif tipo_usuario == 'discente':
            discente = Discente(IDUser=new_user.IDUser, Matricula=matricula)
            db.session.add(discente)
        elif tipo_usuario == 'externo':
            externo = Externo(IDUser=new_user.IDUser, CPF=cpf)
            db.session.add(externo)

        db.session.commit()
        flash('Registro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    eventos = Evento.query.all()
    return render_template('dashboard.html', eventos=eventos)


@app.route('/criar_evento', methods=['GET', 'POST'])
@login_required
def criar_evento():
    if current_user.tipo != 'discente':
        flash('Somente discentes podem criar eventos.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data = request.form['data']
        horario = request.form['horario']
        vagas = request.form['vagas']

        novo_evento = Evento(IDUserDocente=current_user.IDUser, Titulo=titulo, Descricao=descricao,
                             Data=data, Horario=horario, Vagas=vagas, Status='pendente')
        db.session.add(novo_evento)
        db.session.commit()
        flash('Evento criado com sucesso! Aguarde a aprovação do docente.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('criar_evento.html')


@app.route('/aprovar_evento/<int:event_id>', methods=['GET', 'POST'])
@login_required
def aprovar_evento(event_id):
    if current_user.tipo != 'docente':
        flash('Apenas docentes podem aprovar eventos.', 'danger')
        return redirect(url_for('dashboard'))

    evento = Evento.query.get(event_id)
    if request.method == 'POST':
        acao = request.form['acao']
        evento.Status = 'aprovado' if acao == 'aprovar' else 'reprovado'
        db.session.commit()
        flash('Evento atualizado com sucesso', 'success')
        return redirect(url_for('dashboard'))

    return render_template('aprovar_evento.html', evento=evento)


@app.route('/editar_evento/<int:event_id>', methods=['GET', 'POST'])
@login_required
def editar_evento(event_id):
    evento = Evento.query.get(event_id)
    if current_user.tipo != 'docente' or evento.IDUserDocente != current_user.IDUser:
        flash('Você não tem permissão para editar este evento.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        evento.Titulo = request.form['titulo']
        evento.Descricao = request.form['descricao']
        evento.Data = request.form['data']
        evento.Horario = request.form['horario']
        evento.Vagas = request.form['vagas']

        db.session.commit()
        flash('Evento atualizado com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('editar_evento.html', evento=evento)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'success')
    return redirect(url_for('login'))


# Inicializando a aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados

    app.run(host='0.0.0.0', port=5000, debug=True)
