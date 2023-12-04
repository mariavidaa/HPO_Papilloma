# -*- coding: utf-8 -*-

# Flujo de trabajo

## Obtencion de los genes


import stringdb
import pandas as pd
import requests
import shutil
from IPython.display import Image

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

print("Número de genes asociados al fenotipo Papilloma: ",len(genes_asociados_papiloma))



## Conexion con stringDB

base_url = 'https://string-db.org/api/image/'
# Crear una cadena con los símbolos de genes separados por '%'
symbols = "%0d".join([gen['geneSymbol'] for gen in genes_asociados_papiloma])
species = "human"
# Construir la URL con los símbolos de genes para la solicitud
url_request = f"{base_url}network?identifiers={symbols}&species={species}&network_type=functional"
print("Requesting to "+url_request)

response = requests.get(url_request, stream=True)
with open('../results/red_inicial.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response


# Obtener los símbolos de genes de la lista de genes obtenida anteriormente
genes = [gen['geneSymbol'] for gen in genes_asociados_papiloma]

# Llamar a la función get_enrichment() con los genes obtenidos
enrichment_df = stringdb.get_enrichment(genes)

# Enriquecimiento por categorias (nuestro fdr (p-value ajustado) es tan pequeño que no vamos a considerarlo)
# Filtramos por categorias 'Process' y 'KEGG'
categorias = ['Process', 'KEGG']
enrichment_df_filtrado = enrichment_df[enrichment_df['category'].isin(categorias)]

# Imprimimos los resultados filtrados
enrichment_df_filtrado.to_csv('../results/enriquecimiento_categorias', index = False)

# Busqueda por palabras clave
palabras_buscadas = ['cervix', 'ovarian', 'HPV', 'herpes', 'papillomavirus', 'costellos', 'cowden']

patron = '|'.join(palabras_buscadas)

resultados_enfermedades = enrichment_df[enrichment_df['description'].str.contains(patron, case=False)]

resultados_enfermedades.to_csv('../results/enriquecimiento_enfermedades', index = False)

# Busqueda por genes relevantes
palabras_buscadas = ['TP53', 'AKT1', 'SDHB', 'SDHD', 'HRAS']

patron = '|'.join(palabras_buscadas)

resultados_genes = enrichment_df_filtrado[enrichment_df_filtrado['inputGenes'].str.contains(patron, case=False)]

resultados_genes.to_csv('../results/enriquecimiento_genes', index = False)

# Descarga de la red en formato tsv
base_url = 'https://string-db.org/api/tsv/'

url_request = f"{base_url}network?identifiers={symbols}&species={species}&network_type=functional"
response = requests.get(url_request, stream=True)

if response.ok:
    # Obtener el nombre del archivo de la URL (si está disponible)
    content_disposition = response.headers.get('content-disposition')
    filename = None

    if content_disposition:
        filename = content_disposition.split('filename=')[1]

    # Guardar el archivo descargado
    if filename:
        with open(filename, 'wb') as file:
            file.write(response.content)

        print(f"Archivo {filename} descargado exitosamente.")
    else:
        print("No se pudo obtener el nombre del archivo. Guardando como 'red_descargada.tsv'.")
        with open('../results/red_descargada.tsv', 'wb') as file:
            file.write(response.content)
else:
    print("Error al descargar el archivo. Código de estado:", response.status_code)


# Limpieza del archivo tsv
# Ruta del archivo TSV descargado desde la API de StringDB
file_path = '../results/red_descargada.tsv'  

# Cargar el archivo TSV
data = pd.read_csv(file_path, sep='\t')

# Seleccionar solo las columnas 'preferredName_A' y 'preferredName_B'
selected_columns = data[['preferredName_A', 'preferredName_B']]

# Eliminar duplicados
selected_columns.drop_duplicates(inplace=True)

# Guardar estas columnas en un nuevo archivo de texto
selected_columns.to_csv('../results/genes_igraph.txt', sep='\t', index=False, header=False)

print("Se han guardado las columnas 'preferredName_A' y 'preferredName_B' en genes_igraph.txt")
