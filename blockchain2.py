import hashlib  
import json  
import time  
from flask import Flask, request, jsonify  
import sqlite3  

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
        self.current_transactions = []  
        self.create_block(previous_hash='1')  # بلاک جنسیس  

    def create_block(self, previous_hash):  
        index = len(self.chain) + 1  
        timestamp = time.time()  
        block = Block(index, previous_hash, timestamp, self.current_transactions, '')  # هش را موقتا خالی بگذارید  
        block.hash = self.hash(block)  # حالا هش را محاسبه و به بلاک اضافه کنید  
        self.current_transactions = []  # خالی کردن معاملات  
        self.chain.append(block)  
        return block  

    def add_transaction(self, sender, recipient, amount):  
        self.current_transactions.append({  
            'sender': sender,  
            'recipient': recipient,  
            'amount': amount,  
        })  

    def hash(self, block):  
        block_string = json.dumps(block.__dict__, sort_keys=True).encode()  
        return hashlib.sha256(block_string).hexdigest()  

    def get_last_block(self):  
        return self.chain[-1]  

# ایجاد پایگاه داده و جدول  
def init_db():  
    conn = sqlite3.connect('blockchain.db')  
    cursor = conn.cursor()  
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS users (  
            id INTEGER PRIMARY KEY,  
            password TEXT UNIQUE NOT NULL  
        )  
    ''')  
    conn.commit()  
    conn.close()  

# زنجیره بلاک‌چین  
blockchain = Blockchain()  

@app.route('/register', methods=['POST'])  
def register():  
    password = request.json['password']  
    conn = sqlite3.connect('blockchain.db')  
    cursor = conn.cursor()  
    
    try:  
        cursor.execute('INSERT INTO users (password) VALUES (?)', (password,))  
        conn.commit()  
        response = {'status': 'success', 'message': 'User registered.'}  
    except sqlite3.IntegrityError:  
        response = {'status': 'error', 'message': 'User already exists.'}  

    conn.close()  
    return jsonify(response)  

@app.route('/authenticate', methods=['POST'])  
def authenticate():  
    password = request.json['password']  
    conn = sqlite3.connect('blockchain.db')  
    cursor = conn.cursor()  
    
    cursor.execute('SELECT * FROM users WHERE password = ?', (password,))  
    user = cursor.fetchone()  
    
    conn.close()  
    
    if user:  
        return jsonify({'status': 'success', 'message': 'Authentication successful.'})  
    else:  
        return jsonify({'status': 'error', 'message': 'Authentication failed.'})  

@app.route('/transaction/new', methods=['POST'])  
def new_transaction():  
    values = request.json  
    required = ['sender', 'recipient', 'amount']  
    
    if not all(k in values for k in required):  
        return 'Missing values', 400  
    
    blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])  
    
    response = {'message': f'Transaction will be added to Block {blockchain.get_last_block().index + 1}'}  
    return jsonify(response), 201  

@app.route('/mine', methods=['GET'])  
def mine():  
    last_block = blockchain.get_last_block()  
    previous_hash = last_block.hash  
    block = blockchain.create_block(previous_hash)  

    response = {  
        'index': block.index,  
        'previous_hash': block.previous_hash,  
        'timestamp': block.timestamp,  
        'transactions': block.data,  
        'hash': block.hash  
    }  
    return jsonify(response), 200  

if __name__ == '__main__':  
    init_db()  
    app.run(host='127.0.0.1', port=5000)