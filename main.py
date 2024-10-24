import random

#Person class to initiate sender and receiver
class Person():
    
    def __init__(self, name, sent_message="", received_message="", shared_key=""):
        self.name = name
        self.sent_message = sent_message
        self.received_message = received_message
        self.shared_key = shared_key
        
    def whoami(self):
        print(f"Hi my name is {self.name}")
        
    def writeMessage(self, text):
        self.sent_message = text
        return self.sent_message
    
    def receivedMessage(self, text):
        self.received_message = text
        return self.received_message


#functions to implement RSA
# Step 1: Generate large prime numbers (p, q)
def miller_rabin_test(n, k=40):  # k is the number of iterations
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n == 1:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime_candidate(length):
    while True:
        candidate = random.getrandbits(length)
        if candidate % 2 != 0 and miller_rabin_test(candidate):
            return candidate


def generate_keypair(keysize):
    p = generate_prime_candidate(keysize // 2)
    q = generate_prime_candidate(keysize // 2)
    
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # Standard value for e
    d = pow(e, -1, phi)  # Modular inverse of e

    return ((e, n), (d, n))  # Public key, Private key

# Step 2: Encrypt and Decrypt Functions
def encrypt(public_key, plaintext):
    e, n = public_key
    # Convert the message to an integer (plaintext should be smaller than n)
    message = int.from_bytes(plaintext.encode(), 'big')
    ciphertext = pow(message, e, n)
    return ciphertext

def decrypt(private_key, ciphertext):
    d, n = private_key
    # Decrypt and convert integer back to string
    message = pow(ciphertext, d, n)
    plaintext = message.to_bytes((message.bit_length() + 7) // 8, 'big').decode()
    return plaintext

# Step 3: Demonstration
keysize = 1024
public_key, private_key = generate_keypair(keysize)



#Simulation of End-to-End Encryption
alice = Person("Alice")
bob = Person("Bob")

#testing with print statements
alice.writeMessage("Hi Bob")
message = alice.sent_message
print("Original Message:", message)

print(f"\n")

# Encrypt the message
ciphertext = encrypt(public_key, message)
print(f"Ciphertext: {ciphertext} \nwith public key: {public_key}")

print(f"\n")

# Decrypt the message
decrypted_message = decrypt(private_key, ciphertext)
print(f"Decrypted Message: {decrypted_message} \nwith private key: {private_key}")