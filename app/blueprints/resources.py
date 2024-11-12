from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/add_resource', methods=['GET', 'POST'])
def add_resource():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO resources (title, link) VALUES (%s, %s)", (title, link))
        connection.commit()
        connection.close()
        flash('Resource added successfully!')
        return redirect(url_for('resources.view_resources'))
    return render_template('add_resource.html')
