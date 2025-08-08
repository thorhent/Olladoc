import re
import difflib


def estructurar_dialogo(texto_crudo: str):
    """
    Estructura el texto transcrito de una entrevista médico-paciente
    para presentarlo de forma clara y útil a un modelo de IA.
    """
    # Limpieza inicial
    texto = texto_crudo.strip()
    texto = re.sub(r'\s+', ' ', texto)  # Quitar espacios dobles
    texto = re.sub(r'\b(eh|este|mmm|ajá)\b', '', texto, flags=re.IGNORECASE)  # Quitar muletillas

    # Segmentación robusta: cortar en frases por puntuación fuerte
    frases = re.split(r'(?<=[\.\?\!])\s+', texto)
    frases = [f.strip() for f in frases if f.strip()]

    #dialogo_json = []
    texto_final = ""
    rol_actual = "Médico"  # Suponemos que comienza el médico

    # Lista de indicios de pregunta médica
    indicios_pregunta = [
        "cuándo", "desde cuándo", "ha tenido", "ha notado", "ha presentado",
        "tiene antecedentes", "usa", "ha usado", "ha sufrido", "qué siente",
        "puede describir", "dónde le duele", "ha visto", "ha percibido"
    ]

    for frase in frases:
        frase_lower = frase.lower()

        # Detectar si es pregunta
        es_pregunta = frase.endswith("?") or any(indicio in frase_lower for indicio in indicios_pregunta)

        if es_pregunta:
            rol = "Médico"
        else:
            # Si no es pregunta y el rol anterior fue Médico, pasamos a Paciente
            rol = "Paciente" if rol_actual == "Médico" else rol_actual

        # Guardar turno
        #dialogo_json.append({"rol": rol, "texto": frase})
        texto_final += f"{rol}: {frase}\n"
        rol_actual = rol

    return texto_final.strip()
