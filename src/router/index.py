from flask import Flask, request
from disambiguation.disambiguation import Disambiguation

app = Flask(__name__, instance_relative_config=True)
Disamb = Disambiguation()

@app.route('/disambiguate', methods=['GET'])
def disambiguate():
    text = request.args.get('text')
    #lang = request.args.get('lang')
    lang = "english"
    return Disamb.disambiguate_text(text, lang)

def create_app():
    app.run(debug=True)