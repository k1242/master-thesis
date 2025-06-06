import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, bwr, purple


data = np.load("../data/factorisability/data.npz")
A, I = data['A'], data['I']

H, S, V = np.linalg.svd(I)
H = -H[:, :, :1]
V = -V[:, :1, :]

factorisability = S[:, 0] / S.sum(axis=1)
f_mean = np.mean(factorisability)
f_std = np.std(factorisability)

I_rec = H @ V * S[:, 0, None, None]
I_err = I_rec - I
I_err_rel = (I_rec - I)/I

# resifuals hist
# factorisability hist
# + R2 score
fig, axs = plt.subplots(1, 3, figsize=(7,2))

axs[0].hist(factorisability, 25, color=blue)
axs[0].set_xlim(f_mean-5*f_std, f_mean+5*f_std)
axs[0].set_xlabel('Factorisability')
axs[0].set_ylabel('Counts')

bins = np.linspace(-1.5, 1.5, 60)
axs[1].hist(I_err_rel[:, 4, 0] * 1e2, bins=bins, color=blue, density=True)
axs[1].hist(I_err_rel[:, 1, 0] * 1e2, bins=bins, color=red, density=True)
axs[1].hist(I_err_rel.flatten() * 1e2, bins=bins, color=purple, alpha=0.75, density=True)
axs[1].set_xlabel(r'Relative error $(\hat{I}-I)/I$, \%')
axs[1].set_ylabel('Probability density')
	

cbar = fig.colorbar(im, cax=fig.add_axes([0.92, 0.14, 0.01, 0.71]))
cbar.ax.text(
    0.5, 1.04, r'\%',
    ha='center', va='bottom',
    transform=cbar.ax.transAxes
)

# fig.colorbar(im, ax=axs[2])
# axs[1].hist(I_err_rel.flatten(), 30, alpha=0.5)
# axs[1].hist(I_err_rel[:, 0, 1], 30, alpha=0.5)
# axs[1].hist(I_err_rel[:, 0, 2], 30, alpha=0.5)
# axs[1].hist(I_err_rel[:, 1, 1], 30, alpha=0.5)


for ax  in (axs[2],):
	ax.set_xticks([0, 1, 2, 3, 4, 5])
	ax.set_yticks([0, 1, 2, 3, 4, 5])
	ax.set_xticklabels(["$V_1$", "$V_2$", "$V_3$", "$V_4$", "$V_5$", "$V_6$"])
	ax.set_yticklabels(["$H_1$", "$H_2$", "$H_3$", "$H_4$", "$H_5$", "$H_6$"])

# plt.tight_layout()
fig.subplots_adjust(wspace=0.4)
plt.savefig("factorisability.pdf", bbox_inches='tight')

# for i in range(3):
#     for j, ax in enumerate(axs):
#         ax.set_visible(i == j)
#     cbar.ax.set_visible(i == 2)
#     plt.savefig(f"factorisability-{i+1}.pdf", bbox_inches='tight')

plt.close()