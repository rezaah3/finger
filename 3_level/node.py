import socket
import json
import cryptoquantum

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
intermediary_address = ('localhost', 65432)

client_socket.connect(intermediary_address)

action = input("Do you want to 'register' or 'authenticate'? ")

image_path = "fingerprint.jpg"

encrypted_image, final_key = cryptoquantum.encrypt(image_path)
final_key = json.dumps(final_key)
password_list = [encrypted_image, final_key]

message = {
    'action': action, 
    'data': password_list
}
message_json = json.dumps(message)

client_socket.sendall(message_json.encode())

result = client_socket.recv(1024).decode()
print("Result: ", result)

client_socket.close()