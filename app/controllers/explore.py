from flask import render_template
from app import app
from app.models.tables import Word2VecModel
import random


@app.route('/explore/<model_id>')
@app.route('/explore/<model_id>/<word>')
def explore(model_id, word=None):
    model = Word2VecModel.query.get(model_id)
    word_dict = get_words(model.file_hash)
    words = sorted([(v, k) for k, v in word_dict.items()], reverse=True)
    related_words_dict = get_related_words(model.file_hash,word)
    related_words = sorted([(v,k) for k,v in related_words_dict.items()], reverse=True)
    return render_template('explore.html', model=model, words=words,related_words=related_words, selected=word)


def get_words(hash):  # todo: plug in the model for actual results
    random.seed(1)
    random_words = ['notice', 'kill', 'curtain', 'friends', 'fairies', 'pumped', 'fax', 'cause', 'decisive', 'onerous',
        'crooked', 'ambiguous', 'number', 'pigs', 'drown', 'healthy', 'move', 'time', 'versed', 'capricious', 'ossified', 'throne',
        'nest', 'eggs', 'earsplitting', 'slope', 'tidy', 'pipe', 'lopsided', 'six', 'depressed', 'planes', 'acceptable', 'kindly',
        'trashy', 'talented', 'defeated', 'exclusive', 'rhetorical', 'wry', 'supreme', 'eminent', 'general', 'futuristic', 'fine', 'owe',
        'weight', 'creator', 'questionable', 'righteous']
    ret = {}
    for w in random_words:
        ret[w] = random.random()
    return ret

def get_related_words(hash, word): # todo: plug in the model for actual results
    if word:
        return get_words(hash)
    else:
        return {}