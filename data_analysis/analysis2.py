import os
import pathlib
import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import pytensor.tensor as pt
import seaborn as sns
from dataclasses import dataclass

from typing import Optional

import scienceplots
plt.style.use(['science', 'ieee'])

LOAD_TRACE=False
YEAR = 2015

@dataclass()
class AnalisisData:
    year: int
    trace: Optional[az.InferenceData]= None
    data: Optional[pd.DataFrame]= None
    p_aprobado: Optional[pd.Series]= None
    p_rechazado_leve : Optional[pd.Series]= None
    p_rechazado_grave: Optional[pd.Series]= None
    summary: Optional[pd.DataFrame]= None

    def calc_estimates(self):
        self.p_aprobado_calc = self.data['Aprobado'].sum()/len(self.data['Aprobado'])
        self.p_rechazado_leve_calc = self.data['RechazadoLeveModerado'].sum()/len(self.data['RechazadoLeveModerado'])
        self.p_rechazado_grave_calc = self.data['RechazadoGrave'].sum()/len(self.data['RechazadoGrave'])

    def estimate_year(self, load_trace):

        print("--x--"*10)
        print(f"Inferencia para YEAR={self.year}")
        DATA = pathlib.Path(os.getcwd()) / f"dataset/joined/{YEAR}_CERTIFICADOS.csv"

        self.data = pd.read_csv(DATA)
        self.data = self.data[["Aprobado", "RechazadoLeveModerado", "RechazadoGrave"]]

        if load_trace:
            trace = az.from_netcdf(f"analysis_data/trace_{YEAR}.nc")
        else:
            with pm.Model() as coin_flipping:
                p = pm.Dirichlet('p', np.ones(3))
                y = pm.Multinomial('likelihood', n=1, p=p, observed=self.data.head(10000))
                trace = pm.sample(1000, tune=1000)
                # ppc = pm.sample_posterior_predictive(trace)
                trace.to_netcdf(f"analysis_data/trace_{YEAR}.nc")

        self.summ = az.summary(trace)
        print(self.summ)
        df = trace.to_dataframe()
        self.p_aprobado = df[('posterior', 'p[0]', 0)]
        self.p_rechazado_leve = df[('posterior', 'p[1]', 1)]
        self.p_rechazado_grave = df[('posterior', 'p[2]', 2)]
        az.plot_trace(trace)
        plt.savefig(f"analysis_data/traceplot_{YEAR}.png")

    def plot_data(self):

        self.calc_estimates()
        fig, ax = plt.subplots(1,3, sharey=True)
        fig.set_size_inches(6.3,3.1)
        hist, bins, patches = ax[0].hist(self.p_aprobado, density=True, label=r"$P_{Ap}$")
        sns.kdeplot(data=self.p_aprobado, ax=ax[0])
        ax[0].vlines(self.p_aprobado_calc,0,np.max(hist)*1.1, colors='r', label=r"$P_{ApEstimada}$")
        ax[0].set_xlabel(r"$p_{Aprobado}$")
        ax[0].set_ylabel("Frecuencia")
        # ax[0].legend(loc='center', bbox_to_anchor=(0.1,-0.2),
        #              shadow=True,
        #              frameon=True,
        #              fancybox=True)

        hist, bins, patches = ax[1].hist(self.p_rechazado_leve, density=True, label=r"$P_{Cond}$")
        sns.kdeplot(data=self.p_rechazado_leve, ax=ax[1])
        ax[1].vlines(self.p_rechazado_leve_calc,0,np.max(hist)*1.1, colors='r', label=r"$P_{Estimada}$")
        ax[1].set_xlabel(r"$p_{ReLe}$")
        # ax[1].set_ylabel("Frecuencia")
        # ax[0].legend(loc='center',
        #              bbox_to_anchor=(0.1,-0.2),
        #              shadow=True,
        #              frameon=True,
        #              fancybox=True)

        hist, bins, patches = ax[2].hist(self.p_rechazado_grave, density=True, label=r"$P_{Cond}$")
        sns.kdeplot(data=self.p_rechazado_grave, ax=ax[2])
        ax[2].vlines(self.p_rechazado_grave_calc, 0, np.max(hist)*1.1, colors='r', label=r"$P_{Estimada}$")
        ax[2].set_xlabel(r"$p_{ReGr}$")
        # ax[2].set_ylabel("Frecuencia")
        # print(ppc.posterior_predictive)
        # az.plot_ppc(ppc, ax=ax[1])
        # ax[1].plot(ppc)
        # ax[2].legend(loc='center',
        #              bbox_to_anchor=(0.1,-0.2),
        #              shadow=True,
        #              frameon=True,
        #              fancybox=True)
        plt.legend()
        plt.savefig(f"analysis_data/ppc_{YEAR}.png", dpi=600)


def plot_p(summs, key, ax, label):
    years = list(summs.keys())
    means = np.array([summ["mean"][key] for summ in summs.values()])
    sds = np.array([summ["sd"][key] for summ in summs.values()])

    ax.plot(years, means, label=label)
    ax.plot(years, means+sds)
    ax.plot(years, means-sds)
    ax.fill_between(years, means-sds, means+sds, alpha = 0.4)

    ax.set_xlabel("Año")
    ax.set_ylabel(r"$\mathcal{P}$")
    ax.legend()

    return ax

def plot_densities(sample_dict, ax, label, set_legend=False):
    cmap = plt.get_cmap("RdPu")
    tot_years = len(list(sample_dict.keys()))
    for i, (year, samples) in enumerate(sample_dict.items()):
        color = cmap(i/tot_years + 0.3)
        label_parsed = f"Año {year}"
        sns.kdeplot(data=samples, ax=ax, label=label_parsed, fill=True, color=color)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title(label)
    if set_legend:
        plt.legend(# loc="center", ncols=2,
                bbox_to_anchor=(0, 0)
            )
    return ax



def extract_key(df, key, component):
    return df[key].iloc[component]

if __name__ == "__main__":

    summ_dict = {}
    p_ap_dict = {}
    p_rele_dict = {}
    p_regr_dict = {}

    for YEAR in range(2015, 2022):
        analisis = AnalisisData(YEAR)
        analisis.estimate_year(True)
        # analisis.plot_data()
        summ_dict[YEAR] = analisis.summ
        p_ap_dict[YEAR] = analisis.p_aprobado
        p_rele_dict[YEAR] = analisis.p_rechazado_leve
        p_regr_dict[YEAR] = analisis.p_rechazado_grave

    fig, axs = plt.subplots(1,3, sharex=True)
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.4, hspace=0.4)
    fig.set_size_inches(6.3,3.1)

    ax = plot_p(summ_dict, 0, axs[0], label = r"$P_{Ap}$")
    ax = plot_p(summ_dict, 1, axs[1], label = r"$P_{AC}$")
    ax = plot_p(summ_dict, 2, axs[2], label = r"$P_{Re}$")
    plt.legend()
    plt.savefig(f"analysis_data/p_aprobado_anual.png", dpi=600)

    fig, axs = plt.subplots(3,1, sharex=False)
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.4, hspace=0.6)
    fig.set_size_inches(6.3,3.1)

    ax = plot_densities(p_ap_dict, axs[0], label = r"$P_{Ap}$")
    ax = plot_densities(p_rele_dict,axs[1], label = r"$P_{AC}$")
    ax = plot_densities(p_regr_dict,axs[2], label = r"$P_{Re}$", set_legend=True)
    plt.legend()
    plt.savefig(f"analysis_data/kde_total_cool.png", dpi=600)
