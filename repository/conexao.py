import sqlite3



def conexaoFactory():
    try:
        nova_conexao = sqlite3.connect("database/data.db", check_same_thread=False)
        return nova_conexao
    except sqlite3.DatabaseError:
        print(f"Não foi possivel se conectar ao banco")
        return None
