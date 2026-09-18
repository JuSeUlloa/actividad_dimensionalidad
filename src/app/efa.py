import pandas as pd
import numpy as np
from scipy import stats
from factor_analyzer import FactorAnalyzer
import factor_analyzer.factor_analyzer as _fa_mod
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
import matplotlib.pyplot as plt
import seaborn as sns



def _patched_check_array(*args, **kwargs):
    if "force_all_finite" in kwargs:
        kwargs["ensure_all_finite"] = kwargs.pop("force_all_finite")
    return _original_check_array(*args, **kwargs)


import sklearn.utils.validation as _val
_original_check_array = _val.check_array
_val.check_array = _patched_check_array
_fa_mod.check_array = _patched_check_array


class EFA:

    def __init__(self, n_factors=None, method="ml", rotation="varimax"):
        self.n_factors = n_factors
        self.method = method
        self.rotation = rotation
        self.fa = None
        self.fa_rotated = None
        self.loadings = None
        self.loadings_rotated = None
        self.var_names = None

    def get_summary(self):
            print("\n=== Resumen AFE ===")
            print(f"Número de factores: {self.n_factors}")
            print(f"Método: {self.method}")
            print(f"Rotación: {self.rotation}")

    def test_bartlett(self, data):
        chi2, p_value = calculate_bartlett_sphericity(data)
        print("\n=== Prueba de esfericidad de Bartlett ===")
        print(f"Chi-cuadrado: {chi2:.2f}")
        print(f"Valor p: {p_value:.2e}")
        print("Resultado: se rechaza H0 (la matriz no es identidad)")
        return chi2, p_value

    def calculate_kmo(self, data):
        R = data.corr()
        kmo_per_var, kmo_overall = calculate_kmo(R)
        print(f"\n=== Índice KMO ===")
        print(f"KMO global: {kmo_overall:.4f}")
        kmo_df = pd.DataFrame({"KMO": kmo_per_var}, index=data.columns)
        print("\nKMO por variable:")
        print(kmo_df.round(4).to_string())
        return kmo_overall, kmo_df

    def parallel_analysis(self, data, n_iter=200, random_state=123):
        rng = np.random.RandomState(random_state)
        n, p = data.shape
        eigen_reales = np.sort(np.linalg.eigvalsh(data.corr()))[::-1]

        eigen_simulados = np.zeros(p)
        for _ in range(n_iter):
            datos_sim = rng.normal(size=(n, p))
            R_sim = np.corrcoef(datos_sim, rowvar=False)
            eigen_sim = np.sort(np.linalg.eigvalsh(R_sim))[::-1]
            eigen_simulados += eigen_sim
        eigen_simulados /= n_iter

        n_factors = sum(eigen_reales > eigen_simulados)

        fig, ax = plt.subplots(figsize=(8, 5))
        x = range(1, len(eigen_reales) + 1)
        ax.plot(x, eigen_reales, "o-", color="steelblue", label="Eigenvalores reales")
        ax.plot(x, eigen_simulados, "o--", color="darkorange",
                label="Eigenvalores simulados (media)")
        ax.axhline(y=1, color="red", linestyle=":", alpha=0.5,
                   label="Kaiser (eigenval = 1)")
        ax.set_xlabel("Número de Factor")
        ax.set_ylabel("Valor Propio")
        ax.set_title("Análisis Paralelo")
        ax.set_xticks(list(x))
        ax.legend()
        plt.tight_layout()
        plt.show()

        print(f"\n=== Análisis paralelo ===")
        print(f"Factores sugeridos: {n_factors}")
        return eigen_reales, eigen_simulados, n_factors

    def fit(self, data, n_factors=None):
        
        if n_factors is not None:
            self.n_factors = n_factors
            
        self.var_names = data.columns
        self.data = data  

        self.fa = FactorAnalyzer(
            n_factors=self.n_factors, method=self.method, rotation=None
        )
        self.fa.fit(data)

        self.loadings = pd.DataFrame(
            self.fa.loadings_,
            index=self.var_names,
            columns=[f"F{i+1}" for i in range(self.n_factors)]
        )
        return self

    def rotate(self, method="varimax"):
        self.rotation = method
        self.fa_rotated = FactorAnalyzer(
            n_factors=self.n_factors, method=self.method, rotation=method
        )
        self.fa_rotated.fit(self.data) 

        self.loadings_rotated = pd.DataFrame(
            self.fa_rotated.loadings_,
            index=self.var_names,
            columns=[f"F{i+1}" for i in range(self.n_factors)]
        )
        print(f"\n=== AFE: {self.n_factors} factores, rotación {method.upper()} ===")
        cargas_display = self.loadings_rotated.copy()
        cargas_display[cargas_display.abs() < 0.30] = np.nan
        print("\nCargas factoriales (|carga| > 0.30):")
        print(cargas_display.round(4).to_string())
        return self.loadings_rotated

    def get_loadings(self, rotated=True):
        cargas = self.loadings_rotated if rotated and self.loadings_rotated is not None else self.loadings
        print("\n=== Cargas factoriales ===")
        print(cargas.round(4).to_string())
        return cargas

    def get_communalities(self):
        comunalidades = pd.DataFrame({
            "comunalidad": self.fa.get_communalities(),
            "varianza_unica": self.fa.get_uniquenesses()
        }, index=self.var_names)
        print("\n=== Comunalidades y Varianzas únicas ===")
        print(comunalidades.round(4).to_string())
        return comunalidades

    def get_residuals(self):
        R = self.fa.model_.corr() if hasattr(self.fa.model_, 'corr') else pd.DataFrame()
        L = self.fa.loadings_
        psi = np.diag(self.fa.get_uniquenesses())
        R_hat = L @ L.T + psi
        residuos = R.values - R_hat if hasattr(R, 'values') else R - R_hat
        print("\n=== Correlación residual ===")
        print(pd.DataFrame(residuos, index=self.var_names, columns=self.var_names).round(3).to_string())
        return residuos

    def plot_loadings(self, rotated=True):
        cargas = self.loadings_rotated if rotated and self.loadings_rotated is not None else self.loadings
        fig, ax = plt.subplots(figsize=(8, 8))
        sns.heatmap(
            cargas, annot=True, fmt=".3f", cmap="RdBu_r",
            center=0, vmin=-1, vmax=1, linewidths=0.5, ax=ax,
            cbar_kws={"shrink": 0.8}
        )
        ax.set_title(f"Cargas Factoriales ({'Rotadas' if rotated else 'Sin rotar'})")
        ax.set_ylabel("Variable")
        ax.set_xlabel("Factor")
        plt.tight_layout()
        plt.show()

    def plot_communalities(self):
        com = self.get_communalities()
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(com))
        width = 0.35
        ax.bar([i - width/2 for i in x], com["comunalidad"], width,
               label="Comunalidad", color="steelblue", alpha=0.8)
        ax.bar([i + width/2 for i in x], com["varianza_unica"], width,
               label="Varianza única", color="darkorange", alpha=0.8)
        ax.axhline(y=0.7, color="red", linestyle="--", alpha=0.5,
                   label="Umbral comunalidad (0.7)")
        ax.axhline(y=0.3, color="green", linestyle="--", alpha=0.5,
                   label="Umbral var. única (0.3)")
        ax.set_xticks(list(x))
        ax.set_xticklabels(com.index, rotation=45, ha="right")
        ax.set_ylabel("Valor")
        ax.set_title("Comunalidades y Varianzas Únicas")
        ax.legend()
        plt.tight_layout()
        plt.show()

    