from flask import render_template
from app import app


@app.route('/')
def index():
    return render_template('default.html')

@app.route('/add_dataset')
def add_dataset():
    return render_template('add_dataset.html')