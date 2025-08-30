import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
from gi.repository import GObject
from . import consulta

class PreferenciasWindow(Adw.PreferencesWindow):
    
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Preferencias")
        self.set_default_size(600, 600)
        self.set_search_enabled(False)

        self.connect("close-request", self.on_close)
        

        # Crear una página
        page = Adw.PreferencesPage()
        

        # Grupo para selección de modelo
        group = Adw.PreferencesGroup(title="Modelo de IA")
        
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
            title="Modelo Ollama",
            subtitle="Selecciona el modelo que se usará para generar el diagnóstico",
            model=string_list,
            selected=index_modelo
        )

        self.combo_modelo.connect("notify::selected-item", self.on_modelo_cambiado)


        # Grupo adicional de descripción
        descripcion_group = Adw.PreferencesGroup(title="Modelos de IA testados y recomendados")

        # Lista de ActionRows informativas
        rows = [
            ("gemma3:4b", """Modelo de Google, 4 B parámetros, rápido y eficiente, con capacidad multimodal (texto e imágenes) y buena comprensión de instrucciones."""),
            ("llama3.2:3b", """Modelo de Meta, 3 B parámetros, multilingüe, optimizado para diálogo y tareas generales con bajo consumo."""),
            ("phi3.5:3.8b", """Modelo de lenguaje desarrollado por Microsoft, perteneciente a la familia Phi. Consta de aproximadamente 3.8 mil millones de parámetros, lo que lo sitúa en la categoría de modelos ligeros, optimizados para eficiencia y despliegue en hardware con recursos limitados.""")
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
            

