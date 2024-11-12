from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/forum')
def view_forum():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM forum_posts")
    posts = cursor.fetchall()
    connection.close()
    return render_template('forum.html', posts=posts)

@forum_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO forum_posts (title, content) VALUES (%s, %s)", (title, content))
        connection.commit()
        connection.close()
        flash('Post added successfully!')
        return redirect(url_for('forum.view_forum'))
    return render_template('add_post.html')
