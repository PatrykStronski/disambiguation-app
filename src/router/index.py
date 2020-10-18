from flask import Flask, request
from disambiguation.disambiguation import Disambiguation

app = Flask(__name__, instance_relative_config=True)
    
@app.route('/disambiguate', methods=['GET'])
def disambiguate():
    text = request.args.get('text')
    disambiguate = Disambiguation(text)

def create_app():
    app.run(debug=True)

create_app()
