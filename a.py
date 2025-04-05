import threading
import socket
import json
import requests
import hashlib
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# مدل بلاک
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def __repr__(self):
        return json.dumps(self.__dict__)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data='Genesis Block', previous_hash='1')  # بلاک جنسیس

    def create_block(self, data, previous_hash):
        index = len(self.chain) + 1
        timestamp = time.time()
        block = Block(index, previous_hash, timestamp, data, '')
        block.hash = self.hash(block)
        self.chain.append(block)
        return block

    def hash(self, block):
        block_string = json.dumps(block.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_last_block(self):
        return self.chain[-1]

blockchain = Blockchain()

@app.route('/register', methods=['POST'])
def register():
    data = request.json['fingerprint_hash']  # هش اثر انگشت
    previous_hash = blockchain.get_last_block().hash
    block = blockchain.create_block(data, previous_hash)
    response = {
        'message': 'Fingerprint hash has been registered!',
        'block': {
            'index': block.index,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'data': block.data,
            'hash': block.hash
        }
    }
    return jsonify(response), 201

@app.route('/authenticate', methods=['POST'])
def authenticate():
    fingerprint_hash = request.json['fingerprint_hash']  # هش اثر انگشت وارد شده
    for block in blockchain.chain:
        if block.data == fingerprint_hash:
            return jsonify({'status': 'success', 'message': 'Authentication successful.'}), 200

    return jsonify({'status': 'error', 'message': 'Authentication failed.'}), 401

def decrypt_image(encrypted_image, final_key):
    def text_to_bits(text):
        bits = []
        for char in text:
            bits.extend([int(bit) for bit in format(ord(char), '08b')])
        return bits

    def bits_to_text(bits):
        chars = []
        for b in range(len(bits) // 8):
            byte = bits[b * 8:(b + 1) * 8]
            chars.append(chr(int(''.join(str(bit) for bit in byte), 2)))
        return ''.join(chars)

    encrypted_bits = text_to_bits(encrypted_image)
    decrypted_bits = [bit ^ key_bit for bit, key_bit in zip(encrypted_bits, final_key)]
    decrypted_image = bits_to_text(decrypted_bits)

    return decrypted_image

def run_flask():
    app.run(host='127.0.0.1', port=5000)

def run_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 65433)
    server_socket.bind(server_address)
    server_socket.listen()

    print("Socket Server Running...")

    correct_decrypted_image = 'cc678ccfdbe0be15e5e1adbbe6f0ceda6f4c01f9c24946f8f487ade4a9ec448067c8003f62cbe3bc6eaabf6bcabbadc162b733d2145b742d61ed528a5223ae1e'

    while True:
        connection, client_address = server_socket.accept()
        try:
            print("New connection from:", client_address)
            message = connection.recv(4096).decode()
            message_dict = json.loads(message)

            # استخراج عملیات و داده
            action = message_dict['action']
            password_list = message_dict['data']

            encrypted_image = password_list[0]
            final_key = json.loads(password_list[1])

            # رمزگشایی تصویر
            decrypted_image = decrypt_image(encrypted_image, final_key)
            print("Decrypted Image:", decrypted_image)

            fingerprint_hash = hashlib.sha256(decrypted_image.encode()).hexdigest()

            if action == 'register':
                print("Registering fingerprint hash:", fingerprint_hash)
                response = requests.post('http://127.0.0.1:5000/register', json={'fingerprint_hash': fingerprint_hash})
                print("Blockchain Registration Response:", response.json())
                connection.sendall(response.json().get('message', 'Error occurred').encode())

            elif action == 'authenticate':
                print("Authenticating fingerprint hash:", fingerprint_hash)
                auth_response = requests.post('http://127.0.0.1:5000/authenticate', json={'fingerprint_hash': fingerprint_hash})
                print("Authentication Response:", auth_response.json())
                connection.sendall(auth_response.json().get('message', 'Error occurred').encode())

            else:
                connection.sendall("Invalid action specified.".encode())

        finally:
            connection.close()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    socket_thread = threading.Thread(target=run_socket)

    flask_thread.start()
    socket_thread.start()

    flask_thread.join()
    socket_thread.join()