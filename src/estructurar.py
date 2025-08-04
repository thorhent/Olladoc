import re

def estructurar_dialogo(texto_crudo):
    """
    Convierte una transcripción de entrevista médica en diálogo estructurado.

    Args:
        texto_crudo (str): Texto continuo sin separación de roles.

    Returns:
        str: Diálogo estructurado con 'Médico:' y 'Paciente:'.
    """

    # Lista base de preguntas médicas frecuentes
    preguntas_base = [
        "cómo está", "cómo se llama", "cuántos años tiene", "por qué razón viene",
        "cuándo ha empezado", "ha tenido náuseas", "ha tenido diarrea", 
        "ha viajado fuera del país", "desde cuándo", "dónde le duele",
        "qué síntomas ha presentado", "tiene fiebre", "ha tenido escalofríos"
    ]

    # Frases del texto
    frases = re.split(r"(?<=[.?!])\s+|(?<=\s)(?=[A-Z])", texto_crudo)
    resultado = []
    es_pregunta = True  # Alternamos entre médico y paciente

    for frase in frases:
        frase = frase.strip().capitalize()

        if not frase:
            continue

        # Heurística: contiene una pregunta conocida
        if any(p in frase.lower() for p in preguntas_base) or frase.endswith("?") or frase.lower().startswith("por qué"):
            resultado.append(f"Médico: {frase}")
            es_pregunta = False
        else:
            resultado.append(f"Paciente: {frase}")
            es_pregunta = True

    return "\n".join(resultado)
