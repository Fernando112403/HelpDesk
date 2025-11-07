from flask import Blueprint, render_template, request, redirect, session
from db import get_connection
import hashlib

auth_bp = Blueprint("auth", __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        password = request.form["password"].strip()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
        u = cur.fetchone()
        conn.close()
        if u and u["password"] == hash_password(password):
            session["usuario"] = usuario
            session["rol"] = u["rol"]
            return redirect("/")
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")
    return render_template("login.html")

@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        password = request.form["password"].strip()
        rol = request.form.get("rol", "usuario")  # se elige 'usuario' o 'tecnico'
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)",
                (usuario, hash_password(password), rol),
            )
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return render_template("register.html", error="Usuario ya existe")
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
