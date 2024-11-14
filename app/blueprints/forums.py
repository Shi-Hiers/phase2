import pymysql
from pymysql.cursors import DictCursor
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.db_connect import get_db

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/forum')
def view_forum():
    connection = get_db()
    cursor = connection.cursor(DictCursor)  # Use DictCursor to return rows as dictionaries

    # Fetch all posts
    cursor.execute("SELECT * FROM forum_posts ORDER BY created_at DESC")
    posts = cursor.fetchall()

    # Fetch replies for each post
    for post in posts:
        cursor.execute("SELECT * FROM forum_replies WHERE post_id = %s ORDER BY created_at ASC", (post['post_id'],))
        post['replies'] = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('forum.html', posts=posts)

@forum_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        user_name = request.form['user_name']
        title = request.form['title']
        content = request.form['content']
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO forum_posts (user_name, topic, post_content, created_at) VALUES (%s, %s, %s, NOW())",
            (user_name, title, content))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Post added successfully!')
        return redirect(url_for('forum.view_forum'))
    return render_template('add_forum.html')

@forum_bp.route('/forum/add_reply/<int:post_id>', methods=['POST'])
def add_reply(post_id):
    if request.method == 'POST':
        user_name = request.form['user_name']
        reply_content = request.form['reply_content']
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO forum_replies (post_id, user_name, reply_content, created_at) VALUES (%s, %s, %s, NOW())",
                       (post_id, user_name, reply_content))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Reply added successfully!')
        return redirect(url_for('forum.view_forum'))


@forum_bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    connection = get_db()
    cursor = connection.cursor(DictCursor)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("UPDATE forum_posts SET topic = %s, post_content = %s, updated_at = NOW() WHERE post_id = %s",
                       (title, content, post_id))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Post updated successfully!')
        return redirect(url_for('forum.view_forum'))
    cursor.execute("SELECT * FROM forum_posts WHERE post_id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_forum.html', post=post)

@forum_bp.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    connection = get_db()
    cursor = connection.cursor()
    try:
        # Update likes_count for the post
        cursor.execute("UPDATE forum_posts SET likes_count = likes_count + 1 WHERE post_id = %s", (post_id,))
        connection.commit()

        # Get the updated likes_count
        cursor.execute("SELECT likes_count FROM forum_posts WHERE post_id = %s", (post_id,))
        likes_count = cursor.fetchone()['likes_count']

        response = {"success": True, "likes_count": likes_count}
    except Exception as e:
        response = {"success": False, "error": str(e)}
    finally:
        cursor.close()
        connection.close()

    return jsonify(response)

@forum_bp.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM forum_posts WHERE post_id = %s", (post_id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash('Post deleted successfully!')
    return redirect(url_for('forum.view_forum'))

@forum_bp.route('/forum/edit_reply/<int:reply_id>', methods=['POST'])
def edit_reply(reply_id):
    if request.method == 'POST':
        reply_content = request.form['reply_content']
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE forum_replies SET reply_content = %s WHERE reply_id = %s",
                       (reply_content, reply_id))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Reply updated successfully!')
        return redirect(url_for('forum.view_forum'))


@forum_bp.route('/forum/delete_reply/<int:reply_id>', methods=['POST'])
def delete_reply(reply_id):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM forum_replies WHERE reply_id = %s", (reply_id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash('Reply deleted successfully!')
    return redirect(url_for('forum.view_forum'))
