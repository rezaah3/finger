# client.py  
import socket  

HOST = '127.0.0.1'  
PORT = 65432  

def client_program():  
    password = input("Enter your password: ")  
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
        s.connect((HOST, PORT))  
        s.sendall(password.encode('utf-8'))  
        
        data = s.recv(1024)  
        print(f"Received from server: {data.decode('utf-8')}")  

if __name__ == "__main__":  
    client_program()