# https://arc-alkali-rydberg-calculator.readthedocs.io/en/latest/generated/arc.alkali_atom_functions.AlkaliAtom.breitRabi.html#arc.alkali_atom_functions.AlkaliAtom.breitRabi

from arc import Lithium6
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue

atom = Lithium6()
B = np.linspace(0, 600, 1000)

ES12,_,_ = atom.breitRabi(2, 0, 1/2, B*1e-4)
EP32,_,_ = atom.breitRabi(2, 1, 3/2, B*1e-4)
EP32 = EP32[:, ::3]
# ES12 = ES12[:, ::3]
# plt.plot(EP32 * 1e-6)

# j = int(527/600 * 1000)
# print(EP32[j] * 1e-6)
# print(ES12[j] * 1e-6)
# d1 = ES12[j][2] - EP32[j][0]
# d2 = ES12[j][5] - EP32[j][2]
# print((d2-d1)*1e-6)


fig, ax = plt.subplots(1, 1, figsize=(2, 2))
for (j, c) in enumerate([blue, red, 'k', 'k', 'k', 'k']):
	ax.plot(B, ES12[:, j] * 1e-9, color=c, 
		linewidth=0.75 if c=='k' else 1.5,
		label={blue: r"$|2\rangle$", red: r"$|1\rangle$"}[c] if c != 'k' else None
		)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# ax.axvline(x=27, color='k', linestyle='--', linewidth=0.75, zorder=-10, label=r"$\mu_{|2\rangle} = 0$") # spin dependent spilling
# ax.axvline(x=527, color='k', linestyle='--', linewidth=1, zorder=-10, label="$a_{12}=0$") # no intercation for 1-2 mixture
# ax.axvline(x=568, color='k', linestyle=':', linewidth=1, zorder=-10, label="$a_{13}=0$") # no intercation for 1-3 mixture
# ax.legend(frameon=False, loc='center right')
# ax.legend(frameon=False, loc='upper right')
# ax.text(540, 0, r'$a_{\mathrm{sc}}= 0$', color="k", 
	# verticalalignment='center', horizontalalignment='left', rotation=90)
# plt.axis('off')
ax.text(30, -0.85, r"$2\,{}^2S_{1/2}$", ha='left', va='center')

# ax.set_ylim(-0.3,-0)
# ax.set_xlim(0, 100)

ax.set_ylim(-1.1,1.1)
ax.set_xlim(0,600)

ax.minorticks_off()
ax.set_xlabel("Magnetic field, Gs")
ax.set_ylabel("Energy, GHz")
ax.tick_params(axis='both', which='major', length=4)
# ax.tick_params(axis='both', which='minor', labelsize=8)
# plt.tight_layout()
# plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig("li6-zeeman.pdf", bbox_inches='tight')
plt.close()
