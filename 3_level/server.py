import socket  

# ایجاد سوکت برای سرور  
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

# آدرس و پورت سرور را مشخص کنید  
server_address = ('localhost', 65433)  
server_socket.bind(server_address)  

# گوش دادن به اتصالات  
server_socket.listen()  

print("سرور آماده دریافت اتصالات...")  

# متغیر رمز عبور صحیح  
correct_password = "secret123"  # شما می‌توانید این رمز را تغییر دهید  

while True:  
    # پذیرش اتصالات ورودی  
    connection, client_address = server_socket.accept()  
    try:  
        print("اتصال جدید از:", client_address)  

        # دریافت رمز عبور از واسط  
        password = connection.recv(1024).decode()  
        print("رمز عبور دریافت شد:", password)  

        # بررسی رمز عبور  
        if password == correct_password:  
            connection.sendall("تایید شدی".encode())  
        else:  
            connection.sendall("تایید نشدی".encode())  

    finally:  
        # بستن اتصال  
        connection.close()