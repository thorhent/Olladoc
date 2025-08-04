import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
from gi.repository import GObject

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
        

        # Crear lista de opciones
        modelos = ["Llama3", "Elixpo", "Mistral"]
        string_list = Gtk.StringList.new(modelos)

        
        # Obtener índice del modelo guardado, o usar 0 si no existe
        modelo_actual = app.modelo_IA if hasattr(app, "modelo_IA") else "Llama3"
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
        descripcion_group = Adw.PreferencesGroup(title="Sobre cada modelo")

        # Lista de ActionRows informativas
        rows = [
            ("Llama3", """Última generación de Meta. Ajustado para instrucciones, con excelente capacidad de  comprensión contextual y generación de lenguaje técnico. Capacidad avanzada para razonamiento clínico complejo. Ideal para casos diferenciales, protocolos médicos, manejo integral y análisis estructurado de historias clínicas."""),
            ("Elixpo/LlamaMedicine", """Modelo especializado en medicina, afinado con corpus clínico. Lenguaje médico técnico y orientado a razonamiento diagnóstico. Recomendado para generación de hipótesis clínicas, estudios complementarios y orientación terapéutica general."""),
            ("Mistral", """Modelo ágil y eficiente de código abierto. Entrenado para seguir instrucciones con rapidez y claridad. Útil para tareas clínicas generales, sugerencias rápidas y generación de texto médico básico.""")

             
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
            
        