# server.py  
import socket  
import json  
import requests  

HOST = '127.0.0.1'  
PORT = 65432  

def start_server():  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
        s.bind((HOST, PORT))  
        s.listen()  
        print("Server is listening...")  
        
        conn, addr = s.accept()  
        with conn:  
            print(f"Connected by {addr}")  
            while True:  
                data = conn.recv(1024)  
                if not data:  
                    break  
                
                password = data.decode('utf-8')  
                response = requests.post('http://127.0.0.1:5000/authenticate', json={'password': password})  
                conn.sendall(response.content)  

if __name__ == "__main__":  
    start_server()