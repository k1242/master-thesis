import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, dblue


data = np.load("../data/flashing-oscilloscope/data.npz")
X_mean = data['X_mean']
Y_mean = data['Y_mean']
Y1 = data['Y1']
Y_std = data['Y_std']

fig, ax = plt.subplots(1, 1, figsize=(7.5, 1))
ax.fill_between(X_mean, Y_mean-Y_std, Y_mean+Y_std, color=blue, alpha=0.5)
# ax.plot(X_mean, Y_mean, color=blue, alpha=0.5)
ax.plot(X_mean, Y1, color='k', linewidth=0.5)
ax.set_xlim(-0.9, 15.9)
ax.set_xlabel(r'time, $\mu$s')
ax.set_ylabel(r'PD signal, a.u.')
ax.grid(alpha=0.25)

ax.plot([0.5, 0.85], [1, 1], color=dblue)
ax.text(0.4, 1, '350ns', ha='right', va='center', fontsize=8, color=dblue)

ax.plot([0.45, 0.5], [0.5, 0.5], color=red)
ax.text(0.4, 0.5, r'50$\,$ns', ha='right', va='center', fontsize=8, color=red)

plt.savefig("flashing-oscilloscope.pdf", bbox_inches='tight', pad_inches=0.06)
plt.close()