// ticket-form.js - v3 Autocompletado visible en descripción
// 📌 Muestra las fallas más comunes según la categoría elegida

document.addEventListener("DOMContentLoaded", () => {
    const tituloInput = document.getElementById("titulo");
    const descripcion = document.getElementById("descripcion");

    // 📋 Diccionario de fallas comunes
    const fallasComunes = {
        "IMPRESORA": [
            "Sin tinta o tóner",
            "Atasco de papel",
            "No imprime",
            "Problema de red/driver"
        ],
        "LAPTOP": [
            "No enciende",
            "Pantalla azul / fallo SO",
            "Batería no carga",
            "Wi-Fi no conecta"
        ],
        "MONITOR": [
            "Pantalla negra",
            "Sin señal",
            "Flickering / parpadeo",
            "Colores distorsionados"
        ],
        "CPU": [
            "No arranca",
            "Ruido ventilador",
            "Sobrecalentamiento",
            "Perdida de datos"
        ],
        "TECLADO": [
            "Teclas no responden",
            "Conexión suelta",
            "Teclas pegadas"
        ],
        "MOUSE": [
            "Cursor no se mueve",
            "Problemas con el clic",
            "Desconexiones constantes"
        ],
        "ESCÁNER DE DOCUMENTOS": [
            "No detecta documentos",
            "Escaneo borroso",
            "Error de comunicación"
        ],
        "CAJERO AUTOMÁTICO (ATM)": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
        "CONTADORA DE BILLETES": [
            "Error al contar billetes",
            "Atasco frecuente",
            "Pantalla sin respuesta"
        ],
		"LECTOR DE TARJETAS": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"ROUTER": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"SERVIDOR": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"SISTEMA DE CÁMARAS CCTV": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"SISTEMA CORE BANCARIO": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"SISTEMA DE CAJA": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"SISTEMA DE CRÉDITOS": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"SISTEMA DE CAJA": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"SISTEMA DE CRÉDITOS": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"SISTEMA DE CLIENTES (CRM": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"SISTEMA DE PLANILLAS": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"SISTEMA DE TRANSACCIONES INTERNAS": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"CORREO CORPORATIVO": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"OFFICE 365": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"ANTIVIRUS CORPORATIVO": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"VPN INSTITUCIONAL": [
            "No dispensa efectivo",
            "Error de lectura de tarjeta",
            "Pantalla fuera de servicio"
        ],
		"FIRMAS DIGITALES": [
            "Certificado no reconocido",
            "Error al firmar",
            "Certificado expirado"
        ]
    };

    // 🔹 Contenedor de sugerencias (se mostrará debajo de la descripción)
    const contenedorSugerencias = document.createElement("div");
    contenedorSugerencias.style.marginTop = "10px";
    contenedorSugerencias.style.background = "#fff";
    contenedorSugerencias.style.border = "1px solid #ccc";
    contenedorSugerencias.style.borderRadius = "6px";
    contenedorSugerencias.style.boxShadow = "0 2px 8px rgba(0,0,0,0.1)";
    contenedorSugerencias.style.padding = "8px";
    contenedorSugerencias.style.display = "none";
    contenedorSugerencias.style.maxWidth = "100%";
    contenedorSugerencias.style.fontSize = "14px";
    contenedorSugerencias.style.cursor = "pointer";

    // Insertamos el contenedor justo después del campo de descripción
    descripcion.parentNode.insertBefore(contenedorSugerencias, descripcion.nextSibling);

    // 🎯 Escuchar cuando el usuario cambia el tipo de equipo
    tituloInput.addEventListener("input", () => {
        const categoria = tituloInput.value.trim().toUpperCase();
        contenedorSugerencias.innerHTML = "";
        contenedorSugerencias.style.display = "none";

        if (fallasComunes[categoria]) {
            const titulo = document.createElement("strong");
            titulo.textContent = "Fallas comunes:";
            contenedorSugerencias.appendChild(titulo);

            fallasComunes[categoria].forEach(falla => {
                const item = document.createElement("div");
                item.textContent = "• " + falla;
                item.style.padding = "6px 0";
                item.style.color = "#333";

                item.addEventListener("mouseover", () => {
                    item.style.background = "#f4f7fb";
                });
                item.addEventListener("mouseout", () => {
                    item.style.background = "white";
                });
                item.addEventListener("click", () => {
                    descripcion.value = falla;
                    contenedorSugerencias.style.display = "none";
                });

                contenedorSugerencias.appendChild(item);
            });

            contenedorSugerencias.style.display = "block";
        }
    });

    // 🧹 Ocultar sugerencias si se hace clic fuera
    document.addEventListener("click", (e) => {
        if (!contenedorSugerencias.contains(e.target) && e.target !== tituloInput) {
            contenedorSugerencias.style.display = "none";
        }
    });
});
