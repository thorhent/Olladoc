import datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from gi.repository import Gtk, Gio, GLib

def guardar_historia_clinica_pdf(widget, datos_historia_clinica, modelo, idHC):
    # Paso 1: Diálogo para elegir carpeta
    file_dialog = Gtk.FileDialog()
    file_dialog.set_title("Guardar HC")
    
    # Crear sugerencia de nombre de archivo
    fecha_actual = datetime.date.today().isoformat()
    nombre_archivo = f"HC_{fecha_actual}_{modelo}_{idHC}.pdf"

    # Crear sugerencia de archivo
    initial_file = Gio.File.new_for_path(GLib.get_home_dir() + "/" + nombre_archivo)
    file_dialog.set_initial_file(initial_file)

    file_dialog.save(
        widget,
        None,
        lambda dialog, result: _on_guardar_pdf_resultado(dialog, result, datos_historia_clinica, widget)
    )
    

def _on_guardar_pdf_resultado(dialog, result, datos_historia_clinica, widget):
    try:
        archivo = dialog.save_finish(result)
        ruta = archivo.get_path()
        if not ruta.endswith(".pdf"):
            ruta += ".pdf"

        generar_pdf_historia_clinica(ruta, datos_historia_clinica)

        # Emitir señal o directamente lanzar toast
        if hasattr(widget, "toast_overlay"):
            from gi.repository import Adw
            toast = Adw.Toast.new("Historia clínica guardada correctamente.")
            widget.toast_overlay.add_toast(toast)
        

    except GLib.Error as e:
        print(f"Error al guardar archivo: {e.message}")

def generar_pdf_historia_clinica(ruta, datos):
    c = canvas.Canvas(ruta, pagesize=A4)
    c.setTitle("Historia Clínica")
    ancho, alto = A4
    y = alto - 50  # Margen superior

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Historia Clínica")
    y -= 30

    c.setFont("Helvetica", 11)
    fecha_actual = datetime.date.today().strftime("%d/%m/%Y")
    c.drawString(50, y, f"Fecha: {fecha_actual}")
    y -= 30

    for seccion, contenido in datos.items():
        if not contenido:
            continue
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"{seccion}:")
        y -= 20
        c.setFont("Helvetica", 11)
        
        for linea in contenido.split("\n"):
            for sublinea in dividir_linea(linea, max_chars=95):
                if y < 80:
                    c.showPage()
                    y = alto - 50
                c.drawString(60, y, sublinea)
                y -= 15

        y -= 15  # Espacio extra entre secciones

    c.save()

def dividir_linea(texto, max_chars=95):
    """Divide una línea larga en sublíneas más cortas."""
    palabras = texto.split()
    linea_actual = ""
    resultado = []

    for palabra in palabras:
        if len(linea_actual + " " + palabra) <= max_chars:
            linea_actual += " " + palabra if linea_actual else palabra
        else:
            resultado.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        resultado.append(linea_actual)

    return resultado
