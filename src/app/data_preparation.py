import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns


class DataPreparation:
    
    def __init__(self):
        self.data = None
        self.data_scaled = None
        self.scaler = StandardScaler()
        self.variety = None
        self.var_names = None

    def get_numeric_variables(self):
            return self.data[self.var_names]
    
    def get_variety(self):
            return self.variety
    
    def get_scaled_data(self):
            return self.data_scaled

    def load_data(self, url):
        self.data = pd.read_csv(url, header=None, sep='\s+')
        self.data.columns = [
            "area", "perimeter", "compactness", "kernel_length",
            "kernel_width", "asymmetry_coefficient",
            "kernel_groove_length", "variety"
        ]
        self.data["variety"] = pd.Categorical(
            self.data["variety"],
            categories=[1, 2, 3],
            ordered=True
        ).rename_categories({1: "Kama", 2: "Rosa", 3: "Canadian"})

        self.variety = self.data["variety"]
        self.var_names = [c for c in self.data.columns if c != "variety"]
        return self.data

    def describe(self):
        desc = self.data[self.var_names].describe().loc[["mean", "std", "min", "max"]]
        print(desc.round(4).to_string())
        return desc

    def correlation_matrix(self):
        correlation = self.data[self.var_names].corr()
        print("\n=== Matriz de correlaciones ===")
        print(correlation.round(3).to_string())

        fig, ax = plt.subplots(figsize=(10, 8))
        mask = np.triu(np.ones_like(correlation, dtype=bool), k=1)
        sns.heatmap(
            correlation, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
            center=0, vmin=-1, vmax=1, square=True,
            linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8}
        )
        ax.set_title("Matriz de Correlaciones")
        plt.tight_layout()
        plt.show()
        return correlation

    def standardize(self):
        X = self.data[self.var_names].values
        self.data_scaled = self.scaler.fit_transform(X)
        self.data_scaled = pd.DataFrame(
            self.data_scaled, columns=self.var_names
        )
        print("\n=== Datos estandarizados ===")
        print(self.data_scaled.describe().round(4).to_string())
        return self.data_scaled

    