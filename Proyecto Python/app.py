from flask import Flask
from db import init_db
from auth import auth_bp
from tickets import tickets_bp

app = Flask(__name__)
app.secret_key = "clave_segura_123"  # cámbiala por seguridad

# Inicializar base de datos
init_db()

# Registrar rutas (módulos)
app.register_blueprint(auth_bp)
app.register_blueprint(tickets_bp)

if __name__ == "__main__":
    app.run(debug=True)

