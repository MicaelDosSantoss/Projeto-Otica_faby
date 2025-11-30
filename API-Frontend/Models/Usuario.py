import mysql.connector
from flask import jsonify
from flask_login import UserMixin
from Database.database import conexao
import hashlib
from datetime import datetime

class Usuario(UserMixin):
    def __init__(self, Nome, Sexo, Data_Nascimento, Idade, Email, Senha, ID_Usuario=None, is_adm=False):
        self.ID_Usuario = ID_Usuario
        self.Nome = Nome
        self.Sexo = Sexo
        self.Data_Nascimento = Data_Nascimento
        self.Idade = Idade
        self.Email = Email
        self.Senha = Senha
        self.is_adm = is_adm

    def get_id(self):
        """Retorna o ID do usuário para o Flask-Login"""
        return f"{'adm' if self.is_adm else 'user'}:{self.ID_Usuario}"

    @staticmethod
    def hash_senha(senha):
        """Hash de senha usando SHA-256"""
        return hashlib.sha256(senha.encode('utf-8')).hexdigest()

    @staticmethod
    def verificar_senha(senha_fornecida, senha_hash, id_usuario, is_adm=False):
        """Verifica se a senha fornecida corresponde ao hash.
        
        Se a senha_hash não for um hash (e.g., senha em texto puro),
        verifica o texto puro e, se correto, atualiza para o hash.
        """
        
        # 1. Tenta verificar com o hash (comportamento padrão e seguro)
        if Usuario.hash_senha(senha_fornecida) == senha_hash:
            return True
            
        # 2. Se falhar, verifica se a senha_hash é um hash válido (SHA-256 tem 64 caracteres)
        # Se não for um hash (e.g., texto puro), tenta verificar o texto puro
        if len(senha_hash) != 64:
            if senha_fornecida == senha_hash:
                # Login bem-sucedido com senha em texto puro.
                # ATUALIZA a senha no banco para o hash por segurança.
                try:
                    conn = conexao()
                    if conn:
                        cursor = conn.cursor()
                        tabela = "Adm" if is_adm else "Usuario"
                        nova_senha_hash = Usuario.hash_senha(senha_fornecida)
                        query = f"UPDATE {tabela} SET Senha = %s WHERE Id_Usuario = %s"
                        cursor.execute(query, (nova_senha_hash, id_usuario))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        print(f"AVISO: Senha do {'Admin' if is_adm else 'Usuário'} {id_usuario} atualizada para hash.")
                except Exception as e:
                    print(f"ERRO ao atualizar senha para hash: {e}")
                
                return True
        
        # 3. Falha na verificação
        return False

    @staticmethod
    def calcular_idade(data_nascimento):
        """Calcula a idade a partir da data de nascimento"""
        if not data_nascimento:
            return None
        
        # Se for string, converte para date
        if isinstance(data_nascimento, str):
            try:
                data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            except ValueError:
                return None
        
        hoje = datetime.now().date()
        idade = hoje.year - data_nascimento.year
        
        # Ajusta se ainda não fez aniversário este ano
        if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1
        
        return idade

    def salvar(self, is_adm=False):
        """Salva o usuário no banco de dados"""
        tabela = "Adm" if is_adm else "Usuario"
        id_coluna = "Id_Usuario"
        
        try:
            conn = conexao()
            if conn is None:
                return jsonify({"erro": "Falha na conexão com o banco"}), 500

            cursor = conn.cursor()
            
            # Hash da senha antes de salvar
            senha_hasheada = self.hash_senha(self.Senha)

            query = f"""
                INSERT INTO {tabela} (
                    Nome, Sexo, Data_Nascimento, Idade, Email, Senha
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (
                self.Nome,
                self.Sexo,
                self.Data_Nascimento,
                self.Idade,
                self.Email,
                senha_hasheada
            )

            cursor.execute(query, valores)
            conn.commit()
            
            # Pega o ID gerado
            usuario_id = cursor.lastrowid
            
            # Se for usuário cliente, cria o carrinho automaticamente
            if not is_adm:
                cursor.execute("INSERT INTO Carrinho (Usuario_FK) VALUES (%s)", (usuario_id,))
                conn.commit()
            
            cursor.close()
            conn.close()
            
            return jsonify({
                "mensagem": f"{'Administrador' if is_adm else 'Usuário'} registrado com sucesso!",
                "ID": usuario_id
            }), 201

        except mysql.connector.IntegrityError as err:
            if 'Duplicate entry' in str(err) and 'Email' in str(err):
                return jsonify({"erro": "E-mail já cadastrado."}), 409
            return jsonify({'erro': f'Erro de integridade ao registrar: {err}'}), 500
        except mysql.connector.Error as err:
            return jsonify({'erro': f'Erro ao registrar: {err}'}), 500

    @staticmethod
    def buscar_por_email(email, is_adm=False):
        """Busca um usuário pelo email"""
        tabela = "Adm" if is_adm else "Usuario"
        
        try:
            conn = conexao()
            if conn is None:
                return None, "Falha na conexão com o banco"

            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {tabela} WHERE Email = %s"
            cursor.execute(query, (email,))
            usuario = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if usuario:
                return usuario, None
            return None, f"Usuário não encontrado."
            
        except mysql.connector.Error as err:
            return None, f"Erro ao buscar usuário por email: {err}"

    @staticmethod
    def buscar_por_id(user_id, is_adm=False):
        """Busca um usuário pelo ID"""
        tabela = "Adm" if is_adm else "Usuario"
        
        try:
            conn = conexao()
            if conn is None:
                return None

            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {tabela} WHERE Id_Usuario = %s"
            cursor.execute(query, (user_id,))
            usuario = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return usuario
            
        except mysql.connector.Error as err:
            print(f"Erro ao buscar usuário por ID: {err}")
            return None

    @staticmethod
    def login(email, senha, is_adm=False):
        """Realiza o login do usuário"""
        usuario, erro = Usuario.buscar_por_email(email, is_adm)
        
        if erro:
            return jsonify({"erro": "Usuário ou senha inválidos."}), 401
            
        if usuario and Usuario.verificar_senha(senha, usuario['Senha']):
            # Remove a senha do objeto antes de retornar
            usuario.pop('Senha')
            return jsonify({"mensagem": "Login bem-sucedido!", "usuario": usuario}), 200
        else:
            return jsonify({"erro": "Usuário ou senha inválidos."}), 401

    @staticmethod
    def criar_usuario_objeto(usuario_dict, is_adm=False):
        """Cria um objeto Usuario a partir de um dicionário"""
        return Usuario(
            Nome=usuario_dict.get('Nome'),
            Sexo=usuario_dict.get('Sexo'),
            Data_Nascimento=usuario_dict.get('Data_Nascimento'),
            Idade=usuario_dict.get('Idade'),
            Email=usuario_dict.get('Email'),
            Senha=usuario_dict.get('Senha', ''),
            ID_Usuario=usuario_dict.get('Id_Usuario'),
            is_adm=is_adm
        )
