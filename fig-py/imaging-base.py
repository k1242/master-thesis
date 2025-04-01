import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrow
from matplotlib.transforms import Affine2D
plt.style.use('thesis.mplstyle')
from colors import red

data = np.load("../data/imaging-base/data.npz")
img, img_bi, img_bi_bl = data['img'], data['img_bi'], data['img_bi_bl']

tw_pos = np.array([[ 38,146],[ 43,110],[ 49, 74],[ 55, 38],
                   [ 73,152],[ 79,116],[ 85, 80],[ 91, 44],
                   [109,158],[115,122],[121, 86],[127, 50],
                   [145,163],[151,127],[157, 92],[163, 56]])

fig, axs = plt.subplots(1, 3, figsize=(5, 2))
axs[0].matshow(img, cmap='Blues', vmin=0, vmax=1000)
axs[1].matshow(img_bi, cmap='Blues')
axs[2].matshow(img_bi_bl, cmap='Blues')
for ax, title in zip(
	axs, 
	# ['Raw image', 'Binarized image', 'Blured image']
	['Raw image', 'Binarization', 'Low-pass filter']
):
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])

angle = np.degrees(np.arctan2(tw_pos[1,1]-tw_pos[0,1], tw_pos[1,0]-tw_pos[0,0]))
reg_size = 32
for ax in axs:
    for cx, cy in tw_pos:
        rect = patches.Rectangle((-reg_size/2, -reg_size/2), reg_size, reg_size,
                                 edgecolor=(0.5, 0.5, 0.5), facecolor='none', linewidth=0.3)
        rect.set_transform(Affine2D().rotate_deg(angle).translate(cx, cy) + ax.transData)
        ax.add_patch(rect)

# add scale
for ax in axs:
    h = img.shape[0]
    x0, y0 = 5, h - 6
    ax.plot([x0, x0 + 50/1.5], [y0, y0], color=(0.5, 0.5, 0.5), lw=1.5)
    ax.text(x0 + 25/1.5, y0 - 16, r'50$\mu$m', ha='center', va='top', fontsize=8, color=(0.5, 0.5, 0.5))


for (i, x) in enumerate([0.328, 0.65]):
    p1, p2 = axs[i].get_position(), axs[i+1].get_position()
    y = (p1.y0 + p1.y1) / 2
    # x = (p1.x1 + p2.x0) / 2
    fig.patches.append(FancyArrow(
        x, y, 0.02, 0, transform=fig.transFigure,
        width=0.005, head_width=0.015, head_length=0.007,
        length_includes_head=True, color=(0.5, 0.5, 0.5)
    ))

plt.tight_layout()
# plt.subplots_adjust(bottom=0.2)
plt.savefig("imaging-base.pdf", bbox_inches='tight')
plt.close()
