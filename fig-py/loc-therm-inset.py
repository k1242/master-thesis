import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import uBlues, uReds

b = 0.1
w = 1

# uv_val = labels = {'ETH':(1,1), 'ETH2':(1,0.1), 'AL':(0, 10), 'MBL':(0.1, 10), 'MBL2':(1, 10)}
data = np.load("../data/loc-therm/data.npz")
ts = np.logspace(0, 3, 200)


labels = ['ETH', 'AL', 'MBL', 'MBL2']

for K in range(2):
	for (J, label) in enumerate(labels):

		imb = data[f'{label}-imb']
		den = data[f'{label}-den']


		js = [0, 25, 35, 42, 199]
		n = len(js)

		fig, axs = plt.subplots(1, n, figsize=(0.5*n,0.5))

		for (i, (ax, j)) in enumerate(zip(axs, js)):
			if i != (n - 2):	
				if K == 0:
					cmap = uBlues
					img = np.abs(den[:, j, 0]-den[:, j, 1])
				else:
					cmap = uReds
					img = den[:, j, 0]+den[:, j, 1]
				img = img.mean(axis=0)
				ax.matshow(img, cmap=cmap, vmin=0, vmax=1)
			else:
				ax.axis('off')


		for ax in axs:	
			ax.set_xticks([])
			ax.set_yticks([])
			ax.set_xlim(-0.5-b, 3.5+b)
			ax.set_ylim(-0.5-b, 3.5+b)

			for v in [-0.5, 0.5, 1.5, 2.5, 3.5]:
				ax.axvline(x=v, color=(1,1,1), linewidth=w)
				ax.axhline(y=v, color=(1,1,1), linewidth=w)

		fig.subplots_adjust(wspace=0.1)
		plt.savefig(f"loc-therm-inset/{K}{J}.pdf", pad_inches=0.01, bbox_inches='tight')
		plt.close()