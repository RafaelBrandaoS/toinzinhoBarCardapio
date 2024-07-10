import mysql.connector
host = 'roundhouse.proxy.rlwy.net'
usuario = 'root'
senha = 'LVPufVkmQJJGJnxGSPJHgkWaeeMhVqPp'
porta = '43227'
banco = 'cardapio'

def criar_conexao():
    return mysql.connector.connect(host=host, user=usuario, password=senha, database=banco, port=porta)


def fechar_conexao(con):
    return con.close()
