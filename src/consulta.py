import requests
from requests.exceptions import RequestException


# Diccionario para mapear alias a nombres reales de modelos
MODELOS_DISPONIBLES = {
    "Gemma3": "gemma3:4b",
    "Llama3.2": "llama3.2:3b",
    "Mistral": "mistral:7b-instruct-v0.3-q2_K",
}

def definir_modelo_IA(modelo):
    return MODELOS_DISPONIBLES.get(modelo, modelo)


def generar_historia_clinica_ollama(modelo_IA, texto_transcrito):
    modelo = definir_modelo_IA(modelo_IA)

    prompt = f"""Eres un médico clínico experto en historia clínica. Recibirás a continuación la transcripción de una entrevista entre un médico y un paciente, incluyendo tanto las preguntas del médico como las respuestas del paciente.

    Tu tarea es:

    1. Redactar la sección **Enfermedad actual** de la historia clínica.

    2. Redactar la sección **Antecedentes personales** de la historia clínica.

    3. Redactar la sección **Antecedentes familiares** de la historia clínica.

    4. Evaluar la historia clínica, sugerir diagnóstico presuntivo y preguntas adicionales para completar la historia clínica.

    ---

    Transcripción de la entrevista:

    {texto_transcrito}
    """

    response = llamar_ollama(modelo, prompt)
    return response


def generar_diagnostico_completo_ollama(modelo_IA, datos_personales, motivo_consulta, enfermedad_actual, antecedentes, exploracion):

    modelo = definir_modelo_IA(modelo_IA)


    # Preparar mensaje como si fuera un prompt para los modelos mistral, llama3 y Elixpo
    prompt = f"""Eres un médico clínico meticuloso. Debes generar de modo conciso un diagnóstico más probable, diagnóstico diferencial y estudios complementarios para confirmar diagnóstico basado en los posteriores datos clínicos que te doy.

Respetar la forma:

1. Diagnóstico presuntivo:

2. Diagnóstico diferencial:

3. Estudios complementarios:

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
            timeout=720  # Aumentar el tiempo de espera a 12 minutos

        ) as response:
            if response.ok:
                return response.json().get("response", "").strip()
            else:
                raise RuntimeError(f"Error en la respuesta de Ollama: {response.status_code} - {response.text}")

    except RequestException as e:
        raise RuntimeError(f"Error de conexión con Ollama: {str(e)}")
