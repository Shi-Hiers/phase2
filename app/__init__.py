from flask import Flask, g
from flask_mail import Mail
from dotenv import load_dotenv
import os
from .app_factory import create_app
from .db_connect import close_db, get_db

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = create_app()
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')  # Fallback to a default if not set in .env

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Get email username from .env
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Get email password from .env
app.config['MAIL_DEFAULT_SENDER'] = (os.getenv('MAIL_SENDER_NAME', 'Music Education Website'), os.getenv('MAIL_USERNAME'))

mail = Mail(app)  # Initialize Flask-Mail

# Register Blueprints
from app.blueprints.forums import forum_bp
app.register_blueprint(forum_bp)

from app.blueprints.instructors import instructors_bp
app.register_blueprint(instructors_bp)

from app.blueprints.testimonials import testimonials_bp
app.register_blueprint(testimonials_bp)

from . import routes

@app.before_request
def before_request():
    g.db = get_db()

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)
