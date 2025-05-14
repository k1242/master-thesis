import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, bwr, uBlues, purple

data = np.load("../data/crosstalk/data.npz")
img = data['img_camera']
img = img / img.max()

fig, ax = plt.subplots(1, 1, figsize=(1.5, 1.95))


im = ax.matshow(img, cmap=uBlues)
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

# vals = [0.421, 0.356, 0.48 , 0.387, 0.588, 0.48 , 0.648, 0.53 , 0.913, 0.696, 1.   , 0.778, 0.547, 0.449, 0.626, 0.502]
# for v in vals:
#     y = v * (cbar.ax.get_ylim()[1] - cbar.ax.get_ylim()[0]) + cbar.ax.get_ylim()[0]
#     cbar.ax.hlines(y, xmin=0.0, xmax=1.0, colors=purple, linewidth=0.5, transform=cbar.ax.get_yaxis_transform())

ax.set_xticks([])
ax.set_yticks([])
x0, y0 = 350, 500
ax.plot([x0, x0 + (432-95)/3/0.75], [y0, y0], color=(0.5, 0.5, 0.5), lw=1.5)
ax.text(x0 + (432-95)/3/2/0.75, y0 - 50, r'1 MHz', ha='center', va='top', fontsize=8, color=(0.5, 0.5, 0.5))

# fig.subplots_adjust(bottom=0.2)

plt.savefig("crosstalk-camera-img.pdf", bbox_inches='tight')
plt.close()
