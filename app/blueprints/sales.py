import matplotlib.pyplot as plt
import io
import base64
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import pandas as pd
from app.functions import calculate_total_sales_by_region, analyze_monthly_sales_trends, get_top_performing_region, create_total_sales_chart

sales = Blueprint('sales', __name__)

@sales.route('/show_sales')
def show_sales():
    connection = get_db()
    query = """
        SELECT sd.sales_data_id, sd.monthly_amount, sd.date, sd.region, r.region_name
        FROM sales_data sd
        JOIN regions r ON sd.region = r.region_id
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    except Exception as e:
        flash("An error occurred while accessing the database.", "danger")
        print(e)
        return redirect(url_for('sales.show_sales'))

    # Convert the result to a DataFrame
    df = pd.DataFrame(result, columns=['sales_data_id', 'monthly_amount', 'date', 'region', 'region_name'])

    # Add Actions column for edit and delete
    df['Actions'] = df['sales_data_id'].apply(lambda id:
        f'<a href="{url_for("sales.edit_sales_data", sales_data_id=id)}" class="btn btn-sm btn-info">Edit</a> '
        f'<form action="{url_for("sales.delete_sales_data", sales_data_id=id)}" method="post" style="display:inline;">'
        f'<button type="submit" class="btn btn-sm btn-danger">Delete</button></form>'
    )

    # Generate HTML table with region_name as a column
    table_html = df.to_html(classes='dataframe table table-striped table-bordered', index=False, escape=False)

    # Only include the rows in the table (no <thead>, <tbody>, etc.)
    rows_only = table_html.split('<tbody>')[1].split('</tbody>')[0]

    return render_template("sales_data.html", table=rows_only)



@sales.route('/add_sales_data', methods=['GET', 'POST'])
def add_sales_data():
    if request.method == 'POST':
        monthly_amount = request.form['monthly_amount']
        date = request.form['date']
        region_id = request.form['region']

        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO sales_data (monthly_amount, date, region) VALUES (%s, %s, %s)",
                       (monthly_amount, date, region_id))
        connection.commit()
        connection.close()

        flash('Sales data added successfully!')
        return redirect(url_for('sales.show_sales'))

    # Fetch the regions to display in the dropdown
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM regions")
    regions = cursor.fetchall()  # Fetch all available regions
    connection.close()

    return render_template('add_sales_data.html', regions=regions)

@sales.route('/edit_sales_data/<int:sales_data_id>', methods=['GET', 'POST'])
def edit_sales_data(sales_data_id):
    connection = get_db()
    if request.method == 'POST':
        monthly_amount = request.form['monthly_amount']
        date = request.form['date']
        region = request.form['region']

        query = "UPDATE sales_data SET monthly_amount = %s, date = %s, region = %s WHERE sales_data_id = %s"
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (monthly_amount, date, region, sales_data_id))
            connection.commit()
            flash("Sales data updated successfully!", "success")
        except Exception as e:
            flash("An error occurred while updating sales data.", "danger")
            print(e)
        return redirect(url_for('sales.show_sales'))

    query = "SELECT * FROM sales_data WHERE sales_data_id = %s"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (sales_data_id,))
            sales_data = cursor.fetchone()
    except Exception as e:
        flash("An error occurred while accessing the sales data.", "danger")
        print(e)
        return redirect(url_for('sales.show_sales'))

    return render_template("edit_sales_data.html", sales_data=sales_data)

@sales.route('/delete_sales_data/<int:sales_data_id>', methods=['POST'])
def delete_sales_data(sales_data_id):
    connection = get_db()
    query = "DELETE FROM sales_data WHERE sales_data_id = %s"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (sales_data_id,))
        connection.commit()
        flash("Sales data deleted successfully!", "success")
    except Exception as e:
        flash("An error occurred while deleting sales data.", "danger")
        print(e)
    return redirect(url_for('sales.show_sales'))


@sales.route('/reports')
def reports():
    connection = get_db()
    query = """
        SELECT sd.sales_data_id, sd.monthly_amount, sd.date, sd.region, r.region_name
        FROM sales_data sd
        JOIN regions r ON sd.region = r.region_id
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    except Exception as e:
        flash("An error occurred while accessing the database.", "danger")
        print(e)
        return redirect(url_for('sales.show_sales'))

    # Convert the result to a DataFrame
    df = pd.DataFrame(result, columns=['sales_data_id', 'monthly_amount', 'date', 'region', 'region_name'])

    # Call functions from functions.py here to generate analysis
    total_sales_by_region = calculate_total_sales_by_region(df)
    monthly_trends = analyze_monthly_sales_trends(df)
    top_region = get_top_performing_region(df)

    # Pass the correct variable name to the template
    return render_template("reports.html", total_sales_by_region=total_sales_by_region, trends=monthly_trends,
                           top_region=top_region)


@sales.route('/visualization')
def visualization():
    connection = get_db()
    query = """
        SELECT sd.sales_data_id, sd.monthly_amount, sd.date, sd.region, r.region_name
        FROM sales_data sd
        JOIN regions r ON sd.region = r.region_id
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    except Exception as e:
        flash("An error occurred while accessing the database.", "danger")
        print(e)
        return redirect(url_for('sales.show_sales'))

    df = pd.DataFrame(result, columns=['sales_data_id', 'monthly_amount', 'date', 'region', 'region_name'])

    # Extract total sales by region for visualization
    total_sales_by_region = calculate_total_sales_by_region(df)
    region_labels = total_sales_by_region['region_name'].tolist()  # Use 'region_name' here
    region_data = total_sales_by_region['monthly_amount'].tolist()

    # Extract monthly sales trends for visualization
    monthly_trends = analyze_monthly_sales_trends(df)
    monthly_labels = monthly_trends['date'].dt.strftime('%Y-%m').tolist()
    monthly_data = monthly_trends['monthly_amount'].tolist()

    # Pass all required data to the template
    return render_template("visualization.html",
                           region_labels=region_labels,
                           region_data=region_data,
                           monthly_labels=monthly_labels,
                           monthly_data=monthly_data)

