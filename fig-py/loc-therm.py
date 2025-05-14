import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator
plt.style.use('thesis.mplstyle')
from colors import red, blue, purple
from math import log

# uv_val = {'ETH':(1,1), 'ETH2':(1,0.1), 'AL':(0, 10), 'MBL':(0.1, 10), 'MBL2':(1, 10)}
data = np.load("../data/loc-therm/data.npz")
ts = np.logspace(0, 3, 200)


labels = ['ETH', 'AL', 'MBL', 'MBL2']

fig, axs = plt.subplots(2, 4, figsize=(7,2.5))

S_max =  4.33 # log(154)
for (j, label) in enumerate(labels):

	imb = data[f'{label}-imb']
	# den = data[f'{label}-den']
	
	# magnetization imbalance
	y, ye = imb.mean(axis=0)[:, 0], imb.std(axis=0)[:, 0]
	axs[0, j].fill_between(ts, y-ye, y+ye, color=blue, alpha=0.25)
	axs[0, j].plot(ts, y,  label='spin', color=blue, alpha=0.75)
	# density imbalance
	y, ye = (imb**2).mean(axis=0)[:, 1], (imb**2).std(axis=0)[:, 1]
	axs[0, j].fill_between(ts, y-ye, y+ye, color=red, alpha=0.25)
	axs[0, j].plot(ts, y,  label='density', color=red, alpha=0.75)
	# label
	if j == 0: axs[0, j].set_ylabel('Imbalance')

	# entanglement entropy
	y, ye = imb.mean(axis=0)[:, 2]/S_max, imb.std(axis=0)[:, 2]/S_max
	axs[1, j].fill_between(ts, y-ye, y+ye, color=purple, alpha=0.25)
	axs[1, j].plot(ts, y,  label='entropy', color=purple, alpha=0.75)
	# label
	if j == 0: axs[1, j].set_ylabel(r'Entropy $S/S_{\mathrm{max}}$')

	axs[1, j].set_xlabel('Time, 1/t')



for ax in axs.flatten():
	ax.set_ylim(-0.025, 1.025)
	# ax.set_xlabel('Time, 1/t')
	ax.set_xscale('log')
	ax.set_xticks([1e0, 1e1, 1e2, 1e3])
	ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))

# for j in range(4):
# 	axs[0, j].set_xticklabels(['', '', '', ''])

# plt.tight_layout()
fig.subplots_adjust(hspace=0.5, wspace=0.5)
plt.savefig("loc-therm.pdf", bbox_inches='tight')