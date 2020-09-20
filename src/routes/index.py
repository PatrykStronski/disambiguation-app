from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    @app.route('/disambiguate')
    def disambiguate():
        return "disambiguated"
    return app
create_app()
