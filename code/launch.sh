#!/bin/bash

mkdir -p "../results"

echo "Instalamos dependencias"
# Script para instalar dependencias
./setup.sh

echo "Ejecutamos biologiasistemas_flujo.py"
# Ejecutar el script de Python
python3 biologiasistemas_flujo.py

echo "Ejecutamos biologiasistemas_igraph.R"
# Ejecutar el archivo de R
Rscript biologiasistemas_igraph.R

echo "Ejecutamos enriquecimiento_cluster.py"
# Ejecutar el script de Python
python3 enriquecimiento_cluster.py
