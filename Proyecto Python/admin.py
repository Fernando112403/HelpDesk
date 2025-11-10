from flask import Blueprint, render_template, session, redirect, url_for
from db import get_db

admin_bp = Blueprint("admin_bp", __name__)

# 🧠 Decorador simple de protección
def admin_required(func):
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session or session.get("rol") != "admin":
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# 📊 Panel principal
@admin_bp.route("/admin/dashboard")
@admin_required
def dashboard():
    conn = get_db()
    cur = conn.cursor()

    # Tickets por estado
    cur.execute("""
        SELECT estado, COUNT(*) AS total 
        FROM tickets 
        GROUP BY estado
    """)
    tickets_por_estado = cur.fetchall()

    # Tickets por técnico
    cur.execute("""
        SELECT asignado_a, COUNT(*) AS total 
        FROM tickets 
        GROUP BY asignado_a
    """)
    tickets_por_tecnico = cur.fetchall()

    # Promedio de resolución (en días)
    cur.execute("""
        SELECT AVG(
            JULIANDAY(fecha_cierre) - JULIANDAY(fecha)
        ) AS promedio_dias
        FROM tickets
        WHERE estado = 'Resuelto' AND fecha_cierre IS NOT NULL
    """)
    promedio = cur.fetchone()["promedio_dias"] if cur.fetchone() else None

    conn.close()
    return render_template(
        "admin_dashboard.html",
        tickets_por_estado=tickets_por_estado,
        tickets_por_tecnico=tickets_por_tecnico,
        promedio=promedio
    )
