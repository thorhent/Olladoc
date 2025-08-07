<p align="center">
  <img src="data/logo.svg" width="150" alt="Olladoc Logo"/>
</p>

<h1 align="center">🩺 Olladoc</h1>

<p align="center">
  Aplicación médica moderna desarrollada con <b>GTK 4</b> y <b>libadwaita</b>, diseñada para generar historias clínicas profesionales con entrada por voz e inteligencia artificial.
</p>

<p align="center">
  <img src="data/olladoc-img1.png" width="600" alt="Captura de pantalla principal"/>
</p>

---

## 🚀 Características destacadas

- 🧠 Entrada por voz y texto para anamnesis rápida
- 📄 Generación de historia clínica en PDF
- 🤖 Orientación diagnóstica con IA local (Ollama + Llama3)
- 🩺 Flujo clínico profesional con AdwNavigationView
- 🎨 Interfaz moderna con diseño limpio y responsivo
- 🐧 Compatible con Flatpak y Flathub

---

## 📷 Capturas de pantalla

| Inicio | Consulta |
|--------|----------|
| ![Home](data/home.png) | ![Consulta](data/consulta.png) |

---

## 🧪 Cómo ejecutar localmente (Flatpak)

### 📦 1. Construcción, prueba e instalación

```bash
flatpak-builder --force-clean build-dir com.github.thorhent.Olladoc
flatpak-builder --run build-dir com.github.thorhent.Olladoc olladoc
flatpak-builder --user --force-clean --install build-dir com.github.thorhent.Olladoc

