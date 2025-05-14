# can be deleted

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue

fig, ax = plt.subplots(1, 1, figsize=(1.5,1.5))
data = np.load("../data/step-plot/data.npz")
df, df2, x = data['df'], data['df2'], data['spill_powers']

df_mean = df[:, ::3]
df_std = df[:, 1::3]
df_counts = df[:, 2::3]
df_sem = df_std / df_counts**0.5

df2_mean = df2[:, ::3]
df2_std = df2[:, 1::3]
df2_counts = df2[:, 2::3]
df2_sem = df2_std / df2_counts**0.5
