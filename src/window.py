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

import threading, time, json, re

import speech_recognition as sr


@Gtk.Template(resource_path='/io/github/thorhent/Olladoc/window.ui')
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
    btn_generar_historia_clinica = Gtk.Template.Child("btn_generar_historia_clinica")

    spinner_HC = Gtk.Template.Child("spinner_historia_clinica")


    #Página 3 widgets
    text_antecedentes_personales = Gtk.Template.Child("text_antecedentes_personales")
    text_antecedentes_familiares = Gtk.Template.Child("text_antecedentes_familiares")


    # Página 4 widgets
    text_evaluacion_IA = Gtk.Template.Child("text_evaluacion_IA")
    btn_evaluacion_IA = Gtk.Template.Child("btn_evaluacion_IA")
    AdwPage4Evaluacion = Gtk.Template.Child("AdwPage4Evaluacion")
    spinner_evaluacion_IA = Gtk.Template.Child("spinner_evaluacion_IA")


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


        # Conectar eventos de cambio de texto o selección
        self.entry_nombre.connect("changed", self.validar_anamnesis)
        self.entry_edad.connect("changed", self.validar_anamnesis)
        self.entry_ocupacion.connect("changed", self.validar_anamnesis)  # opcional, pero refresca validación
        self.entry_motivo.connect("changed", self.validar_anamnesis)

        self.text_enfermedad_actual.get_buffer().connect("changed", self.validar_anamnesis)
        self.text_antecedentes_personales.get_buffer().connect("changed", self.validar_anamnesis)
        self.text_antecedentes_familiares.get_buffer().connect("changed", self.validar_anamnesis)

        # pagina 2
        self.btn_iniciar_audio.connect("clicked", self.on_iniciar_audio)
        self.btn_detener_audio.connect("clicked", self.on_detener_audio)
        self.btn_detener_audio.set_sensitive(False)

        self.recognizer = sr.Recognizer()
        self.microfono = sr.Microphone()
        self.escuchando = False
        self.texto_transcrito = ""
        self.detener_funcion = None


        self.btn_generar_historia_clinica.connect("clicked", self.on_generar_historia_clinica)
        self.btn_generar_historia_clinica.set_sensitive(False)

        # pagina 4
        self.btn_evaluacion_IA.connect("clicked", self.on_generar_evaluacion_inicial)
        self.btn_evaluacion_IA.set_sensitive(False)  # Deshabilitado al inicio
        self.modelo_IA = self.get_application().modelo_IA
        self.AdwPage4Evaluacion.set_title(f"Consultar para diagnóstico inicial [{self.modelo_IA}]")

        #pagina 6
        self.btn_limpiar.connect("clicked", self.limpiar_campos)
        self.btn_limpiar.set_sensitive(False)

        self.btn_generar_resumen.connect("clicked", self.on_generar_resumen)
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
        self.AdwPage4Evaluacion.set_title(f"Consultar para diagnóstico inicial [{nuevo_modelo}]")

    def validar_anamnesis(self, *args):
        """Habilita el botón solo si los datos básicos están completos (ocupación opcional)."""
        nombre = self.entry_nombre.get_text().strip()
        edad = self.entry_edad.get_text().strip()
        ocupacion = self.entry_ocupacion.get_text().strip()  # opcional
        motivo = self.entry_motivo.get_text().strip()

        enfermedad_actual = self.get_text_from_view(self.text_enfermedad_actual).strip()
        antecedentes_pers = self.get_text_from_view(self.text_antecedentes_personales).strip()
        antecedentes_fam = self.get_text_from_view(self.text_antecedentes_familiares).strip()

        # Lista de campos obligatorios (ocupación NO incluida)
        campos_ok = all([
            nombre, edad, motivo,
            enfermedad_actual, antecedentes_pers, antecedentes_fam
        ])

        self.btn_evaluacion_IA.set_sensitive(campos_ok)

    def on_generar_evaluacion_inicial(self, button):
        motivo_consulta = self.entry_motivo.get_text()
        enfermedad_actual = self.get_text_from_view(self.text_enfermedad_actual)
        antecedentes = self.get_text_from_view(self.text_antecedentes_personales) + "\n" + self.get_text_from_view(self.text_antecedentes_familiares)

        #datos personales
        nombre = self.entry_nombre.get_text()
        edad = self.entry_edad.get_text()
        ocupacion = self.entry_ocupacion.get_text()


        selected_index_sexo = self.entry_sexo.get_selected()
        if selected_index_sexo != -1:
            sexo = self.entry_sexo.get_model().get_string(selected_index_sexo)
        else:
            sexo = ""

        selected_index_estado = self.entry_estado_civil.get_selected()
        if selected_index_estado != -1:
            estado_civil = self.entry_estado_civil.get_model().get_string(selected_index_estado)
            if sexo == "Femenino" and estado_civil.endswith("o"):
                estado_civil = estado_civil[:-1] + "a"  # Cambiar a femenino si es necesario
        else:
            estado_civil = ""

        datos_personales = f"Nombre: {nombre}, Edad: {edad}, Sexo: {sexo}, Estado Civil: {estado_civil}, Ocupación: {ocupacion}"

        buffer = self.text_evaluacion_IA.get_buffer()
        buffer.set_text("")

        self.btn_evaluacion_IA.set_sensitive(False)
        self.spinner_evaluacion_IA.set_visible(True)
        self.spinner_evaluacion_IA.start()


        def worker():
            try:
                respuesta = consulta.generar_diagnostico_parcial_ollama(self.modelo_IA, datos_personales, motivo_consulta, enfermedad_actual, antecedentes)

                GLib.idle_add(buffer.set_text, respuesta)

            except Exception as e:
                GLib.idle_add(self.mostrar_error, str(e))
            finally:
                GLib.idle_add(self.btn_evaluacion_IA.set_sensitive, True)
                self.spinner_evaluacion_IA.stop()


        threading.Thread(target=worker, daemon=True).start()




    def on_iniciar_audio(self, button):
        if self.escuchando:
            return

        self.recognizer = sr.Recognizer()
        self.microfono = sr.Microphone()

        # Ajuste inicial de ruido
        with self.microfono as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Calibración inicial completada.")

        self.texto_transcrito = ""
        self.fragmentos_transcritos = []  # Lista para fragmentos con timestamp
        self.escuchando = True
        self.inicio_entrevista = time.time()
        self.ultima_calibracion = time.time()

        self.btn_iniciar_audio.set_sensitive(False)
        self.btn_detener_audio.set_sensitive(True)

        def procesar_audio(recognizer, audio):
            # Recalibrar cada 2 minutos para entornos con ruido variable
            if time.time() - self.ultima_calibracion > 120:
                try:
                    with self.microfono as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    self.ultima_calibracion = time.time()
                    print("Recalibración de ruido realizada.")
                except Exception as e:
                    print(f"Error en recalibración: {e}")

            try:
                texto = recognizer.recognize_google(audio, language="es-ES")
                if texto.strip():
                    ts = time.strftime("%H:%M:%S")
                    fragmento = f"[{ts}] {texto}"
                    self.fragmentos_transcritos.append(fragmento)

                    # Actualizar texto completo
                    self.texto_transcrito += " " + texto
                    print(f"Transcripción parcial: {texto}")

            except sr.UnknownValueError:
                # No mostrar error emergente por cada fragmento no entendido
                print("Silencio o audio no reconocido.")
            except sr.RequestError as e:
                print(f"Error de conexión con el servicio de reconocimiento: {e}")

        self.hilo_escucha = self.recognizer.listen_in_background(
            self.microfono,
            procesar_audio,
            phrase_time_limit=None  # Permite capturar frases largas
        )

        print("Grabación iniciada.")


    def on_detener_audio(self, button):
        if not self.escuchando:
            return

        self.escuchando = False
        if hasattr(self, "hilo_escucha"):
            self.hilo_escucha(wait_for_stop=False)

        self.btn_iniciar_audio.set_sensitive(True)
        self.btn_detener_audio.set_sensitive(False)
        self.btn_generar_historia_clinica.set_sensitive(True)



    #def actualizar_transcripcion(self, nuevo_texto):
        #self.texto_transcrito += " " + nuevo_texto.strip()

    def limpiar_y_parsear_json(self, respuesta):
        # Buscar el primer bloque JSON en la respuesta
        match = re.search(r"\{[\s\S]*\}", respuesta)
        if not match:
            raise ValueError("No se encontró un JSON en la respuesta:\n" + respuesta)
        bloque_json = match.group(0)

        try:
            return json.loads(bloque_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al parsear JSON: {e}\nBloque:\n{bloque_json}")


    def normalizar_valor(self, valor):
        if isinstance(valor, str):
            return valor
        elif isinstance(valor, dict):
            # dict -> texto tipo "hipertensión: Sí, diabetes: No"
            return "\n".join([f"{k}: {'Sí' if v else 'No'}" for k, v in valor.items()])
        elif isinstance(valor, list):
            # lista -> texto tipo "• Infarto (padre)\n• Diabetes (madre)"
            return "\n".join([f"• {item}" for item in valor])
        else:
            return str(valor)


    def on_generar_historia_clinica(self, button):
        if not self.texto_transcrito.strip():
            self.mostrar_error("No se ha grabado ningún audio.")
            return
        # limpiar los GtkTextViews de la anamnesis
        self.text_enfermedad_actual.get_buffer().set_text("")
        self.text_antecedentes_personales.get_buffer().set_text("")
        self.text_antecedentes_familiares.get_buffer().set_text("")


        # Desactivar botones y mostrar spinner
        self.btn_generar_historia_clinica.set_sensitive(False)
        self.btn_iniciar_audio.set_sensitive(False)
        self.spinner_HC.set_visible(True)
        self.spinner_HC.start()
        self.spinner_HC.set_size_request(20, 20)

        def worker():
            try:
                # --- Preprocesamiento ---
                texto_crudo = self.texto_transcrito.strip()

                # Limitar tamaño para IA si es muy largo (ej. 10k caracteres)
                if len(texto_crudo) > 10000:
                    print("Texto muy largo, truncando para IA...")
                    texto_crudo = texto_crudo[:10000] + " ...[Texto truncado]"

                # Estructurar diálogo (operación pesada)
                texto_estructurado = estructurar.estructurar_dialogo(texto_crudo)

                # --- Llamada a la IA ---
                respuesta = consulta.generar_historia_clinica_ollama(
                    self.modelo_IA,
                    texto_estructurado
                )

                print(respuesta)
                dic_respuesta = self.limpiar_y_parsear_json(respuesta)

                # --- Actualizar los GtkTextView ---
                GLib.idle_add(
                    self.text_enfermedad_actual.get_buffer().set_text,
                    self.normalizar_valor(dic_respuesta.get("enfermedad_actual", ""))
                )
                GLib.idle_add(
                    self.text_antecedentes_personales.get_buffer().set_text,
                    self.normalizar_valor(dic_respuesta.get("antecedentes_personales", ""))
                )
                GLib.idle_add(
                    self.text_antecedentes_familiares.get_buffer().set_text,
                    self.normalizar_valor(dic_respuesta.get("antecedentes_familiares", ""))
                )

            except Exception as e:
                GLib.idle_add(self.mostrar_error, str(e))
            finally:
                GLib.idle_add(self.btn_generar_historia_clinica.set_sensitive, True)
                GLib.idle_add(self.btn_iniciar_audio.set_sensitive, True)
                GLib.idle_add(self.spinner_HC.stop)
                GLib.idle_add(self.spinner_HC.set_visible, False)
                print("Procesamiento finalizado.")

        threading.Thread(target=worker, daemon=True).start()


    def limpiar_campos(self, *args):
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

        # Pagina 4
        limpiar_textview(self.text_evaluacion_IA)


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
            if sexo == "Femenino" and estado_civil.endswith("o"):
                estado_civil = estado_civil[:-1] + "a"  # Cambiar a femenino si es necesario
        else:
            estado_civil = ""



        # Recoger datos de contacto
        telefono = self.entry_telefono.get_text()
        email = self.entry_email.get_text()
        datos_personales_completo = f"Nombre: {nombre}, DNI: {dni}, Edad: {edad}, Dirección: {direccion}, Ocupación: {ocupacion}, Sexo: {sexo}, Estado Civil: {estado_civil}, Teléfono: {telefono}, Email: {email}"
        datos_personales = f"Nombre: {nombre}, Edad: {edad}, Sexo: {sexo}, Estado Civil: {estado_civil}"

        enfermedad_actual = self.get_text_from_view(self.text_enfermedad_actual)
        antecedentes = self.get_text_from_view(self.text_antecedentes_personales) + "\n" + self.get_text_from_view(self.text_antecedentes_familiares)

        # diagnostico preliminar y diferencial de page4
        diagnostico_page4 = self.get_text_from_view(self.text_evaluacion_IA) or None

        #recoger signos vitales
        fc = self.spin_fc.get_value_as_int()
        fr = self.spin_fr.get_value_as_int()
        temp = self.spin_temp.get_value()
        sat = self.spin_sat.get_value_as_int()
        ta = self.entry_pa.get_text()
        signos_vitales = f"FC: {fc}, FR: {fr}, Temp: {temp}°C, Sat: {sat}%, PA: {ta}"
        exploracion = f"{signos_vitales} \n "+ self.get_text_from_view(self.text_exploracion_fisica)

        modelo_IA = getattr(self.get_application(), "modelo_IA", None)

        self.btn_generar_resumen.set_sensitive(False)
        self.spinner_resumen.start()
        self.loading_box.set_visible(True)


        buffer = self.text_solucion.get_buffer()
        buffer.set_text("")


        self.historia_clinica = {
            "Datos personales": datos_personales_completo,
            "Motivo consulta": motivo_consulta,
            "Enfermedad actual": enfermedad_actual,
            "Antecedentes": antecedentes,
        }

        if diagnostico_page4 is not None:
            self.historia_clinica["Diagnóstico preliminar y diferencial"] = diagnostico_page4

        self.historia_clinica["Exploración"] = exploracion
        self.historia_clinica["Diagnóstico, estudios y acciones"] = ""


        def worker():
            try:
                respuesta =  consulta.generar_diagnostico_completo_ollama(modelo_IA,
                    datos_personales,
                    motivo_consulta,
                    enfermedad_actual,
                    antecedentes,
                    exploracion
                )

                GLib.idle_add(buffer.set_text, respuesta)
                #GLib.idle_add(self.mostrar_respuesta, respuesta)
                self.historia_clinica["Diagnóstico, estudios y acciones"] = respuesta

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
        guardar.guardar_historia_clinica_pdf(self, self.historia_clinica, self.modelo_IA, self.idHC)
        
