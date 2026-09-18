import pandas as pd
import numpy as np
from sklearn.decomposition import KernelPCA as SklearnKernelPCA
import matplotlib.pyplot as plt


class KernelPCA:

    def __init__(self, n_components=2, kernel="rbf", gamma=None):
        self.n_components = n_components
        self.kernel = kernel
        self.gamma = gamma
        self.kpca = None
        self.ind_coord = None
        self.eigenvalues = None
        self.var_names = None

    def fit(self, data_scaled, var_names=None):
        self.var_names = var_names if var_names is not None else data_scaled.columns
        self.kpca = SklearnKernelPCA(
            n_components=self.n_components,
            kernel=self.kernel,
            gamma=self.gamma,
            random_state=42
        )
        self.ind_coord = pd.DataFrame(
            self.kpca.fit_transform(data_scaled),
            columns=[f"KPC{i+1}" for i in range(self.n_components)]
        )
        self.eigenvalues = self.kpca.eigenvalues_
        return self

    def get_summary(self):
        print("\n=== Resumen Kernel PCA ===")
        print(f"Kernel: {self.kernel}")
        print(f"Gamma: {self.gamma}")
        print(f"Componentes: {self.n_components}")
        print(f"Varianza KPC1: {self.eigenvalues[0]/self.eigenvalues.sum()*100:.2f}%")
        print(f"Varianza KPC2: {self.eigenvalues[1]/self.eigenvalues.sum()*100:.2f}%")

    def get_eigenvalues(self):

        df = pd.DataFrame({
            "eigenvalue": self.eigenvalues,
            "percent": self.eigenvalues / self.eigenvalues.sum() * 100,
            "cumulative": np.cumsum(self.eigenvalues) / self.eigenvalues.sum() * 100
        }, index=[f"KPC{i+1}" for i in range(len(self.eigenvalues))])
        print("\n=== Valores propios Kernel PCA ===")
        print(df.round(4).to_string())
        return df

    def get_individual_coordinates(self):
        print("\n=== Coordenadas de los individuos (primeras 10) ===")
        print(self.ind_coord.head(10).round(4).to_string())
        return self.ind_coord

    def plot_2d(self, variety):
        fig, ax = plt.subplots(figsize=(10, 8))

        for label, color in zip(["Kama", "Rosa", "Canadian"],
                                ["#E63946", "#457B9D", "#2A9D8F"]):
            mask = variety == label
            ax.scatter(
                self.ind_coord.loc[mask.values, "KPC1"],
                self.ind_coord.loc[mask.values, "KPC2"],
                c=color, label=label, alpha=0.7, s=60, edgecolors="white"
            )

        ax.set_xlabel("KPC1")
        ax.set_ylabel("KPC2")
        ax.set_title(f"Kernel PCA ({self.kernel.upper()}) - Individuos")
        ax.axhline(y=0, color="gray", linewidth=0.5)
        ax.axvline(x=0, color="gray", linewidth=0.5)
        ax.legend()
        plt.tight_layout()
        plt.show()

    def compare_with_pca(self, pca_analysis, variety):
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))

        for label, color in zip(["Kama", "Rosa", "Canadian"],
                                ["#E63946", "#457B9D", "#2A9D8F"]):
            mask = variety == label

            axes[0].scatter(
                pca_analysis.ind_coord.loc[mask.values, "PC1"],
                pca_analysis.ind_coord.loc[mask.values, "PC2"],
                c=color, label=label, alpha=0.7, s=60, edgecolors="white"
            )
            axes[1].scatter(
                self.ind_coord.loc[mask.values, "KPC1"],
                self.ind_coord.loc[mask.values, "KPC2"],
                c=color, label=label, alpha=0.7, s=60, edgecolors="white"
            )

        axes[0].set_xlabel(f"PC1 ({pca_analysis.prop_var[0]*100:.1f}%)")
        axes[0].set_ylabel(f"PC2 ({pca_analysis.prop_var[1]*100:.1f}%)")
        axes[0].set_title("PCA Lineal")
        axes[0].axhline(y=0, color="gray", linewidth=0.5)
        axes[0].axvline(x=0, color="gray", linewidth=0.5)
        axes[0].legend()

        axes[1].set_xlabel("KPC1")
        axes[1].set_ylabel("KPC2")
        axes[1].set_title(f"Kernel PCA ({self.kernel.upper()})")
        axes[1].axhline(y=0, color="gray", linewidth=0.5)
        axes[1].axvline(x=0, color="gray", linewidth=0.5)
        axes[1].legend()

        plt.tight_layout()
        plt.show()

