import mysql.connector

def conexao():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project_db_faby"
        )
        print(" Conexão bem-sucedida!")
        return conn

    except mysql.connector.Error as err:
        print(f" Erro ao conectar ao banco de dados: {err}")
        return None

# Teste direto
if __name__ == "__main__":
    conn = conexao()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")  # só pra confirmar que a conexão funciona
        for tabela in cursor.fetchall():
            print("📦 Tabela encontrada:", tabela[0])
        cursor.close()
        conn.close()
