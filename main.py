from src.app.pca_module import  PCA_Module
from src.app.efa import EFA
from src.app.data_preparation import DataPreparation
from src.app.kernel_pca import KernelPCA

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 8)

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00236/seeds_dataset.txt"

def main():
    # ============================
    # 1. Preparación de datos
    # ============================
    print("=" * 60)
    print("SECCIÓN 1: PREPARACIÓN DE DATOS")
    print("=" * 60)

    data_prep = DataPreparation()
    data_prep.load_data(URL)
    data_prep.describe()
    data_prep.correlation_matrix()
    data_scaled = data_prep.standardize()

    print("\n" + "=" * 60)
    print("SECCIÓN 2: ANÁLISIS DE COMPONENTES PRINCIPALES")
    print("=" * 60)

    pca = PCA_Module()
    pca.fit(data_scaled, var_names=data_prep.var_names)
    pca.get_eigenvalues()
    pca.get_loadings()
    pca.get_variable_coordinates()
    pca.get_cos2()
    pca.get_contributions()
    pca.get_individual_coordinates()

    pca.plot_scree()
    pca.plot_correlation_circle(pc_x=0, pc_y=1)
    pca.plot_individuals(variety=data_prep.get_variety(), pc_x=0, pc_y=1)
    pca.plot_biplot(variety=data_prep.get_variety(), pc_x=0, pc_y=1)
    pca.plot_contributions(component=1)
    pca.plot_contributions(component=2)
    pca.get_summary()

    print("\n" + "=" * 60)
    print("SECCIÓN 3: ANÁLISIS FACTORIAL EXPLORATORIO")
    print("=" * 60)

    efa = EFA()
    variables = data_prep.get_numeric_variables()

    efa.test_bartlett(variables)
    efa.calculate_kmo(variables)
    eigen_reales, eigen_simulados, n_factors = efa.parallel_analysis(variables)

    efa.fit(variables, n_factors=n_factors)
    efa.get_loadings(rotated=False)
    efa.get_communalities()

    efa.rotate(method="varimax")
    efa.plot_loadings(rotated=True)
    efa.plot_communalities()
    efa.get_summary()

    print("\n" + "=" * 60)
    print("SECCIÓN 4: KERNEL PCA")
    print("=" * 60)

    kpca = KernelPCA(n_components=2, kernel="rbf", gamma=None)
    kpca.fit(data_scaled, var_names=data_prep.var_names)
    kpca.get_eigenvalues()
    kpca.get_individual_coordinates()
    kpca.plot_2d(variety=data_prep.get_variety())
    kpca.compare_with_pca(pca, variety=data_prep.get_variety())
    kpca.get_summary()

    print("\n" + "=" * 60)
    print("SECCIÓN 5: COMPARACIÓN DE RESULTADOS")
    print("=" * 60)

    print("\n--- Estructura global (ACP) ---")
    print(f"PC1 y PC2 explican {pca.cum_var[1]*100:.2f}% de la varianza total.")
    print("Las variedades muestran separación en el espacio de componentes.")

    print("\n--- Dimensiones latentes (AFE) ---")
    print(f"Se retuvieron {efa.n_factors} factores con rotación varimax.")
    print("Los factores capturan dimensiones morfológicas subyacentes.")

    print("\n--- Patrón no lineal (Kernel PCA) ---")
    print("Kernel PCA revela estructura no lineal que PCA lineal no captura.")
    print("La separación entre variedades puede ser más clara en el espacio kernel.")

    print("\n=== Análisis completado ===")


if __name__ == "__main__":
    main()