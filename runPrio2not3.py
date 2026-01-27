# ===== app.py (Main Flask Application) =====
"""
Flask App with Blueprints and Popup Dialog for Table Editing
"""

from flask import Flask, render_template
import os
from tracker.ToDo.ToDo import ToDo
from tracker.ToDo.items import bp

ext = ToDo()

app = Flask(__name__)
app.secret_key = '685ced89519dfc2bd879c3dcbeefa36fc50172a4eda8f914b65dfc6cf9a442d4'

# Register blueprints
app.register_blueprint(bp, url_prefix='/items')

@app.route('/')
def index():
    return render_template('Prio2not3.html')

app.run(debug=True, port=8001)

