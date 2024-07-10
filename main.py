from flask import Flask
from routes.home import home_route
from routes.admin import admin_route

def main():
    app = Flask(__name__)
    
    app.register_blueprint(home_route)
    app.register_blueprint(admin_route, url_prefix='/admin')
    
    app.run(debug=True)
    

if __name__ == '__main__':
    main()