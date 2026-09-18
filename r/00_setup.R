# Entorno reproducible para la Actividad 1 - Métodos No Supervisados
# Semillas de trigo (seeds_dataset): ACP, AFE y Kernel PCA
#
# Este script centraliza:
#   - Parámetros del análisis (escalables sin tocar el .Rmd)
#   - Verificación/instalación de dependencias con versión fija de CRAN (checkpoint-like manual)
#   - Fijación de semilla para reproducibilidad
#   - Función de carga de datos con caché local

# ---- 1. Parámetros globales (modificables) ---------------------------------
params_analisis = list(
  seed             = 2024,
  url_datos        = "https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt",
  ruta_datos_local = file.path("data", "seeds_dataset.txt"),
  ncp_pca_max      = 7,     # componentes a calcular en el ACP (todas las variables activas)
  umbral_carga_afe = 0.3,   # umbral para reportar cargas factoriales relevantes
  kpca_kernel      = "rbfdot",
  kpca_sigma       = 0.1,   # ancho de banda del kernel RBF
  kpca_features    = 2
)

# ---- 2. Paquetes requeridos --------------------------------------------------
paquetes_requeridos = c(
  "dplyr", "tidyr", "tibble",
  "FactoMineR", "factoextra", "missMDA",
  "psych", "GPArotation",
  "ggplot2", "ggrepel", "ggcorrplot",
  "kernlab", "knitr"
)

instalar_paquetes_faltantes = function(paquetes = paquetes_requeridos) {
  # mirror fijo de CRAN: requerido para instalaciones no interactivas (Rscript)
  options(repos = c(CRAN = "https://cloud.r-project.org"))

  # biblioteca de usuario escribible: evita fallos de permisos en instalaciones sin privilegios de administrador
  lib_usuario = Sys.getenv("R_LIBS_USER", file.path(Sys.getenv("USERPROFILE"), "R", "library"))
  dir.create(lib_usuario, showWarnings = FALSE, recursive = TRUE)
  .libPaths(c(lib_usuario, .libPaths()))

  faltantes = paquetes[!paquetes %in% rownames(installed.packages())]
  if (length(faltantes) > 0) {
    install.packages(faltantes, dependencies = TRUE, lib = lib_usuario)
  }
  invisible(lapply(paquetes, library, character.only = TRUE))
}

# ---- 3. Función de carga de datos con caché local ---------------------------
cargar_datos_semillas = function(params = params_analisis) {

  dir.create(dirname(params$ruta_datos_local), showWarnings = FALSE, recursive = TRUE)

  if (!file.exists(params$ruta_datos_local)) {
    download.file(params$url_datos, destfile = params$ruta_datos_local, quiet = TRUE, mode = "wb")
  }

  datos = read.table(params$ruta_datos_local, header = FALSE)
  names(datos) = c("area", "perimeter", "compactness", "kernel_length", "kernel_width",
                    "asymmetry_coefficient", "kernel_groove_length", "variety")
  datos$variety = factor(datos$variety, levels = c(1, 2, 3),
                          labels = c("Kama", "Rosa", "Canadian"))
  datos
}

# ---- 4. Inicialización del entorno ------------------------------------------
inicializar_entorno = function(params = params_analisis) {
  set.seed(params$seed)
  options(scipen = 999)
  instalar_paquetes_faltantes()
  cargar_datos_semillas(params)
}
