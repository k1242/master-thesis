import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, uBlues, uReds
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

def plot_filling(ax, filling_123, filling_456, s=40, delta=0.18, b=0.75, n=6):
    filling_123 = filling_123.astype(bool).reshape(n,n)[::-1, ::-1].reshape(-1)
    filling_456 = filling_456.astype(bool).reshape(n,n)[::-1, ::-1].reshape(-1)
    filling_123456 = filling_123 & filling_456
    filling_123 = filling_123 & (~filling_123456)
    filling_456 = filling_456 & (~filling_123456) 
    filling_holes = ~(filling_123456 | filling_123 | filling_456)
    xy = []
    for i in range(n):
        for j in range(n):
            xy.append([n-1-j,i])
    xy = np.array(xy)
    ax.scatter(xy[filling_123, 0], xy[filling_123, 1], s=s, facecolors=red, edgecolors='w', linewidths=1)
    ax.scatter(xy[filling_456, 0], xy[filling_456, 1], s=s, facecolors=blue, edgecolors='w', linewidths=1)
    ax.scatter(xy[filling_123456, 0]-delta, xy[filling_123456, 1]+delta, s=s, facecolors=red, edgecolors='w', linewidths=1)
    ax.scatter(xy[filling_123456, 0], xy[filling_123456, 1], s=s, facecolors=blue, edgecolors='w', linewidths=1)
    ax.scatter(xy[filling_holes, 0], xy[filling_holes, 1], s=s, facecolors=(0.75, 0.75, 0.75), edgecolors='w', linewidths=1)
    ax.set_xlim(-b, n-1+0.75*b)
    ax.set_ylim(-0.75*b, n-1+b)
    ax.set_xticks([])
    ax.set_yticks([])

data = np.load("../data/preparation/data.npz")

i0, i1, i2, i3 = data["i0"], data["i1"], data["i2"], data["i3"]

f0 = np.array([
    1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1,
])
f1 = np.array([
    1, 1, 1, 0, 1, 1,
    1, 1, 1, 0, 1, 1,
    1, 1, 1, 0, 1, 1,
    1, 1, 1, 0, 1, 1,
    1, 1, 1, 0, 1, 1,
    1, 1, 1, 0, 1, 1,
])
f2 = np.array([
    1, 1, 1, 0, 1, 1,
    1, 1, 1, 0, 1, 1,
    1, 1, 1, 0, 0, 0,
    1, 1, 1, 0, 1, 1,
    1, 1, 1, 0, 1, 1,
    1, 1, 1, 0, 1, 1,
])
f3 = np.array([
    1, 1, 0, 0, 1, 1,
    1, 1, 0, 0, 1, 1,
    1, 1, 0, 0, 0, 0,
    1, 1, 0, 0, 1, 1,
    1, 1, 1, 0, 1, 1,
    1, 1, 1, 0, 1, 1,
])
fb4 = np.array([
    1, 1, 0, 0, 0, 0,
    1, 1, 0, 0, 0, 0,
    1, 1, 0, 0, 0, 0,
    1, 1, 0, 0, 0, 0,
    1, 1, 1, 0, 0, 0,
    1, 1, 1, 0, 0, 0,
])
fr4 = np.array([
    1, 1, 0, 0, 1, 1,
    1, 1, 0, 0, 1, 1,
    1, 1, 0, 0, 0, 0,
    1, 1, 0, 0, 1, 1,
    1, 1, 1, 0, 1, 1,
    1, 1, 1, 0, 1, 1,
])
fr5 = fb4.copy()
fb5 = fr4.copy()
fr6 = np.array([
    1, 1, 0, 0, 0, 0,
    1, 1, 0, 0, 0, 0,
    1, 1, 0, 0, 0, 0,
    1, 1, 0, 0, 0, 0,
    1, 1, 1, 0, 0, 0,
    1, 1, 1, 0, 0, 0,
])
fb6 = np.array([
    0, 0, 0, 0, 1, 1,
    0, 0, 0, 0, 1, 1,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 1,
    0, 0, 0, 0, 1, 1,
    0, 0, 0, 0, 1, 1,
])



fig, axs = plt.subplots(2, 6, figsize=(7, 2.6), dpi=500)
plot_filling(axs[0, 0], f0, f0)
# plot_filling(axs[1], f1, f1)
plot_filling(axs[0, 1], f2, f2)
plot_filling(axs[0, 2], f3, f3)
plot_filling(axs[0, 3], fr4, fb4)
plot_filling(axs[0, 4], fr5, fb5)
plot_filling(axs[0, 5], fr6, fb6)
# axs[1,5].remove()
# axs[1,4].remove()

contrast = 3
plot_img(axs[1,0], contrast*i0)
plot_img(axs[1,1], contrast*i1)
plot_img(axs[1,2], contrast*i2)
plot_img(axs[1,3], contrast*i3)
plot_img(axs[1,4], contrast*i0*np.nan)
plot_img(axs[1,5], contrast*i0*np.nan)

for ax in axs.flatten():
    ax.set_xticks([])
    ax.set_yticks([])
# fig.subplots_adjust(hspace=0)
plt.tight_layout()

plt.savefig("preparation-array.pdf", bbox_inches='tight')
plt.close()