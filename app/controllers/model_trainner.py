import time
import uuid
import os
from gensim.test.utils import common_texts
from gensim.models import Phrases, Word2Vec
from app import db
from app.models.tables import (DatasetFile, LabelFile, Word2VecModel)
from app.controllers.env_configs import EnvConf

def perform(id):
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