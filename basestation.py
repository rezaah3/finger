import sqlite3
import json

def receive_data():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data")
    rows = c.fetchall()
    conn.close()
    return rows


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


def decrypt():
    received_data = receive_data()
    encrypted_image, final_key = received_data[0]
    final_key = json.loads(final_key)
    decrypted_image = decrypt_image(encrypted_image, final_key)
    return decrypted_image


if __name__ == "__main__":
    decrypted_image = decrypt()
    print("received_hash", decrypted_image)
