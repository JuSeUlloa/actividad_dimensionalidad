# Cómo ejecutar el análisis (ACP, AFE y Kernel PCA)

Esta guía explica cómo preparar el entorno y ejecutar el código Python de la actividad de reducción de dimensionalidad aplicada a la caracterización morfológica de granos de trigo.

## 1. Requisitos previos

- **Python** (versión >= 3.14, según `pyproject.toml`).
- **uv**, gestor de paquetes y entornos: https://docs.astral.sh/uv/
- Conexión a internet para descargar el conjunto de datos y las dependencias la primera vez.

Verifica la instalación desde una terminal nueva:

```bash
python --version
uv --version
```

Si aparece una advertencia sobre `VIRTUAL_ENV`, desactiva el entorno virtual previamente activado:

```bash
```

Después utiliza `uv run`, que ejecuta el proyecto dentro del entorno `.venv` administrado por uv.

## 2. Estructura del proyecto

```
actividad_dimensionalidad/
├── main.py                       # flujo principal del análisis
├── pyproject.toml                # configuración y dependencias
├── uv.lock                       # versiones bloqueadas
├── src/
│   ├── README.MD                 # esta guía
│   └── app/
│       ├── data_preparation.py   # clase DataPreparation
│       ├── pca_module.py         # clase PCA_Module
│       ├── efa.py                # clase EFA
│       └── kernel_pca.py         # clase KernelPCA
└── docs/                         # guía y ejemplos de la actividad
```

## 3. Instalar las dependencias

Desde la carpeta raíz `actividad_dimensionalidad`, sincroniza el entorno del proyecto:

```bash
uv sync
```

El análisis utiliza `pandas`, `numpy`, `scikit-learn`, `factor-analyzer`, `matplotlib`, `seaborn` y `scipy`. Si se necesita agregar un paquete nuevo, utiliza:

```bash
uv add nombre-del-paquete
```

Este comando actualiza `pyproject.toml` y `uv.lock`.

## 4. Ejecutar el análisis

Desde la raíz del proyecto, ejecuta el flujo completo con:

```bash
uv run python main.py
```

El programa descarga el conjunto de datos Seeds desde UCI y ejecuta, en orden, la preparación de los datos, el ACP, el AFE, el Kernel PCA y una comparación general de los resultados. Las tablas se imprimen en la terminal y los gráficos se muestran durante la ejecución.

## 5. Cambiar parámetros del análisis

Los parámetros se modifican al crear los objetos en `main.py`:

```python
pca = PCA_Module(n_components=3)

efa = EFA(n_factors=3, method="ml", rotation="varimax")

kpca = KernelPCA(n_components=2, kernel="rbf", gamma=None)
```

En el ACP, `n_components` controla el número máximo de componentes calculadas. En el AFE, `n_factors` define el número de factores, `method="ml"` utiliza máxima verosimilitud y `rotation="varimax"` aplica una rotación ortogonal. En Kernel PCA, `kernel="rbf"` permite modelar relaciones no lineales y `gamma` controla el alcance del kernel; cuando es `None`, scikit-learn utiliza su valor predeterminado.

La variable `variety` se conserva para colorear los gráficos y contrastar la separación entre Kama, Rosa y Canadian, pero no participa en la construcción de las representaciones.

## 6. Solución de problemas

- **Error al descargar el dataset:** verifica la conexión a internet y que la URL de UCI siga disponible.
- **Error de paquete no encontrado:** ejecuta `uv sync` desde la raíz del proyecto.
- **Advertencia sobre `VIRTUAL_ENV`:** ejecuta `deactivate` y después utiliza `uv run python main.py`.
- **Error de compatibilidad de `factor-analyzer`:** revisa el ajuste de compatibilidad incluido al inicio de `src/app/efa.py`.
- **Error `var_names` en Kernel PCA:** en `main.py` debe usarse la clase propia `KernelPCA` importada desde `src.app.kernel_pca`, no la clase `KernelPCA` directamente desde scikit-learn.
- **Conflicto de nombres en Kernel PCA:** dentro de `kernel_pca.py`, la clase de scikit-learn se importa con el alias `SklearnKernelPCA`.
