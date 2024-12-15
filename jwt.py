from cryptography.fernet import Fernet
from flask import Flask, request, jsonify

class SimpleEncryptor:
    def __init__(self, key=None):
        """
        Initialize the SimpleEncryptor with an optional key.
        If no key is provided, a new key will be generated.
        """
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        """
        Encrypt the given data.

        :param data: The data to encrypt (str or bytes).
        :return: The encrypted data (bytes).
        """
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data)

    def decrypt(self, token):
        """
        Decrypt the given token.

        :param token: The encrypted data (bytes).
        :return: The decrypted data (str).
        """
        decrypted_data = self.cipher.decrypt(token)
        return decrypted_data.decode()

    def get_key(self):
        """
        Get the encryption key.

        :return: The key (bytes).
        """
        return self.key

# Flask app
app = Flask(__name__)
encryptor = SimpleEncryptor()

@app.route("/get_key", methods=["GET"])
def get_key():
    return jsonify({"key": encryptor.get_key().decode()}), 200

@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.json.get("data")
    if not data:
        return jsonify({"error": "No data provided"}), 400

    encrypted_data = encryptor.encrypt(data)
    return jsonify({"encrypted": encrypted_data.decode()}), 200

@app.route("/decrypt", methods=["POST"])
def decrypt():
    encrypted_data = request.json.get("encrypted")
    if not encrypted_data:
        return jsonify({"error": "No encrypted data provided"}), 400

    try:
        decrypted_data = encryptor.decrypt(encrypted_data.encode())
        return jsonify({"decrypted": decrypted_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
