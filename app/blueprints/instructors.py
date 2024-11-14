import pymysql
from pymysql.cursors import DictCursor
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.db_connect import get_db  # Adjust based on your project structure

instructors_bp = Blueprint('instructors', __name__)

# Route to display all instructors
@instructors_bp.route('/instructors')
def display_instructors():
    connection = get_db()
    cursor = connection.cursor(DictCursor)
    cursor.execute("SELECT * FROM instructors")
    instructors = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('instructors.html', instructors=instructors)

# Route to add a new instructor
@instructors_bp.route('/instructors/add', methods=['GET', 'POST'])
def add_instructor():
    if request.method == 'POST':
        name = request.form['name']
        specialty = request.form['specialty']
        bio = request.form['bio']
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO instructors (name, specialty, bio) VALUES (%s, %s, %s)", (name, specialty, bio))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Instructor added successfully!')
        return redirect(url_for('instructors.display_instructors'))
    return render_template('add_instructor.html')

# Route to edit an existing instructor
@instructors_bp.route('/instructors/edit/<int:instructor_id>', methods=['GET', 'POST'])
def edit_instructor(instructor_id):
    connection = get_db()
    cursor = connection.cursor(DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        specialty = request.form['specialty']
        bio = request.form['bio']
        cursor.execute("UPDATE instructors SET name = %s, specialty = %s, bio = %s WHERE instructor_id = %s",
                       (name, specialty, bio, instructor_id))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Instructor updated successfully!')
        return redirect(url_for('instructors.display_instructors'))
    cursor.execute("SELECT * FROM instructors WHERE instructor_id = %s", (instructor_id,))
    instructor = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_instructor.html', instructor=instructor)

# Route to delete an instructor
@instructors_bp.route('/instructors/delete/<int:instructor_id>', methods=['POST'])
def delete_instructor(instructor_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM instructors WHERE instructor_id = %s", (instructor_id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash('Instructor deleted successfully!')
    return redirect(url_for('instructors.display_instructors'))
