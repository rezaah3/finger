import socket  

# ایجاد سوکت  
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

# آدرس و پورت واسط را مشخص کنید  
intermediary_address = ('localhost', 65432)  

# اتصال به واسط  
client_socket.connect(intermediary_address)  

# دریافت رمز عبور از کاربر  
password = input("رمز عبور خود را وارد کنید: ")  

# ارسال رمز عبور به واسط  
client_socket.sendall(password.encode())  

# دریافت نتیجه از واسط  
result = client_socket.recv(1024).decode()  
print("نتیجه:", result)  

# بستن سوکت  
client_socket.close()