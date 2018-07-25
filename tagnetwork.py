# coding: utf-8
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def network():
    return render_template('network.html')

if __name__ == "__main__":
    app.run(debug=True)
