from arc import Lithium6
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow
from matplotlib.lines import Line2D
plt.style.use('thesis.mplstyle')
from colors import red, blue, cyan, gold

gray = (0.5, 0.5, 0.5)

atom = Lithium6()
B = np.linspace(0, 600, 1000)

ES12, _, _ = atom.breitRabi(2, 0, 1/2, B * 1e-4)
EP32, _, _ = atom.breitRabi(2, 1, 3/2, B * 1e-4)
EP32 = EP32[:, ::3] 

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(2, 3), gridspec_kw={'height_ratios': [1, 3/2], 'hspace': 0.1})

# 2S_{1/2}
for (j, c) in enumerate([blue, red, 'k', gray, gray, 'k']):
    ax2.plot(B, ES12[:, j] * 1e-9, color=c,
             linewidth=0.75 if c in ['k',gray]  else 1.5,
             label={blue: r"$|2\rangle$", red: r"$|1\rangle$"}.get(c, None))

# 2P_{3/2}
for (j, c) in zip(range(EP32.shape[1]), ['k', gray, gray, 'k']):
    ax1.plot(B, EP32[:, j] * 1e-9, color=c, linewidth=0.75)

# frame
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax2.spines['right'].set_visible(False)
# combine
ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.set_xticks([])
ax1.yaxis.set_ticks_position('left')
ax2.yaxis.set_ticks_position('left')
ax2.xaxis.set_ticks_position('bottom')
# limits
for ax in (ax1, ax2):
    ax.minorticks_off()
    ax.tick_params(axis='both', which='major', length=4)
    ax.set_xlim(0,600)
ax1.set_ylim(-1.9,1.9)
ax2.set_ylim(-1.1,1.1)

# levels labels
ax1.text(40, 1, r"$2\,{}^2\mathrm{P}_{3/2}$", ha='left', va='center')
ax2.text(40, 0.6, r"$2\,{}^2\mathrm{S}_{1/2}$", ha='left', va='center')

# m_j
fig.text(0.97, 0.92, "$m_j$", va='center', size=8)
fig.text(0.93, 0.865, "$+3/2$", va='center', size=8)
fig.text(0.93, 0.78, "$+1/2$", va='center', size=8, color=gray)
fig.text(0.93, 0.69, "$-1/2$", va='center', size=8, color=gray)
fig.text(0.93, 0.60, "$-3/2$", va='center', size=8, color=gray)
fig.text(0.93, 0.50, "$+1/2$", va='center', size=8)
fig.text(0.93, 0.16, "$-1/2$", va='center', size=8)

# axis label
fig.text(-0.1, 0.5, "Energy, GHz", va='center', rotation='vertical')
ax2.set_xlabel("Magnetic field, G")

# fluorescence
kwargs = dict(transform=fig.transFigure, width=0.002, head_width=0.02, head_length=0.02, length_includes_head=True, color=red)
fig.patches.append(FancyArrow(0.65, 0.234, 0.0, 0.405, **kwargs))
fig.patches.append(FancyArrow(0.7, 0.473, 0.0, 0.35, **kwargs))
fig.text(0.625, 0.55, r"$\sigma_-$", va='center', ha='right', color=red)
fig.text(0.725, 0.55, r"$\sigma_+$", va='center', ha='left', color=red)

# RF&MW
kwargs.update(color=cyan, head_length=0, head_width=0)
fig.patches.append(FancyArrow(0.65, 0.216, 0.0, 0.014, **kwargs))
kwargs.update(color=gold)
fig.patches.append(FancyArrow(0.7, 0.190, 0.0, 0.264+0.0145, **kwargs))
legend_elements = [
    Line2D([0], [0], color=cyan, lw=1.5, linestyle='-', label="RF"),
    Line2D([0], [0], color=gold, lw=1.5, linestyle='-', label="MW")
]
fig.legend(
    handles=legend_elements, frameon=False, 
    handlelength=1, fontsize=8, 
    bbox_to_anchor=(0.85, 0.33), loc='center', bbox_transform=fig.transFigure
)

# broken
fig.text(0.089, 0.569, r"...", va='center', ha='left', rotation=90, size=8)

plt.savefig("li6-zeeman-broken.pdf", bbox_inches='tight')
plt.close()