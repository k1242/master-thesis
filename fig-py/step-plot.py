import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue

fig, ax = plt.subplots(1, 1, figsize=(2,2))
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


ax.fill_between(x_fit,  y_fits.mean(axis=0)-y_fits.std(axis=0), y_fits.mean(axis=0)+y_fits.std(axis=0), color=red, alpha=0.3, edgecolor='none')
ax.plot(x_fit, y_fits.mean(axis=0), color=red, alpha=0.75, linewidth=1)


# ax.axvline(x=0.95)
# ax.axvline(x=1.05)

# ax.axvline(x=popts[:, 2].mean()-0.05, color=(0.5, 0.5, 0.5), linewidth=1)
# ax.axvline(x=popts[:, 2].mean()+0.05, color=(0.5, 0.5, 0.5), linewidth=1)

ax.set_xlabel("Tweezer depth, a.u.")
ax.set_ylabel("Atom number")

# print(f"{ax.get_xlim() = }") # (0.6645021645021645, 1.2835497835497836)
# print(f"{ax.get_ylim() = }") # (-0.2272933773873748, 4.55798784806102)

plt.savefig("step-plot.pdf", bbox_inches='tight')
plt.close()
