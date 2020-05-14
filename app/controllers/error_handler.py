from flask import render_template
from app import app

@app.errorhandler(500)
@app.route('/error')
def internal_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404