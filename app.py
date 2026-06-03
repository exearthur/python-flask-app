from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    length = int(request.form.get('length', 12))
    use_symbols = request.form.get('symbols') == 'on'

    characters = string.ascii_letters + string.digits
    if use_symbols:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))

    return render_template('result.html', password=password)


if __name__ == '__main__':
    app.run(debug=True)
