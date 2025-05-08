import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from scipy.ndimage import gaussian_filter

data = np.load("../data/m-bec/data.npz")
imgs = data['imgs'] # 6mW, 20mW, 80mW

sigma = 3
y0, x0, b = 102, 113, 40
imgs = [gaussian_filter(img, sigma=sigma)[y0-b:y0+b, x0-b:x0+b] for img in imgs]

fig, axs = plt.subplots(1, 3, figsize=(1.5, 0.5), dpi=1000)
for (ax, img) in zip(axs, imgs):
    ax.matshow(-img, cmap='gray', vmin=-0.7, vmax=0.0)
    ax.set_xticks([])
    ax.set_yticks([])

for i in range(3):
    for j, ax in enumerate(axs):
        ax.set_visible(i == j)
    plt.savefig(f"m-bec-inset-{i+1}.pdf", bbox_inches='tight', pad_inches=0.01)