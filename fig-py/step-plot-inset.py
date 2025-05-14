import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue

data = np.load("../data/step-plot/data.npz")
df, x = data['df'], data['spill_powers']

df_mean = df[:, ::3]
df_std = df[:, 1::3]
df_counts = df[:, 2::3]
df_sem = df_std / df_counts**0.5


def sigmoid(x, a, sigma, x0, offset):
    return a / (1 + np.exp(-(x - x0) / sigma)) + offset

def sigmoid2(x, a, sigma, x01, x02, offset):
    return a / (1 + np.exp(-(x - x01) / sigma)) + a / (1 + np.exp(-(x - x02) / sigma)) + offset


x0 = 0.462
y0 = 28.57 / 2
y_min = 7.8

x /= x0
x_fit = np.linspace(0.32/x0, 0.58/x0, 400)


popts = []
pcovs = []
y_fits = []
for j in range(16):
	y, y_err = df_mean[:, j]/y0, df_sem[:, j]/y0
	y -= y_min/y0
	popt, pcov = curve_fit(sigmoid2, x, y, p0=[2, 0.02, 0.86, 1.13, 0], sigma=y_err)
	popts.append(popt)
	pcovs.append(pcov)
	y_fit = sigmoid2(x_fit, *popt)
	y_fits.append(y_fit)
popts = np.array(popts)
y_fits = np.array(y_fits)
print(popts.mean(axis=0))


fig, axs = plt.subplots(4, 4, figsize=(2,2))

for (j, ax) in enumerate(axs.flatten()[::-1]):
	y, y_err = df_mean[:, j]/y0, df_sem[:, j]/y0
	y -= y_min/y0
	ax.errorbar(x, y, yerr=y_err, fmt=',', alpha=1, color=blue, zorder=-10, linewidth=1)

	y_fit = sigmoid2(x_fit, *popts[j])
	# ax.plot(x_fit, y_fit, color=red, alpha=0.5, linewidth=0.5)
	ax.plot(x_fit, y_fits.mean(axis=0), color=red, alpha=0.5, linewidth=0.5)

for ax in axs.flatten():
	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_xlim(0.6645, 1.2835)
	ax.set_ylim(-0.2273, 4.55799)


fig.subplots_adjust(hspace=0, wspace=0)
plt.savefig("step-plot-inset.pdf", bbox_inches='tight', pad_inches=0.005)
plt.close()
