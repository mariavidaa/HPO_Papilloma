#!/bin/bash

echo "Instalamos dependencias"
# Script para instalar dependencias
./setup.sh

# Ejecutar el script de Python
python3 biologiasistemas_flujo.py

# Ejecutar el archivo de RMarkdown
Rscript -e 'rmarkdown::render("biologiasistemas_igraph.Rmd")'

# Ejecutar el script de Python
python3 enriquecimiento_cluster.py
