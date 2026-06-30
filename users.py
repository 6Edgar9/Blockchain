import json
import os
from decimal import Decimal
from config import USER_FILE, SECRET_KEY
from crypto_utils import encrypt_data, decrypt_data
from market import get_crypto_price, SUPPORTED_CRYPTOS

def load_users():
    """Carga y desencripta el archivo de usuarios."""
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            encrypted_data = file.read()
            if encrypted_data:
                decrypted = decrypt_data(encrypted_data, SECRET_KEY)
                if decrypted:
                    try:
                        return json.loads(decrypted)
                    except json.JSONDecodeError:
                        return {}
    return {}

def save_users(users):
    """Encripta y guarda los usuarios."""
    encrypted_data = encrypt_data(json.dumps(users), SECRET_KEY)
    with open(USER_FILE, "w") as file:
        file.write(encrypted_data)

def register_user():
    """Registra a un nuevo usuario."""
    users = load_users()
    username = input("Ingrese un nombre de usuario: ")
    if username in users:
        print("[!] El usuario ya existe.")
        return
    password = input("Ingrese una contraseña: ")
    
    # Inicializar balances para cada moneda soportada
    initial_balances = {symbol: "0.00" for symbol in SUPPORTED_CRYPTOS.keys()}
    users[username] = {"password": password, "usd": "1000.00", "balances": initial_balances}
    
    save_users(users)
    print("[+] Usuario registrado con éxito. ¡Se te han obsequiado 1000 USD de bienvenida!")

def login():
    """Valida credenciales de un usuario."""
    users = load_users()
    username = input("Usuario: ")
    password = input("Contraseña: ")
    
    if username in users and users[username]["password"] == password:
        print("[+] Inicio de sesión exitoso.")
        return username
    
    print("[!] Credenciales incorrectas.")
    return None

def view_balance(username):
    """Muestra el balance actual de USD y de todas las Criptos."""
    users = load_users()
    print(f"Saldo en USD: {Decimal(users[username]['usd']):.2f}")
    print("Portafolio de Criptomonedas:")
    for symbol, amount in users[username]["balances"].items():
        print(f"  - {symbol}: {Decimal(amount):.8f}")

def deposit_money(username, amount):
    """Deposita USD a la cuenta."""
    users = load_users()
    current_usd = Decimal(users[username]["usd"])
    users[username]["usd"] = str(current_usd + amount)
    save_users(users)
    print(f"[+] Depósito exitoso de {amount:.2f} USD.")

def withdraw_money(username, amount):
    """Retira USD de la cuenta."""
    users = load_users()
    current_usd = Decimal(users[username]["usd"])
    
    if current_usd >= amount:
        users[username]["usd"] = str(current_usd - amount)
        save_users(users)
        print(f"[+] Retiro exitoso de {amount:.2f} USD.")
    else:
        print("[!] Fondos insuficientes.")

def buy_crypto(username, blockchain, symbol, amount_usd):
    """Compra criptomoneda cobrando 1% de fee y registra en blockchain."""
    users = load_users()
    crypto_price = get_crypto_price(symbol)
    current_usd = Decimal(users[username]["usd"])
    
    if current_usd >= amount_usd:
        # Cobrar comisión del 1%
        fee = amount_usd * Decimal("0.01")
        amount_after_fee = amount_usd - fee
        
        # Calcular criptos recibidas
        crypto_bought = amount_after_fee / crypto_price
        
        users[username]["usd"] = str(current_usd - amount_usd)
        
        # Por si el usuario es viejo y no tiene el balance de esa moneda
        if symbol not in users[username].get("balances", {}):
             users[username].setdefault("balances", {})[symbol] = "0.00"
             
        users[username]["balances"][symbol] = str(Decimal(users[username]["balances"][symbol]) + crypto_bought)
        save_users(users)
        
        # Registrar en la cadena
        blockchain.add_block({
            "user": username,
            "action": "buy",
            "symbol": symbol,
            "amount_usd_total": str(amount_usd),
            "fee_usd": str(fee),
            "price_usd": str(crypto_price),
            "crypto_amount": str(crypto_bought)
        })
        print(f"[+] Compra exitosa: {crypto_bought:.8f} {symbol} a {crypto_price} USD/unidad.")
        print(f"    Comisión cobrada (1%): {fee:.2f} USD")
    else:
        print("[!] Fondos en USD insuficientes.")

def sell_crypto(username, blockchain, symbol, amount_crypto):
    """Vende criptomoneda cobrando 1% de fee y registra en blockchain."""
    users = load_users()
    crypto_price = get_crypto_price(symbol)
    
    # Manejar balances viejos
    if "balances" not in users[username]:
         users[username]["balances"] = {s: "0.00" for s in SUPPORTED_CRYPTOS.keys()}
    if symbol not in users[username]["balances"]:
         users[username]["balances"][symbol] = "0.00"
         
    current_crypto = Decimal(users[username]["balances"][symbol])
    
    if current_crypto >= amount_crypto:
        # Calcular USD recibidos antes del fee
        usd_gross = amount_crypto * crypto_price
        
        # Cobrar 1% de comisión de los USD recibidos
        fee = usd_gross * Decimal("0.01")
        usd_net = usd_gross - fee
        
        users[username]["balances"][symbol] = str(current_crypto - amount_crypto)
        users[username]["usd"] = str(Decimal(users[username]["usd"]) + usd_net)
        save_users(users)
        
        # Registrar en la cadena
        blockchain.add_block({
            "user": username,
            "action": "sell",
            "symbol": symbol,
            "amount_crypto": str(amount_crypto),
            "price_usd": str(crypto_price),
            "usd_received_net": str(usd_net),
            "fee_usd": str(fee)
        })
        print(f"[+] Venta exitosa: Recibiste {usd_net:.2f} USD a {crypto_price} USD/unidad.")
        print(f"    Comisión cobrada (1%): {fee:.2f} USD")
    else:
        print(f"[!] Fondos de {symbol} insuficientes.")

