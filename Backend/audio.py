import fitz
import re
import nltk
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np
import os
import numpy as np
import librosa
import soundfile as sf
from pyttsx3 import init
import random
from pydub import AudioSegment

def extract_text(file_name):
    s = ''  
    file_path = f'./uploads/{file_name}'
    doc = fitz.open(file_path)
    page_content = []  

    # Text extraction
    for page in doc:
        text = page.get_text()
        # Clean the text
        cleaned_text = re.sub(r'\uf0b7|\n', ' ', text)
        cleaned_text = re.sub(r'[^\w\s.,!?;:]', '', cleaned_text)  
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        page_content.append(cleaned_text.strip())
        s += cleaned_text.strip() + " "
    # print("content is ", s)
    # print("string is ", s)

    splitter = RecursiveCharacterTextSplitter(
        separators=['.', '\n'],
        chunk_size=250,
        chunk_overlap=0
    )

    chunks = splitter.split_text(s)
    q = []
    for i in chunks:
        i = i.lstrip('.')
        i = i + '.'
        q.append(i)
        # tokenization_prediction(i,labeled_sentences)
    print("size is", len(page_content))
    return page_content




def generate_tts_with_sentiment(text):
    sentiment = 'neutral'
    global count 
    count = 0
    tts_engine = init()
    tts_engine.setProperty('rate', 190)
    tts_engine.setProperty('volume', 0.8)
    
    tts_temp_file = 'hello_world_temp.wav'
    tts_engine.save_to_file(text, tts_temp_file)
    tts_engine.runAndWait()
    
    output_file = f'{sentiment}_{count}.wav'
    count += 1
    y, sr = librosa.load(tts_temp_file, sr=None)

    settings = {
        'pitch_shift':  0.0,
        'speed_factor': 1.0,
        'volume_gain': 0
    }

    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=settings['pitch_shift'])
    y_stretched = librosa.effects.time_stretch(y_shifted, rate=settings['speed_factor'])
    y_adjusted = y_stretched * (10 ** (settings['volume_gain'] / 20.0))
    
    y_normalized = librosa.util.normalize(y_adjusted)
    y_final = np.clip(y_normalized, -1.0, 1.0)
    
    sf.write(output_file, y_final, sr)
    
    combined_audio = AudioSegment.from_wav(output_file)
    combined_audio_duration = combined_audio.duration_seconds
    minutes, seconds = divmod(combined_audio_duration, 60)
    time_cal = minutes * 60 + seconds
    
    return output_file, time_cal



x  = extract_text('ml.pdf')
generate_tts_with_sentiment(x)