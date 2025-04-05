import cv2
import hashlib


def load_and_preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    image = cv2.resize(image, (1024, 1024))
    
    image = cv2.GaussianBlur(image, (5, 5), 0)    
    return image

def extract_features(image):
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(image, None)
    
    return keypoints, descriptors

def hash_features(descriptors):
    descriptors_str = ''.join(descriptor.tobytes().decode('latin1') for descriptor in descriptors)
    
    sha512 = hashlib.sha512()
    sha512.update(descriptors_str.encode('latin1'))
    
    return sha512.hexdigest()

def generate_fingerprint_hash(image_path):
    image = load_and_preprocess_image(image_path)
    
    keypoints, descriptors = extract_features(image)
    
    if descriptors is None:
        print("No features detected in the fingerprint image.")
        return None
    
    hash_result = hash_features(descriptors)
    return hash_result


if __name__ == "__main__":
    image_path = "fingerprint.jpg" 
    hash_result = generate_fingerprint_hash(image_path)
    if hash_result:
        print("Hash of the fingerprint features:", hash_result)
