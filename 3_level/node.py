import socket 
import json 
import cryptoquantum

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
 
intermediary_address = ('localhost', 65432)  

client_socket.connect(intermediary_address)  

input('Are You Ready ?')
image_path = "fingerprint.jpg"
encrypted_image, final_key = cryptoquantum.encrypt(image_path)
final_key = json.dumps(final_key)
password_list = [encrypted_image, final_key]
password_json = json.dumps(password_list)
 
client_socket.sendall(password_json.encode())  

 
result = client_socket.recv(1024).decode()  
print("Result: ", result)  

 
client_socket.close()