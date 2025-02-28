import socket  
import json


def text_to_bits(text):
    bits = []
    for char in text:
        bits.extend([int(bit) for bit in format(ord(char), '08b')])
    return bits


def bits_to_text(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join(str(bit) for bit in byte), 2)))
    return ''.join(chars)


def decrypt_image(encrypted_image, final_key):
    encrypted_bits = text_to_bits(encrypted_image)

    decrypted_bits = [bit ^ key_bit for bit, key_bit in zip(encrypted_bits, final_key)]
    decrypted_image = bits_to_text(decrypted_bits)

    return decrypted_image
 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
 
server_address = ('localhost', 65433)  
server_socket.bind(server_address)  

server_socket.listen()  

print("سرور آماده دریافت اتصالات...")  

correct_decrypted_image = 'cc678ccfdbe0be15e5e1adbbe6f0ceda6f4c01f9c24946f8f487ade4a9ec448067c8003f62cbe3bc6eaabf6bcabbadc162b733d2145b742d61ed528a5223ae1e'

while True:  
    connection, client_address = server_socket.accept()  
    try:  
        print("اتصال جدید از:", client_address)  
 
        password = connection.recv(4096).decode() 
        password_list = json.loads(password)

        encrypted_image = password_list[0]
        final_key = json.loads(password_list[1]) 
        print("رمز عبور دریافت شد:", password_list)  
        decrypted_image = decrypt_image(encrypted_image, final_key)

        # بررسی رمز عبور  
        if decrypted_image == correct_decrypted_image:  
            connection.sendall("تایید شدی".encode())  
        else:  
            connection.sendall("تایید نشدی".encode())  

    finally:  
        # بستن اتصال  
        connection.close()