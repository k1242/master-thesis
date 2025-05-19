import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue

# fig, ax = plt.subplots(1, 1, figsize=(2,2))
data = np.load("../data/svf/data.npz")
h, v, H, V = data['h'], data['v'], data['H'], data['V']

N = 6
s = 10
alpha = 0.5
linestyle = '--'
fig, axs = plt.subplots(4, N, figsize=(3.9,3))
steps = np.arange(1,3+1)
for j in range(N):
    y1 = H[:, j]
    y2 = (h[:, j] - h[-1, j]) * 1e2
    y3 = V[:, j]
    y4 = (v[:, j] - v[-1, j]) * 1e2
    # H
    axs[0, j].plot(steps, y1, color=blue)
    axs[0, j].scatter(steps, y1, color=blue, s=s)
    axs[0, j].set_ylim(0.6, 1.4)
    axs[0, j].axhline(y=1, color='k', linestyle=linestyle, linewidth=1, alpha=alpha)
    # h
    axs[1, j].plot(steps, y2, color=blue)
    axs[1, j].scatter(steps, y2, color=blue, s=s)
    axs[1, j].set_ylim(-1.5, 1.5)
    axs[1, j].axhline(y=0, color='k', linestyle=linestyle, linewidth=1, alpha=alpha)
    # V
    axs[2, j].plot(steps, y3, color=red)
    axs[2, j].scatter(steps, y3, color=red, s=s)
    axs[2, j].set_ylim(0.6, 1.4)
    axs[2, j].axhline(y=1, color='k', linestyle=linestyle, linewidth=1, alpha=alpha)
    # v
    axs[3, j].plot(steps, y4, color=red)
    axs[3, j].scatter(steps, y4, color=red, s=s)
    axs[3, j].set_ylim(-1.5, 1.5)
    axs[3, j].axhline(y=0, color='k', linestyle=linestyle, linewidth=1, alpha=alpha)
    if j > 0:
        axs[0, j].set_yticks([])
        axs[1, j].set_yticks([])
        axs[2, j].set_yticks([])
        axs[3, j].set_yticks([])

for ax in axs.flatten():
    ax.set_xticks([])
    ax.set_xlim(0.75, 3.25)

axs[0, 0].set_ylabel('$6H$')
axs[1, 0].set_ylabel('$h - h^*$')
axs[2, 0].set_ylabel('$6V$')
axs[3, 0].set_ylabel('$v - v^*$')

fig.subplots_adjust(wspace=0)
plt.savefig("svf.pdf" , bbox_inches='tight')
plt.close()