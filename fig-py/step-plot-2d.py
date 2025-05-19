import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, uBlues, wbr, wbrg
from scipy.ndimage import gaussian_filter

data = np.load("../data/step-plot-2d/data.npz")
Z = data['Z']

Z = gaussian_filter(Z, 0.5)

dx, dy   = 0.02, 0.8        # step sizes
x0, y0   = 0.35, 14.0       # starting coordinates
ny, nx   = Z.shape          # matrix size: rows (y) × columns (x)

# Centres of each pixel (for tick labels, if you want them)
x_centers = np.arange(x0, x0 + nx*dx, dx)
y_centers = np.arange(y0, y0 + ny*dy, dy)

# Build the bounding box so each pixel centre lands on the correct x,y
extent = [x_centers[0] - dx/2, x_centers[-1] + dx/2,
          y_centers[0] - dy/2, y_centers[-1] + dy/2]

fig, ax = plt.subplots(1, 1, figsize=(2,2))
im = ax.imshow(Z/1.22, cmap=wbr, aspect='auto', extent=extent)
cbar = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.04)
cbar.set_ticks([0, 1, 2, 3, 4])

ax.set_xticks([0.4, 0.5, 0.6])
ax.set_yticks([15, 20, 25])

ax.set_xlabel('Tweezer power, mW')
ax.set_ylabel('Magnetic gradient, G/cm')

# x0, y0 = 2, 16
# ax.plot([x0, x0 + 2], [y0, y0], color=(0.5, 0.5, 0.5), lw=1.5)
# ax.plot([x0, x0], [y0, y0 - 1.25], color=(0.5, 0.5, 0.5), lw=1.5)
# ax.text(x0 + 2/2, y0 + 0.5, r'10$\mu$W', ha='center', va='top', fontsize=8, color=(0.5, 0.5, 0.5))
# ax.text(x0, y0 - 1.25/2, r'G/cm', ha='right', va='center', fontsize=8, color=(0.5, 0.5, 0.5))


plt.savefig("step-plot-2d.pdf", bbox_inches='tight')
plt.close()