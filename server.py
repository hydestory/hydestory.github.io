from flask import Flask, render_template, request
from flask_ngrok2 import run_with_ngrok
import matplotlib.pyplot as plt
import numpy as np
import logomaker
import matplotlib.pyplot as plt

app = Flask(__name__)
sequences = []
sequence=''

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    file = request.files['file-upload']
    sequence = request.form.get('sequence')
    if sequence:
        sequences=sequence.split('\r\n')
        matrix = logomaker.alignment_to_matrix(sequences=sequences, to_type='counts')
        logo = logomaker.Logo(matrix)
        fig=logo.fig
        logo_filepath = 'static/logo.png' 
        logo_filepath1 = 'static/logo.jpg'
        logo_filepath2 = 'static/logo.svg'
        fig.savefig(logo_filepath)
        fig.savefig(logo_filepath1)
        fig.savefig(logo_filepath2)
        return render_template('result.html')
    elif file:
        filecotent = file.read()
        
        sequences=filecotent.decode().split('\r\n')
        matrix = logomaker.alignment_to_matrix(sequences=sequences, to_type='counts')
        logo = logomaker.Logo(matrix)
        fig=logo.fig
        logo_filepath = 'static/logo.png' 
        logo_filepath1 = 'static/logo.jpg'
        logo_filepath2 = 'static/logo.svg'
        fig.savefig(logo_filepath)
        fig.savefig(logo_filepath1)
        fig.savefig(logo_filepath2)
        return render_template('result.html')

   

if __name__ == '__main__':
    app.run()
