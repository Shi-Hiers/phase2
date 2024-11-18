from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.functions import fetch_all, fetch_one, execute_query

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/forum')
def view_forum():
    # Fetch all posts with their replies
    posts = fetch_all("SELECT * FROM forum_posts ORDER BY created_at DESC")
    for post in posts:
        post['replies'] = fetch_all("SELECT * FROM forum_replies WHERE post_id = %s ORDER BY created_at ASC", (post['post_id'],))
    return render_template('forum.html', posts=posts)

@forum_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        user_name = request.form['user_name']
        title = request.form['title']
        content = request.form['content']
        execute_query(
            "INSERT INTO forum_posts (user_name, topic, post_content, created_at) VALUES (%s, %s, %s, NOW())",
            (user_name, title, content)
        )
        flash('Post added successfully!')
        return redirect(url_for('forum.view_forum'))
    return render_template('add_forum.html')

@forum_bp.route('/forum/add_reply/<int:post_id>', methods=['POST'])
def add_reply(post_id):
    user_name = request.form['user_name']
    reply_content = request.form['reply_content']
    execute_query(
        "INSERT INTO forum_replies (post_id, user_name, reply_content, created_at) VALUES (%s, %s, %s, NOW())",
        (post_id, user_name, reply_content)
    )
    flash('Reply added successfully!')
    return redirect(url_for('forum.view_forum'))

@forum_bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        execute_query(
            "UPDATE forum_posts SET topic = %s, post_content = %s, updated_at = NOW() WHERE post_id = %s",
            (title, content, post_id)
        )
        flash('Post updated successfully!')
        return redirect(url_for('forum.view_forum'))
    post = fetch_one("SELECT * FROM forum_posts WHERE post_id = %s", (post_id,))
    return render_template('edit_forum.html', post=post)

@forum_bp.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    try:
        # Update likes_count for the post
        execute_query("UPDATE forum_posts SET likes_count = likes_count + 1 WHERE post_id = %s", (post_id,))
        # Fetch the updated likes count
        likes_count = fetch_one("SELECT likes_count FROM forum_posts WHERE post_id = %s", (post_id,))['likes_count']
        response = {"success": True, "likes_count": likes_count}
    except Exception as e:
        response = {"success": False, "error": str(e)}
    return jsonify(response)

@forum_bp.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    execute_query("DELETE FROM forum_posts WHERE post_id = %s", (post_id,))
    flash('Post deleted successfully!')
    return redirect(url_for('forum.view_forum'))

@forum_bp.route('/forum/edit_reply/<int:reply_id>', methods=['POST'])
def edit_reply(reply_id):
    reply_content = request.form['reply_content']
    execute_query(
        "UPDATE forum_replies SET reply_content = %s WHERE reply_id = %s",
        (reply_content, reply_id)
    )
    flash('Reply updated successfully!')
    return redirect(url_for('forum.view_forum'))

@forum_bp.route('/forum/delete_reply/<int:reply_id>', methods=['POST'])
def delete_reply(reply_id):
    execute_query("DELETE FROM forum_replies WHERE reply_id = %s", (reply_id,))
    flash('Reply deleted successfully!')
    return redirect(url_for('forum.view_forum'))
