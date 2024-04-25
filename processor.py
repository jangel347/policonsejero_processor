import spacy
# Carga del modelo de lenguaje en español

# Función para buscar reglas relacionadas con la situación dada
nlp = spacy.load("es_core_news_sm")
def buscar_reglas(situacion, reglas):
    print(situacion)
    situacion_doc = nlp(situacion)
    reglas_relacionadas = []
    tags = []
    for regla in reglas:
        # similitud = 1
        # print(regla["contenido"])
        descripcion_doc = nlp(regla["contenido"])
        similitud = situacion_doc.similarity(descripcion_doc)
        if similitud > 0.5:  # Umbral de similitud arbitrario
            print(f'Similar {similitud}')
            reglas_relacionadas.append(regla)
            tags = list(set(tags + regla["tags"]))
        else:
            print(f'No similar {similitud}')

    return reglas_relacionadas, tags