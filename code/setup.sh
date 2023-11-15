#!/bin/bash

# Crear las carpetas donde estarán las dependencias de python y de R
mkdir -p ../software
mkdir -p ../software/python
mkdir -p ../software/R

# Limpieza de cache
python3 -m pip cache purge

# Instalar dependencias de Python del archivo pythonreqs
python3 -m pip install -r ../results/pythonreqs.txt --target=../software/python 1> /dev/null

# Instalar dependencias de R del archivo Rreqs
Rscript -e 'install.packages(readLines("../results/Rreqs.txt"), repos="http://cran.us.r-project.org", dependencies=TRUE, lib="../software/R")' 1> /dev/null