from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

instructors_bp = Blueprint('instructors', __name__)

@instructors_bp.route('/add_instructor', methods=['GET', 'POST'])
def add_instructor():
    if request.method == 'POST':
        name = request.form['name']
        specialty = request.form['specialty']
        bio = request.form['bio']
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO instructors (name, specialty, bio) VALUES (%s, %s, %s)", (name, specialty, bio))
        connection.commit()
        connection.close()
        flash('Instructor added successfully!')
        return redirect(url_for('instructors.view_instructors'))
    return render_template('add_instructor.html')
