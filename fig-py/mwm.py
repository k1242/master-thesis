import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, uBlues
from scipy.spatial import Voronoi


n_grid = 4
n_grid_full = 2 * n_grid + 1
grid_step = 1

scale = 20
shift2 = -(2 * np.pi / scale) * 0.2 * 0
Lq1 = (n_grid+5) * grid_step
Lq2 = (n_grid+5) * grid_step * scale

data = np.load("../data/mwm/data.npz")
xfc, yfc, xfc2, yfc2 = data['xfc'], data['yfc'], data['xfc2'], data['yfc2']
hist_i, hist_f, hist_f_normal = data['hist_i'], data['hist_f'], data['hist_f_normal']

vor = Voronoi(np.column_stack([xfc, yfc]))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4, 2))

ax1.imshow(hist_i, extent=(-Lq1, Lq1, -Lq1, Lq1), vmin=0, vmax=np.percentile(hist_i.flatten(), 99.9), cmap=uBlues)            

lim = 160
for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
    if v1 >= 0 and v2 >= 0:
        mask = np.abs(np.concatenate((vor.vertices[v1],vor.vertices[v2]))) < lim
        if mask.all():
            ax2.plot(*zip(vor.vertices[v1], vor.vertices[v2]), c='k', lw=0.5)

ax2.imshow(hist_f, extent=(-Lq2, Lq2, -Lq2, Lq2), vmin=0, vmax=np.percentile(hist_f.flatten(), 99.9), cmap=uBlues)            

xlim = 150
ylim = 150
ax1.set_xlim(-xlim/scale,xlim/scale)
ax1.set_ylim(-ylim/scale,ylim/scale)
ax2.set_xlim(-xlim,xlim)
ax2.set_ylim(-ylim,ylim)

for ax in (ax1, ax2):
	ax.set_xlabel(r'$x$, $\mu$m')
	ax.set_ylabel(r'$y$, $\mu$m')

plt.tight_layout()
for i in range(2):
    for j, ax in enumerate((ax1, ax2)):
        ax.set_visible(i == j)
    plt.savefig(f"mwm-{i+1}.pdf", bbox_inches='tight')
# plt.savefig("mwm.pdf", bbox_inches='tight')
plt.close()