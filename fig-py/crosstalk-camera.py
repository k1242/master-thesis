import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, bwr

data = np.load("../data/crosstalk/data.npz")
crosstalk = data['crosstalk_camera']

fig, ax = plt.subplots(1, 1, figsize=(2, 2))
normed = crosstalk / crosstalk.max()

im = ax.matshow(normed, cmap=bwr, vmin=-1, vmax=1)
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7])
ax.set_xticklabels(["$h_1$", "$h_2$", "$h_3$", "$h_4$", "$v_1$", "$v_2$", "$v_3$", "$v_4$"])
ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7])
ax.set_yticklabels(["$H_1$", "$H_2$", "$H_3$", "$H_4$", "$V_1$", "$V_2$", "$V_3$", "$V_4$"])

ax.set_xlabel('AOD amplitude')
ax.set_ylabel('Normalized intensity')

for i in range(normed.shape[0]):
    for j in range(normed.shape[1]):
        value = normed[i, j]
        value = np.abs(value)
        ax.text(j, i, f"{value:.1f}", va='center', ha='center', fontsize=6, alpha=0.5)

plt.savefig("crosstalk-camera.pdf", bbox_inches='tight')
plt.close()