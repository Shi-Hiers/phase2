from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.functions import fetch_all, fetch_one, execute_query

instructors_bp = Blueprint('instructors', __name__)

@instructors_bp.route('/instructors')
def display_instructors():
    instructors = fetch_all("SELECT * FROM instructors")
    return render_template('instructors.html', instructors=instructors)

@instructors_bp.route('/instructors/add', methods=['GET', 'POST'])
def add_instructor():
    if request.method == 'POST':
        name = request.form['name']
        specialty = request.form['specialty']
        bio = request.form['bio']
        execute_query(
            "INSERT INTO instructors (name, specialty, bio) VALUES (%s, %s, %s)",
            (name, specialty, bio)
        )
        flash('Instructor added successfully!')
        return redirect(url_for('instructors.display_instructors'))
    return render_template('add_instructor.html')

@instructors_bp.route('/instructors/edit/<int:instructor_id>', methods=['GET', 'POST'])
def edit_instructor(instructor_id):
    if request.method == 'POST':
        name = request.form['name']
        specialty = request.form['specialty']
        bio = request.form['bio']
        execute_query(
            "UPDATE instructors SET name = %s, specialty = %s, bio = %s WHERE instructor_id = %s",
            (name, specialty, bio, instructor_id)
        )
        flash('Instructor updated successfully!')
        return redirect(url_for('instructors.display_instructors'))
    instructor = fetch_one("SELECT * FROM instructors WHERE instructor_id = %s", (instructor_id,))
    return render_template('edit_instructor.html', instructor=instructor)

@instructors_bp.route('/instructors/delete/<int:instructor_id>', methods=['POST'])
def delete_instructor(instructor_id):
    execute_query("DELETE FROM instructors WHERE instructor_id = %s", (instructor_id,))
    flash('Instructor deleted successfully!')
    return redirect(url_for('instructors.display_instructors'))
