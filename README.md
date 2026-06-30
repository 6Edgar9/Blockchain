# Crypto Simulator (Blockchain-focused) 🚀

Este proyecto es una **simulación de un exchange de criptomonedas y blockchain**, diseñado para enseñar y demostrar de forma interactiva y modular cómo interactúan las finanzas descentralizadas y las estructuras de datos inmutables. 

Está desarrollado íntegramente en **Python** (con PyCryptodome para la seguridad) y cuenta con una arquitectura modular que separa las responsabilidades de criptografía, mercado, usuarios y blockchain.

---

## 🧩 Descripción del proyecto

La idea central es actuar como un Exchange donde los usuarios depositan USD, observan las fluctuaciones del mercado en tiempo real, y compran o venden diferentes criptomonedas (BTC, ETH, SOL). Cada transacción que ocurre en este exchange se empaqueta y asegura criptográficamente en un **Libro Mayor (Blockchain)** descentralizado (simulado localmente en JSON).

El proyecto fue refactorizado y potenciado para incluir lógicas avanzadas presentes en exchanges y blockchains del mundo real.

---

## 🔥 Características Principales

*   **Proof of Work (Minería):** Cada bloque añadido a la cadena requiere que la computadora calcule un `nonce` hasta encontrar un Hash SHA-256 que comience con cuatro ceros consecutivos (`0000...`).
*   **Portafolio Multi-Criptomoneda:** Soporte transaccional para **BTC (Bitcoin), ETH (Ethereum) y SOL (Solana)**.
*   **Mercado Dinámico y Concurrencia:** Un hilo (Thread) en segundo plano fluctúa de manera independiente el precio de todas las criptomonedas, protegido por Mutex (`threading.Lock`) para evitar corrupción de datos.
*   **Comisiones (Fees):** El exchange cobra un **1%** estricto por cada transacción de compra o venta, cuyo cobro queda inmutado en la blockchain para auditoría.
*   **Precisión Financiera Total:** Se ha implementado la librería `decimal` de Python, erradicando los problemas del estándar IEEE-754 y evitando pérdidas o creación de fondos de la nada.
*   **Cifrado de Alta Seguridad:** Los datos sensibles de usuarios y contraseñas se resguardan bajo encriptación simétrica avanzada **AES-CBC** (256-bit).
*   **Validación de Integridad:** Cada vez que el programa arranca, verifica criptográficamente que la cadena no haya sido manipulada, recalculando y comprobando el `previous_hash` de toda la historia.

---

## 📂 Arquitectura Modular

El proyecto implementa el Principio de Responsabilidad Única para máxima mantenibilidad:

```text
Blockchain/
│── main.py                 # Punto de entrada. Interfaz CLI robusta con Try/Except.
│── blockchain.py           # Core lógico. Clases Block, Blockchain y minería (PoW).
│── users.py                # Lógica de registro, saldos y lógica de negocio (buy/sell/fee).
│── market.py               # Hilo de fondo y Lock para actualizar el valor de las criptos.
│── crypto_utils.py         # Abstracción limpia del cifrado AES (pad, unpad, base64).
│── config.py               # Constantes del programa (rutas JSON y SECRET_KEY).
│── requirements.txt        # Dependencias necesarias.
│── README.md               # Este archivo.
```

*(Nota: Los archivos `.json` se generan automáticamente al correr el programa).*

---

## 📦 Instalación y Uso

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/6Edgar9/Blockchain.git
   cd Blockchain
   ```

2. **Crea y activa un entorno virtual (Recomendado):**
   * En Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * En Linux/Mac:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instala las dependencias necesarias:**
   ```bash
   pip install pycryptodome
   ```
   *(Alternativamente, puedes usar `pip install -r requirements.txt` si existe).*

4. **Inicia el Simulador:**
   ```bash
   python main.py
   ```

---

## 📝 Riesgos y Advertencias

> [!WARNING]
> **Solo con fines educativos.** 
> * La clave AES se encuentra *hardcodeada* temporalmente en `config.py`. En un entorno real, debe inyectarse vía Variables de Entorno (`.env`) o Secret Managers.
> * Aunque el archivo está encriptado con AES, las contraseñas deberían someterse a hashing unidireccional (ej. `bcrypt` o `argon2`) antes de serializarse.
> * No hay consenso en red (P2P). La base de datos es puramente local, por lo que es vulnerable a borrados (Single Point of Failure).

---

#### Dios, Assembly y la Patria
#### Edrem

*Desarrollado con fines académicos para profundizar en la lógica del ecosistema criptográfico y buenas prácticas en Python.*