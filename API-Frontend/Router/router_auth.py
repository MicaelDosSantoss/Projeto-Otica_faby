from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from Models.Usuario import Usuario

auth_bp = Blueprint('auth', __name__)

# --- Rotas de Registro ---

@auth_bp.route('/registro', methods=['GET'])
def registro_view():
    """Exibe a tela de registro"""
    # Se já estiver logado, redireciona para home
    if current_user.is_authenticated:
        return redirect(url_for('oculos.home'))
    return render_template('registro.html')

@auth_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    """Processa o cadastro de um novo usuário"""
    form = request.form
    
    # Validação básica de campos
    if not all([form.get('Nome'), form.get('Email'), form.get('Senha'), form.get('Data_Nascimento')]):
        return jsonify({"erro": "Campos obrigatórios ausentes."}), 400
    
    # Calcula a idade a partir da data de nascimento
    idade = Usuario.calcular_idade(form.get('Data_Nascimento'))
    
    if idade is None:
        return jsonify({"erro": "Data de nascimento inválida."}), 400
    
    usuario = Usuario(
        Nome=form.get('Nome'),
        Sexo=form.get('Sexo'),
        Data_Nascimento=form.get('Data_Nascimento'),
        Idade=idade,
        Email=form.get('Email'),
        Senha=form.get('Senha')
    )
    
    resp, status = usuario.salvar(is_adm=False)
    
    if status == 201:
        # Redireciona para a tela de login após o registro
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login_view'))
    
    return resp, status

# --- Rotas de Login ---

@auth_bp.route('/login', methods=['GET'])
@auth_bp.route('/', methods=['GET'])
def login_view():
    """Exibe a tela de login"""
    # Se já estiver logado, redireciona para home
    if current_user.is_authenticated:
        return redirect(url_for('oculos.home'))
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def logar_usuario():
    """Processa o login do usuário"""
    form = request.form
    email = form.get('Email')
    senha = form.get('Senha')
    
    if not all([email, senha]):
        return jsonify({"erro": "E-mail e senha são obrigatórios."}), 400
    
    # Busca o usuário no banco
    usuario_dict, erro = Usuario.buscar_por_email(email, is_adm=False)
    
    if erro or not usuario_dict:
        return render_template('login.html', error="Usuário ou senha inválidos.")
    
    # Verifica a senha
    if Usuario.verificar_senha(senha, usuario_dict['Senha'], usuario_dict['Id_Usuario'], is_adm=False):
        # Cria objeto Usuario e faz login
        usuario_obj = Usuario.criar_usuario_objeto(usuario_dict, is_adm=False)
        login_user(usuario_obj)
        
        # Redireciona para a home
        return redirect(url_for('oculos.home'))
    else:
        return render_template('login.html', error="Usuário ou senha inválidos.")

# --- Rotas de Logout ---

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Faz logout do usuário"""
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login_view'))

# --- Rotas de ADM ---

@auth_bp.route('/adm/login', methods=['GET'])
def adm_login_view():
    """Exibe a tela de login do administrador"""
    # Se já estiver logado como admin, redireciona
    if current_user.is_authenticated and current_user.is_adm:
        return redirect(url_for('oculos.mostrar_todos_oculos'))
    return render_template('adm_login.html')

@auth_bp.route('/adm/login', methods=['POST'])
def logar_adm():
    """Processa o login do administrador"""
    form = request.form
    email = form.get('Email')
    senha = form.get('Senha')
    
    if not all([email, senha]):
        return jsonify({"erro": "E-mail e senha são obrigatórios."}), 400
    
    # Busca o admin no banco
    usuario_dict, erro = Usuario.buscar_por_email(email, is_adm=True)
    
    if erro or not usuario_dict:
        return render_template('adm_login.html', error="Administrador ou senha inválidos.")
    
    # Verifica a senha
    if Usuario.verificar_senha(senha, usuario_dict['Senha'], usuario_dict['Id_Usuario'], is_adm=True):
        # Cria objeto Usuario e faz login
        usuario_obj = Usuario.criar_usuario_objeto(usuario_dict, is_adm=True)
        login_user(usuario_obj)
        
        # Redireciona para a área administrativa
        return redirect(url_for('oculos.mostrar_todos_oculos'))
    else:
        return render_template('adm_login.html', error="Administrador ou senha inválidos.")

@auth_bp.route('/adm/logout', methods=['GET', 'POST'])
@login_required
def adm_logout():
    """Faz logout do administrador"""
    logout_user()
    flash('Você saiu da conta de administrador.', 'info')
    return redirect(url_for('auth.adm_login_view'))
