# coding: utf-8
from flask import Flask, render_template, request, jsonify, Response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm  #form作成用
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import json

from network import TagNetwork #個人作成

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret' # CSRF対策でtokenの生成に必要
bootstrap = Bootstrap(app)


@app.route('/')
def network():

    return render_template('network.html')

@app.route('/getnetwork', methods=["GET", "POST"])
def getnetwork():
    n = TagNetwork()
    n.get_tags()
    n.make_network()
    n.make_json()
    return Response(json.dumps(n.network_json))

@app.route('/getjson', methods=["GET", "POST"])
def getjson():

    return render_template('network.html')
if __name__ == "__main__":
    app.run(debug=True)
