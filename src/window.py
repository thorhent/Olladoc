# window.py
#
# Copyright 2025 Taylan Branco Meurer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import GLib

from . import consulta, estructurar, guardar

import threading

import speech_recognition as sr


@Gtk.Template(resource_path='/com/github/thorhent/Olladoc/window.ui')
class OlladocWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'OlladocWindow'

    navigation_view = Gtk.Template.Child("navigation_view")

    btn_to_page2 = Gtk.Template.Child("btn_to_page2")
    btn_to_page3 = Gtk.Template.Child("btn_to_page3")
    btn_to_page4 = Gtk.Template.Child("btn_to_page4")
    btn_to_page5 = Gtk.Template.Child("btn_to_page5")
    btn_to_page6 = Gtk.Template.Child("btn_to_page6")

    btn_back_to_page1 = Gtk.Template.Child("btn_back_to_page1")
    btn_back_to_page2 = Gtk.Template.Child("btn_back_to_page2")
    btn_back_to_page3 = Gtk.Template.Child("btn_back_to_page3")
    btn_back_to_page4 = Gtk.Template.Child("btn_back_to_page4")
    btn_back_to_page5 = Gtk.Template.Child("btn_back_to_page5")


    # Pagina 1 widgets
    entry_motivo = Gtk.Template.Child("entry_motivo")
    entry_nombre = Gtk.Template.Child("entry_nombre")
    entry_dni = Gtk.Template.Child("entry_dni")
    entry_edad = Gtk.Template.Child("entry_edad")
    entry_direccion = Gtk.Template.Child("entry_direccion")
    entry_ocupacion = Gtk.Template.Child("entry_ocupacion")
    entry_sexo = Gtk.Template.Child("entry_sexo")
    entry_estado_civil = Gtk.Template.Child("entry_estado_civil")
    entry_telefono = Gtk.Template.Child("entry_telefono")
    entry_email = Gtk.Template.Child("entry_email")

    # Página 2 widgets
    text_enfermedad_actual = Gtk.Template.Child("text_enfermedad_actual")
    btn_iniciar_audio = Gtk.Template.Child("btn_iniciar_audio")
    btn_detener_audio = Gtk.Template.Child("btn_detener_audio")
    btn_generar_enfermedad_actual = Gtk.Template.Child("btn_generar_enfermedad_actual")

    spinner_EA = Gtk.Template.Child("spinner_enfermedad_actual")


    #Página 3 widgets
    text_antecedentes_personales = Gtk.Template.Child("text_antecedentes_personales")
    text_antecedentes_familiares = Gtk.Template.Child("text_antecedentes_familiares")

    # Página 4 widgets switchs
    switch_fiebre = Gtk.Template.Child("switch_fiebre")
    switch_escalofrios = Gtk.Template.Child("switch_escalofrios")
    switch_sudor_nocturno = Gtk.Template.Child("switch_sudor_nocturno")
    switch_perdida_peso = Gtk.Template.Child("switch_perdida_peso")
    switch_fatiga = Gtk.Template.Child("switch_fatiga")
    switch_malestar_general = Gtk.Template.Child("switch_malestar_general")
    switch_cambios_piel = Gtk.Template.Child("switch_cambios_piel")
    switch_ulceras = Gtk.Template.Child("switch_ulceras")
    switch_cambios_cabello_unhas = Gtk.Template.Child("switch_cambios_cabello_unhas")
    switch_menor_agudeza_visual = Gtk.Template.Child("switch_menor_agudeza_visual")
    switch_dolor_ocular = Gtk.Template.Child("switch_dolor_ocular")
    switch_fotofobia = Gtk.Template.Child("switch_fotofobia")
    switch_vision_doble = Gtk.Template.Child("switch_vision_doble")
    switch_lagrimeo = Gtk.Template.Child("switch_lagrimeo")
    switch_hipoacusia = Gtk.Template.Child("switch_hipoacusia")
    switch_tinnitus = Gtk.Template.Child("switch_tinnitus")
    switch_otalgia = Gtk.Template.Child("switch_otalgia")
    switch_secrecion = Gtk.Template.Child("switch_secrecion")
    switch_congestión_nasal = Gtk.Template.Child("switch_congestion_nasal")
    switch_rinorrea = Gtk.Template.Child("switch_rinorrea")
    switch_epistaxis = Gtk.Template.Child("switch_epistaxis")
    switch_estornudos = Gtk.Template.Child("switch_estornudos")
    switch_dolor_facial = Gtk.Template.Child("switch_dolor_facial")
    switch_dolor_garganta = Gtk.Template.Child("switch_dolor_garganta")
    switch_aftas = Gtk.Template.Child("switch_aftas")
    switch_sangrado_encias = Gtk.Template.Child("switch_sangrado_encias")
    switch_disfonia = Gtk.Template.Child("switch_disfonia")
    switch_mal_aliento = Gtk.Template.Child("switch_mal_aliento")
    switch_dolor_rigidez_cuello = Gtk.Template.Child("switch_dolor_rigidez_cuello")
    switch_masas_cuello = Gtk.Template.Child("switch_masas_cuello")
    switch_ganglios_palpables_cuello = Gtk.Template.Child("switch_ganglios_palpables_cuello")
    switch_tos = Gtk.Template.Child("switch_tos")
    switch_disnea = Gtk.Template.Child("switch_disnea")
    switch_sibilancias = Gtk.Template.Child("switch_sibilancias")
    switch_hemoptisis = Gtk.Template.Child("switch_hemoptisis")
    switch_dolor_toracico = Gtk.Template.Child("switch_dolor_toracico")
    switch_dolor_precordial = Gtk.Template.Child("switch_dolor_precordial")
    switch_palpitaciones = Gtk.Template.Child("switch_palpitaciones")
    switch_disnea_paroxistica_nocturna = Gtk.Template.Child("switch_disnea_paroxistica_nocturna")
    switch_ortopnea = Gtk.Template.Child("switch_ortopnea")
    switch_edemas_perifericos = Gtk.Template.Child("switch_edemas_perifericos")
    switch_claudicacion_intermitente = Gtk.Template.Child("switch_claudicacion_intermitente")
    switch_vomitos = Gtk.Template.Child("switch_vomitos")
    switch_dolor_abdominal = Gtk.Template.Child("switch_dolor_abdominal")
    switch_cambios_apetito = Gtk.Template.Child("switch_cambios_apetito")
    switch_pirosis = Gtk.Template.Child("switch_pirosis")
    switch_diarrea_constipacion = Gtk.Template.Child("switch_diarrea_constipacion")
    switch_hematoquecia_melenas = Gtk.Template.Child("switch_hematoquecia_melenas")
    switch_distension_abdominal = Gtk.Template.Child("switch_distension_abdominal")
    switch_ictericia = Gtk.Template.Child("switch_ictericia")
    switch_disuria = Gtk.Template.Child("switch_disuria")
    switch_polaquiuria = Gtk.Template.Child("switch_polaquiuria")
    switch_hematuria = Gtk.Template.Child("switch_hematuria")
    switch_incontinencia_urinaria = Gtk.Template.Child("switch_incontinencia_urinaria")
    switch_flujo_vaginal = Gtk.Template.Child("switch_flujo_vaginal")
    switch_dolor_pelvico = Gtk.Template.Child("switch_dolor_pelvico")
    switch_dificultad_iniciar_miccion = Gtk.Template.Child("switch_dificultad_iniciar_miccion")
    switch_artralgia = Gtk.Template.Child("switch_artralgia")
    switch_mialgia = Gtk.Template.Child("switch_mialgia")
    switch_inflamacion_articular = Gtk.Template.Child("switch_inflamacion_articular")
    switch_rigidez_matutina = Gtk.Template.Child("switch_rigidez_matutina")
    switch_menor_movimientos_articulares = Gtk.Template.Child("switch_menor_movimientos_articulares")
    switch_mareos = Gtk.Template.Child("switch_mareos")
    switch_parestesias = Gtk.Template.Child("switch_parestesias")
    switch_convulsiones = Gtk.Template.Child("switch_convulsiones")
    switch_debilidad_muscular = Gtk.Template.Child("switch_debilidad_muscular")
    switch_alteracion_marcha = Gtk.Template.Child("switch_alteracion_marcha")
    switch_cambios_memoria_concentracion = Gtk.Template.Child("switch_cambios_memoria_concentracion")
    switch_estado_animo = Gtk.Template.Child("switch_estado_animo")
    switch_insomnio = Gtk.Template.Child("switch_insomnio")
    switch_alucinaciones = Gtk.Template.Child("switch_alucinaciones")
    switch_ideacion_suicida = Gtk.Template.Child("switch_ideacion_suicida")
    switch_intolerancia_frio = Gtk.Template.Child("switch_intolerancia_frio")
    switch_intolerancia_calor = Gtk.Template.Child("switch_intolerancia_calor")
    switch_cambios_peso = Gtk.Template.Child("switch_cambios_peso")
    switch_poliuria_polidipsia = Gtk.Template.Child("switch_poliuria_polidipsia")
    switch_cambios_vello_corporal = Gtk.Template.Child("switch_cambios_vello_corporal")

    # Pagina 5 widgets
    spin_fc = Gtk.Template.Child("spin_fc")
    spin_fr = Gtk.Template.Child("spin_fr")
    spin_temp = Gtk.Template.Child("spin_temp")
    spin_sat = Gtk.Template.Child("spin_sat")
    entry_pa = Gtk.Template.Child("entry_pa")


    text_exploracion_fisica = Gtk.Template.Child("text_exploracion_fisica")


    # Pagina 6 widgets
    text_solucion = Gtk.Template.Child("text_solucion")

    btn_generar_resumen = Gtk.Template.Child("btn_generar_resumen")

    spinner_resumen = Gtk.Template.Child("spinner_resumen")
    loading_box = Gtk.Template.Child("loading_box")
    label_loading = Gtk.Template.Child("label_loading")

    btn_guardar_pdf = Gtk.Template.Child("btn_guardar_pdf")
    btn_limpiar = Gtk.Template.Child("btn_limpiar")

    historia_clinica = dict
    idHC = 0  # ID de la historia clínica, se asignará al guardar

    toast_overlay = Gtk.Template.Child("toast_overlay")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Conectar señales
        self.btn_to_page2.connect("clicked", self.on_to_page2)
        self.btn_to_page3.connect("clicked", self.on_to_page3)
        self.btn_to_page4.connect("clicked", self.on_to_page4)
        self.btn_to_page5.connect("clicked", self.on_to_page5)
        self.btn_to_page6.connect("clicked", self.on_to_page6)

        self.btn_back_to_page1.connect("clicked", self.on_back_to_page1)
        self.btn_back_to_page2.connect("clicked", self.on_back_to_page2)
        self.btn_back_to_page3.connect("clicked", self.on_back_to_page3)
        self.btn_back_to_page4.connect("clicked", self.on_back_to_page4)
        self.btn_back_to_page5.connect("clicked", self.on_back_to_page5)

        # pagina 2
        self.btn_iniciar_audio.connect("clicked", self.on_iniciar_audio)
        self.btn_detener_audio.connect("clicked", self.on_detener_audio)
        self.btn_detener_audio.set_sensitive(False)

        self.recognizer = sr.Recognizer()
        self.microfono = sr.Microphone()
        self.audio_escuchando = False
        self.texto_transcrito = ""
        self.detener_funcion = None


        self.btn_generar_enfermedad_actual.connect("clicked", self.on_generar_enfermedad_actual)
        self.btn_generar_enfermedad_actual.set_sensitive(False)

        #pagina 6
        self.btn_limpiar.connect("clicked", self.limpiar_campos)
        self.btn_limpiar.set_sensitive(False)

        self.btn_generar_resumen.connect("clicked", self.on_generar_resumen)
        self.modelo_IA = self.get_application().modelo_IA
        self.btn_generar_resumen.set_label(f"Consultar {self.modelo_IA}")


        self.btn_guardar_pdf.connect("clicked", self.on_generar_pdf_historia_clinica)
        self.btn_guardar_pdf.set_sensitive(False)

    def on_to_page2(self, button):
        self.navigation_view.push_by_tag("page2")

    def on_to_page3(self, button):
        self.navigation_view.push_by_tag("page3")

    def on_to_page4(self, button):
        self.navigation_view.push_by_tag("page4")

    def on_to_page5(self, button):
        self.navigation_view.push_by_tag("page5")

    def on_to_page6(self, button):
        self.navigation_view.push_by_tag("page6")


    def on_back_to_page1(self, button):
        page1 = self.navigation_view.find_page("page1")
        self.navigation_view.pop_to_page(page1)

    def on_back_to_page2(self, button):
        page2 = self.navigation_view.find_page("page2")
        self.navigation_view.pop_to_page(page2)

    def on_back_to_page3(self, button):
        page3 = self.navigation_view.find_page("page3")
        self.navigation_view.pop_to_page(page3)

    def on_back_to_page4(self, button):
        page4 = self.navigation_view.find_page("page4")
        self.navigation_view.pop_to_page(page4)

    def on_back_to_page5(self, button):
        page5 = self.navigation_view.find_page("page5")
        self.navigation_view.pop_to_page(page5)

    def on_modelo_actualizado(self, nuevo_modelo):
        self.modelo_IA = nuevo_modelo
        self.btn_generar_resumen.set_label(f"Consultar {nuevo_modelo}")

    def on_iniciar_audio(self, button):

        self.audio_escuchando = True
        self.texto_transcrito = ""  # Vaciar antes de cada nueva grabación

        self.btn_iniciar_audio.set_sensitive(False)
        self.btn_detener_audio.set_sensitive(True)


        def callback(recognizer, audio):
            try:
                texto = recognizer.recognize_google(audio, language="es-ES")
                GLib.idle_add(self.actualizar_transcripcion, texto)
            except sr.UnknownValueError:
                GLib.idle_add(self.mostrar_error, "No se entendió el audio.")
            except sr.RequestError as e:
                GLib.idle_add(self.mostrar_error, f"Error de reconocimiento: {e}")


        def iniciar_en_hilo():
            with self.microfono as source:
                self.recognizer.adjust_for_ambient_noise(source)
            self.detener_funcion = self.recognizer.listen_in_background(self.microfono, callback)



        threading.Thread(target=iniciar_en_hilo, daemon=True).start()


    def on_detener_audio(self, button):
        self.audio_escuchando = False
        self.btn_iniciar_audio.set_sensitive(True)
        self.btn_detener_audio.set_sensitive(False)
        self.btn_generar_enfermedad_actual.set_sensitive(True)

        if self.detener_funcion:
            self.detener_funcion(wait_for_stop=False)  # Detiene el reconocimiento en segundo plano

        print(self.texto_transcrito)

    def actualizar_transcripcion(self, nuevo_texto):
        self.texto_transcrito += " " + nuevo_texto.strip()


    def on_generar_enfermedad_actual(self, button):
        if not self.texto_transcrito.strip():
            self.mostrar_error("No se ha grabado ningún audio.")
            return

        texto_estructurado = estructurar.estructurar_dialogo(self.texto_transcrito)
        print(texto_estructurado)
        self.btn_generar_enfermedad_actual.set_sensitive(False)
        self.btn_iniciar_audio.set_sensitive(False)

        #activar spinner
        self.spinner_EA.set_visible(True)
        self.spinner_EA.start()
        self.spinner_EA.set_size_request(24, 24)

        def worker():
            try:
                respuesta = consulta.generar_enfermedad_actual(self.modelo_IA, texto_estructurado)
                GLib.idle_add(self.text_enfermedad_actual.get_buffer().set_text, respuesta)

            except Exception as e:
                pass
                #GLib.idle_add(self.mostrar_error, str(e))
            finally:
                GLib.idle_add(self.btn_generar_enfermedad_actual.set_sensitive, True)
                GLib.idle_add(self.spinner_EA.stop)
                GLib.idle_add(self.spinner_EA.set_visible, False)
                GLib.idle_add(self.btn_iniciar_audio.set_sensitive, True)
                print(f"Respuesta: {respuesta}")


        threading.Thread(target=worker, daemon=True).start()


    def limpiar_campos(self, *args):
        #if response == 'confirm' :
        def limpiar_textview(tv):
            tv.get_buffer().set_text("")

        def limpiar_entry(entry):
            if isinstance(entry, Adw.EntryRow) or isinstance(entry, Gtk.Entry):
                entry.set_text("")
            elif isinstance(entry, Adw.ComboRow):
                entry.set_selected(0)

        def limpiar_spin(spin):
            spin.set_value(spin.get_adjustment().get_lower())

        # Página 1
        limpiar_entry(self.entry_motivo)
        limpiar_entry(self.entry_nombre)
        limpiar_entry(self.entry_dni)
        limpiar_entry(self.entry_edad)
        limpiar_entry(self.entry_direccion)
        limpiar_entry(self.entry_ocupacion)
        limpiar_entry(self.entry_sexo)
        limpiar_entry(self.entry_estado_civil)
        limpiar_entry(self.entry_telefono)
        limpiar_entry(self.entry_email)

        # Página 2
        limpiar_textview(self.text_enfermedad_actual)

        # Página 3
        limpiar_textview(self.text_antecedentes_personales)
        limpiar_textview(self.text_antecedentes_familiares)

        # Página 4
        for attr in dir(self):
            if attr.startswith("switch_"):
                getattr(self, attr).set_active(False)

        # Página 5
        limpiar_spin(self.spin_fc)
        limpiar_spin(self.spin_fr)
        limpiar_spin(self.spin_temp)
        limpiar_spin(self.spin_sat)
        limpiar_entry(self.entry_pa)
        limpiar_textview(self.text_exploracion_fisica)

        # Página 6
        limpiar_textview(self.text_solucion)

        self.btn_guardar_pdf.set_sensitive(False)
        self.btn_limpiar.set_sensitive(False)
        # Mostrar Toast
        toast = Adw.Toast.new("Historia clínica borrada correctamente")
        self.toast_overlay.add_toast(toast)

    def get_text_from_view(self, textview):
        buffer = textview.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        return buffer.get_text(start_iter, end_iter, True)

    def mostrar_respuesta(self, respuesta):
        print(f"Respuesta de Ollama\n: {respuesta}")



    def mostrar_error(self, mensaje):
        dialog = Adw.MessageDialog(
            transient_for=self,
            modal=True,
            heading="Error",
            body=mensaje
        )
        dialog.add_response("ok", "Aceptar")
        dialog.set_default_response("ok")
        dialog.set_close_response("ok")
        dialog.show()

    def on_generar_resumen(self, button):
        motivo_consulta = self.entry_motivo.get_text()

        #datos personales
        nombre = self.entry_nombre.get_text()
        dni = self.entry_dni.get_text()
        edad = self.entry_edad.get_text()
        direccion = self.entry_direccion.get_text()
        ocupacion = self.entry_ocupacion.get_text()


        selected_index_sexo = self.entry_sexo.get_selected()
        if selected_index_sexo != -1:
            sexo = self.entry_sexo.get_model().get_string(selected_index_sexo)
        else:
            sexo = ""

        selected_index_estado = self.entry_estado_civil.get_selected()
        if selected_index_estado != -1:
            estado_civil = self.entry_estado_civil.get_model().get_string(selected_index_estado)
        else:
            estado_civil = ""

        # Recoger datos de contacto
        telefono = self.entry_telefono.get_text()
        email = self.entry_email.get_text()
        datos_personales = f"Nombre: {nombre}, DNI: {dni}, Edad: {edad}, Dirección: {direccion}, Ocupación: {ocupacion}, Sexo: {sexo}, Estado Civil: {estado_civil}, Teléfono: {telefono}, Email: {email}"

        enfermedad_actual = self.get_text_from_view(self.text_enfermedad_actual)
        antecedentes = self.get_text_from_view(self.text_antecedentes_personales) + "\n" + self.get_text_from_view(self.text_antecedentes_familiares)

        #recoger signos vitales
        fc = self.spin_fc.get_value_as_int()
        fr = self.spin_fr.get_value_as_int()
        temp = self.spin_temp.get_value()
        sat = self.spin_sat.get_value_as_int()
        pa = self.entry_pa.get_text()
        signos_vitales = f"FC: {fc}, FR: {fr}, Temp: {temp}°C, Sat: {sat}%, PA: {pa}"
        exploracion = f"{signos_vitales} \n "+ self.get_text_from_view(self.text_exploracion_fisica)

        modelo_IA = getattr(self.get_application(), "modelo_IA", None)
        if modelo_IA is None:
            modelo_IA = "Llama3"  # valor por defecto si no se seleccionó aún

        print(f"Modelo: {modelo_IA}")


        self.btn_generar_resumen.set_sensitive(False)
        self.spinner_resumen.start()
        self.loading_box.set_visible(True)


        buffer = self.text_solucion.get_buffer()
        buffer.set_text("")

        self.historia_clinica = {
            "datos_personales": datos_personales,
            "motivo_consulta": motivo_consulta,
            "enfermedad_actual": enfermedad_actual,
            "antecedentes": antecedentes,
            "exploracion": exploracion,
            "solucion": "",
        }


        def worker():
            try:
                repuesta =  consulta.generar_diagnostico_completo_ollama(modelo_IA, datos_personales, motivo_consulta, enfermedad_actual, antecedentes, exploracion)

                GLib.idle_add(buffer.set_text, repuesta)
                GLib.idle_add(self.mostrar_respuesta, repuesta)
                self.historia_clinica["solucion"] = repuesta

            except Exception as e:
                GLib.idle_add(self.mostrar_error, str(e))
            finally:
                GLib.idle_add(self.btn_generar_resumen.set_sensitive, True)
                GLib.idle_add(self.spinner_resumen.stop)
                GLib.idle_add(self.loading_box.set_visible, False)
                GLib.idle_add(self.btn_guardar_pdf.set_sensitive, True)
                GLib.idle_add(self.btn_limpiar.set_sensitive, True)




        threading.Thread(target=worker, daemon=True).start()

    def on_generar_pdf_historia_clinica(self, button):
        if not self.historia_clinica:
            self.mostrar_error("Debe generar un resumen antes de guardar la historia clínica.")
            return

        self.idHC += 1  # Incrementar el ID de la historia clínica
        guardar.guardar_historia_clinica_pdf(self, self.historia_clinica, self.idHC)
        
