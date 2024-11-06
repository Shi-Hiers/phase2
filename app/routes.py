from flask import render_template
from . import app

from flask import redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('sales.show_sales'))
