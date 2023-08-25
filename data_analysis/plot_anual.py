import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import scienceplots
plt.style.use(["science", "ieee"])

plt.rc('ytick', labelsize=6)
plt.rc('xtick', labelsize=4)

plt.rc('axes', labelsize=6)
plt.rc('axes', titlesize=6)
plt.rc('font', size=6)
plt.rc('legend', fontsize=6)

verificaciones = pd.read_csv("cantidades.csv")["Cant verificaciones"]
ParqueAutomotor = np.array([266115, 282901, 303739, 323238, 338987, 347396, 354816, 364748,])
years = range(2015, 2023)

proportions = np.array(verificaciones) / ParqueAutomotor
recip_proportions = 1-proportions
proportions *= 100
recip_proportions *= 100

# plot bars in stack manner
fig, ax = plt.subplots(1,1)
fig.set_size_inches(3.2,3.2)

ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.bar(years, recip_proportions, color='r', label="Porcentaje sin verificar")
ax.bar(years, proportions, bottom=recip_proportions, color='b', label="Porcentaje Verificado")
ax.set_xlabel("Año")
ax.legend(bbox_to_anchor=(1.1,-0.1), ncols=2)
plt.savefig("analysis_data/proportions.jpg", dpi=600)
