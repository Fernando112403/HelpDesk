import sqlite3

DATABASE = "helpdesk.db"

# 🔹 Conexión a la base de datos
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# 🔹 Inicializar base de datos y tablas
def init_db():
    conn = get_db()
    cur = conn.cursor()  # ✅ <--- aquí definimos cur antes de ejecutar nada

    # Crear tabla de usuarios
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        )
    """)

    # Crear tabla de técnicos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tecnicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        )
    """)

    # Crear tabla de tickets
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            prioridad TEXT NOT NULL,
            estado TEXT DEFAULT 'Abierto',
            asignado_a TEXT,
            usuario_id INTEGER,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    # 🔹 Insertar técnicos iniciales solo si no existen
    cur.execute("SELECT COUNT(*) FROM tecnicos")
    if cur.fetchone()[0] == 0:
        tecnicos = [
        ("Fernando Rodriguez", "fernando.rodriguez@bancotorogoz.com.sv", "1234"),
        ("Pamela Coreas", "pamela.coreas@bancotorogoz.com.sv", "1234"),
        ("Alejandra Marquez", "alejandra.marquez@bancotorogoz.com.sv", "1234"),
        ("Jonathan Fuentes", "jonathan.fuentes@bancotorogoz.com.sv", "1234"),
        ("Diego Morales", "diego.morales@bancotorogoz.com.sv", "1234"),
        ]
        cur.executemany("INSERT INTO tecnicos (nombre, correo, contrasena) VALUES (?, ?, ?)", tecnicos)
        print("✅ Técnicos iniciales creados correctamente.")

    conn.commit()
    conn.close()
