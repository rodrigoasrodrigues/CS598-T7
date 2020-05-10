import os
import uuid
from flask import render_template, request, redirect
from app import app
from app import db
from app.controllers.env_configs import EnvConf
from app.models.tables import (DatasetFile, LabelFile)
import hashlib

def word_count_dataset(hash):
    filepath = os.path.abspath(EnvConf.dataset_dir+'/'+hash)
    file = open(filepath, "rt")
    data = file.read()
    words = data.split()
    wcount = len(words)
    return wcount

def count_labels(hash):
    #todo implement
    return 5, 6

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
        if request.files["fupLabel"] and request.form['labelRadio'] == 'new':
            label_file = request.files["fupLabel"]
            label_hash = save_file(label_file,EnvConf.label_dir)
            label_name = request.form['txtLabelName']
            print(f'label hash = {label_hash}')
            positive, negative = count_labels(label_hash)
            label = LabelFile(label_hash,label_name,positive, negative)
            db.session.add(label)
    db.session.commit()
    return redirect('/')