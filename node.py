import cryptoquan2
import sqlite3
import json


def create_database():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data
                 (encrypted_image TEXT, final_key TEXT)''')
    conn.commit()
    conn.close()


def send_message(image_path):
    encrypted_image, final_key = cryptoquan2.encrypt(image_path)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    final_key_str = json.dumps(final_key)
    c.execute("INSERT INTO data VALUES (?,?)", (encrypted_image, final_key_str))
    conn.commit()
    conn.close()
    print("is sended!")
    return encrypted_image


if __name__ == "__main__":
    create_database()
    image_path = "fingerprint.jpg"
    encrypted_image = send_message(image_path)
    print("encrypted_send", encrypted_image)
