import socket
import hashlib
import os
import sqlite3
from Crypto.Cipher import DES
from urllib.parse import urlparse

# This file contains multiple Python functions that intentionally demonstrate common security vulnerabilities and coding pitfalls. 
# The file provides examples for issues such as weak cryptography, SQL injection, incomplete sanitization, and more, likely for 
# educational or testing purposes.
# Last updated on 2025-10-22 @ 9:34 PM by @DaveOps30

# BIND_SOCKET_ALL_NETWORK_INTERFACES test
def bind_socket_to_all_interfaces():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 8080))  # Binds to all network interfaces (0.0.0.0)
    sock.listen(5)
    conn, addr = sock.accept()
    print(f"Connection established with {addr}")
    conn.close()

# CA5350: Do Not Use Weak Cryptographic Algorithms
def weak_cryptography():
    des = DES.new('12345678', DES.MODE_ECB)  # DES is considered a weak algorithm
    plaintext = 'Sensitive Data'
    encrypted_text = des.encrypt(
        plaintext
        .ljust(64)
        .encode())
    print(f"Encrypted text: {encrypted_text}")

# SQL_INJECTION
def sql_injection(user_input):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{user_input}'"  # Vulnerable to SQL injection
    cursor.execute(query)
    rows = cursor.fetchall()
    print("User data:", rows)
    conn.close()

# INCOMPLETE_SANTIZATION
def incomplete_sanitization(user_input):
    dangerous_chars = ['<', '>', '\"', '\'', ';']
    for char in dangerous_chars:
        user_input = user_input.replace(char, '')  # Incomplete sanitization
    print(f"Sanitized user input: {user_input}")

# INCOMPLETE_URL_SUBSTRING_SANITIZATION
def incomplete_url_substring_sanitization(url):
    parsed_url = urlparse(url)
    if "http" in parsed_url.scheme:  # Incomplete sanitization
        print(f"Valid URL: {url}")
    else:
        print(f"Invalid URL: {url}")

# WEAK_CRYPTOGRAPHIC_ALGORITHM
def weak_hashing(data):
    hashed_data = hashlib.md5(data.encode()).hexdigest()  # MD5 is considered weak
    print(f"MD5 hashed data: {hashed_data}")

# CONDITIONALLY_UNINITIALIZED_VARIABLE
def conditionally_uninitialized_variable(flag):
    if flag:
        value = "Initialized"
    print(value)  # This will fail if flag is False

# SIZEOF_PTR
def sizeof_ptr_issue():
    array = [1, 2, 3]
    pointer_size = len(array) * 8  # Incorrect calculation mimicking sizeof(ptr)
    print(f"Pointer size: {pointer_size}")

def main():
    bind_socket_to_all_interfaces()
    
    weak_cryptography()

    user_input = "'; DROP TABLE users; --"
    sql_injection(user_input)
    
    incomplete_sanitization("<script>alert('XSS')</script>")

    incomplete_url_substring_sanitization("http://example.com")
    
    weak_hashing("Sensitive Information")
    
    conditionally_uninitialized_variable(False)
    
    sizeof_ptr_issue()

if __name__ == "__main__":
    main()
