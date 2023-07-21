import os
import pathlib
import pandas as pd
import numpy as np
import pymc as pm
import arviz as az

YEAR = 2015
DATA = pathlib.Path(os.getcwd()) / f"dataset/joined/{YEAR}_CERTIFICADOS.csv"

data = pd.read_csv(DATA).loc["Aprobado", "RechazadoLeveModerado", "RechazadoGrave"]

print(data.head())
with pm.Model() as coin_flipping:
    p = pm.Uniform('p', lower=0, upper=1, shape=(3,))
    y = pm.Bernoulli('y', p=p, observed=data.head(100))
    trace = pm.sample(1000, tune=1000)
    # reset value to get the shape right
    ppc = pm.sample_posterior_predictive(trace)
    az.traceplot(trace)
