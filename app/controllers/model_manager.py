import time
import uuid
import os
from gensim.test.utils import common_texts
from gensim.models import Phrases, Word2Vec
from app import db
from app.models.tables import (DatasetFile, LabelFile, Word2VecModel)
from app.controllers.env_configs import EnvConf

def train(id):
    w2v_model = Word2VecModel.query.get(id)
    dataset = w2v_model.dataset
    #generates bigrams
    print('Getting Data')
    textdata = dataset.get_text_data()
    print('Generating Bigrams')
    bigram_transformer = Phrases(textdata)
    print('Transforming Corpus')
    corpus = bigram_transformer[textdata]
    # actually train a model
    print('Training W2V Model')
    model = Word2Vec(corpus, min_count=10, window=3,  workers=4 ,iter=10)
    #for models makes sense to just keep all trained instead of trying to match hashes and deduplicate
    print('Done!')
    model_name = str(uuid.uuid4())
    print(model_name)
    folder = EnvConf.model_dir
    path = os.path.abspath(folder)+'/'+model_name
    model.save(path)
    w2v_model.file_hash = model_name
    db.session.commit()
    return w2v_model.file_hash

def load(id):
    w2v_model = Word2VecModel.query.get(id)
    folder = EnvConf.model_dir
    path = os.path.abspath(folder)+'/'+w2v_model.file_hash
    model = Word2Vec.load(path)
    return model

def get_words(id, rel_word=None):
    model = load(id)
    if rel_word:
        result = model.wv.most_similar(positive=[rel_word], topn=20)
    else:
        positive_labels, negative_labels = get_labels(id)
        result = model.wv.most_similar(positive=positive_labels, negative=negative_labels, topn=100)
    return result

def get_labels(id):
    w2v_model = Word2VecModel.query.get(id)
    label = w2v_model.label
    model = load(id)
    positive_labels = []
    negative_labels = []
    folder = EnvConf.label_dir
    path = os.path.abspath(folder)+'/'+label.file_hash
    
    with open (path, 'r') as f:
        for line in f.readlines():
            elements = line.split('\t')
            key = elements[0].strip()
            value = elements[1].strip()
            if value == '1':
                words = key.split()
                bigram = "_".join(words)
                if bigram in model.wv.vocab:
                    positive_labels.append(bigram)
            else:
                words = key.split()
                bigram = "_".join(words)
                if bigram in model.wv.vocab:
                    negative_labels.append(bigram)
    return positive_labels, negative_labels