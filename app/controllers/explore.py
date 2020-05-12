from flask import render_template
from app import app
from app.models.tables import Word2VecModel
from app.controllers import model_manager



@app.route('/explore/<model_id>')
@app.route('/explore/<model_id>/<word>')
def explore(model_id, word=None):
    model = Word2VecModel.query.get(model_id)
    word_dict = get_words(model_id)
    words = sorted([(v, k) for k, v in word_dict], reverse=True)
    related_words_dict = get_related_words(model_id,word)
    related_words = sorted([(v,k) for k,v in related_words_dict], reverse=True)
    return render_template('explore.html', model=model, words=words,related_words=related_words, selected=word)


def get_words(id):
    return model_manager.get_words(id)

def get_related_words(id, word):
    if word:
        return model_manager.get_words(id, word)
    else:
        return []