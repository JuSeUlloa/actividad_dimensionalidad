import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns


class PCA_Module:

    def __init__(self, n_components=None):
        self.n_components = n_components
        self.pca = None
        self.eigenvalues = None
        self.prop_var = None
        self.cum_var = None
        self.loadings = None
        self.var_coord = None
        self.cos2 = None
        self.contrib = None
        self.ind_coord = None
        self.var_names = None

    def get_loadings(self):
            print("\n=== Vectores propios (loadings) ===")
            print(self.loadings.round(4).to_string())
            return self.loadings
    
    def get_variable_coordinates(self):
            print("\n=== Coordenadas de las variables ===")
            print(self.var_coord.round(4).to_string())
            return self.var_coord
    
    def get_cos2(self):
            print("\n=== Cosenos cuadrados ===")
            print(self.cos2.round(4).to_string())
            return self.cos2
    
    def get_contributions(self):
            print("\n=== Contribuciones (%) ===")
            print(self.contrib.round(4).to_string())
            return self.contrib
    
    def get_individual_coordinates(self):
            print("\n=== Coordenadas de los individuos (primeras 10) ===")
            print(self.ind_coord.head(10).round(4).to_string())
            return self.ind_coord

    def fit(self, data_scaled, var_names=None):

        self.var_names = var_names if var_names is not None else data_scaled.columns
        self.pca = PCA(n_components=self.n_components)
        self.pca.fit(data_scaled)

        self.eigenvalues = self.pca.explained_variance_
        self.prop_var = self.pca.explained_variance_ratio_
        self.cum_var = np.cumsum(self.prop_var)

        eigvecs = self.pca.components_
        self.loadings = pd.DataFrame(
            eigvecs.T,
            index=self.var_names,
            columns=[f"PC{i+1}" for i in range(eigvecs.shape[0])]
        )

        self.var_coord = self.loadings * np.sqrt(self.eigenvalues)
        self.cos2 = (self.var_coord ** 2).div(
            (self.var_coord ** 2).sum(axis=1), axis=0
        )
        self.contrib = (self.var_coord ** 2).div(
            (self.var_coord ** 2).sum(axis=0), axis=1
        ) * 100

        self.ind_coord = pd.DataFrame(
            self.pca.transform(data_scaled),
            columns=[f"PC{i+1}" for i in range(eigvecs.shape[0])]
        )
        return self

    def get_eigenvalues(self):

        df = pd.DataFrame({
            "sd": np.sqrt(self.eigenvalues),
            "eigenvalue": self.eigenvalues,
            "percent": self.prop_var * 100,
            "cumulative": self.cum_var * 100
        }, index=[f"PC{i+1}" for i in range(len(self.eigenvalues))])
        print("\n=== Valores propios e inercia ===")
        print(df.round(4).to_string())
        return df

    

    def plot_scree(self):
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        axes[0].bar(
            range(1, len(self.prop_var) + 1),
            self.prop_var * 100, alpha=0.7, color="steelblue"
        )
        axes[0].set_xlabel("Componente")
        axes[0].set_ylabel("% de Varianza Explicada")
        axes[0].set_title("Scree Plot")
        axes[0].set_xticks(range(1, len(self.prop_var) + 1))

        axes[1].plot(
            range(1, len(self.cum_var) + 1),
            self.cum_var * 100, "o-", color="darkorange"
        )
        axes[1].set_xlabel("Número de Componentes")
        axes[1].set_ylabel("Varianza Acumulada (%)")
        axes[1].set_title("Varianza Acumulada")
        axes[1].set_xticks(range(1, len(self.cum_var) + 1))
        axes[1].axhline(y=80, color="red", linestyle="--", alpha=0.5)

        plt.tight_layout()
        plt.show()

    def plot_correlation_circle(self, pc_x=0, pc_y=1):
        pcx = f"PC{pc_x+1}"
        pcy = f"PC{pc_y+1}"
        fig, ax = plt.subplots(figsize=(8, 8))

        theta = np.linspace(0, 2 * np.pi, 100)
        ax.plot(np.cos(theta), np.sin(theta), "k--", alpha=0.3)

        for var in self.var_names:
            ax.annotate(
                "",
                xy=(self.var_coord.loc[var, pcx], self.var_coord.loc[var, pcy]),
                xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="steelblue", lw=1.5)
            )
            ax.text(
                self.var_coord.loc[var, pcx] * 1.1,
                self.var_coord.loc[var, pcy] * 1.1,
                var, fontsize=11, ha="center", va="center"
            )

        ax.set_xlabel(f"{pcx} ({self.prop_var[pc_x]*100:.1f}%)")
        ax.set_ylabel(f"{pcy} ({self.prop_var[pc_y]*100:.1f}%)")
        ax.set_title(f"Círculo de Correlaciones ({pcx} vs {pcy})")
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.axhline(y=0, color="gray", linewidth=0.5)
        ax.axvline(x=0, color="gray", linewidth=0.5)
        ax.set_aspect("equal")
        plt.tight_layout()
        plt.show()

    def get_summary(self):
            print("\n=== Resumen ACP ===")
            print(f"Componentes retenidas: {len(self.eigenvalues)}")
            print(f"Varianza PC1: {self.prop_var[0]*100:.2f}%")
            print(f"Varianza PC2: {self.prop_var[1]*100:.2f}%")
            print(f"Varianza acumulada (2 comp): {self.cum_var[1]*100:.2f}%")

    def plot_individuals(self, variety, pc_x=0, pc_y=1):
        pcx = f"PC{pc_x+1}"
        pcy = f"PC{pc_y+1}"
        fig, ax = plt.subplots(figsize=(10, 8))

        for label, color in zip(["Kama", "Rosa", "Canadian"],
                                ["#E63946", "#457B9D", "#2A9D8F"]):
            mask = variety == label
            ax.scatter(
                self.ind_coord.loc[mask.values, pcx],
                self.ind_coord.loc[mask.values, pcy],
                c=color, label=label, alpha=0.7, s=60, edgecolors="white"
            )

        ax.set_xlabel(f"{pcx} ({self.prop_var[pc_x]*100:.1f}%)")
        ax.set_ylabel(f"{pcy} ({self.prop_var[pc_y]*100:.1f}%)")
        ax.set_title(f"ACP - Individuos ({pcx} vs {pcy})")
        ax.axhline(y=0, color="gray", linewidth=0.5)
        ax.axvline(x=0, color="gray", linewidth=0.5)
        ax.legend()
        plt.tight_layout()
        plt.show()

    def plot_biplot(self, variety, pc_x=0, pc_y=1):
        pcx = f"PC{pc_x+1}"
        pcy = f"PC{pc_y+1}"
        fig, ax = plt.subplots(figsize=(12, 10))

        for label, color in zip(["Kama", "Rosa", "Canadian"],
                                ["#E63946", "#457B9D", "#2A9D8F"]):
            mask = variety == label
            ax.scatter(
                self.ind_coord.loc[mask.values, pcx],
                self.ind_coord.loc[mask.values, pcy],
                c=color, label=label, alpha=0.5, s=40, edgecolors="white", zorder=2
            )

        scale = max(
            self.ind_coord[pcx].max() - self.ind_coord[pcx].min(),
            self.ind_coord[pcy].max() - self.ind_coord[pcy].min()
        ) / 2

        for var in self.var_names:
            ax.annotate(
                "",
                xy=(self.var_coord.loc[var, pcx] * scale,
                    self.var_coord.loc[var, pcy] * scale),
                xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="red", lw=2),
                zorder=3
            )
            ax.text(
                self.var_coord.loc[var, pcx] * scale * 1.15,
                self.var_coord.loc[var, pcy] * scale * 1.15,
                var, fontsize=10, ha="center", va="center",
                color="red", fontweight="bold", zorder=3
            )

        ax.set_xlabel(f"{pcx} ({self.prop_var[pc_x]*100:.1f}%)")
        ax.set_ylabel(f"{pcy} ({self.prop_var[pc_y]*100:.1f}%)")
        ax.set_title("Biplot ACP - Seeds Dataset")
        ax.axhline(y=0, color="gray", linewidth=0.5)
        ax.axvline(x=0, color="gray", linewidth=0.5)
        ax.legend()
        plt.tight_layout()
        plt.show()

    def plot_contributions(self, component=1):
        pc = f"PC{component}"
        contrib_pc = self.contrib[pc].sort_values(ascending=True)
        umbral = 100 / len(self.var_names)

        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ["red" if v > umbral else "steelblue" for v in contrib_pc.values]
        contrib_pc.plot(kind="barh", ax=ax, color=colors)
        ax.axvline(x=umbral, color="red", linestyle="--", alpha=0.7,
                   label=f"Umbral ({umbral:.1f}%)")
        ax.set_xlabel("Contribución (%)")
        ax.set_ylabel("Variable")
        ax.set_title(f"Contribución de Variables a {pc}")
        ax.legend()
        plt.tight_layout()
        plt.show()

    