import requests
from requests.exceptions import RequestException


# Diccionario para mapear alias a nombres reales de modelos
MODELOS_DISPONIBLES = {
    "Llama3": "llama3.1:8b",
    "Elixpo": "Elixpo/LlamaMedicine:latest",
    "Mistral": "mistral:instruct",
}

def definir_modelo_IA(modelo):
    return MODELOS_DISPONIBLES.get(modelo, modelo)


def generar_enfermedad_actual(modelo_IA, texto_transcrito):
    modelo = definir_modelo_IA(modelo_IA)

    prompt = f"""Eres un médico clínico experto en historia clínica. Recibirás a continuación la transcripción de una entrevista entre un médico y un paciente, incluyendo tanto las preguntas del médico como las respuestas del paciente.

    Tu tarea es triple:

    1. Redactar la sección **"Enfermedad actual"** de la historia clínica, utilizando lenguaje médico técnico, claro, profesional y narrativo. Describe cronológicamente el inicio, evolución, características de los síntomas, factores agravantes o atenuantes, tratamientos realizados y cualquier otro dato relevante.

    2. Realizar una **evaluación de la entrevista médica**, señalando si faltaron datos clave, si las preguntas fueron poco específicas o si hubo información que el médico podría haber indagado mejor.

    3. Sugerir una lista de **preguntas adicionales** que sería útil realizar al paciente para completar la información clínica, sin emitir diagnósticos.

    ---

    Transcripción de la entrevista:

    {texto_transcrito}
    """

    response = llamar_ollama(modelo, prompt, stream=False)
    return response


def generar_diagnostico_completo_ollama(modelo_IA, datos_personales, motivo_consulta, enfermedad_actual, antecedentes, exploracion):

    modelo = definir_modelo_IA(modelo_IA)


    # Preparar mensaje como si fuera un prompt para los modelos mistral, llama3 y Elixpo
    prompt = f"""
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

        Generar manejo médico con diagnóstico presuntivo y diferencial, estudios complementarios y tratamientos (farmacológicos, no farmacológicos o quirúrgicos). Siempre de forma clara, meticulosa, concreta y en español.
        Respetar la siguiente forma:

        Diagnóstico presuntivo:

        Diagnóstico diferencial:

        Estudios complementarios:

        Tratamiento:

        """

    respuesta = llamar_ollama(modelo, prompt, stream=False)
    return respuesta

def llamar_ollama(modelo, prompt, stream):
    # Llamada HTTP POST al servidor local de Ollama
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": modelo,
                "prompt": prompt,
                "stream": stream,
            },
            stream=stream
        )
        if not response.ok:
            raise RuntimeError(f"Error en la respuesta de Ollama: {response.status_code} - {response.text}")
        else:
            return response.json().get("response", "").strip()


    except RequestException as e:
        raise RuntimeError(f"Error de conexión con Ollama: {str(e)}")
