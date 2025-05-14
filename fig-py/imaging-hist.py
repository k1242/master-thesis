import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.style.use('thesis.mplstyle')
from colors import red, blue

data = np.load("../data/imaging-hist/data.npz")
lm_tw, lm_ref = data['lm_tw'], data['lm_ref']
lm = np.concatenate((lm_tw, lm_ref))

print(np.mean(lm < 9))

bins = np.linspace(0, 40, 50)
counts, bin_edges = np.histogram(lm, bins=bins, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# two-Gaussian function (sum of two Gaussian bell curves)
def two_gaussians(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return A1 * np.exp(-((x - mu1)**2) / (2 * sigma1**2)) + A2 * np.exp(-((x - mu2)**2) / (2 * sigma2**2))

# A1, mu1, sigma1, A2, mu2, sigma2
p0 = [0.14, 3.7, 1.28, 0.051, 18.5, 4]
popt, pcov = curve_fit(two_gaussians, bin_centers, counts, p0=p0)
A1, mu1, sigma1, A2, mu2, sigma2 = popt

x_fit = np.linspace(0, 40, 400)
y_fit_total = two_gaussians(x_fit, *popt)
y_fit1 = A1 * np.exp(-((x_fit - mu1)**2) / (2 * sigma1**2))
y_fit2 = A2 * np.exp(-((x_fit - mu2)**2) / (2 * sigma2**2))


fig, ax = plt.subplots(1, 1, figsize=(1.8, 2))
ax.hist(lm, bins=bins, density=True, color=blue, alpha=0.6)
ax.plot(x_fit, y_fit1, linewidth=1.5, label='Noise', color='k', alpha=0.7)
ax.plot(x_fit, y_fit2, linewidth=1.5, label='Atom', color=red, alpha=0.7)
ax.axvline(x=9, linestyle='--', color='black', alpha=1.0, linewidth=1)
ax.set_xticks([0, 10, 20, 30, 40])
ax.set_ylim(0, 0.19)
ax.set_xlim(0, 30)
ax.set_title('Peak intensity, counts')
ax.legend(frameon=False)
plt.tight_layout()
plt.savefig("imaging-hist.pdf", bbox_inches='tight')
plt.close()