import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, purple

# fig, ax = plt.subplots(1, 1, figsize=(2,2))
data = np.load("../data/svf/data.npz")
M_std_rel = data['M_std_rel']

N = 6
s = 10
alpha = 0.5
linestyle = '--'
fig, ax = plt.subplots(1, 1, figsize=(2.5,2.4))
steps = np.arange(1,3+1)

scale = 10
ax.errorbar(steps, M_std_rel[:, 0]*scale, M_std_rel[:, 1]*scale, color=purple, fmt=',')
ax.scatter(steps, M_std_rel[:, 0]*scale, color=purple, s=10)
ax.plot(steps, M_std_rel[:, 0]*scale, color=purple)
ax.set_ylim(0, 4)
ax.set_xlim(0.75, 3.25)
ax.set_xticks([1, 2, 3])
ax.set_yticks([0, 1, 2, 3, 4])
ax.set_xticklabels([0, 1, 2])
# axs[0, j].scatter(steps, y1, color=purple, s=s)

ax.set_xlabel('SVF step')
ax.set_ylabel(r'Relative deviation, \%')

plt.savefig("svf-avg.pdf", bbox_inches='tight')
plt.close()