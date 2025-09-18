import requests
from requests.exceptions import RequestException, ConnectionError



def listar_modelos_instalados():
    url = "http://localhost:11434/api/tags"
    try:
        response = requests.get(url, timeout=5)  # Añade un tiempo de espera para evitar bloqueos
        response.raise_for_status()  # Lanza un error para códigos de estado 4xx/5xx

        datos = response.json()
        modelos = [m["name"] for m in datos["models"]]
        return modelos

    except (ConnectionError, RequestException) as e:
        print(f"Advertencia: No se pudo conectar con el servicio Ollama. {e}")
        return []
    except Exception as e:
        print(f"Verificar instalación y configuración de ollama: {e}")
        return []


def generar_historia_clinica_ollama(modelo, texto_transcrito):
    prompt = f"""Eres un médico clínico experto en historia clínica. Recibirás a continuación la transcripción de una entrevista entre un médico y un paciente, incluyendo tanto las preguntas del médico como las respuestas del paciente.

Tu tarea es redactar de forma completa y profesional la enfermedad actual, los antecedentes personales y los antecedentes familiares en un JSON válido solo con estas claves exactas:

{{
  "enfermedad_actual": "...",
  "antecedentes_personales": "...",
  "antecedentes_familiares": "..."
}}

No incluyas explicaciones ni texto fuera del JSON. Respetar "clave": "string".

Transcripción de la entrevista:

{texto_transcrito}
"""


    response = llamar_ollama(modelo, prompt)
    return response

def generar_diagnostico_parcial_ollama(modelo, datos_personales, motivo_consulta, enfermedad_actual, antecedentes):
    prompt = f"""Como médico clínico, realizar respuesta corta solo con diagnóstico inicial más probable y diferencial basado en los datos siguientes de la anamnesis.

Datos de anamnesis:

- Datos personales:
{datos_personales}

- Motivo de consulta:
{motivo_consulta}

- Enfermedad actual:
{enfermedad_actual}

- Antecedentes:
{antecedentes}
"""

    respuesta = llamar_ollama(modelo, prompt)
    return respuesta

def generar_diagnostico_completo_ollama(modelo, datos_personales, motivo_consulta, enfermedad_actual, antecedentes, exploracion):
    # Preparar mensaje como si fuera un prompt para los modelos mistral, llama3 y Elixpo
    prompt = f"""Eres un médico clínico meticuloso. Debes generar respuesta estrictamente concisa y solo sobre diagnóstico más probable, estudios complementarios esenciales para confirmar diagnóstico y acción inicial, todo basado en los posteriores datos clínicos que te doy.

Datos clínicos:

- Datos personales:
{datos_personales}

- Motivo de consulta:
{motivo_consulta}

- Enfermedad actual:
{enfermedad_actual}

- Antecedentes:
{antecedentes}

- Exploración física:
{exploracion}
"""

    respuesta = llamar_ollama(modelo, prompt)
    return respuesta

def llamar_ollama(modelo, prompt):
    # Llamada HTTP POST al servidor local de Ollama

    try:
        with requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": modelo,
                "prompt": prompt,
                "stream": False
            },
            stream=False,
            timeout=480  # tiempo de espera 8 minutos

        ) as response:
            if response.ok:
                return response.json().get("response", "").strip()
            else:
                raise RuntimeError(f"Error en la respuesta de Ollama: {response.status_code} - {response.text}")

    except RequestException as e:
        raise RuntimeError(f"Error de conexión con Ollama: {str(e)}")
