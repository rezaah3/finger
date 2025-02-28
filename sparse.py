import numpy as np
import random
from scipy.sparse import random as sparse_random
from scipy.sparse import csr_matrix
import fingertohash

# پروتکل BB84
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

# تابع ایجاد ماتریس اسپارس
def generate_sparse_matrix(size, density=0.1):
    return sparse_random(size, size, density=density, format='csr', dtype=np.int8)

# تابع ضرب ماتریس اسپارس در بیت‌ها
def sparse_matrix_multiply(matrix, bits):
    bits_matrix = csr_matrix(bits).transpose()
    return matrix.dot(bits_matrix).toarray().flatten().tolist()

# تبدیل بیت‌ها به ماتریس
def bits_to_matrix(bits, size):
    return np.reshape(bits, (size, size))

# تبدیل ماتریس به بیت‌ها
def matrix_to_bits(matrix):
    return matrix.flatten().tolist()

# تبدیل متن به بیت‌ها
def text_to_bits(text):
    bits = []
    for char in text:
        bits.extend([int(bit) for bit in format(ord(char), '08b')])
    return bits

# تبدیل بیت‌ها به متن
def bits_to_text(bits):
    chars = []
    for b in range(len(bits) // 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join(str(bit) for bit in byte), 2)))
    return ''.join(chars)

# تابع رمزگذاری با استفاده از پروتکل BB84 و ماتریس اسپارس
def encrypt_text(text, size=64, density=0.1):
    bits = text_to_bits(text)
    key_length = size * size

    # پروتکل BB84
    node_bits = generate_random_bits(key_length)
    node_bases = generate_random_bases(key_length)
    encoded_bits = encode_bits(node_bits, node_bases)
    basestation_bases = generate_random_bases(key_length)
    basestation_measured_bits = measure_bits(encoded_bits, basestation_bases)
    final_key = generate_final_key(node_bases, basestation_bases, node_bits)

    # بررسی طول کلید نهایی
    if len(final_key) < key_length:
        final_key.extend(np.random.randint(0, 2, key_length - len(final_key)).tolist())
    elif len(final_key) > key_length:
        final_key = final_key[:key_length]

    # ایجاد ماتریس اسپارس
    sparse_matrix = generate_sparse_matrix(size, density)

    # ضرب ماتریس اسپارس در بیت‌ها
    encrypted_bits = sparse_matrix_multiply(sparse_matrix, final_key)

    # کلید رمزگذاری (ماتریس اسپارس)
    key = sparse_matrix

    return encrypted_bits, key

def encrypt(image_path, size=64, density=0.1):
    image_hash = fingertohash.generate_fingerprint_hash(image_path)
    encrypted_bits, final_key = encrypt_text(image_hash, size, density)
    return encrypted_bits, final_key

if __name__ == "__main__":
    image_path = "fingerprint.jpg"
    encrypted_bits, _ = encrypt(image_path)
    print(f"Encrypted Bits: {encrypted_bits}")

