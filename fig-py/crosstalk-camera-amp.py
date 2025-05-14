import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, bwr

data = np.load("../data/crosstalk/data.npz")
I, A = data['I_camera'], data['A_camera']

fig, ax = plt.subplots(1, 1, figsize=(1.5, 1.5))

x = A.mean(axis=1)
y = I.sum(axis=1)
# y = (y - y.min()) / (y.max() - y.min())
y = y / y.mean()


p, cov = np.polyfit(x, y, 1, cov=True)
x_fit = np.linspace(x.min(), x.max(), 20)
y_fit = np.poly1d(p)(x_fit)
y_pred = np.poly1d(p)(x)

ax.plot(x_fit, y_fit, color='r', alpha=0.5, linewidth=1, label='linear fit')
ax.scatter(x, y, s=3, color=blue, edgecolors='none', alpha=0.75)
# print(p)

ax.set_xlabel("Avg. AOD amplitude")
ax.set_ylabel("Avg. intensity, a.u.")
# im = ax.matshow(crosstalk / crosstalk.max(), cmap=bwr, vmin=-1, vmax=1)
# fig.colorbar(im, ax=ax)
# ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7])
# ax.set_xticklabels(["$h_1$", "$h_2$", "$h_3$", "$h_4$", "$v_1$", "$v_2$", "$v_3$", "$v_4$"])
# ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7])
# ax.set_yticklabels(["$H_1$", "$H_2$", "$H_3$", "$H_4$", "$V_1$", "$V_2$", "$V_3$", "$V_4$"])

r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)

# print(p[0], np.sqrt(cov[0, 0]))
# print(p[1], np.sqrt(cov[1, 1]))
# print(r2)

# n_boot = 1000
# r2_samples = []
# for _ in range(n_boot):
#     idx = np.random.choice(len(x), len(x), replace=True)
#     p_bs = np.polyfit(x[idx], y[idx], 1)
#     y_bs_pred = np.polyval(p_bs, x[idx])
#     r2_bs = 1 - np.sum((y[idx] - y_bs_pred)**2) / np.sum((y[idx] - np.mean(y[idx]))**2)
#     r2_samples.append(r2_bs)
# r2_std = np.std(r2_samples)
# print(f"R² = {r2:.4f} ± {r2_std:.4f}")

# plt.legend(frameon=False)
ax.text(0.05, 0.85, f"$R^2 = ${r2:.3f}", transform=ax.transAxes, fontsize=8)

plt.savefig("crosstalk-camera-amp.pdf", bbox_inches='tight')
plt.close()