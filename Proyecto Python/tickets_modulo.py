from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_db
import os
from werkzeug.utils import secure_filename
from datetime import datetime

tickets_bp = Blueprint("tickets_bp", __name__)

# =============================
# 📁 Configuración de archivos
# =============================
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf", "docx", "txt"}

# Crear carpeta de uploads si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    """Verifica si la extensión del archivo está permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# =============================
# 🎫 Tickets de usuarios
# =============================
@tickets_bp.route("/tickets")
def lista_tickets():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") == "tecnico":
        return redirect(url_for("tickets_bp.tickets_tecnico"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            t.id, 
            t.titulo, 
            t.descripcion, 
            t.estado, 
            t.prioridad, 
            t.asignado_a, 
            t.fecha, 
            t.archivo,
            t.fecha_inicio,
            t.fecha_finalizacion,
            t.descripcion_tecnico,
            u.nombre AS reportado_por
        FROM tickets t
        JOIN usuarios u ON t.usuario_id = u.id
        WHERE u.id = ?
        ORDER BY t.fecha DESC
    """, (session["usuario_id"],))
    tickets = cur.fetchall()
    conn.close()
    return render_template("tickets.html", tickets=tickets)


# =============================
# 👨‍🔧 Tickets asignados a técnico
# =============================
@tickets_bp.route("/tickets/tecnico")
def tickets_tecnico():
    if "usuario_id" not in session or session.get("rol") != "tecnico":
        return redirect(url_for("auth.login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            t.id, 
            t.titulo, 
            t.descripcion, 
            t.estado, 
            t.prioridad, 
            t.asignado_a, 
            t.fecha, 
            t.archivo,
            t.fecha_inicio,
            t.fecha_finalizacion,
            t.descripcion_tecnico,
            u.nombre AS reportado_por
        FROM tickets t
        LEFT JOIN usuarios u ON t.usuario_id = u.id
        WHERE t.asignado_a = ?
        ORDER BY t.fecha DESC
    """, (session["nombre"],))
    tickets = cur.fetchall()
    conn.close()
    return render_template("tickets_tecnico.html", tickets=tickets)


# =============================
# 🆕 Crear nuevo ticket (con archivo)
# =============================
@tickets_bp.route("/tickets/nuevo", methods=["GET", "POST"])
def nuevo_ticket():
    if "usuario_id" not in session or session.get("rol") != "usuario":
        return redirect(url_for("auth.login"))

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        # Obtener valores del formulario de forma segura
        titulo = request.form.get("titulo") or request.form.get("equipo", "")
        descripcion = request.form.get("descripcion", "")
        
        # Asignar prioridad fija (usuario ya no la elige)
        prioridad = "Media"

        # 📎 Manejo del archivo adjunto
        archivo = request.files.get("archivo")
        nombre_archivo = None

        if archivo and allowed_file(archivo.filename):
            nombre_archivo = secure_filename(archivo.filename)
            ruta_guardar = os.path.join(UPLOAD_FOLDER, nombre_archivo)
            archivo.save(ruta_guardar)
            nombre_archivo = f"{UPLOAD_FOLDER}/{nombre_archivo}"

        # 🎯 Asignar técnico automáticamente
        cur.execute("SELECT id, nombre FROM tecnicos ORDER BY id")
        tecnicos = cur.fetchall()

        cur.execute("SELECT COUNT(*) FROM tickets")
        total_tickets = cur.fetchone()[0]

        indice = total_tickets % len(tecnicos)
        tecnico_asignado = tecnicos[indice]["nombre"]

        # 💾 Guardar ticket en la base de datos
        cur.execute("""
            INSERT INTO tickets (titulo, descripcion, prioridad, asignado_a, usuario_id, archivo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (titulo, descripcion, prioridad, tecnico_asignado, session["usuario_id"], nombre_archivo))

        conn.commit()
        conn.close()
        return redirect(url_for("tickets_bp.lista_tickets"))

    conn.close()
    return render_template("nuevo_ticket.html")


# =============================
# 🔄 Actualizar estado (técnico)
# =============================
@tickets_bp.route("/tickets/actualizar_estado/<int:id>", methods=["POST"])

def actualizar_estado(id):
    if "usuario_id" not in session or session.get("rol") != "tecnico":
        return redirect(url_for("auth.login"))
    nuevo_estado = request.form.get("estado")
    comentario = request.form.get("comentario", "").strip()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not nuevo_estado:
        return redirect(url_for("tickets_bp.tickets_tecnico"))

    conn = get_db()
    cur = conn.cursor()

    # Guardar fechas y comentarios dependiendo del estado
    if nuevo_estado == "En proceso":
        cur.execute(
            "UPDATE tickets SET estado=?, fecha_inicio=? WHERE id=?",
            (nuevo_estado, ahora, id)
        )

    elif nuevo_estado in ("Resuelto", "Cancelado", "Cerrado por ausencia"):
        cur.execute(
            "UPDATE tickets SET estado=?, fecha_finalizacion=?, descripcion_tecnico=? WHERE id=?",
            (nuevo_estado, ahora, comentario, id)
        )

    else:
        cur.execute("UPDATE tickets SET estado=? WHERE id=?", (nuevo_estado, id))

    conn.commit()
    conn.close()

    return redirect(url_for("tickets_bp.tickets_tecnico"))
