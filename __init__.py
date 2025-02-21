from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import jsonify
from urllib.request import urlopen
import sqlite3
import base64, hashlib

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('hello.html')


# key = Fernet.generate_key()
# f = Fernet(key)


def _make_key(key: str) -> Fernet:
    # # key doit être adapté pour satisfaire aux caractéristique des paramètres qu'accepte Fernet
    # # URL-safe base64-encoded 32-byte key
    # # ajustement pour avoir 32 charactéres
    # key = key.ljust(32)[:32]
    # # conversion en bytes
    # key_byte = key.encode()
    # # base64 - encoded et URL-safe
    # key_base64 = base64.urlsafe_b64encode(key_byte)
    # # print(key_base64)
    # # instanciation de l'objet avec la clé compatible avec ses algorythmes Fernet

    # ------------------------------
    key_hash = hashlib.sha256(key.encode())
    key_32 = key_hash.digest()
    key_base64 = base64.urlsafe_b64encode(key_32)
    f = Fernet(key_base64)
    return f


@app.route('/encrypt/<string:key>/<string:valeur>')
def encryptage(key, valeur):
    # récupération de la clée dans l'url mise en paramètre dans _make_key
    f = _make_key(key)

    valeur_bytes = valeur.encode()  # Conversion str -> bytes

    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return jsonify({"response":
                    token.decode()}), 200  # Retourne le token en str


@app.route('/decrypt/<string:key>/<string:valeur>')
def decryptage(key, valeur):

    f = _make_key(key)

    token = f.decrypt(valeur)

    return jsonify({"response": token.decode()}), 200


if __name__ == "__main__":
    app.run(debug=True)
