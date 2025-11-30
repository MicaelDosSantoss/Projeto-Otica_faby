from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from Models.Vendas import Carrinho, Pagamento
from Models.Oculos import Oculos
from Models.CRUD import CRUD

venda_bp = Blueprint('venda', __name__)

@venda_bp.route('/carrinho/adicionar', methods=['POST'])
@login_required
def adicionar_ao_carrinho():
    """Adiciona um item ao carrinho do usuário logado"""
    # Verifica se é cliente (não admin)
    if current_user.is_adm:
        return jsonify({"erro": "Administradores não podem adicionar itens ao carrinho"}), 403
    
    # 1. Obter dados do POST
    data = request.get_json()
    oculos_id = data.get('oculos_id')
    quantidade = data.get('quantidade', 1)
    
    if not oculos_id:
        return jsonify({"erro": "ID do óculos não fornecido"}), 400
    
    # 2. Buscar Carrinho para o usuário logado
    carrinho_id, erro_carrinho = Carrinho.buscar_carrinho_por_usuario(current_user.ID_Usuario)
    
    if erro_carrinho:
        return jsonify({"erro": erro_carrinho}), 500
        
    if not carrinho_id:
        # Se não existir carrinho, cria um (não deveria acontecer pois é criado no cadastro)
        carrinho_id, erro_carrinho = Carrinho.criar_carrinho(current_user.ID_Usuario)
        if erro_carrinho:
            return jsonify({"erro": erro_carrinho}), 500
            
    # 3. Adicionar Item ao Carrinho
    return Carrinho.adicionar_item(carrinho_id, oculos_id, quantidade)

@venda_bp.route('/carrinho', methods=['GET'])
@login_required
def ver_carrinho():
    """Exibe o carrinho do usuário logado"""
    # Verifica se é cliente (não admin)
    if current_user.is_adm:
        return jsonify({"erro": "Administradores não possuem carrinho"}), 403
    
    # 1. Buscar Carrinho do usuário
    carrinho_id, erro_carrinho = Carrinho.buscar_carrinho_por_usuario(current_user.ID_Usuario)
    
    if erro_carrinho:
        return jsonify({"erro": erro_carrinho}), 500
        
    if not carrinho_id:
        return render_template("carrinho.html", itens=[], total=0)
        
    # 2. Mostrar Itens do Carrinho
    itens, erro_itens = Carrinho.mostrar_itens(carrinho_id)
    
    if erro_itens:
        return jsonify({"erro": erro_itens}), 500
        
    total = sum(item['Valor'] * item['Quantidade'] for item in itens)
    
    return render_template("carrinho.html", itens=itens, total=total)

@venda_bp.route('/carrinho/atualizar', methods=['POST'])
@login_required
def atualizar_quantidade():
    """Atualiza a quantidade de um item no carrinho"""
    if current_user.is_adm:
        return jsonify({"erro": "Administradores não possuem carrinho"}), 403
    
    data = request.get_json()
    item_id = data.get('item_id')
    quantidade = data.get('quantidade')
    
    if not item_id or not quantidade:
        return jsonify({"erro": "Dados incompletos"}), 400
    
    return Carrinho.atualizar_quantidade_item(item_id, quantidade)

@venda_bp.route('/carrinho/remover', methods=['POST'])
@login_required
def remover_item():
    """Remove um item do carrinho"""
    if current_user.is_adm:
        return jsonify({"erro": "Administradores não possuem carrinho"}), 403
    
    data = request.get_json()
    item_id = data.get('item_id')
    
    if not item_id:
        return jsonify({"erro": "ID do item não fornecido"}), 400
    
    return Carrinho.remover_item(item_id)

@venda_bp.route('/carrinho/limpar', methods=['POST'])
@login_required
def limpar_carrinho():
    """Limpa todos os itens do carrinho"""
    if current_user.is_adm:
        return jsonify({"erro": "Administradores não possuem carrinho"}), 403
    
    carrinho_id, erro = Carrinho.buscar_carrinho_por_usuario(current_user.ID_Usuario)
    
    if erro:
        return jsonify({"erro": erro}), 500
    
    if not carrinho_id:
        return jsonify({"erro": "Carrinho não encontrado"}), 404
    
    return Carrinho.limpar_carrinho(carrinho_id)

