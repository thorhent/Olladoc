import datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from gi.repository import Gtk, Gio, GLib

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY

# Obtener estilos predefinidos y personalizarlos
estilos = getSampleStyleSheet()

# Estilo para el cuerpo del texto
estilo_normal = estilos['Normal']
estilo_normal.fontName = 'NotoSans-Regular'
estilo_normal.fontSize = 11
estilo_normal.leading = 15
estilo_normal.spaceAfter = 15
estilo_normal.alignment = TA_JUSTIFY

# Estilo para el título del documento
estilo_titulo = estilos['Title']
estilo_titulo.fontName = 'NotoSans-Bold'
estilo_titulo.fontSize = 18
estilo_titulo.alignment = 1 # Centro

# Estilo para los títulos de sección
estilo_seccion = estilos['Heading2']
estilo_seccion.fontName = 'NotoSans-Bold'
estilo_seccion.fontSize = 12
estilo_seccion.spaceAfter = 5
estilo_seccion.leftIndent = 0

#---- configuracion para Canvas
BASE_DIR = "/app/share/olladoc/fonts/"

pdfmetrics.registerFont(TTFont("DejaVuSans", os.path.join(BASE_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", os.path.join(BASE_DIR, "DejaVuSans-Bold.ttf")))

pdfmetrics.registerFont(TTFont("NotoSans-Regular", os.path.join(BASE_DIR, "NotoSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("NotoSans-Bold", os.path.join(BASE_DIR, "NotoSans-Bold.ttf")))


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

        generar_pdf_historia_clinica_platus(ruta, datos_historia_clinica)

        # Emitir señal o directamente lanzar toast
        if hasattr(widget, "toast_overlay"):
            from gi.repository import Adw
            toast = Adw.Toast.new("Historia clínica guardada correctamente.")
            widget.toast_overlay.add_toast(toast)
        

    except GLib.Error as e:
        print(f"Error al guardar archivo: {e.message}")



# Esta función reemplaza a la antigua que usaba canvas.drawString
def generar_pdf_historia_clinica_platus(ruta, datos):

    # Definir el documento (SimpleDocTemplate)
    # Se define pagesize y los márgenes
    doc = SimpleDocTemplate(
        ruta,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50,
        title="HC-olladoc"
    )
    story = []

    # 1. Título principal
    titulo_principal = Paragraph("Historia Clínica", estilo_titulo)
    story.append(titulo_principal)
    story.append(Spacer(1, 15))

    # 2. Fecha
    fecha_actual = datetime.date.today().strftime("%d/%m/%Y")
    fecha_parrafo = Paragraph(f"Fecha: {fecha_actual}", estilo_normal)
    story.append(fecha_parrafo)
    story.append(Spacer(1, 15))

    # 3. Contenido de las secciones
    for seccion, contenido in datos.items():
        if not contenido:
            continue

        # Título de la sección
        titulo_seccion = Paragraph(f"{seccion}:", estilo_seccion)
        story.append(titulo_seccion)

        # Contenido como Párrafo
        # Usamos <br/> para forzar saltos de línea (incluyendo líneas en blanco)
        contenido_formateado = contenido.replace('\n', '<br/>')

        parrafo_contenido = Paragraph(contenido_formateado, estilo_normal)
        story.append(parrafo_contenido)
        story.append(Spacer(1, 10)) # Espacio extra entre secciones

    # 4. Construir el documento
    doc.build(story)


def generar_pdf_historia_clinica_canvas(ruta, datos):
    c = canvas.Canvas(ruta, pagesize=A4)
    c.setTitle("Historia Clínica")
    ancho, alto = A4
    y = alto - 50  # Margen superior

    c.setFont("NotoSans-Bold", 16)
    c.drawString(50, y, "Historia Clínica")
    y -= 30

    c.setFont("NotoSans-Regular", 11)
    fecha_actual = datetime.date.today().strftime("%d/%m/%Y")
    c.drawString(50, y, f"Fecha: {fecha_actual}")
    y -= 30

    for seccion, contenido in datos.items():
        if not contenido:
            continue
        c.setFont("NotoSans-Bold", 12)
        c.drawString(50, y, f"{seccion}:")
        y -= 20
        c.setFont("NotoSans-Regular", 11)
        
        for linea in contenido.split("\n"):
            # Preservar líneas en blanco
            if linea.strip() == "":
                y -= 15
                continue
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
