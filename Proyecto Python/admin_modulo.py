from flask import Blueprint, render_template, session, redirect, url_for
from db import get_db

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
def dashboard():
    if "usuario_id" not in session or session.get("rol") != "admin":
        return redirect(url_for("auth.login"))

    conn = get_db()
    cur = conn.cursor()

    # Total de tickets
    cur.execute("SELECT COUNT(*) FROM tickets")
    row = cur.fetchone()
    total_tickets = row[0] if row else 0

    # Tickets por estado
    cur.execute("""
        SELECT estado, COUNT(*) as cantidad 
        FROM tickets 
        GROUP BY estado
    """)
    tickets_estado = cur.fetchall() or []

    # Tickets por técnico
    cur.execute("""
        SELECT asignado_a, COUNT(*) as cantidad 
        FROM tickets 
        GROUP BY asignado_a
    """)
    tickets_tecnico = cur.fetchall() or []

    # Promedio de resolución (si hay datos)
    cur.execute("""
        SELECT AVG(julianday(fecha_cierre) - julianday(fecha)) as promedio
        FROM tickets
        WHERE fecha_cierre IS NOT NULL
    """)
    row = cur.fetchone()
    promedio_resolucion = round(row["promedio"], 2) if row and row["promedio"] else 0

    conn.close()

    return render_template("admin_dashboard.html",
                           total_tickets=total_tickets,
                           tickets_estado=tickets_estado,
                           tickets_tecnico=tickets_tecnico,
                           promedio_resolucion=promedio_resolucion)

