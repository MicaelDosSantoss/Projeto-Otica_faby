from uuid import uuid4
from flask import jsonify
import mysql.connector
from Database.database import conexao

class Carrinho:
    @staticmethod
    def criar_carrinho(usuario_fk):
        try:
            conn = conexao()
            if conn is None:
                return None, "Falha na conexão com o banco"

            cursor = conn.cursor()
            query = "INSERT INTO Carrinho (Usuario_FK) VALUES (%s)"
            cursor.execute(query, (usuario_fk,))
            conn.commit()
            carrinho_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return carrinho_id, None
        except mysql.connector.Error as err:
            return None, f"Erro ao criar carrinho: {err}"

    @staticmethod
    def buscar_carrinho_por_usuario(usuario_fk):
        try:
            conn = conexao()
            if conn is None:
                return None, "Falha na conexão com o banco"

            cursor = conn.cursor(dictionary=True)
            query = "SELECT Id_Carrinho FROM Carrinho WHERE Usuario_FK = %s"
            cursor.execute(query, (usuario_fk,))
            carrinho = cursor.fetchone()
            cursor.close()
            conn.close()
            return carrinho['Id_Carrinho'] if carrinho else None, None
        except mysql.connector.Error as err:
            return None, f"Erro ao buscar carrinho: {err}"

    @staticmethod
    def adicionar_item(carrinho_fk, oculos_fk, quantidade):
        try:
            conn = conexao()
            if conn is None:
                return jsonify({"erro": "Falha na conexão com o banco"}), 500

            cursor = conn.cursor()
            
            # Verificar se o item já existe no carrinho
            query_check = "SELECT Id_Item, Quantidade FROM Itens_Carrinho WHERE Carrinho_FK = %s AND Oculos_FK = %s"
            cursor.execute(query_check, (carrinho_fk, oculos_fk))
            item_existente = cursor.fetchone()
            
            if item_existente:
                # Atualizar quantidade
                nova_quantidade = item_existente[1] + quantidade
                query_update = "UPDATE Itens_Carrinho SET Quantidade = %s WHERE Id_Item = %s"
                cursor.execute(query_update, (nova_quantidade, item_existente[0]))
                mensagem = "Quantidade do item atualizada no carrinho."
            else:
                # Inserir novo item
                query_insert = "INSERT INTO Itens_Carrinho (Carrinho_FK, Oculos_FK, Quantidade) VALUES (%s, %s, %s)"
                cursor.execute(query_insert, (carrinho_fk, oculos_fk, quantidade))
                mensagem = "Item adicionado ao carrinho."
                
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"mensagem": mensagem}), 200
        except mysql.connector.Error as err:
            return jsonify({'erro': f'Erro ao adicionar item ao carrinho: {err}'}), 500

    @staticmethod
    def mostrar_itens(carrinho_fk):
        try:
            conn = conexao()
            if conn is None:
                return None, "Falha na conexão com o banco"

            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    IC.Id_Item, IC.Quantidade,
                    O.Id_Oculos, O.Modelo, O.Valor, O.Imagem
                FROM Itens_Carrinho IC
                JOIN Oculos O ON IC.Oculos_FK = O.Id_Oculos
                WHERE IC.Carrinho_FK = %s
            """
            cursor.execute(query, (carrinho_fk,))
            itens = cursor.fetchall()
            cursor.close()
            conn.close()
            return itens, None
        except mysql.connector.Error as err:
            return None, f"Erro ao buscar itens do carrinho: {err}"

    @staticmethod
    def atualizar_quantidade_item(item_id, quantidade):
        try:
            conn = conexao()
            if conn is None:
                return jsonify({"erro": "Falha na conexão com o banco"}), 500

            cursor = conn.cursor()
            query = "UPDATE Itens_Carrinho SET Quantidade = %s WHERE Id_Item = %s"
            cursor.execute(query, (quantidade, item_id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"mensagem": "Quantidade atualizada com sucesso."}), 200
        except mysql.connector.Error as err:
            return jsonify({"erro": f"Erro ao atualizar quantidade: {err}"}), 500

    @staticmethod
    def remover_item(item_id):
        try:
            conn = conexao()
            if conn is None:
                return jsonify({"erro": "Falha na conexão com o banco"}), 500

            cursor = conn.cursor()
            query = "DELETE FROM Itens_Carrinho WHERE Id_Item = %s"
            cursor.execute(query, (item_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"mensagem": "Item removido do carrinho."}), 200
        except mysql.connector.Error as err:
            return jsonify({"erro": f"Erro ao remover item: {err}"}), 500

    @staticmethod
    def limpar_carrinho(carrinho_id):
        try:
            conn = conexao()
            if conn is None:
                return jsonify({"erro": "Falha na conexão com o banco"}), 500

            cursor = conn.cursor()
            query = "DELETE FROM Itens_Carrinho WHERE Carrinho_FK = %s"
            cursor.execute(query, (carrinho_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"mensagem": "Carrinho limpo com sucesso."}), 200
        except mysql.connector.Error as err:
            return jsonify({"erro": f"Erro ao limpar carrinho: {err}"}), 500

class Pagamento:
    @staticmethod
    def salvar_endereco(pagamento_id, endereco_string):
        """Salva a string de endereço na coluna Endereco_Entrega da tabela Pagamento."""
        try:
            conn = conexao()
            if conn is None:
                return False, "Falha na conexão com o banco"

            cursor = conn.cursor()
            query = "UPDATE Pagamento SET Endereco_Entrega = %s WHERE Id_Pagamento = %s"
            cursor.execute(query, (endereco_string, pagamento_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True, None
        except mysql.connector.Error as err:
            return False, f"Erro ao salvar endereço: {err}"

    @staticmethod
    def registrar_pagamento(usuario_fk, metodo, valor_total, status, nome_cartao=None, ultimos_4=None, parcelas=None, bandeira=None):
        """Registra o pagamento inicial, sem o endereço."""
        try:
            conn = conexao()
            if conn is None:
                return jsonify({"erro": "Falha na conexão com o banco"}), 500

            cursor = conn.cursor()
            # Note que a coluna Endereco_Entrega não está aqui, pois será atualizada depois
            query = """
                INSERT INTO Pagamento (
                    Id_Usuario_FK, Metodo, Valor_Total, Status, 
                    Nome_Cartao, Ultimos_4, Parcelas, Bandeira
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                usuario_fk, metodo, valor_total, status,
                nome_cartao, ultimos_4, parcelas, bandeira
            )

            cursor.execute(query, valores)
            conn.commit()
            pagamento_id = cursor.lastrowid
            cursor.close()
            conn.close()
            # Retorna o ID do pagamento para que o endereço possa ser salvo
            return jsonify({"mensagem": "Pagamento registrado com sucesso!", "Id_Pagamento": pagamento_id}), 201

        except mysql.connector.Error as err:
            return jsonify({'erro': f'Erro ao registrar pagamento: {err}'}), 500
