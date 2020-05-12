import os
import uuid
import json
import hashlib
from flask import render_template, request, redirect
from app import app
from app import db
from app.controllers.env_configs import EnvConf
from app.models.tables import (DatasetFile, LabelFile, Word2VecModel)
from threading import Thread

from app.controllers import model_manager

def word_count_dataset(hash):
    filepath = os.path.abspath(EnvConf.dataset_dir+'/'+hash)
    file = open(filepath, "rt")
    data = file.read()
    words = data.split()
    wcount = len(words)
    return wcount

def count_labels(hash):
    filepath = os.path.abspath(EnvConf.label_dir+'/'+hash)
    label_file = open(filepath, 'r') 
    Lines = label_file.readlines() 
    count = 0
    positive = 0
    # counts positive and total then calculate negatives
    for line in Lines: 
        count = count+1
        pos = line.strip().split('\t')[1] == '1'
        if pos:
            positive = positive + 1
    negative = count - positive
    #todo implement
    return positive, negative

def save_file(file, folder):
    fullpath_folder = os.path.abspath(folder)
    temp_filename = 'temp_'+str(uuid.uuid4())
    fullpath = fullpath_folder+'/'+temp_filename
    file.save(fullpath)
    with open(fullpath, "rb") as f:
                file_hash = hashlib.md5()
                while chunk := f.read(8192):
                    file_hash.update(chunk)
    hashstr = file_hash.hexdigest()
    dest = fullpath_folder+'/'+hashstr
    if not os.path.exists(dest):
        os.rename(fullpath,dest)
    else:
        os.remove(fullpath)
    return hashstr

@app.route('/add_dataset')
def add_dataset():
    dataset_list = DatasetFile.query.all()
    label_list = LabelFile.query.all()
    return render_template('add_dataset.html', dataset_list=dataset_list, label_list=label_list)

@app.route('/train', methods=["POST"])
def train():
    dataset_id = -1
    label_id = -1
    if request.files:
        if request.files["fupDataset"] and request.form['datasetRadio'] == 'new':
            dataset_file = request.files["fupDataset"]
            dataset_hash = save_file(dataset_file,EnvConf.dataset_dir)
            dataset_name = request.form['txtDatasetName']
            print(f'dataset hash = {dataset_hash}')
            nwords = word_count_dataset(dataset_hash)
            print(f'words = {nwords}')
            dataset = DatasetFile(dataset_hash,dataset_name,nwords)
            db.session.add(dataset)
            db.session.commit()
            dataset_id = dataset.id
        if request.files["fupLabel"] and request.form['labelRadio'] == 'new':
            label_file = request.files["fupLabel"]
            label_hash = save_file(label_file,EnvConf.label_dir)
            label_name = request.form['txtLabelName']
            print(f'label hash = {label_hash}')
            positive, negative = count_labels(label_hash)
            label = LabelFile(label_hash,label_name,positive, negative)
            db.session.add(label)
            db.session.commit()
            label_id = label.id

    if dataset_id == -1:
        dataset_id = int(request.form['datasetRadio'])
    if label_id == -1:
        label_id = int(request.form['labelRadio'])
    description = request.form['txtDescription']
    w2v_model = Word2VecModel('training', description, dataset_id, label_id)

    db.session.add(w2v_model)
    db.session.commit()
    print(f'dataset = {dataset_id} ; label = {label_id}')
    return redirect(f'/training/{w2v_model.id}')

@app.route('/training/<model_id>')
def training(model_id):
    model = Word2VecModel.query.get(model_id)
    return render_template('training_model.html',model=model)

    
@app.route('/training_status/<model_id>')
def training_status(model_id):
    model = Word2VecModel.query.get(model_id)
    return json.dumps(model.file_hash != 'training')

    
@app.route('/training_exec/<model_id>')
def training_exec(model_id):
    hash = model_manager.train(model_id)
    return json.dumps(hash)