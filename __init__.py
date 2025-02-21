from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import jsonify
from urllib.request import urlopen
import sqlite3
import base64

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('hello.html')


# key = Fernet.generate_key()
# f = Fernet(key)


def _make_key(key: str) -> Fernet:
    key = key.ljust(32)[:32]
    key_byte = key.encode()
    key_base64 = base64.urlsafe_b64encode(key_byte)

    f = Fernet(key_base64)

    return f


@app.route('/encrypt/<string:key>/<string:valeur>')
def encryptage(key, valeur):
    f = _make_key(key)
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    # return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str
    return jsonify({"token_encrypt":
                    token.decode()}), 200  # Retourne le token en str


@app.route('/decrypt/<string:key>/<string:valeur>')
def decryptage(key, valeur):
    f = _make_key(key)
    token = f.decrypt(valeur)

    return jsonify({"token_decrypt": token.decode()}), 200


if __name__ == "__main__":
    app.run(debug=True)
