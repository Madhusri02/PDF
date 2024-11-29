import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from main import extract_text
from Audio.toranto.aud import generate_audio
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from QandA import questionAndAnswer
from summarise import summarise_content

import json

from Audio_generation import combining_audios


app = Flask(__name__, static_folder='Generatedaudio')
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# mongo url
mongo_uri = "mongodb+srv://admin:root12@cluster0.iycxjhk.mongodb.net/dreampdf?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client['dreampdf']
collection = db['pdf_names']

file_name = ''

combined_sentences = {}

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# File access, save, and process
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file:
        labeled_sentences = {}
        file_name = file.filename
        print("file name is ", file_name)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        file.save(filepath)
        print("saved")

        extracted_text = extract_text(file_name, labeled_sentences)
        print("looking for")
        print(extracted_text)

        summarised_Content = summarise_content(extracted_text['text'])
        print(summarised_Content)

      
        return jsonify({'text': extracted_text['text'] , "summary" : summarised_Content}), 200
    
@app.route('/article' , methods=['POST'])
def article():
    print("article link is ")
    data = request.get_json()  # Extract JSON from the request body
    # text = data.get('text')
    print(data)

    reterived_Answer = questionAndAnswer(data['link'] , data["question"])
    return {"answer" : reterived_Answer}

@app.route('/get_pdfs', methods=['GET'])
def get_pdfs():
    pdfs = collection.find()
    return dumps(list(pdfs)), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
