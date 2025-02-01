import fingertohash
import numpy as np
import time
import cirq
from hashlib import sha256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# تبدیل هش به آرایه بایت
def hash_to_bytes(hash_value):
    if isinstance(hash_value, str):
        hash_value = bytes.fromhex(hash_value)
    return hash_value


# رمزنگاری با پروتکل BB84
def bb84_encode(hash_value):
    hash_bytes = hash_to_bytes(hash_value)
    qubits = [cirq.GridQubit(i, 0) for i in range(len(hash_bytes) * 8)]
    circuit = cirq.Circuit()
    for i, byte in enumerate(hash_bytes):
        for bit in range(8):
            if (byte >> bit) & 1:
                circuit.append(cirq.X(qubits[i * 8 + bit]))
            else:
                circuit.append(cirq.H(qubits[i * 8 + bit]))
    circuit.append(cirq.measure(*qubits, key='result'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    encoded_hash = np.array(list(result.measurements['result'][0])).astype(int)
    key = sha256(encoded_hash.tobytes()).digest()
    return encoded_hash, key

# رمزنگاری با پروتکل BB84 اصلاح‌شده
def bb84_encode2(hash_value):
    hash_bytes = hash_to_bytes(hash_value)
    qubits = [cirq.GridQubit(i, 0) for i in range(len(hash_bytes) * 8)]
    circuit = cirq.Circuit()
    for i, byte in enumerate(hash_bytes):
        for bit in range(8):
            if (byte >> bit) & 1:
                circuit.append(cirq.X(qubits[i * 8 + bit]))
            else:
                circuit.append(cirq.H(qubits[i * 8 + bit]))
                circuit.append(cirq.T(qubits[i * 8 + bit]))  # استفاده از گیت T
    circuit.append(cirq.measure(*qubits, key='result'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    encoded_hash = np.array(list(result.measurements['result'][0])).astype(int)
    key = sha256(encoded_hash.tobytes()).digest()
    return encoded_hash, key

# رمزنگاری با پروتکل B92
def b92_encode(hash_value):
    hash_bytes = hash_to_bytes(hash_value)
    qubits = [cirq.GridQubit(i, 0) for i in range(len(hash_bytes) * 8)]
    circuit = cirq.Circuit()
    for i, byte in enumerate(hash_bytes):
        for bit in range(8):
            if (byte >> bit) & 1:
                circuit.append(cirq.X(qubits[i * 8 + bit]))
            circuit.append(cirq.measure(qubits[i * 8 + bit], key=f'm{i * 8 + bit}'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    encoded_hash = np.array([result.measurements[f'm{i * 8 + bit}'][0][0] for i in range(len(hash_bytes)) for bit in range(8)]).astype(int)
    key = sha256(encoded_hash.tobytes()).digest()
    return encoded_hash, key

# رمزنگاری با پروتکل RSA
def rsa_encrypt(hash_value):
    hash_bytes = hash_to_bytes(hash_value)
    key = RSA.generate(2048, e=65537)
    public_key = key.publickey()
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_hash = cipher.encrypt(hash_bytes)  # رمزنگاری بدون استفاده از چانک‌ها
    return encrypted_hash, key.export_key()

# تبدیل بایت به آرایه‌ای از بیت‌ها
def bytes_to_bits(byte_array):
    bits = []
    for byte in byte_array:
        for i in range(8):
            bits.append((byte >> i) & 1)
    return bits

# تابع بهینه‌سازی الگوریتم‌های کوانتومی
def optimized_quantum_encrypt(hash_value):
    hash_bytes = hash_to_bytes(hash_value)
    qubits = [cirq.GridQubit(i, 0) for i in range(len(hash_bytes) * 8)]
    circuit = cirq.Circuit()
    for i, byte in enumerate(hash_bytes):
        for bit in range(8):
            if (byte >> bit) & 1:
                circuit.append(cirq.X(qubits[i * 8 + bit]))
                circuit.append(cirq.Z(qubits[i * 8 + bit]))  # استفاده از گیت Z
            else:
                circuit.append(cirq.H(qubits[i * 8 + bit]))
                circuit.append(cirq.T(qubits[i * 8 + bit]))  # استفاده از گیت T
    circuit.append(cirq.measure(*qubits, key='result'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=3)
    encoded_hash = np.array(list(result.measurements['result'][0])).astype(int)
    key = sha256(encoded_hash.tobytes()).digest()
    return encoded_hash, key

# تابع رمزنگاری با پروتکل‌های مختلف
def quantum_encrypt(hash_value, method='BB84'):
    start_time = time.time()
    if method == 'BB84':
        encoded_hash, key = bb84_encode(hash_value)
    elif method == 'B92':
        encoded_hash, key = b92_encode(hash_value)
    elif method == 'RSA':
        encoded_hash, key = rsa_encrypt(hash_value)
    elif method == 'OptimizedQuantum':
        encoded_hash, key = optimized_quantum_encrypt(hash_value)
    elif method == '2':
        encoded_hash, key = bb84_encode2(hash_value)
    end_time = time.time()
    encryption_time = end_time - start_time
    return encoded_hash, key, round(encryption_time, 3)

# بررسی امنیت و پیچیدگی
def evaluate_security_and_complexity(method, encoded_hash, hash_value, key, encryption_time):
    key_length = len(key)
    # تبدیل هش به آرایه بایت در صورت لزوم
    if isinstance(hash_value, str):
        hash_value = hash_to_bytes(hash_value)
    # تبدیل encoded_hash به آرایه NumPy
    encoded_hash_np = np.frombuffer(encoded_hash, dtype=np.uint8) if isinstance(encoded_hash, bytes) else np.array(encoded_hash, dtype=np.uint8)
    hash_value_np = np.frombuffer(hash_value, dtype=np.uint8)

    # پد کردن آرایه‌ها به اندازه مشابه
    max_length = max(len(encoded_hash_np), len(hash_value_np))
    padded_encoded_hash_np = np.pad(encoded_hash_np, (0, max_length - len(encoded_hash_np)), constant_values=0)
    padded_hash_value_np = np.pad(hash_value_np, (0, max_length - len(hash_value_np)), constant_values=0)

    changed_bits = np.sum(padded_encoded_hash_np.flatten() != padded_hash_value_np.flatten())
    
    # تبدیل بایت به بیت‌ها برای RSA
    encrypted_hash_bits = bytes_to_bits(encoded_hash_np.tobytes()) if isinstance(encoded_hash, np.ndarray) else bytes_to_bits(encoded_hash)
    
    return {
        'method': method,
        'key_length': key_length,
        'changed_bits': changed_bits,
        'encrypted_hash': encrypted_hash_bits,
        'encryption_time': encryption_time
    }

# تابع مقایسه مدل‌ها
def compare_models(hash_value):
    results = []
    methods = ['BB84', 'B92', 'RSA', 'OptimizedQuantum', '2']
    for method in methods:
        encoded_hash, key, encryption_time = quantum_encrypt(hash_value, method=method)
        results.append(evaluate_security_and_complexity(method, encoded_hash, hash_value, key, encryption_time))
    return results

# بارگذاری هش تصویر اثر انگشت
fingerprint_hash = fingertohash.generate_fingerprint_hash('fingerprint2.jpg')

# مقایسه مدل‌ها
results = compare_models(fingerprint_hash)
for result in results:
    pass
    #print(f"Method: {result['method']}, Key Length: {result['key_length']} bytes, Changed Bits: {result['changed_bits']}, Encryption Time: {result['encryption_time']} seconds")
    #print(f"Encrypted Hash: {result['encrypted_hash']}")