@venda_bp.route('/pagamento', methods=['POST'])
@login_required
def finalizar_pagamento():
    """Finaliza o pagamento do usuário logado"""
    # Verifica se é cliente (não admin)
    if current_user.is_adm:
        return jsonify({"erro": "Administradores não podem realizar pagamentos"}), 403
    
    # 1. Obter dados do POST
    form = request.form
    metodo = form.get('Metodo')
    valor_total = form.get('Valor_Total')
    
    # Dados de cartão (não sensíveis)
    nome_cartao = form.get('Nome_Cartao')
    ultimos_4 = form.get('Ultimos_4')
    parcelas = form.get('Parcelas')
    bandeira = form.get('Bandeira')
    
    # 2. Validar dados
    if not all([metodo, valor_total]):
        return jsonify({"erro": "Dados de pagamento incompletos"}), 400
        
    # 3. Registrar Pagamento
    resp, status = Pagamento.registrar_pagamento(
        current_user.ID_Usuario, 
        metodo, 
        valor_total, 
        'Aprovado', # Simulação de status
        nome_cartao, 
        ultimos_4, 
        parcelas, 
        bandeira
    )
    
    if status != 201:
        return resp, status
        
    # 4. Salvar Endereço e Limpar Sessão
    from flask import session, flash
    pagamento_id = resp.get_json().get('Id_Pagamento')
    endereco_string = session.pop('endereco_entrega', None)
    
    if pagamento_id and endereco_string:
        sucesso, erro = Pagamento.salvar_endereco(pagamento_id, endereco_string)
        if not sucesso:
            # Logar o erro, mas não impedir o redirecionamento
            print(f"Erro ao salvar endereço para o pagamento {pagamento_id}: {erro}")
            
    # 5. Redirecionar para a Home
    flash('Pagamento realizado com sucesso! Seu pedido será enviado para o endereço cadastrado.', 'success')
    return redirect(url_for('oculos.home'))

@venda_bp.route('/<id>/pag', methods=['GET'])
@login_required
def pagamento_view(id):
    """Exibe a tela de pagamento"""
    # Verifica se é cliente (não admin)
    if current_user.is_adm:
        return jsonify({"erro": "Administradores não podem acessar a tela de pagamento"}), 403
    
    # Redireciona para a tela de endereço se o endereço ainda não estiver na sessão
    from flask import session
    if 'endereco_entrega' not in session:
        return redirect(url_for('venda.endereco_view', id_compra=id))

    # Se o ID for "carrinho", exibe a tela de pagamento do carrinho
    if id == 'carrinho':
        carrinho_id, _ = Carrinho.buscar_carrinho_por_usuario(current_user.ID_Usuario)
        if not carrinho_id:
            return redirect(url_for('venda.ver_carrinho'))
            
        itens, _ = Carrinho.mostrar_itens(carrinho_id)
        total = sum(item['Valor'] * item['Quantidade'] for item in itens)
        
        return render_template("pagamento.html", itens=itens, total=total)
        
    # Se for um ID de óculos, simula a compra direta de 1 unidade
    oculos_resp, status = Oculos.buscarPorId(id)
    if status != 200:
        return "Óculos não encontrado", 404
        
    oculos = oculos_resp.get_json()
    total = oculos['Valor']
    
    return render_template("pagamento.html", itens=[oculos], total=total)
# --- Rotas de Endereço ---

@venda_bp.route('/endereco/<id_compra>', methods=['GET'])
@login_required
def endereco_view(id_compra):
    """Exibe a tela de cadastro de endereço."""
    return render_template("endereco.html", id_compra=id_compra)

@venda_bp.route('/endereco/<id_compra>', methods=['POST'])
@login_required
def salvar_endereco(id_compra):
    """Salva o endereço e redireciona para o pagamento."""
    form = request.form
    
    # 1. Concatena o endereço em uma única string
    endereco_string = f"{current_user.Nome} — {form['Rua']}, {form['Numero']} — {form['Bairro']} — {form['Cidade']} — {form['Estado']} — {form['CEP']}"
    if form.get('Complemento'):
        endereco_string += f" — {form['Complemento']}"

    # 2. Armazena o endereço na sessão para usar após o pagamento
    from flask import session
    session['endereco_entrega'] = endereco_string

    # 3. Redireciona para a tela de pagamento, passando o ID da compra
    return redirect(url_for('venda.pagamento_view', id=id_compra))
