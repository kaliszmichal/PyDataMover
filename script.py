#test lokalnie
import os
import base64
from cryptography.fernet import Fernet

def load_or_generate_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        print("[+] Wygenerowano nowy klucz i zapisano w 'secret.key'")
    else:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

# 2. Funkcja szyfrująca nazwy plików
def encrypt_filenames(directory_path, cipher):
    print(f"\n[!] Szyfrowanie plików w katalogu: {directory_path}")
    
    for filename in os.listdir(directory_path):
        # Pomijamy sam skrypt, klucz oraz pliki już zaszyfrowane
        if filename in ["encrypt_filenames.py", "secret.key"] or filename.startswith("ENC_"):
            continue
            
        full_path = os.path.join(directory_path, filename)
        
        if os.path.isfile(full_path):
            # Szyfrujemy samą nazwę pliku (zakodowaną do bajtów)
            encrypted_bytes = cipher.encrypt(filename.encode('utf-8'))
            # Zamieniamy na bezpieczny tekst base64, aby system operacyjny przyjął nazwę pliku
            encrypted_name = "ENC_" + base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')
            
            new_path = os.path.join(directory_path, encrypted_name)
            os.rename(full_path, new_path)
            print(f"Zaszyfrowano: {filename} -> {encrypted_name[:30]}...")

# 3. Funkcja odszyfrowująca nazwy plików
def decrypt_filenames(directory_path, cipher):
    print(f"\n[!] Odszyfrowywanie plików w katalogu: {directory_path}")
    
    for filename in os.listdir(directory_path):
        if filename.startswith("ENC_"):
            full_path = os.path.join(directory_path, filename)
            
            if os.path.isfile(full_path):
                try:
                    # Wyciągamy samą zaszyfrowaną część z nazwy pliku
                    pure_encrypted = filename.replace("ENC_", "").encode('utf-8')
                    encrypted_bytes = base64.urlsafe_b64decode(pure_encrypted)
                    
                    # Odszyfrowujemy i dekodujemy z powrotem na tekst
                    decrypted_name = cipher.decrypt(encrypted_bytes).decode('utf-8')
                    
                    new_path = os.path.join(directory_path, decrypted_name)
                    os.rename(full_path, new_path)
                    print(f"Odszyfrowano: {filename[:20]}... -> {decrypted_name}")
                except Exception as e:
                    print(f"[-] Błąd podczas odszyfrowywania {filename}: {e}")

# --- GŁÓWNY PROGRAM ---
if __name__ == "__main__":
    # Ścieżka do folderu z plikami (kropka oznacza bieżący folder, w którym jest skrypt)
    TARGET_DIR = "./" 
    
    cipher_suite = load_or_generate_key()
    
    wybor = input("Co chcesz zrobić? (1 - Szyfruj nazwy, 2 - Odszyfruj nazwy): ")
    
    if wybor == "1":
        encrypt_filenames(TARGET_DIR, cipher_suite)
    elif wybor == "2":
        decrypt_filenames(TARGET_DIR, cipher_suite)
    else:
        print("Nieprawidłowy wybór.")
