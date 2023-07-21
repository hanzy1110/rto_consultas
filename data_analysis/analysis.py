import os
import pathlib
import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import pytensor.tensor as pt

YEAR = 2015
DATA = pathlib.Path(os.getcwd()) / f"dataset/joined/{YEAR}_CERTIFICADOS.csv"

data = pd.read_csv(DATA)
data = data[["Aprobado", "RechazadoLeveModerado", "RechazadoGrave"]]

print(data.head())
with pm.Model() as coin_flipping:
    p = pm.Dirichlet('p', np.ones(3))
    y = pm.Bernoulli('y', p=p, observed=data)
    trace = pm.sample(1000, tune=1000)
    # ppc = pm.sample_posterior_predictive(trace)
    az.plot_trace(trace)
    plt.savefig(f"analysis_data/traceplot_{YEAR}.png")
    print(az.summary(trace))
    trace.to_netcdf(f"analysis_data/trace_{YEAR}.nc")

fig, ax = plt.subplots(2,1, figsize=(15,15))
az.plot_posterior(trace, ax=ax[0])
# print(ppc.posterior_predictive)
# az.plot_ppc(ppc, ax=ax[1])
# ax[1].plot(ppc)
plt.savefig(f"analysis_data/ppc_{YEAR}.png")
