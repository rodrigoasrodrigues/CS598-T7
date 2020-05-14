import json
from flask import render_template
from app import app
from app.models.tables import Word2VecModel
from app.controllers import model_manager
from decimal import * 


@app.route('/explore/<model_id>')
@app.route('/explore/<model_id>/<word>')
def explore(model_id, word=None):
    model = Word2VecModel.query.get(model_id)
    word_dict = get_words(model_id)
    words = sorted([(v, k) for k, v in word_dict], reverse=True)
    related_words_dict = get_related_words(model_id,word)
    related_words = sorted([(v,k) for k,v in related_words_dict], reverse=True)
    min_t = 0
    max_t = 1
    if word:
        min_w = related_words[-1]
        max_w = related_words[0]
        min_t =  min_w[0]
        max_t = max_w[0]
    set_t =  (min_t+max_t)/2
    return render_template('explore.html', model=model, words=words,related_words=related_words, selected=word,min_t=("%.2f" % min_t),max_t=("%.2f" % max_t),set_t=("%.2f" % set_t))


def get_words(id):
    return model_manager.get_words(id)

def get_related_words(id, word):
    if word:
        return model_manager.get_words(id, word)
    else:
        return []

@app.route('/graph_data/<model_id>/<word>/<float:threshold>')
@app.route('/graph_data/<model_id>/<word>/<float:threshold>/')
@app.route('/graph_data/<model_id>/<word>/<float:threshold>/<force_tree>')
def graph_data(model_id,word,threshold,force_tree='false'):
    data = get_related_words(model_id, word)
    results = [d for d in data if d[1]>=threshold]
    allnodes = []
    allnodes.append(word)
    nodes = [{'id':r[0],'level':1} for r in results]
    for r in results: 
        allnodes.append(r[0])
    nodes.append({'id':word,'level':0})
    links = [{"source": word, "target": r[0], "value": r[1]} for r in results]
    for r in results: 
        #second level
        w = r[0]
        new_results = [nr for nr in get_related_words(model_id, w) if nr[1]>=threshold]
        for nr in new_results:
            if not nr[0] in allnodes:
                allnodes.append(nr[0])
                nodes.append({'id':nr[0],'level':2})
                links.append({"source": w, "target": nr[0], "value": nr[1]})
            elif force_tree == 'false':
                links.append({"source": w, "target": nr[0], "value": nr[1]})
    ret = {'nodes':nodes, 'links':links}
    return json.dumps(ret)
