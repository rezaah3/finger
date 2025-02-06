# blockchain.py  
from flask import Flask, request, jsonify  
import sqlite3  

app = Flask(__name__)  

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

if __name__ == '__main__':  
    init_db()  
    app.run(host='127.0.0.1', port=5000)