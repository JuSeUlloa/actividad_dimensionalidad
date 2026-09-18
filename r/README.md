# Cómo ejecutar el análisis (ACP, AFE y Kernel PCA)

Esta guía explica cómo instalar R y ejecutar el código de la carpeta `Act_1_MetNoSup`
para generar el informe reproducible.

## 1. Requisitos previos

- **R** (versión >= 4.2): https://cran.r-project.org/bin/windows/base/
- **RStudio Desktop** (opcional pero recomendado): https://posit.co/download/rstudio-desktop/
- Conexión a internet (para descargar el dataset y los paquetes la primera vez).

Verifica la instalación abriendo una terminal nueva (PowerShell) y ejecutando:

```powershell
Rscript --version
```

Si el comando no se reconoce, reinicia la terminal/VS Code después de instalar R para que
`PATH` se actualice, o agrega manualmente la carpeta `bin` de R al `PATH` del sistema.

## 2. Estructura del proyecto

```
Script_R/
└── Act_1_MetNoSup/
    ├── Act_1_MetNoSup.Rmd   # informe principal (RMarkdown)
    ├── R/
    │   └── 00_setup.R       # entorno reproducible: parámetros, paquetes, carga de datos
    └── data/                # se crea automáticamente con el dataset descargado (caché local)
```

## 3. Instalar los paquetes necesarios

Desde la carpeta `Act_1_MetNoSup`, ejecuta en R (o en una terminal con Rscript):

```powershell
cd "Act_1_MetNoSup"
Rscript -e "source('R/00_setup.R'); instalar_paquetes_faltantes()"
```

Esto instala (si faltan) y carga: `dplyr`, `tidyr`, `tibble`, `FactoMineR`, `factoextra`,
`missMDA`, `psych`, `GPArotation`, `ggplot2`, `ggrepel`, `ggcorrplot`, `kernlab`, `knitr`.

## 4. Generar el informe (knit)

**Opción A — RStudio:** abre `Act_1_MetNoSup.Rmd` y presiona el botón **Knit**.

**Opción B — Línea de comandos:**

```powershell
cd "Act_1_MetNoSup"
Rscript -e "rmarkdown::render('Act_1_MetNoSup.Rmd')"
```

El resultado es `Act_1_MetNoSup.html` con todas las tablas, gráficos e interpretaciones.

## 5. Cambiar parámetros del análisis

Los parámetros (semilla, número máximo de componentes del ACP, umbral de cargas del AFE,
kernel y sigma del Kernel PCA) están centralizados en el encabezado YAML del `.Rmd`
(sección `params:`) y en `R/00_setup.R` (`params_analisis`). Para probar otra configuración
sin tocar el código del análisis:

```powershell
Rscript -e "rmarkdown::render('Act_1_MetNoSup.Rmd', params = list(kpca_sigma = 0.05))"
```

## 6. Solución de problemas

- **Error al descargar el dataset:** verifica la conexión a internet; el archivo se guarda en
  `data/seeds_dataset.txt` tras la primera descarga y no se vuelve a descargar.
- **Error de paquete no encontrado:** vuelve a ejecutar el paso 3.
- **Rotación oblicua en AFE:** si cambias `rotate` a una rotación oblicua (p. ej. `"oblimin"`),
  asegúrate de tener instalado `GPArotation` (ya incluido en la lista de paquetes).
