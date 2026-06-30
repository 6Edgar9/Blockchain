import time
from decimal import Decimal, InvalidOperation
from blockchain import Blockchain
from market import start_market_thread, get_crypto_price, get_all_crypto_prices, SUPPORTED_CRYPTOS
import users

def get_valid_decimal(prompt):
    """Pide al usuario un número y asegura que sea un Decimal válido."""
    while True:
        user_input = input(prompt)
        try:
            amount = Decimal(user_input)
            if amount <= 0:
                print("[!] Ingresa una cantidad mayor a 0.")
                continue
            return amount
        except InvalidOperation:
            print("[!] Error: Por favor ingresa un número válido (ej. 100 o 50.5).")

def get_valid_symbol():
    """Pide al usuario una criptomoneda válida."""
    valid_symbols = list(SUPPORTED_CRYPTOS.keys())
    while True:
        symbol = input(f"Ingrese la criptomoneda ({', '.join(valid_symbols)}): ").strip().upper()
        if symbol in valid_symbols:
            return symbol
        print("[!] Criptomoneda no soportada.")

def main():
    print("Iniciando Simulador Blockchain...")
    
    # Iniciar blockchain y validar
    blockchain = Blockchain()
    
    # Iniciar hilo de precios (mercado)
    start_market_thread()
    
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        option = input("Seleccione una opción: ")
        
        if option == "1":
            users.register_user()
        elif option == "2":
            user = users.login()
            if user:
                while True:
                    print(f"\n=== PANEL DE USUARIO ({user}) ===")
                    print("1. Ver saldo completo")
                    print("2. Ver mercado de criptomonedas")
                    print("3. Depositar USD")
                    print("4. Retirar USD")
                    print("5. Comprar criptomonedas")
                    print("6. Vender criptomonedas")
                    print("7. Cerrar sesión")
                    
                    action = input("Seleccione una opción: ")
                    
                    if action == "1":
                        users.view_balance(user)
                    
                    elif action == "2":
                        print("\n=== PRECIOS DEL MERCADO ===")
                        prices = get_all_crypto_prices()
                        for sym, price in prices.items():
                            print(f"[*] {sym}: {price:.2f} USD")
                    
                    elif action == "3":
                        amount = get_valid_decimal("Ingrese la cantidad a depositar en USD: ")
                        users.deposit_money(user, amount)
                    
                    elif action == "4":
                        amount = get_valid_decimal("Ingrese la cantidad a retirar en USD: ")
                        users.withdraw_money(user, amount)
                    
                    elif action == "5":
                        symbol = get_valid_symbol()
                        crypto_price = get_crypto_price(symbol)
                        print(f"[*] Precio actual de {symbol}: {crypto_price:.2f} USD")
                        amount = get_valid_decimal("Ingrese la cantidad de USD a gastar: ")
                        users.buy_crypto(user, blockchain, symbol, amount)
                    
                    elif action == "6":
                        symbol = get_valid_symbol()
                        crypto_price = get_crypto_price(symbol)
                        print(f"[*] Precio actual de {symbol}: {crypto_price:.2f} USD")
                        amount = get_valid_decimal(f"Ingrese la cantidad de {symbol} a vender: ")
                        users.sell_crypto(user, blockchain, symbol, amount)
                    
                    elif action == "7":
                        print("Cerrando sesión...")
                        break
                    
                    else:
                        print("[!] Opción inválida.")
        
        elif option == "3":
            print("Saliendo del simulador...")
            break
        else:
            print("[!] Opción inválida.")

if __name__ == "__main__":
    main()

