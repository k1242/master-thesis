import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, uBlues, uReds, uPurples
# from scipy.ndimage import gaussian_filter

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

data = np.load("../data/loading-from-odt/data.npz")
pi_before, pi_after, img = data['pi_before'], data['pi_after'], data['i0']


fig, axs = plt.subplots(1, 3, figsize=(5.6, 1.5), dpi=1000)

ph2at = 30
vmin, vmax = 231, 366
cmap = uPurples

im0 = axs[1].matshow(np.reshape(pi_before, (4,4))/ph2at, cmap=cmap, vmin=vmin/ph2at, vmax=vmax/ph2at)
cbar0 = fig.colorbar(im0, ax=axs[1])
im1 = axs[2].matshow(np.reshape(pi_after, (4,4))/ph2at, cmap=cmap, vmin=vmin/ph2at, vmax=vmax/ph2at)
cbar1 = fig.colorbar(im1, ax=axs[2])

for ax  in (axs[1], axs[2]):
	ax.set_xticks([0, 1, 2, 3])
	ax.set_yticks([0, 1, 2, 3])
	ax.set_xticklabels(["$V_1$", "$V_2$", "$V_3$", "$V_4$"])
	ax.set_yticklabels(["$H_1$", "$H_2$", "$H_3$", "$H_4$"])

plot_img(axs[0], img/50)

plt.tight_layout()

for i in range(3):
    for j, ax in enumerate(axs):
        ax.set_visible(i == j)
    cbar0.ax.set_visible(i == 1)
    cbar1.ax.set_visible(i == 2)
    plt.savefig(f"loading-from-odt-{i+1}.pdf", bbox_inches='tight')

# plt.savefig("loading-from-odt.pdf", bbox_inches='tight')
plt.close()
