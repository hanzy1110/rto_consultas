import os
import pathlib
import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import pytensor.tensor as pt

import scienceplots
plt.style.use(['science', 'ieee'])

LOAD_TRACE=False
YEAR = 2015
DATA = pathlib.Path(os.getcwd()) / f"dataset/joined/{YEAR}_CERTIFICADOS.csv"

data = pd.read_csv(DATA)
data = data[["Aprobado", "RechazadoLeveModerado", "RechazadoGrave"]]

p_aprobado_calc = data['Aprobado'].sum()/len(data['Aprobado'])
p_rechazado_leve_calc = data['RechazadoLeveModerado'].sum()/len(data['RechazadoLeveModerado'])
p_rechazado_grave_calc = data['RechazadoGrave'].sum()/len(data['RechazadoGrave'])

if LOAD_TRACE:
    trace = az.from_netcdf(f"analysis_data/trace_{YEAR}.nc")
else:
    print(data.head())
    with pm.Model() as coin_flipping:
        p = pm.Dirichlet('p', np.ones(3))
        y = pm.Bernoulli('y', p=p, observed=data.head(10000))
        trace = pm.sample(1000, tune=1000)
        # ppc = pm.sample_posterior_predictive(trace)
        trace.to_netcdf(f"analysis_data/trace_{YEAR}.nc")

print(az.summary(trace))
df = trace.to_dataframe()
p_aprobado = df[('posterior', 'p[0]', 0)]
p_rechazado_leve = df[('posterior', 'p[1]', 1)]
p_rechazado_grave = df[('posterior', 'p[2]', 2)]

az.plot_trace(trace)
plt.savefig(f"analysis_data/traceplot_{YEAR}.png")
fig, ax = plt.subplots(1,3, figsize=(20,10))
hist, bins, patches = ax[0].hist(p_aprobado, density=True, label="Probalidad Certificado Aprobado")
ax[0].vlines(p_aprobado_calc,0,np.max(hist)*1.1, colors='r', label="Ratio Estimado")
ax[0].set_xlabel(r"$p_{Aprobado}$")
ax[0].set_ylabel("Frecuencia")
ax[0].legend(loc='upper left', shadow=True, frameon=True, fancybox=True)

hist, bins, patches = ax[1].hist(p_rechazado_leve, density=True, label="Probalidad Certificado Condicional")
ax[1].vlines(p_rechazado_leve_calc,0,np.max(hist)*1.1, colors='r', label="Ratio Estimado")
ax[1].set_xlabel(r"$p_{ReLe}$")
ax[1].set_ylabel("Frecuencia")
ax[1].legend(loc='upper left', shadow=True, frameon=True, fancybox=True)

hist, bins, patches = ax[2].hist(p_rechazado_grave, density=True, label="Probalidad Certificado Rechazado")
ax[2].vlines(p_rechazado_grave_calc, 0, np.max(hist)*1.1, colors='r', label="Ratio Estimado")
ax[2].set_xlabel(r"$p_{ReGr}$")
ax[2].set_ylabel("Frecuencia")
# print(ppc.posterior_predictive)
# az.plot_ppc(ppc, ax=ax[1])
# ax[1].plot(ppc)
ax[2].legend(loc='upper left', shadow=True, frameon=True, fancybox=True)
plt.savefig(f"analysis_data/ppc_{YEAR}.png")
