
from flask import render_template

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')
