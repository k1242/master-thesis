import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrow
from matplotlib.transforms import Affine2D
import matplotlib.colors as mcolors
plt.style.use('thesis.mplstyle')
from colors import red, blue, purple

delta = 0.12 # shift for doubloon
s = 150 # size of resolved spins
h = 8 # color intensity for combined blured img
y123, x123, y456, x456 = 75, 295, 232, 119 # left bottom corner of the roi
size = 180 # full size of the roi

filling_123 = np.array([ True, False,  True,  True,  True, False,  True,  True,  True, True,  True,  True,  True,  True,  True,  True])
filling_456 = np.array([False,  True, False,  True, False, False, False,  True, False, True, False,  True, False,  True, False,  True])
tw_pos_list_123 = np.array([ [434, 220], [402, 215], [371, 210], [339, 205], [439, 189], [407, 184], [376, 179], [344, 174], [443, 157], [412, 152], [380, 147], [349, 142], [448, 126], [416, 121], [385, 116], [353, 111]])
tw_pos_list_456 =  np.array([ [257, 373], [225, 369], [192, 365], [160, 361], [261, 342], [228, 338], [196, 334], [164, 330], [264, 311], [232, 307], [200, 303], [167, 299], [268, 280], [236, 276], [203, 272], [171, 267]])

mask = np.ones((513, 512), dtype=bool)
cmask_123 = np.tril(mask, k=50)
cmask_456 = np.triu(mask, k=50)

def plot_roi_edges(ax, tw_pos, reg_size=30):
    angle = np.degrees(np.arctan2(tw_pos[1,1]-tw_pos[0,1], tw_pos[1,0]-tw_pos[0,0]))
    for center in tw_pos:
        rect = patches.Rectangle((-reg_size/2, -reg_size/2), reg_size, reg_size,
                                 edgecolor=(0.5, 0.5, 0.5), facecolor='none', linewidth=0.5)
        rect.set_transform(Affine2D().rotate_deg(angle).translate(*center) + ax.transData)
        ax.add_patch(rect)

data = np.load("../data/imaging-spin-resolved/data.npz")
raw_img, img_bi, img_bi_bl = data['img'], data['img_bi'], data['img_bi_bl']
pos_123_x, pos_123_y, pos_456_x, pos_456_y = data['pos_123_x'], data['pos_123_y'], data['pos_456_x'], data['pos_456_y']


fig, axs = plt.subplots(1, 4, figsize=(7, 2), dpi=400)

# RAW IMAGE
img_123 = raw_img.copy()
img_456 = img_123.copy()
img_123[cmask_123] = np.nan
img_456[cmask_456] = np.nan
axs[0].matshow(img_123, vmin=0, vmax=100, cmap='Reds')
axs[0].matshow(img_456, vmin=0, vmax=100, cmap='Blues')
axs[0].grid(False)
axs[0].text(405, 110, 'state 123', color=red, ha="center", va="bottom", size=8, rotation=-8.8)
axs[0].text(220, 265, 'state 456', color=blue, ha="center", va="bottom", size=8, rotation=-8.8)
plot_roi_edges(axs[0], tw_pos_list_123)
plot_roi_edges(axs[0], tw_pos_list_456)
x0, y0 = 130, 435
axs[0].plot([x0, x0 + 50/1.6], [y0, y0], color=(0.5, 0.5, 0.5), lw=1.5)
axs[0].text(x0 + 25/1.5, y0 - 30, r'50 $\mu$m', ha='center', va='top', fontsize=8, color=(0.5, 0.5, 0.5))
axs[0].set_xticks([])
axs[0].set_yticks([])
axs[0].set_xlim(100, 500)
axs[0].set_ylim(450, 50)

# BINARIZATION
cmap = mcolors.ListedColormap([(1, 1, 1), blue, red, purple])
img_123 = img_bi[y123:y123+size, x123:x123+size].copy()
img_456   = img_bi[y456:y456+size, x456:x456+size].copy()
img = 2*img_123 + img_456
axs[1].matshow(img, cmap=cmap)
plot_roi_edges(axs[1], tw_pos_list_123-np.array([[x123, y123]]))

# LOW-PASS FILTER
img_123 = img_bi_bl[y123:y123+size, x123:x123+size].copy()
img_456   = img_bi_bl[y456:y456+size, x456:x456+size].copy()
img = np.ones((*img_456.shape, 3))
channel_blue, channel_red = np.ones((2, *img_456.shape, 3))
channel_blue[:, :, 2], channel_red[:, :, 0] = 0, 0
img -= h * (channel_red * img_123[..., None] + channel_blue * img_456[..., None])
img = np.clip(img, 0, 1)
axs[2].matshow(img)
plot_roi_edges(axs[2], tw_pos_list_123-np.array([[x123, y123]]))
axs[2].scatter(pos_123_x, pos_123_y, s=10, marker='v', facecolors='white', edgecolors=red, linewidths=0.5)
axs[2].scatter(pos_456_x, pos_456_y, s=10, marker='^', facecolors='white', edgecolors=blue, linewidths=0.5)

# RESOLVED IMAGE
filling_123456 = filling_123 & filling_456
filling_123 = filling_123 & (~filling_123456)
filling_456 = filling_456 & (~filling_123456) 
filling_holes = ~(filling_123456 | filling_123 | filling_456)
xy = []
for i in range(4):
    for j in range(4):
        xy.append([3-j,i])
xy = np.array(xy)
axs[3].scatter(xy[filling_123, 0], xy[filling_123, 1], s=s, facecolors=red, edgecolors='w', linewidths=1, label=r'$|1\rangle$')
axs[3].scatter(xy[filling_456, 0], xy[filling_456, 1], s=s, facecolors=blue, edgecolors='w', linewidths=1, label=r'$|2\rangle$')
axs[3].scatter(xy[filling_123456, 0]-delta, xy[filling_123456, 1]+delta, s=s, facecolors=red, edgecolors='w', linewidths=1)
axs[3].scatter(xy[filling_123456, 0], xy[filling_123456, 1], s=s, facecolors=blue, edgecolors='w', linewidths=1)
axs[3].scatter(xy[filling_holes, 0], xy[filling_holes, 1], s=s, facecolors=(0.75, 0.75, 0.75), edgecolors='w', linewidths=1, label='hole')
b = 0.75
axs[3].set_xlim(-b, 3+b)
axs[3].set_ylim(-b, 3+b)
# axs[3].legend(frameon=False, loc='upper right', fontsize=8)


for ax, title in zip(axs, ['Raw image', 'Binarization', 'Low-pass filter', 'Resolved state']):
    ax.set_title(title)
for ax in (axs[1], axs[2]):
    ax.set_xticks([])
    ax.set_yticks([])
    x0, y0 = 5, 180 - 6
    ax.plot([x0, x0 + 50/1.6], [y0, y0], color=(0.5, 0.5, 0.5), lw=1.5)
    ax.text(x0 + 25/1.5, y0 - 14, r'50 $\mu$m', ha='center', va='top', fontsize=8, color=(0.5, 0.5, 0.5))
axs[3].set_xticks([])
axs[3].set_yticks([])
axs[3].set_aspect('equal')

plt.tight_layout()
plt.savefig("imaging-spin-resolved.pdf", bbox_inches='tight')
plt.close()