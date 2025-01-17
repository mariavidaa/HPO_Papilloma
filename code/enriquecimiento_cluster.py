# -*- coding: utf-8 -*-
"""Primero de todo importamos la librería, la URL de la API de StringDB y en el formato en la que queremos exportarla.
"""

import requests ## python -m pip install requests
import json
import pandas as pd

"""Construimos la URL completa para realizar una solicitud a la API de STRINGDB. La función "/".join(...) se utiliza para unir estos elementos que forman la URL con barras ("/").

"""

string_api_url = "https://version-11-5.string-db.org/api"
output_format = "json"
method = "enrichment"

request_url = "/".join([string_api_url, output_format, method])

"""Definimos las categorías funcionales de interés (en nuestro caso HPO)"""

categoria_de_interes = "HPO"

"""Introducimos la especie que estamos estudiando"""

especie = 9606

"""Definimos los genes para el análisis funcional."""

archivo_genes = "../results/genes_cluster.txt"

# Inicializar la lista de genes
my_genes = []

# Leer los genes desde el archivo y agregarlos a la lista
with open(archivo_genes, "r") as file:
    for line in file:
        gene = line.strip()  # Eliminar saltos de línea u espacios en blanco
        my_genes.append(gene)

"""Definimos los parámetros para el análisis funcional."""

params = {

    "identifiers" : "%0d".join(my_genes),
    "species" : especie,
    "caller_identity" : "test_HAB"

}

"""Esta línea recoge la solicitud a la API de STRINGDB utilizando la biblioteca request. Los parametros introducidos se han definido anteriormente."""

response = requests.post(request_url, data=params)

data = json.loads(response.text)

resultados = []

for row in data:
    term = row["term"]
    preferred_names = ",".join(row["preferredNames"])
    NCBI_taxonID = row["ncbiTaxonId"]
    fdr = float(row["fdr"])
    p_value = row["p_value"]
    category = row["category"]
    input_genes = row["inputGenes"]
    number_genes = row["number_of_genes"]
    number_genes_background = ["number_of_genes_in_background"]
    description = row["description"]



    if category == categoria_de_interes:
      resultados.append([term, preferred_names, category, description])

"""Creamos un DataFrame a partir de los resultados y mostraremos los resultados por pantalla:"""

df_resultados = pd.DataFrame(resultados, columns=["Term", "Preferred Names", "Category", "Description"])

"""Guardamos el dataframe en un archivo CSV"""

nombre_archivo_analisis = "../results/resultados_enriquecimiento_cluster.csv"
df_resultados.to_csv(nombre_archivo_analisis, index=False)

print(f"Resultados guardados en '{nombre_archivo_analisis}'.")