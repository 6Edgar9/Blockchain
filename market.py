import json
import os
import time
import random
import threading
from decimal import Decimal
from config import MARKET_FILE

# Lock para evitar colisiones al leer/escribir market.json al mismo tiempo
market_lock = threading.Lock()

# Monedas soportadas y sus rangos de precios aproximados para la simulación
SUPPORTED_CRYPTOS = {
    "BTC": (60000, 70000),
    "ETH": (3000, 4000),
    "SOL": (100, 200)
}

def get_all_crypto_prices():
    """Lee el precio actual de todas las criptomonedas."""
    with market_lock:
        if os.path.exists(MARKET_FILE):
            try:
                with open(MARKET_FILE, "r") as file:
                    data = json.load(file)
                    # Convertimos todos los precios a Decimal
                    return {k: Decimal(str(v)) for k, v in data.items()}
            except json.JSONDecodeError:
                pass
        
        # Si no existe o hubo error, generamos precios iniciales
        prices = {}
        for symbol, (min_p, max_p) in SUPPORTED_CRYPTOS.items():
            prices[symbol] = Decimal(str(round(random.uniform(min_p, max_p), 2)))
        _save_crypto_prices_internal(prices)
        return prices

def get_crypto_price(symbol):
    """Obtiene el precio de una moneda en específico."""
    prices = get_all_crypto_prices()
    return prices.get(symbol, Decimal("0.00"))

def save_crypto_prices(prices):
    """Guarda los precios asegurando el lock."""
    with market_lock:
        _save_crypto_prices_internal(prices)

def _save_crypto_prices_internal(prices):
    """Guarda el precio sin adquirir lock."""
    # Convertimos Decimal a str para guardar en JSON
    prices_str = {k: str(v) for k, v in prices.items()}
    with open(MARKET_FILE, "w") as file:
        json.dump(prices_str, file)

def update_crypto_price():
    """Hilo en segundo plano que actualiza todos los precios cada 10 segundos."""
    while True:
        new_prices = {}
        for symbol, (min_p, max_p) in SUPPORTED_CRYPTOS.items():
            new_prices[symbol] = Decimal(str(round(random.uniform(min_p, max_p), 2)))
        save_crypto_prices(new_prices)
        time.sleep(10)

def start_market_thread():
    """Inicia el hilo del mercado de forma controlada."""
    price_update_thread = threading.Thread(target=update_crypto_price)
    price_update_thread.daemon = True
    price_update_thread.start()

