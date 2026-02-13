import gi
import gettext

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
from gi.repository import GObject
from . import consulta


_ = gettext.gettext


class PreferenciasWindow(Adw.PreferencesWindow):
    
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title(_("Preferencias"))
        self.set_default_size(600, 600)
        self.set_search_enabled(False)

        self.connect("close-request", self.on_close)
        

        # Crear una página
        page = Adw.PreferencesPage()
        

        # Grupo para selección de modelo
        group = Adw.PreferencesGroup(title=_("Modelo de IA"))
        
        # Verificar lista de modelos instalados
        modelos = consulta.listar_modelos_instalados()

        # Crear lista de opciones
        string_list = Gtk.StringList.new(modelos)

        
        # Obtener índice del modelo guardado, o usar 0 si no existe
        modelo_actual = app.modelo_IA if hasattr(app, "modelo_IA") else modelos[0]
        try:
            index_modelo = modelos.index(modelo_actual)
        except ValueError:
            index_modelo = 0
        
        # Crear ComboRow con selección inicial
        self.combo_modelo = Adw.ComboRow(
            title=_("Modelo Ollama"),
            subtitle=_("Selecciona el modelo que se usará para generar el diagnóstico"),
            model=string_list,
            selected=index_modelo
        )

        self.combo_modelo.connect("notify::selected-item", self.on_modelo_cambiado)


        # Grupo adicional de descripción
        descripcion_group = Adw.PreferencesGroup(
            title=_("Modelos de IA testados y recomendados")
        )

        # Lista de ActionRows informativas
        rows = [
            (
                "qwen3-vl:235b-cloud",
                _("Modelo multimodal de gran escala desarrollado por Alibaba Cloud, perteneciente a la tercera generación de la familia Qwen, diseñado para procesar de forma integrada texto, imágenes y video mediante 235 mil millones de parámetros.")
            ),
            (
                "gpt-oss:120b-cloud",
                _("Modelo de lenguaje de código abierto desarrollado por OpenAI que cuenta con aproximadamente 120 mil millones de parámetros (117B según fuentes) y emplea una arquitectura mixture-of-experts (MoE) con cerca de 5.1 mil millones de parámetros activos.")
            ),
            (
                "gpt-oss:20b-cloud",
                _("Modelo de lenguaje abierto con 20 mil millones de parámetros, optimizado para ejecución en la nube y entornos de baja latencia. Emplea arquitectura densa eficiente, con razonamiento contextual sólido, comprensión multilingüe y generación estructurada, adecuado para aplicaciones técnicas, médicas y científicas que requieren análisis de texto clínico, resumen de información y soporte inteligente a la decisión.")
            )
        ]

        for nombre, descripcion in rows:
            row = Adw.ActionRow(
                title=nombre,
                subtitle=descripcion,
                activatable=False  # No es seleccionable
            )
            descripcion_group.add(row)




        group.add(self.combo_modelo)
        page.add(group)
        page.add(descripcion_group)
        self.add(page)

    def obtener_modelo_seleccionado(self):
        item = self.combo_modelo.get_selected_item()
        if item:
            modelo = item.get_string()
            self.get_application().modelo_IA = modelo
            return modelo
        return None

    def on_close(self, *args):
        self.destroy() 
        return True
        # Retorna True para indicar que la ventana puede cerrarse


    def on_modelo_cambiado(self, combo, _):
        item = combo.get_selected_item()
        if item:
            #modelo = item.get_string()
            #self.get_application().modelo_IA = modelo
            modelo = item.get_string()
            app = self.get_application()
            app.actualizar_modelo(modelo)
            

