from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'
db = SQLAlchemy(app)


class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    symbols = db.Column(db.Boolean, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    passwords = Password.query.order_by(Password.id.desc()).all()
    return render_template('index.html', passwords=passwords)


@app.route('/generate', methods=['POST'])
def generate():
    length = int(request.form.get('length', 12))
    use_symbols = request.form.get('symbols') == 'on'

    characters = string.ascii_letters + string.digits
    if use_symbols:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))

    # Save the generated password to the database
    new_password = Password(
        password=password, length=length, symbols=use_symbols)
    db.session.add(new_password)
    db.session.commit()
    print(
        f"Saved password: {password} (Length: {length}, Symbols: {use_symbols})")

    return render_template('result.html', password=password)


if __name__ == '__main__':
    app.run(debug=True)
