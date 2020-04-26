from flask import render_template
from app import app
from app.models.tables import Word2VecModel


@app.route('/')
@app.route('/model/<int:selected>')
def index(selected=None):
    model_list = Word2VecModel.query.all()
    if selected:
        model = Word2VecModel.query.get(selected)
    else:
        model = None

    return render_template('default.html',
                            model_list=model_list,
                            selected=selected,
                            model=model)
