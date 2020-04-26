from app import db


class LabelFile(db.Model):
    __tablename__ = "label_files"

    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(32), unique=True)
    name = db.Column(db.String(80), unique=False)
    positive_labels = db.Column(db.Integer, primary_key=False)
    negative_labels = db.Column(db.Integer, primary_key=False)

    def num_labels():
        return positive_labels+negative_labels

    def __init__(self, file_hash, name, positive_labels, negative_labels):
        self.file_hash = file_hash
        self.name = name
        self.positive_labels = positive_labels
        self.negative_labels = negative_labels

    def __repr__(self):
        return f'<LabelFile {id}:{file_hash}>'

class DatasetFile(db.Model):
    __tablename__ = "dataset_files"

    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(32), unique=True)
    name = db.Column(db.String(80), unique=False)
    words = db.Column(db.Integer, primary_key=False)

    def __init__(self, file_hash, name, words):
        self.file_hash = file_hash
        self.name = name
        self.words = words

    def __repr__(self):
        return f'<DatasetFile {id}:{file_hash}>'

class Word2VecModel(db.Mode):
    __tablename__ = "w2v_models"

    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(32), unique=True)
    description = db.Column(db.Text, unique=False)

    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset_files.id'))
    dataset = db.relationship('DatasetFile',foreign_keys=dataset_id)

    label_id = db.Column(db.Integer, db.ForeignKey('label_files.id'))
    label = db.relationship('LabelFile',foreign_keys=label_id)

    def __init__(self, file_hash, description, dataset_id, label_id):
        self.file_hash = file_hash
        self.description = description
        self.dataset_id = dataset_id
        self.label_id = label_id

    def __repr__(self):
        return f'<Word2VecModel {id}:{file_hash}>'