from flask import Flask
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
app = Flask(__name__)

@app.route('/<string:line>')
def main(line: str):
    tokens  = nltk.word_tokenize(line)
    return {
        'POS-Tagging': nltk.pos_tag(tokens)
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)