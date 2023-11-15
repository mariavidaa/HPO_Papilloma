#!/bin/bash

# Crear las carpetas donde estarán las dependencias de python y de R
mkdir -p ../software
mkdir -p ../software/python
mkdir -p ../software/R

# Instalar dependencias de Python del archivo pythonreqs
pip install -r ../results/pythonreqs.txt --target=../software/python

# Instalar dependencias de R del archivo Rreqs
Rscript -e 'install.packages(readLines("../results/Rreqs.txt"), lib="../software/R")'