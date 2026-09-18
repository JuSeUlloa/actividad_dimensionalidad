# REDUCCIÓN DE DIMENSIONALIDAD Y REPRESENTACIONES LATENTES


Repositorio de trabajo para la  actividad que tiene como propósito aplicar y comparar métodos de reducción de
dimensionalidad sobre un conjunto de datos que contiene mediciones geométricas de
granos de tres variedades de trigo. El estudiante deberá construir la base de datos, preparar
la matriz de análisis, aplicar métodos lineales y no lineales, interpretar los resultados y
elaborar un informe reproducible.
La tarea principal consiste en desarrollar un análisis que incluya: Análisis de Componentes
Principales (ACP), Análisis Factorial Exploratorio (AFE), un método no lineal elegido entre
Kernel PCA, t-SNE o UMAP y la comparación argumentada de los métodos aplicados.

## Presentación del repositorio

Este repositorio contiene el código, la documentación y los ejemplos necesarios para estudiar la estructura morfológica de tres variedades de trigo: **Kama**, **Rosa** y **Canadian**. El flujo de análisis está organizado en clases y métodos independientes, de manera que cada etapa pueda revisarse, ejecutarse y comprenderse por separado.

La actividad busca comparar diferentes formas de representar un conjunto de datos multivariado en un espacio de menor dimensión. Para ello se emplean el Análisis de Componentes Principales (ACP), el Análisis Factorial Exploratorio (AFE) y Kernel PCA como método no lineal.

## Descripción de la actividad

El conjunto de datos Seeds contiene **210 granos de trigo**, distribuidos en 70 observaciones por variedad. Cada observación incluye siete características morfológicas:

- `area`: área del grano.
- `perimeter`: perímetro.
- `compactness`: compacidad.
- `kernel_length`: longitud del grano.
- `kernel_width`: anchura del grano.
- `asymmetry_coefficient`: coeficiente de asimetría.
- `kernel_groove_length`: longitud del surco.

La variable `variety` se conserva como información suplementaria. No se utiliza para construir las representaciones, sino únicamente para colorear los gráficos y contrastar si las variedades se diferencian en los espacios reducidos.

## Objetivos

1. Preparar y describir la matriz de datos morfológicos.
2. Examinar las correlaciones entre las variables originales.
3. Estandarizar las variables para evitar que sus diferentes escalas afecten el análisis.
4. Aplicar ACP e interpretar la inercia, las contribuciones y los cosenos cuadrados.
5. Aplicar AFE para identificar dimensiones latentes de la morfología del grano.
6. Aplicar Kernel PCA para explorar posibles relaciones no lineales.
7. Comparar las representaciones obtenidas y el grado de separación entre variedades.
8. Generacion de informe que responda las preguntas planteadas con resultados reproducibles obtenidas de la ejeucción del ejercicio

## Metodología

### 1. Preparación de los datos

La clase `DataPreparation` descarga los datos desde el repositorio UCI, asigna los nombres de las columnas, convierte la variedad en una categoría y estandariza las siete variables numéricas mediante puntuaciones Z. También calcula estadísticos descriptivos y la matriz de correlaciones.

### 2. Análisis de Componentes Principales

La clase `PCA_Module` transforma las variables correlacionadas en componentes ortogonales ordenadas según la varianza explicada. El análisis incluye valores propios, inercia acumulada, cargas, coordenadas de variables e individuos, cosenos cuadrados, contribuciones, círculo de correlaciones, representación de individuos y biplot.

### 3. Análisis Factorial Exploratorio

La clase `EFA` evalúa si la matriz es adecuada para factorizar mediante la prueba de Bartlett y el índice KMO. Posteriormente realiza un análisis paralelo, ajusta el modelo factorial, calcula cargas y comunalidades, y aplica una rotación varimax para facilitar la interpretación de los factores.

### 4. Kernel PCA

La clase `KernelPCA` aplica una extensión no lineal del ACP utilizando un kernel RBF. Esta representación permite explorar patrones que no necesariamente pueden describirse mediante combinaciones lineales de las variables originales y se compara visualmente con el ACP.

## Estructura del repositorio

```text
actividad_dimensionalidad/
├── README.md                    # Presentación general del repositorio
├── main.py                      # Ejecución completa del análisis
├── pyproject.toml               # Configuración del proyecto y dependencias
├── uv.lock                      # Versiones bloqueadas por uv
├── src/
│   ├── README.MD                # Guía específica de ejecución python
│   └── app/
│       ├── data_preparation.py  # Preparación de datos
│       ├── pca_module.py        # Clase PCA_Module
│       ├── efa.py               # Clase EFA
│       └── kernel_pca.py        # Clase KernelPCA
└── r/
    ├── 00_setup.R
    └── README.md                # Guía equivalente para la versión en R
```


## Resultado esperado

La ejecución genera en la terminal los resultados numéricos principales del análisis y muestra gráficos de correlaciones, varianza explicada, círculo de correlaciones, individuos, biplot, cargas factoriales y comparación entre ACP y Kernel PCA.

La interpretación final debe integrar los resultados de los tres métodos, identificando qué variables explican la mayor variabilidad, qué dimensiones latentes pueden asociarse con la forma o el tamaño del grano y si las variedades aparecen separadas, parcialmente diferenciadas o mezcladas.

## Propósito educativo

El proyecto está organizado para apoyar una metodología de aprendizaje basada en comprender el código mientras se construye el análisis. Las clases permiten estudiar de forma independiente la preparación de datos, el ACP, el AFE y Kernel PCA, relacionando cada método con sus resultados estadísticos y gráficos.

Para conocer instrucciones más específicas de ejecución y solución de problemas, consulta [`src/README.MD`](src/README.MD). en ``python`` para la ejecucion en ``R`` consulta  [`r/README.MD`](src/README.MD).
