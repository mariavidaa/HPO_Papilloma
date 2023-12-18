# Importamos libreria
library(igraph)
# Cargamos los datos
genes <- read.table("../results/genes_igraph.txt", sep = '\t', header = FALSE, stringsAsFactors = FALSE)
#Creamos un nuevo grafo no dirigido a partir de esta información
net <- graph_from_data_frame(genes, directed=F)

# Mostramos la red
par(cex = 0.4)
plot(net)

# Comprobamos que no hay ningun nodo sin conexión.
is.connected(net)

# Comprobamos que no es dirigido
is.directed(net)

# Grado centralidad: numero de conexiones de cada gen
degree_centrality <- degree(net)
degree_centrality

# Centralidad de cercanía: Mide la distancia promedio entre un nodo y todos los demás nodos
closeness_centrality <- closeness(net)
closeness_centrality

# Conectividad:Mide la fortaleza de la conexión en el grafo.
connectivity <- edge_density(net)
connectivity

#  Detección de comunidades mediante in_betweeness.
community <- cluster_edge_betweenness(net)
dendPlot(community, mode="hclust")
# Mostramos el grafo con las clusters detectados
par(cex = 0.4)
png(filename = "../results/clustering_in_betweeness.png", width = 800, height = 600)
plot(community, net)
# Guardamos la imagen en la carpeta results
dev.off()

cfg <- cluster_fast_greedy(as.undirected(net))
par(cex = 0.4)
png(filename = "../results/clustering_fast_greedy.png", width = 800, height = 600)
plot(cfg, as.undirected(net))
# Guardamos la imagen en la carpeta results
#dev.copy(png, filename = "../results/clustering_fast_greedy.png", width = 800, height = 600)  
dev.off()

# Pinta el grafo de manera que los nodos que lo forman compartan un mismo color si pertenecen a la misma comunidad.
V(net)$community <- cfg$membership
colrs <- adjustcolor( c("gray50", "tomato", "gold", "yellowgreen", "blue"), alpha=.6)
par(cex = 0.4)
png(filename = "../results/clustering_coloreado.png", width = 800, height = 600)
plot(net, vertex.color=colrs[V(net)$community])
# Guardamos la imagen en la carpeta results
dev.off()

# Detección de comunidades mediante propagación de etiquetas.
clp <- cluster_label_prop(net)
par(cex = 0.4)
plot(clp, net)
# Guardamos la imagen en la carpeta results
dev.copy(png, filename = "../results/clustering_label_prop.png", width = 800, height = 600)  
dev.off()

community_louvain <- cluster_louvain(net)
par(cex = 0.4)
plot(community_louvain, net)
# Guardamos la imagen en la carpeta results
dev.copy(png, filename = "../results/clustering_louvain.png", width = 800, height = 600)  
dev.off()

library(linkcomm)

lg <- swiss[,3:4]
lc <- getLinkCommunities(genes)

# Visualiza las link communities
options(repr.plot.width=9, repr.plot.height=9)
par(cex = 0.5)# Visualiza las link communities
plot(lc, type = "graph", layout = "spencer.circle")
# Guardamos la imagen en la carpeta results
dev.copy(png, filename = "../results/clustering_link_communities.png", width = 800, height = 600)  
dev.off()

# Genes de interés
genes_interes <- c("TP53", "HRAS", "AKT1", "SDHB", "SDHD")

# Función para encontrar vecinos interesantes
encontrar_vecinos_interesantes <- function(gen, genes_interes) {
  vecinos <- neighbors(net, gen)$name
  vecinos_interesantes <- vecinos[vecinos %in% genes_interes]
  return(paste(vecinos_interesantes, collapse = ", "))
}

# Crear la tabla
tabla_genes <- data.frame(Gen = genes_interes)

# Agregar la columna de vecinos interesantes como cadenas de texto
tabla_genes$Vecinos_Interesantes <- sapply(genes_interes, function(gen) {
  encontrar_vecinos_interesantes(gen, genes_interes)
})

# Imprimir la tabla
print(tabla_genes)

# Identifica los genes de interés
genes_interes <- c("AKT1", "TP53", "SDHD", "SDHB", "HRAS")

# Encuentra los índices de los nodos que representan los genes de interés
nodos_genes_interes <- V(net)$name %in% genes_interes

# Encuentra el índice del cluster que contiene los genes de interés
cluster_containing_genes <- membership(cfg)[nodos_genes_interes]

# Guarda los genes de ese cluster en un archivo de texto
genes_cluster <- V(net)$name[membership(cfg) == cluster_containing_genes]

# Ruta y nombre del archivo de texto
ruta_archivo <- "../results/genes_cluster.txt"

# Guardar la variable genes_cluster en un archivo de texto
write.table(genes_cluster, file = ruta_archivo, quote = FALSE, col.names = FALSE, row.names = FALSE)

# Imprimir mensaje de confirmación
cat("Los genes del cluster se han guardado en el archivo:", ruta_archivo, "\n")


