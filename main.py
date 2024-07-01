from flask import Flask, url_for, render_template
from python.conexao import criar_conexao, fechar_conexao


def lista_produtos(con):
    cursor = con.cursor()
    sql = 'SELECT * FROM produtos order by sessao, nome'
    cursor.execute(sql)
    produtos = cursor.fetchall()
    cursor.close()
    con.commit()    
    return produtos


def lista_sessoes(con):
    produtos = lista_produtos(con)
    sessao = []
    for produto in produtos:
        if produto[3] not in sessao:
            sessao.append(produto[3])
    return sessao


def site(con):
    app = Flask(__name__)
    
    @app.route('/')
    def produtos():
        sessao = lista_sessoes(con)
        produtos = lista_produtos(con)
        return render_template('index.html', sessao=sessao, produtos=produtos)

    app.run(debug=True)

def main():
    con = criar_conexao('localhost', 'root', '', 'produtos')
    
    site(con)
    
    fechar_conexao(con)

if __name__ == '__main__':
    main()