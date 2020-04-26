from flask import render_template
from app import app


@app.route('/add_dataset')
def add_dataset():
    return render_template('add_dataset.html')