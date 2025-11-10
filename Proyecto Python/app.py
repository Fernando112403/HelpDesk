from flask import Flask, render_template, redirect, url_for, session
from db import init_db
from auth import auth_bp
from tickets_modulo import tickets_bp
from admin_modulo import admin_bp  # 👈 asegúrate de que el archivo se llame igual

app = Flask(__name__)
app.secret_key = "clave_secreta_torogoz_2025"

# 🔹 Registrar los módulos (blueprints)
app.register_blueprint(auth_bp)
app.register_blueprint(tickets_bp)
app.register_blueprint(admin_bp)

# 🔹 Página principal — redirige según el rol del usuario
@app.route("/")
def index():
    if "usuario_id" in session:
        rol = session.get("rol")

        if rol == "admin":
            return redirect(url_for("admin_bp.dashboard"))
        elif rol == "tecnico":
            return redirect(url_for("tickets_bp.tickets_tecnico"))
        else:
            return redirect(url_for("tickets_bp.lista_tickets"))

    return redirect(url_for("auth.login"))

# 🔹 Ejecutar aplicación
if __name__ == "__main__":
    init_db()  # crea tablas si no existen
    app.run(debug=True)


