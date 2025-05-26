import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, gold, purple, cyan
# from scipy.ndimage import gaussian_filter1d

data = np.load("../data/movement/data.npz")

x_scale = 36.6 / 5.6
y_scale = 0.95
x_linear, y_linear, s_linear = data["x_linear"]*x_scale, data["y_linear"]/y_scale, data["s_linear"]/y_scale
x_mjt, y_mjt, s_mjt = data["x_mjt"]*x_scale, data["y_mjt"]/y_scale, data["s_mjt"]/y_scale
i0, i1, i2, i3 = data["i0"], data["i1"], data["i2"], data["i3"]

x_linear[0] = x_mjt[0] * 0.8

fig, axs = plt.subplots(1, 2, figsize=(4,1.5))

# ------------------------------------------------------------------------------
# -------------------------------- Liner vs MJT (data) -------------------------
# ------------------------------------------------------------------------------
c1 = red
c2 = blue
J = 0
# axs[J].plot(x_linear, y_linear, color=c1, alpha=0.3)
axs[J].scatter(x_linear, y_linear, color=c1, s=5, label='Linear', alpha=0.75)
axs[J].fill_between(x_linear, y_linear-s_linear, y_linear+s_linear, color=c1, alpha=0.3, edgecolor=None)
# axs[J].errorbar(x_linear, y_linear, s_linear, color=c1, edgecolor=None, fmt=',')

# axs[J].plot(x_mjt, y_mjt, color=c2, alpha=0.3)
axs[J].scatter(x_mjt, y_mjt, color=c2, s=5, label='MJT', alpha=0.75)
axs[J].fill_between(x_mjt, y_mjt-s_mjt, y_mjt+s_mjt, color=c2, alpha=0.3, edgecolor=None)
# axs[J].errorbar(x_mjt, y_mjt, s_mjt, color=c2, edgecolor=None, fmt=',')

axs[J].set_xlabel(r"Velocity, $\mu$m/ms")
axs[J].set_ylabel('Fidelity')
axs[J].set_xscale('log')
axs[J].legend(frameon=False, fontsize=8, handletextpad=0)


# ------------------------------------------------------------------------------
# ------------------------------ Linear vs MJT (curve) -------------------------
# ------------------------------------------------------------------------------
J = 1
L = 10
T = 1
t = np.linspace(0, T, 100)
x_mjt = L * (10 * (t/T)**3 - 15 * (t/T)**4 + 6 * (t/T)**5)
print(t[np.argmin(np.abs(x_mjt-4))])
x_linear = (t/T) * L
axs[J].plot(t, x_linear, color=c1, label='Linear')
axs[J].plot(t, x_mjt, color=c2, label='MJT')
axs[J].set_xlabel(r"Time $t$, ms")
axs[J].set_ylabel(r"Position $x(t)$, $\mu$m")
axs[J].legend(frameon=False, fontsize=8, handletextpad=0.5, handlelength=1.5)

fig.subplots_adjust(wspace=0.6)

for i in range(2):
    for j, ax in enumerate(axs):
        ax.set_visible(i == j)
    plt.savefig(f"movement-{i+1}.pdf", bbox_inches='tight')

# plt.savefig("movement.pdf", bbox_inches='tight')
plt.close()
