from uuid import uuid4
from Models.CRUD import CRUD
from flask import jsonify
import mysql.connector
from Database.database import conexao

class Oculos(CRUD):

    def __init__(self, Modelo=None, ID_Oculos=None, Forma_FK=None, Material_FK=None, Marca_FK=None,
                 Valor=None, Quantidade=None, Descricao=None, Sobre_Produto=None, Imagem=None):
        # O ID_Oculos no novo esquema é VARCHAR(50) e é a chave primária.
        self.ID_Oculos = ID_Oculos if ID_Oculos else str(uuid4())
        self.Modelo = Modelo
        self.Forma_FK = Forma_FK
        self.Material_FK = Material_FK
        self.Marca_FK = Marca_FK
        self.Valor = Valor
        self.Quantidade = Quantidade
        self.Descricao = Descricao
        self.Sobre_Produto = Sobre_Produto
        self.Imagem = Imagem # Campo Imagem reintroduzido

    def salvar(self):
        try:
            # Validações básicas
            if not all([self.Modelo, self.Forma_FK, self.Material_FK, self.Marca_FK, self.Valor, self.Quantidade]):
                print("Campos obrigatórios (Modelo, Forma_FK, Material_FK, Marca_FK, Valor, Quantidade) não fornecidos.")
                return

            conn = conexao()
            if conn is None:
                print("Falha na conexão.")
                return

            cursor = conn.cursor()

            query = """
                INSERT INTO Oculos (
                    Id_Oculos,
                    Modelo,
                    Forma_FK,
                    Material_FK,
                    Marca_FK,
                    Valor,
                    Quantidade,
                    Descricao,
                    Sobre_Produto,
                    Imagem
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                self.ID_Oculos,
                self.Modelo,
                self.Forma_FK,
                self.Material_FK,
                self.Marca_FK,
                self.Valor,
                self.Quantidade,
                self.Descricao,
                self.Sobre_Produto,
                self.Imagem # Imagem adicionada ao INSERT
            )

            cursor.execute(query, valores)
            conn.commit()
            cursor.close()
            conn.close()
            print("Registro inserido com sucesso.")

        except mysql.connector.Error as err:
            print(f"Erro ao registrar: {err}")

    @staticmethod
    def mostrarTudo():
        try:
            conn = conexao()
            if conn is None:
                return jsonify({'erro': 'Falha na conexão com o banco'}), 500

            cursor = conn.cursor(dictionary=True) # Usar dictionary=True para acessar por nome
            
            # Query com JOINs para obter os nomes de Forma, Material e Marca
            query = """
                SELECT 
                    O.Id_Oculos, O.Modelo, O.Valor, O.Quantidade, O.Descricao, O.Sobre_Produto, O.Imagem,
                    F.Id_Forma, F.Nome AS Nome_Forma,
                    M.Id_Material, M.Nome AS Nome_Material,
                    R.Id_Marca, R.Nome AS Nome_Marca
                FROM Oculos O
                JOIN Forma F ON O.Forma_FK = F.Id_Forma
                JOIN Material M ON O.Material_FK = M.Id_Material
                JOIN Marca R ON O.Marca_FK = R.Id_Marca
            """
            cursor.execute(query)
            resultados = cursor.fetchall()

            lista = []
            for row in resultados:
                lista.append({
                    "Id_Oculos": row['Id_Oculos'],
                    "Modelo": row['Modelo'],
                    "Valor": float(row['Valor']) if row['Valor'] else None,
                    "Quantidade": row['Quantidade'],
                    "Descricao": row['Descricao'],
                    "Sobre_Produto": row['Sobre_Produto'],
                    "Imagem": row['Imagem'], # Imagem adicionada ao retorno
                    "Forma_FK": row['Id_Forma'],
                    "Nome_Forma": row['Nome_Forma'],
                    "Material_FK": row['Id_Material'],
                    "Nome_Material": row['Nome_Material'],
                    "Marca_FK": row['Id_Marca'],
                    "Nome_Marca": row['Nome_Marca'],
                })

            cursor.close()
            conn.close()

            if not lista:
                return jsonify({"mensagem": "Nenhum óculos encontrado."}), 404

            return lista

        except mysql.connector.Error as err:
            return jsonify({'erro': f'Erro ao buscar óculos: {err}'}), 500

    @staticmethod
    def buscarPorId(id):
        try:
            conn = conexao()
            if conn is None:
                return jsonify({'erro': 'Falha na conexão com o banco'}), 500

            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT 
                    O.Id_Oculos, O.Modelo, O.Valor, O.Quantidade, O.Descricao, O.Sobre_Produto, O.Imagem,
                    F.Id_Forma, F.Nome AS Nome_Forma,
                    M.Id_Material, M.Nome AS Nome_Material,
                    R.Id_Marca, R.Nome AS Nome_Marca
                FROM Oculos O
                JOIN Forma F ON O.Forma_FK = F.Id_Forma
                JOIN Material M ON O.Material_FK = M.Id_Material
                JOIN Marca R ON O.Marca_FK = R.Id_Marca
                WHERE O.Id_Oculos = %s
            """
            cursor.execute(query, (id.strip(),))
            row = cursor.fetchone()

            cursor.close()
            conn.close()

            if not row:
                return jsonify({'mensagem': 'Óculos não encontrado!'}), 404

            resultado = {
                "Id_Oculos": row['Id_Oculos'],
                "Modelo": row['Modelo'],
                "Valor": float(row['Valor']) if row['Valor'] else None,
                "Quantidade": row['Quantidade'],
                "Descricao": row['Descricao'],
                "Sobre_Produto": row['Sobre_Produto'],
                "Imagem": row['Imagem'], # Imagem adicionada ao retorno
                "Forma_FK": row['Id_Forma'],
                "Nome_Forma": row['Nome_Forma'],
                "Material_FK": row['Id_Material'],
                "Nome_Material": row['Nome_Material'],
                "Marca_FK": row['Id_Marca'],
                "Nome_Marca": row['Nome_Marca'],
            }

            return jsonify(resultado), 200

        except mysql.connector.Error as err:
            return jsonify({'erro': f'Erro ao buscar óculos por ID: {err}'}), 500

    @staticmethod
    def atualizar(id, body_response):
        try:
            conn = conexao()
            if conn is None:
                return jsonify({'erro': 'Falha na conexão com o banco'}), 500

            cursor = conn.cursor(dictionary=True)

            # Buscar os dados atuais
            cursor.execute("SELECT * FROM Oculos WHERE Id_Oculos = %s", (id,))
            atual = cursor.fetchone()

            if not atual:
                return jsonify({'mensagem': 'Óculos não encontrado!'}), 404

            # Campos do novo esquema
            campos = [
                "Modelo", "Forma_FK", "Material_FK", "Marca_FK", "Valor",
                "Quantidade", "Descricao", "Sobre_Produto", "Imagem" # Imagem adicionada aos campos
            ]
            
            # Cria a lista de campos a serem atualizados e seus valores
            set_clauses = []
            valores = []
            
            for campo in campos:
                # Usa o valor do body_response se existir, senão usa o valor atual do banco
                novo_valor = body_response.get(campo, atual.get(campo))
                if novo_valor is not None:
                    set_clauses.append(f"{campo} = %s")
                    valores.append(novo_valor)

            if not set_clauses:
                return jsonify({'mensagem': 'Nenhum campo para atualizar fornecido.'}), 400

            query = f"UPDATE Oculos SET {', '.join(set_clauses)} WHERE Id_Oculos = %s"
            valores.append(id)

            cursor.execute(query, tuple(valores))
            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({'mensagem': 'Óculos atualizado com sucesso!'}), 200

        except mysql.connector.Error as err:
            return jsonify({'erro': f'Erro ao atualizar óculos: {err}'}), 500

    @staticmethod
    def deletar(id):
        return CRUD.deletar("Oculos", "Id_Oculos", id)
