# -*- coding: utf-8 -*-
"""BiologiaSistemas_flujo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MbNHNSU_Jb-eVW7JhTi3dRVlf_znudkA

# Flujo de trabajo

## Obtencion de los genes
"""

!pip install requests

import requests

def buscar_genes_por_fenotipo(fenotipo):
    # URL base de la API de HPO para buscar genes asociados a un fenotipo
    base_url = "https://hpo.jax.org/api/hpo/term/"

    # Realizar una solicitud GET a la API de HPO
    response = requests.get(f"{base_url}{fenotipo}/genes?max=-1")

    if response.status_code == 200:
        # Si la solicitud fue exitosa, obtener los genes asociados al fenotipo
        data = response.json()
        genes_asociados = data.get('genes', [])
        return genes_asociados
    else:
        print("No se pudo obtener información del servidor de HPO.")
        return []

# Ejemplo de búsqueda de genes asociados a "Papilloma"
fenotipo_buscar = "HP:0012740"  # Código HPO para Papilloma
genes_asociados_papiloma = buscar_genes_por_fenotipo(fenotipo_buscar)

if genes_asociados_papiloma:
    print(f"Genes asociados a '{fenotipo_buscar}':")
    for gen in genes_asociados_papiloma:
        print(gen)
else:
    print("No se encontraron genes asociados a este fenotipo en la HPO.")

len(genes_asociados_papiloma)

for gen in genes_asociados_papiloma:
    print(gen['geneSymbol'])

"""## Conexion con stringDB"""

import shutil
from IPython.display import Image


base_url = 'https://string-db.org/api/image/'
# Crear una cadena con los símbolos de genes separados por '%'
symbols = "%0d".join([gen['geneSymbol'] for gen in genes_asociados_papiloma])
species = "human"
# Construir la URL con los símbolos de genes para la solicitud
url_request = f"{base_url}network?identifiers={symbols}&species={species}&network_type=functional"
print("Requesting to "+url_request)

response = requests.get(url_request, stream=True)
with open('img.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response

Image(filename='img.png')



!pip install stringdb

import stringdb
# Obtener los símbolos de genes de la lista de genes obtenida anteriormente
genes = [gen['geneSymbol'] for gen in genes_asociados_papiloma]

# Llamar a la función get_interaction_partners() con los genes obtenidos
interaction_df = stringdb.get_interaction_partners(genes)
enrichment_df = stringdb.get_enrichment(genes)

# Mostrar el DataFrame resultante
print(enrichment_df)

# Enriquecimiento por categorias (nuestro fdr (p-value ajustado) es tan pequeño que no vamos a considerarlo)
# Filtramos por categorias 'Process' y 'KEGG'
categorias = ['Process', 'KEGG']
enrichment_df_filtrado = enrichment_df[enrichment_df['category'].isin(categorias)]

# Imprimimos los resultados filtrados
print(enrichment_df_filtrado)

palabras_buscadas = ['cervix', 'ovarian', 'HPV', 'herpes', 'papillomavirus', 'costellos', 'cowden']

patron = '|'.join(palabras_buscadas)

resultados_enfermedades = enrichment_df[enrichment_df['description'].str.contains(patron, case=False)]

resultados_enfermedades.to_csv('fueij', index = True)