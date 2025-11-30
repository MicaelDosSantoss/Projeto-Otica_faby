from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from Models.Oculos import Oculos
from Models.CRUD import CRUD # Para buscar Forma, Material, Marca

from werkzeug.utils import secure_filename
import os

oculos_bp = Blueprint('oculos', __name__)

UPLOAD_FOLDER = 'static/uploads'

@oculos_bp.route('/oculos', methods=['POST'])
@login_required
def criar_oculos():
    """Cria um novo óculos (apenas para admins)"""
    # Verifica se é admin
    if not current_user.is_adm:
        return jsonify({"erro": "Acesso negado. Apenas administradores podem criar óculos."}), 403
    
    form = request.form
    imagem = request.files.get('Imagem')
    filename = None
    
    if imagem and imagem.filename != '':
        filename = secure_filename(imagem.filename)
        caminho = os.path.join(UPLOAD_FOLDER, filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        try:
            imagem.save(caminho)
        except Exception as e:
            print(f"Erro ao salvar imagem: {e}")

    oculos = Oculos(
        Modelo=form.get('Modelo'),
        Material_FK=form.get('Material_FK'),
        Forma_FK=form.get('Forma_FK'),
        Marca_FK=form.get('Marca_FK'),
        Valor=form.get('Valor'),
        Quantidade=form.get('Quantidade'),
        Descricao=form.get('Descricao'),
        Sobre_Produto=form.get('Sobre_Produto'),
        Imagem=filename
    )

    oculos.salvar()
    return redirect(url_for('oculos.mostrar_todos_oculos'))

@oculos_bp.route('/oculos/update/<id>', methods=['PUT'])
@login_required
def atualizar_oculos(id):
    """Atualiza um óculos existente (apenas para admins)"""
    # Verifica se é admin
    if not current_user.is_adm:
        return jsonify({"erro": "Acesso negado. Apenas administradores podem atualizar óculos."}), 403
    
    form = {}
    imagem = None
    if request.content_type.startswith('multipart/form-data'):
        form = request.form.to_dict()
        imagem = request.files.get('Imagem')
    elif request.is_json:
        form = request.get_json() or {}
    
    # Lógica de upload de imagem para atualização
    if imagem and imagem.filename != '':
        filename = secure_filename(imagem.filename)
        caminho = os.path.join(UPLOAD_FOLDER, filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        try:
            imagem.save(caminho)
            form['Imagem'] = filename
        except Exception as e:
            print(f"Erro ao salvar imagem na atualização: {e}")
    
    # Renomear campos para o novo padrão
    if 'ID_Material' in form:
        form['Material_FK'] = form.pop('ID_Material')
    if 'ID_Forma' in form:
        form['Forma_FK'] = form.pop('ID_Forma')
    if 'ID_Marca' in form:
        form['Marca_FK'] = form.pop('ID_Marca')
    if 'Nome' in form:
        form['Modelo'] = form.pop('Nome')

    resp = Oculos.atualizar(id, form)
    return resp

@oculos_bp.route('/oculos', methods=['GET'])
@login_required
def mostrar_todos_oculos():
    """Exibe todos os óculos (área administrativa - apenas para admins)"""
    # Verifica se é admin
    if not current_user.is_adm:
        # Redireciona clientes para a home
        from flask import flash
        flash('Acesso negado. Esta área é restrita a administradores.', 'error')
        return redirect(url_for('oculos.home'))
    
    oculo = Oculos.mostrarTudo()
    marca = CRUD.mostrar("Marca", "Id_Marca")
    forma = CRUD.mostrar("Forma", "Id_Forma")
    material = CRUD.mostrar("Material", "Id_Material")

    if isinstance(oculo, tuple) and oculo[1] != 200:
        error_message = oculo[0].get_json().get('erro') or oculo[0].get_json().get('mensagem')
        return render_template('controller_oculos.html', error=error_message, oculos=[], marcas=marca, formas=forma, materiais=material)
    
    return render_template('controller_oculos.html', oculos=oculo, marcas=marca, formas=forma, materiais=material)

@oculos_bp.route('/home', methods=['GET'])
@login_required
def home():
    """Exibe a página inicial da loja (para clientes logados)"""
    oculo = Oculos.mostrarTudo()

    if isinstance(oculo, tuple) and oculo[1] != 200:
        return oculo
    
    return render_template('home.html', oculos=oculo)

@oculos_bp.route('/item/<id>', methods=['GET'])
@login_required
def buscar_oculos_por_id(id):
    """Exibe detalhes de um óculos específico"""
    resposta = Oculos.buscarPorId(id)

    marca = CRUD.mostrar("Marca", "Id_Marca")
    forma = CRUD.mostrar("Forma", "Id_Forma")
    material = CRUD.mostrar("Material", "Id_Material")

    if resposta[1] != 200:
        return f"Erro: {resposta[0].get_json().get('mensagem') or 'Não encontrado'}", resposta[1]

    dados = resposta[0].get_json()
    return render_template('item_id.html', oculos_id=dados, marcas=marca, formas=forma, materiais=material)

@oculos_bp.route('/oculos/delete/<id>', methods=['DELETE'])
@login_required
def deletar_oculos(id):
    """Deleta um óculos (apenas para admins)"""
    # Verifica se é admin
    if not current_user.is_adm:
        return jsonify({"erro": "Acesso negado. Apenas administradores podem deletar óculos."}), 403
    
    return Oculos.deletar(id)
