import json
import os
import hashlib
import time
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import threading

# Archivos para almacenar datos
USER_FILE = "users.json"
BLOCKCHAIN_FILE = "blockchain.json"
MARKET_FILE = "market.json"
SECRET_KEY = b'12345678901234567890123456789012'  # Clave de 32 bytes para AES

# Clase Block
class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.transactions}{self.timestamp}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
        }

# Blockchain
class Blockchain:
    def __init__(self):
        self.chain = self.load_blockchain()
        if not self.chain:
            self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", [], time.time())
        self.chain.append(genesis_block)
        self.save_blockchain()

    def add_block(self, transactions):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), last_block.hash, transactions)
        self.chain.append(new_block)
        self.save_blockchain()

    def save_blockchain(self):
        with open(BLOCKCHAIN_FILE, "w") as file:
            json.dump([block.to_dict() for block in self.chain], file)

    def load_blockchain(self):
        if os.path.exists(BLOCKCHAIN_FILE):
            with open(BLOCKCHAIN_FILE, "r") as file:
                data = json.load(file)
                return [Block(block["index"], block["previous_hash"], block["transactions"], block["timestamp"]) for block in data]
        return []

# Funciones de cifrado AES

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + ciphertext).decode()

def decrypt_data(encrypted_data, key):
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size).decode()

# Gestión de usuarios
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            encrypted_data = file.read()
            if encrypted_data:
                return json.loads(decrypt_data(encrypted_data, SECRET_KEY))
    return {}

def save_users(users):
    encrypted_data = encrypt_data(json.dumps(users), SECRET_KEY)
    with open(USER_FILE, "w") as file:
        file.write(encrypted_data)

def register_user():
    users = load_users()
    username = input("Ingrese un nombre de usuario: ")
    if username in users:
        print("El usuario ya existe.")
        return
    password = input("Ingrese una contraseña: ")
    users[username] = {"password": password, "usd": 1000, "crypto": 0}
    save_users(users)
    print("Usuario registrado con éxito.")

def login():
    users = load_users()
    username = input("Usuario: ")
    password = input("Contraseña: ")
    if username in users and users[username]["password"] == password:
        print("Inicio de sesión exitoso.")
        return username
    print("Credenciales incorrectas.")
    return None

def view_balance(username):
    users = load_users()
    print(f"Saldo en USD: {users[username]['usd']}")
    print(f"Saldo en Crypto: {users[username]['crypto']}")

def get_crypto_price():
    if os.path.exists(MARKET_FILE):
        with open(MARKET_FILE, "r") as file:
            return json.load(file).get("price", 50.00)
    else:
        price = round(random.uniform(30, 70), 2)
        save_crypto_price(price)
        return price

def save_crypto_price(price):
    with open(MARKET_FILE, "w") as file:
        json.dump({"price": price}, file)

def update_crypto_price():
    while True:
        new_price = round(random.uniform(30, 70), 2)
        save_crypto_price(new_price)
        time.sleep(10)  # Actualiza el precio cada 10 segundos

def view_market():
    crypto_price = get_crypto_price()
    print(f"El precio actual de la criptomoneda es: {crypto_price} USD")

def deposit_money(username):
    users = load_users()
    amount = float(input("Ingrese la cantidad a depositar en USD: "))
    users[username]["usd"] += amount
    save_users(users)
    print("Depósito exitoso.")

def withdraw_money(username):
    users = load_users()
    amount = float(input("Ingrese la cantidad a retirar en USD: "))
    if users[username]["usd"] >= amount:
        users[username]["usd"] -= amount
        save_users(users)
        print("Retiro exitoso.")
    else:
        print("Fondos insuficientes.")

def buy_crypto(username, blockchain):
    users = load_users()
    crypto_price = get_crypto_price()
    amount = float(input(f"Ingrese la cantidad en USD para comprar criptomonedas (precio actual: {crypto_price} USD): "))
    if users[username]["usd"] >= amount:
        users[username]["usd"] -= amount
        users[username]["crypto"] += amount / crypto_price
        blockchain.add_block({"user": username, "action": "buy", "amount": amount, "price": crypto_price})
        save_users(users)
        print("Compra exitosa.")
    else:
        print("Fondos insuficientes.")

def sell_crypto(username, blockchain):
    users = load_users()
    crypto_price = get_crypto_price()
    amount = float(input(f"Ingrese la cantidad de criptomonedas a vender (precio actual: {crypto_price} USD): "))
    if users[username]["crypto"] >= amount:
        users[username]["crypto"] -= amount
        users[username]["usd"] += amount * crypto_price
        blockchain.add_block({"user": username, "action": "sell", "amount": amount, "price": crypto_price})
        save_users(users)
        print("Venta exitosa.")
    else:
        print("Fondos insuficientes.")

def main():
    blockchain = Blockchain()
    price_update_thread = threading.Thread(target=update_crypto_price)
    price_update_thread.daemon = True
    price_update_thread.start()
    
    while True:
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        option = input("Seleccione una opción: ")
        if option == "1":
            register_user()
        elif option == "2":
            user = login()
            if user:
                while True:
                    print("1. Ver saldo")
                    print("2. Ver mercado")
                    print("3. Depositar")
                    print("4. Retirar")
                    print("5. Comprar criptomonedas")
                    print("6. Vender criptomonedas")
                    print("7. Salir")
                    action = input("Seleccione una opción: ")
                    if action == "1":
                        view_balance(user)
                    elif action == "2":
                        view_market()
                    elif action == "3":
                        deposit_money(user)
                    elif action == "4":
                        withdraw_money(user)
                    elif action == "5":
                        buy_crypto(user, blockchain)
                    elif action == "6":
                        sell_crypto(user, blockchain)
                    elif action == "7":
                        break
        elif option == "3":
            break

if __name__ == "__main__":
    main()