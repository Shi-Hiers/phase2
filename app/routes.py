from flask import render_template
from . import app

from flask import redirect, url_for

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tutorials')
def tutorials():
    return render_template('tutorial.html')

@app.route('/music_theory_hub')
def music_theory_hub():
    return render_template('music_theory_hub.html')

@app.route('/quiz_practice')
def quiz_practice():
    return render_template('quiz_practice.html')



@app.route('/instructors')
def instructors():
    return render_template('instructors.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')


