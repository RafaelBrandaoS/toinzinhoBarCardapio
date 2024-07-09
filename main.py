from flask import Flask
from python.conexao import criar_conexao, fechar_conexao
from routes.home import home_route
from routes.admin import admin_route

def main():
    con = criar_conexao('localhost', 'root', '', 'produtos')
    
    app = Flask(__name__)
    
    app.register_blueprint(home_route)
    app.register_blueprint(admin_route, url_prefix='/admin')
    
    app.run(debug=True)
    
    fechar_conexao(con)

if __name__ == '__main__':
    main()