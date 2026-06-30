import json
import os
import hashlib
import time
from config import BLOCKCHAIN_FILE

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Convertimos las transacciones a string para asegurar consistencia
        transactions_str = json.dumps(self.transactions, sort_keys=True)
        block_string = f"{self.index}{self.previous_hash}{transactions_str}{self.timestamp}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"[*] ¡Bloque minado! Hash: {self.hash}")

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4  # Dificultad del Proof of Work
        self.load_blockchain()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", [], time.time())
        print("Minando bloque génesis...")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        self.save_blockchain()

    def add_block(self, transactions):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), last_block.hash, transactions)
        print("Minando nuevo bloque...")
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_blockchain()

    def save_blockchain(self):
        with open(BLOCKCHAIN_FILE, "w") as file:
            json.dump([block.to_dict() for block in self.chain], file)

    def load_blockchain(self):
        """Carga la blockchain desde el JSON y valida su integridad."""
        if os.path.exists(BLOCKCHAIN_FILE):
            try:
                with open(BLOCKCHAIN_FILE, "r") as file:
                    data = json.load(file)
                    # Aquí recreamos la cadena usando los datos guardados (incluyendo el hash anterior y el nonce)
                    self.chain = []
                    for block in data:
                        b = Block(block["index"], block["previous_hash"], block["transactions"], block["timestamp"], block.get("nonce", 0))
                        b.hash = block["hash"] # Forzamos el hash guardado para la validación
                        self.chain.append(b)
                
                # Validar la cadena al cargar
                if not self.is_chain_valid():
                    print("\n[!] ADVERTENCIA: La blockchain ha sido alterada. Se creará una nueva desde cero por seguridad.")
                    self.chain = []
                    self.create_genesis_block()
            except (json.JSONDecodeError, KeyError):
                print("\n[!] Error al leer la blockchain. Se creará una nueva.")
                self.chain = []
                self.create_genesis_block()
        else:
            self.create_genesis_block()

    def is_chain_valid(self):
        """Valida que cada bloque contenga el hash previo correcto y que su propio hash sea válido."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Verificar si el hash almacenado coincide con el hash recalculado
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Verificar si apunta correctamente al hash del bloque anterior
            if current_block.previous_hash != previous_block.hash:
                return False

        return True
