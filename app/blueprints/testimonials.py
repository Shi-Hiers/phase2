from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message
from app import mail  # Import mail object
from app.functions import fetch_all, execute_query  # Assuming these are defined utility functions

testimonials_bp = Blueprint('testimonials', __name__, template_folder='templates')

@testimonials_bp.route('/testimonials')
def display_testimonials():
    testimonials = fetch_all("SELECT * FROM testimonials")
    return render_template('testimonials.html', testimonials=testimonials)

@testimonials_bp.route('/testimonials/add', methods=['GET', 'POST'])
def add_testimonial():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Save testimonial to database
        execute_query(
            "INSERT INTO testimonials (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )

        # Send thank-you email
        subject = "Thank You for Your Testimonial!"
        body = f"""
        Hi {name},

        Thank you for sharing your testimonial on our Music Education Website! 
        We truly appreciate your feedback and are glad to have you as part of our community.

        Best regards,
        The Music Education Team
        """
        send_email(email, subject, body)

        flash("Thank you for sharing your testimony! We've sent you a confirmation email.")
        return redirect(url_for('testimonials.display_testimonials'))

    return render_template('add_testimonial.html')

def send_email(recipient, subject, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)
