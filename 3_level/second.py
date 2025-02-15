import socket  

# ایجاد سوکت برای واسط  
intermediary_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

# آدرس و پورت واسط را مشخص کنید  
intermediary_address = ('localhost', 65432)  
intermediary_socket.bind(intermediary_address)  

# گوش دادن به اتصالات  
intermediary_socket.listen()  

print("واسط آماده دریافت اتصالات...")  

while True:  
    # پذیرش اتصالات ورودی  
    client_connection, client_address = intermediary_socket.accept()  
    try:  
        print("اتصال جدید از:", client_address)  

        # دریافت رمز عبور از کلاینت  
        password = client_connection.recv(1024).decode()  
        print("رمز عبور دریافت شد:", password)  

        # ایجاد سوکت برای اتصال به سرور  
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        server_address = ('localhost', 65433)  # آدرس سرور  
        server_socket.connect(server_address)  

        # ارسال رمز عبور به سرور  
        server_socket.sendall(password.encode())  

        # دریافت نتیجه از سرور  
        response = server_socket.recv(1024).decode()  
        print("پاسخ از سرور:", response)  

        # ارسال نتیجه به کلاینت  
        client_connection.sendall(response.encode())  

    finally:  
        # بستن اتصال با کلاینت  
        client_connection.close()  
        server_socket.close()