from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

regions_bp = Blueprint('regions', __name__)

@regions_bp.route('/regions', methods=['GET'])
def view_regions():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM regions")
    regions = cursor.fetchall()  # This will now return dictionaries
    connection.close()
    return render_template('regions.html', regions=regions)

@regions_bp.route('/add_region', methods=['GET', 'POST'])
def add_region():
    if request.method == 'POST':
        region_name = request.form['region_name']
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO regions (region_name) VALUES (%s)", (region_name,))
        connection.commit()
        connection.close()
        flash('Region added successfully!')
        return redirect(url_for('regions.view_regions'))
    return render_template('add_region.html')

@regions_bp.route('/edit_region/<int:region_id>', methods=['GET', 'POST'])
def edit_region(region_id):
    connection = get_db()
    cursor = connection.cursor()
    if request.method == 'POST':
        region_name = request.form['region_name']
        cursor.execute("UPDATE regions SET region_name = %s WHERE region_id = %s", (region_name, region_id))
        connection.commit()
        flash('Region updated successfully!')
        connection.close()
        return redirect(url_for('regions.view_regions'))
    else:
        cursor.execute("SELECT * FROM regions WHERE region_id = %s", (region_id,))
        region = cursor.fetchone()  # This will return a dictionary
        print(region)  # Debugging: print the region to ensure it's a dictionary
        connection.close()
        return render_template('edit_region.html', region=region)

@regions_bp.route('/delete_region/<int:region_id>', methods=['POST'])
def delete_region(region_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM regions WHERE region_id = %s", (region_id,))
    connection.commit()
    connection.close()
    flash('Region deleted successfully!')
    return redirect(url_for('regions.view_regions'))

