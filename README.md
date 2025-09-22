# Crypto Simulator (Blockchain-focused)

Este proyecto es una **simulación de un exchange de criptomonedas** cuyo eje central es una **blockchain educativa** para registrar de forma inmutable las transacciones de compra/venta.  
Está desarrollado en **Python** y utiliza **AES (PyCryptodome)** para el cifrado de datos sensibles.

---

## 🧩 Descripción del proyecto (Idea principal)

La idea principal del proyecto es **aprender y demostrar cómo funciona una blockchain básica** aplicada a un mercado de criptomonedas.  
La blockchain actúa como un libro mayor (ledger) descentralizado, en el que cada transacción relevante (compra o venta) se registra dentro de un bloque. Cada bloque contiene:
- Un `index` (posición en la cadena).
- El `previous_hash` (hash del bloque anterior).
- Las `transactions` (datos de la transacción).
- Un `timestamp`.

La integridad de la cadena se protege usando **SHA-256** para el cálculo del `hash` de cada bloque, que se basa en el contenido del bloque (índice, hash previo, transacciones y tiempo). Esto permite detectar cualquier alteración en bloques pasados porque cambiar el contenido modificaría el hash y rompería la vinculación.

**Nota educativa:** Esta implementación es una **blockchain didáctica** (no es una implementación completa de una blockchain pública como Bitcoin o Ethereum):  
- No hay consenso distribuido (solo se guarda localmente en `blockchain.json`).  
- No hay minería ni prueba de trabajo (PoW) ni prueba de participación (PoS).  
- Está diseñada para enseñar los conceptos básicos de inmutabilidad, hashes y registro de transacciones.

---

## 🚀 Características

- Blockchain simple como ledger de transacciones.
- Registro inmutable de compras/ventas en `blockchain.json`.
- Registro y gestión de usuarios (saldo en USD y cripto).
- Almacenamiento cifrado de los datos de usuarios con **AES (CBC)**.
- Mercado de precios simulado que cambia periódicamente (thread).
- Operaciones básicas: depositar, retirar, comprar y vender criptomonedas.

---

## 📦 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/6Edgar9/Blockchain.git
   cd crypto-simulator
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / Mac
   venv\Scripts\activate    # Windows
   ```

3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta el programa:
   ```bash
   python main.py
   ```

---

## ⚙️ Requisitos

- Python 3.8 o superior
- Librerías externas:
  - `pycryptodome`

Instalación directa de la librería principal:
```bash
pip install pycryptodome
```

---

## 🛠️ Diseño técnico (resumen)

- `Block`:
  - Representa un bloque en la cadena.
  - Calcula su propio hash con SHA-256 sobre una serialización simple de sus campos.
  - `to_dict()` produce la representación que se guarda en JSON.

- `Blockchain`:
  - Carga la cadena desde `blockchain.json` (si existe).
  - Si la cadena está vacía, crea el bloque génesis.
  - `add_block(transactions)` añade un nuevo bloque apuntando al hash del último bloque y lo persiste.

- Cifrado:
  - `encrypt_data` y `decrypt_data` usan AES-CBC con `pad/unpad` y codificación en Base64 para persistencia segura de `users.json`.
  - **La clave AES por ahora está embebida en el código** (mejorar leyendo desde `.env` o keystore).

- Mercado:
  - `market.json` almacena el precio actual.
  - Un hilo en segundo plano actualiza el precio cada 10 segundos.

---

## 📂 Estructura del proyecto

```
crypto-simulator/
│── blo.py                  # Código principal
│── requirementos.txt       # Dependencias
│── README.md               # Documentación del proyecto
│── .gitignore              # Archivos ignorados en git
│── users.json              # Usuarios (cifrado con AES)
│── blockchain.json         # Blockchain con transacciones
│── market.json             # Mercado y precios actuales
```

---

## 📝 Riesgos y recomendaciones de seguridad

- **Contraseñas guardadas en texto plano** dentro del JSON (aunque cifradas en el archivo). Es preferible almacenar solo hashes (bcrypt/argon2) para autenticación.
- **Clave AES embebida**: moverla a variables de entorno o gestor de secretos.
- **Sin autenticación adicional** ni protección contra intentos de fuerza bruta.
- **No usar** este código para fondos reales ni entornos productivos sin auditoría y mejoras de seguridad.

---

## 🔧 Mejoras propuestas

- Implementar hashing seguro para contraseñas (`bcrypt` o `argon2`).
- Mover la clave AES a `.env` o un servicio de secretos.
- Añadir pruebas unitarias y validaciones de integridad de la blockchain (verificar `previous_hash`).
- Soporte para nodos remotos y mecanismo de consenso (para convertirlo en una blockchain distribuida real).
- Usar una base de datos (SQLite, PostgreSQL) para escalar almacenamiento.
- Añadir firma digital de transacciones (claves públicas/privadas) para autenticar operaciones.

---

## ⚠️ Advertencia

Este proyecto es **solo con fines educativos**.  
No debe usarse en producción ni para manejar datos financieros reales.

---

#### Dios, Assembly y la Patria
#### Edrem

Desarrollado con fines académicos y de práctica en Python.