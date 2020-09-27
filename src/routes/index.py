from flask import Flask

app = Flask(__name__, instance_relative_config=True)
    
@app.route('/disambiguate')
def disambiguate():
    return "disambiguated"

def create_app():
    app.run(debug=True)

create_app()
