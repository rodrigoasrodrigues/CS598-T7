import time
from app import db
from app.models.tables import (DatasetFile, LabelFile, Word2VecModel)

def perform(id):
    time.sleep(10)
    w2v_model = Word2VecModel.query.get(id)
    w2v_model.file_hash = 'trained'
    db.session.commit()
    return 'trained'