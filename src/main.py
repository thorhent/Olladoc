# main.py
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

import sys
import gi
import gettext
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import OlladocWindow
from .preferencias import PreferenciasWindow
from . import consulta




class OlladocApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.thorhent.Olladoc',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/io/github/thorhent/Olladoc')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        modelos = consulta.listar_modelos_instalados()
        self.modelo_IA = modelos[0] if modelos else ""

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = OlladocWindow(application=self)
            self.ventana_pricipal = win
        win.present()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog(application_name='Olladoc',
                                application_icon='io.github.thorhent.Olladoc',
                                developer_name='Taylan Branco Meurer',
                                version='1.11.25',
                                developers=['Taylan Branco Meurer'],
                                copyright='© 2025 Taylan Branco Meurer')
        # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
        about.set_translator_credits(_('translator-credits'))
        about.present(self.props.active_window)

    def on_preferences_action(self, widget, _):
        if not hasattr(self, "preferencias_window") or not self.preferencias_window.get_visible():
            app = Gtk.Application.get_default()
            self.preferencias_window = PreferenciasWindow(app)

        self.preferencias_window.present()
        
    def actualizar_modelo(self, nuevo_modelo):
        """Actualiza el modelo IA y notifica a la ventana principal."""
        self.modelo_IA = nuevo_modelo
        if self.ventana_pricipal:
            self.ventana_pricipal.on_modelo_actualizado(nuevo_modelo)
            print(f"Modelo actualizado a: {nuevo_modelo}")


    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = OlladocApplication()
    return app.run(sys.argv)
