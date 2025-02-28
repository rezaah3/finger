import socket  
 
intermediary_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
 
intermediary_address = ('localhost', 65432)  
intermediary_socket.bind(intermediary_address)  

intermediary_socket.listen()  

print("واسط آماده دریافت اتصالات...")  

while True:  
    client_connection, client_address = intermediary_socket.accept()  
    try:  
        print("New Connection: ", client_address)  

        password = client_connection.recv(4096).decode()    

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        server_address = ('localhost', 65433)  # آدرس سرور  
        server_socket.connect(server_address)  
 
        server_socket.sendall(password.encode())  

        response = server_socket.recv(1024).decode()  
        print("Respone From Server: ", response)  

        client_connection.sendall(response.encode())  

    finally:  
        client_connection.close()  
        server_socket.close()