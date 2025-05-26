import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, uReds, uBlues
# from scipy.ndimage import gaussian_filter1d

mask = np.ones((513, 512), dtype=bool)
cmask_123 = np.tril(mask, k=0)
cmask_456 = np.triu(mask, k=0)
def plot_img(ax, img):
    img_123 = img.copy()
    img_456 = img.copy()
    img_123[cmask_123] = np.nan
    img_456[cmask_456] = np.nan
    ax.matshow(img_123, vmin=0, vmax=120*2.5, cmap=uReds)
    ax.matshow(img_456, vmin=0, vmax=100*2.5, cmap=uBlues)
    ax.set_xticks([])
    ax.set_yticks([])

data = np.load("../data/movement/data.npz")

x_scale = 36.6 / 5.6
y_scale = 0.95
x_linear, y_linear, s_linear = data["x_linear"]*x_scale, data["y_linear"]/y_scale, data["s_linear"]/y_scale
x_mjt, y_mjt, s_mjt = data["x_mjt"]*x_scale, data["y_mjt"]/y_scale, data["s_mjt"]/y_scale
i0, i1, i2, i3 = data["i0"], data["i1"], data["i2"], data["i3"]

fig, axs = plt.subplots(1, 4, figsize=(4*1.5,1.5), dpi=1000)
plot_img(axs[0], i0)
plot_img(axs[1], i1)
plot_img(axs[2], i2)
plot_img(axs[3], i3)

axs[0].text(0.5, 0.9, r"$t/T=0.0$", transform=axs[0].transAxes, va='center', ha='center', size=8)
axs[1].text(0.5, 0.9, r"$t/T=0.3$", transform=axs[1].transAxes, va='center', ha='center', size=8)
axs[2].text(0.5, 0.9, r"$t/T=0.4$", transform=axs[2].transAxes, va='center', ha='center', size=8)
axs[3].text(0.5, 0.9, r"$t/T=1.0$", transform=axs[3].transAxes, va='center', ha='center', size=8)

fig.subplots_adjust(wspace=0.1)
plt.savefig("movement-inset.pdf", bbox_inches='tight')
plt.close()

# 0, 0.2, 0.4, 1.0