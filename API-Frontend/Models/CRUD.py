
import mysql.connector
from flask import Flask, jsonify

from Database.database import conexao
from uuid import uuid4

class CRUD:
    def __init__(self, Nome = None):
        self.Id = str(uuid4())
        self.Nome = Nome

    def registar(self, table_name, ID):
        try:

            if self.Nome is None:
                print("Nome não fornecido.")
                return

            conn = conexao()
            if conn is None:
                print("Falha na conexão.")
                return

            cursor = conn.cursor()

            query = f"INSERT INTO {table_name} ({ID}, Nome) VALUES (%s, %s)"
            cursor.execute(query, (str(uuid4()),self.Nome))

            conn.commit()
            cursor.close()
            conn.close()
            print("Registro inserido com sucesso.")

        except mysql.connector.Error as err:
            print(f"Erro ao registrar: {err}")

    @staticmethod
    def mostrar(table_name, ID):
        try:
            conn = conexao()

            if conn is None:
                print("Falha na conexão.")
                return None

            cursor = conn.cursor()

            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)

            selects = cursor.fetchall()

            lista_selects = []

            for m in selects:
                lista_selects.append({
                    ID: m[0],
                    'Nome': m[1]
                })

            cursor.close()
            conn.close()

            return lista_selects

        except mysql.connector.Error as err:
            print(f"Erro ao registrar: {err}")
            return None

    @staticmethod
    def buscarId(table_name, ID, ID_value):
        try:
            conn = conexao()
            if conn is None:
                print("Falha na conexão.")
                return jsonify({'mensagem': 'Erro na conexão com o banco'}), 500


            cursor = conn.cursor()
            query = f"SELECT * FROM {table_name} WHERE {ID} = %s"
            print(f"Executando: {query} com valor: {ID_value.strip()}")  # Debug
            cursor.execute(query, (ID_value.strip(),))
            propriedades = cursor.fetchone()
            print(f"Resultado da consulta: {propriedades}")  # Debug

            if propriedades:
                return jsonify({
                    "ID": propriedades[0],
                    "Nome": propriedades[1]
                }), 200
            else:
                return jsonify({'mensagem': 'Item não encontrado!'}), 404

        except mysql.connector.Error as err:
            print(f"Erro em buscar marca: {err}")
            return jsonify({'mensagem': 'Erro interno no servidor'}), 500

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    @staticmethod
    def atualizar(table_name, ID, ID_value, body_response):
        try:
            conn = conexao()
            if conn is None:
                print("Falha na conexão.")
                return jsonify({'error': 'Falha na conexão com o banco'}), 500

            cursor = conn.cursor()
            "UPDATE marca SET Nome = %s WHERE ID_Marca = %s"
            query = f"UPDATE { table_name } SET Nome = %s WHERE {ID} = %s"
            cursor.execute(query, (body_response,ID_value.strip(),))

            if cursor.rowcount == 0:
                return jsonify({'mensagem': 'Item não encontrada!'}), 404

            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({'mensagem': 'Atualizada com sucesso!'}), 200

        except mysql.connector.Error as err:
            return jsonify({'error': f'Erro ao atualizar marca: {err}'}), 500

    @staticmethod
    def deletar(table_name, ID, ID_value):
        try:
            conn = conexao()
            if conn is None:
                print("Falha na conexão.")
                return jsonify({'error': 'Falha na conexão com o banco'}), 500

            cursor = conn.cursor()
            query = f"DELETE FROM {table_name} WHERE {ID} = %s"
            cursor.execute(query,(ID_value.strip(),))

            if cursor.rowcount == 0:
                return jsonify({'mensagem': 'Item não encontrada!'}), 404

            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({'mensagem': 'Deletada com sucesso!'}), 200

        except mysql.connector.Error as err:
            return jsonify({'error': f'Erro ao deletar: {err}'}), 500