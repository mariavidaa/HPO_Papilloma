#!/bin/bash

# Definir las carpetas donde estarán las dependencias de python y de R
PYTHON_FOLDER="../software/python"
R_FOLDER="../software/R"

# Crear las carpetas si no existen
mkdir -p "$PYTHON_FOLDER"
mkdir -p "$R_FOLDER"

# Limpieza de cache
python3 -m pip cache purge

# Instalar dependencias de Python del archivo pythonreqs.txt en la carpeta python
python3 -m pip install -r pythonreqs.txt --target="$PYTHON_FOLDER"

# Instalar dependencias de R del archivo Rreqs.txt en la carpeta R
Rscript -e 'install.packages(readLines("Rreqs.txt"), lib="../software/R")'

# Imprimir mensaje de finalización
echo "Instalación de dependencias completada con éxito."
