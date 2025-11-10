from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_db

auth_bp = Blueprint("auth", __name__)

# 🔹 Página de login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]

        conn = get_db()
        cur = conn.cursor()

        # Buscar primero en usuarios
        cur.execute("SELECT id, nombre, contrasena, rol FROM usuarios WHERE correo = ?", (correo,))
        usuario = cur.fetchone()

        # Buscar en técnicos si no es usuario
        if not usuario:
            cur.execute("SELECT id, nombre, contrasena FROM tecnicos WHERE correo = ?", (correo,))
            tecnico = cur.fetchone()

            if tecnico and tecnico["contrasena"] == contrasena:
                session["usuario_id"] = tecnico["id"]
                session["nombre"] = tecnico["nombre"]
                session["rol"] = "tecnico"
                conn.close()
                return redirect(url_for("tickets_bp.tickets_tecnico"))

            conn.close()
            return render_template("login.html", error="Credenciales incorrectas o usuario no registrado.")

        # Si es usuario normal o admin
        if usuario and usuario["contrasena"] == contrasena:
            session["usuario_id"] = usuario["id"]
            session["nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol"] or "usuario"
            conn.close()

            # Redirigir según el rol
            if usuario["rol"] == "admin":
                return redirect(url_for("admin_bp.dashboard"))
            elif usuario["rol"] == "tecnico":
                return redirect(url_for("tickets_bp.tickets_tecnico"))
            else:
                return redirect(url_for("tickets_bp.lista_tickets"))

        conn.close()
        return render_template("login.html", error="Credenciales incorrectas.")

    return render_template("login.html")


# 🔹 Página de registro
@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT id FROM usuarios WHERE correo = ?", (correo,))
        existente = cur.fetchone()

        if existente:
            return render_template("registro.html", error="Ya existe un usuario con este correo.")

        cur.execute(
            "INSERT INTO usuarios (nombre, correo, contrasena, rol) VALUES (?, ?, ?, ?)",
            (nombre, correo, contrasena, "usuario")
        )
        conn.commit()
        conn.close()
        return redirect(url_for("auth.login"))

    return render_template("registro.html")


# 🔹 Cerrar sesión
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
