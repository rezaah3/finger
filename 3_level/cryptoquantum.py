import numpy as np
import random
import fingertohash


BASES = ['+', 'x']

def generate_random_bits(length):
    return np.random.randint(0, 2, length).tolist()

def generate_random_bases(length):
    return [random.choice(BASES) for _ in range(length)]

def encode_bits(bits, bases):
    encoded_bits = []
    for bit, base in zip(bits, bases):
        if base == '+':
            encoded_bits.append(bit)
        else:  
            encoded_bits.append(bit ^ 1) 
    return encoded_bits

def measure_bits(encoded_bits, bases):
    measured_bits = []
    for encoded_bit, base in zip(encoded_bits, bases):
        if base == '+':
            measured_bits.append(encoded_bit)
        else: 
            measured_bits.append(encoded_bit ^ 1) 
    return measured_bits

def generate_final_key(node_bases, basestation_bases, bits):
    key = []
    for node_base, basestation_base, bit in zip(node_bases, basestation_bases, bits):
        if node_base == basestation_base:
            key.append(bit)
    return key

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

def encrypt_text(text):
    bits = text_to_bits(text)
    key_length = len(bits)

    node_bits = generate_random_bits(key_length)
    node_bases = generate_random_bases(key_length)
    encoded_bits = encode_bits(node_bits, node_bases)

    basestation_bases = generate_random_bases(key_length)
    basestation_measured_bits = measure_bits(encoded_bits, basestation_bases)

    final_key = generate_final_key(node_bases, basestation_bases, node_bits)

    if len(final_key) < key_length:
        final_key.extend(np.random.randint(0, 2, key_length - len(final_key)).tolist())
    elif len(final_key) > key_length:
        final_key = final_key[:key_length]

    encrypted_bits = [bit ^ key_bit for bit, key_bit in zip(bits, final_key)]
    encrypted_text = bits_to_text(encrypted_bits)
    return encrypted_text, final_key


def encrypt(image_path):
    image_hash = fingertohash.generate_fingerprint_hash(image_path)

    encrypted_text, final_key = encrypt_text(image_hash)
    return encrypted_text, final_key


if __name__ == "__main__":
    image_path = "fingerprint.jpg"
    encrypted_text,_  = encrypt(image_path)
    print(f"Encrypted Text: {encrypted_text}")
