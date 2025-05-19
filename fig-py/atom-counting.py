import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue
from scipy.optimize import curve_fit

data = np.load("../data/atom-counting/data.npz")
x, y = data['x'], data['y']

def gauss_sum(x, *params):
    amps = params[:-3]
    shift, delta, sigma = params[-3:]
    return sum(A * np.exp(-0.5 * ((x - (shift + delta * n)) / sigma)**2)
               for n, A in enumerate(amps))

n = 11
p0 = [0.05] * n + [0, 1, 0.13]

popt, _ = curve_fit(gauss_sum, x, y, p0=p0)

fig, ax = plt.subplots(1, 1, figsize=(3,2))

x_fit = np.linspace(x.min(), x.max(), 1000)
plt.bar(x, y, width=0.160292, label='Data', color=blue)
plt.plot(x_fit, gauss_sum(x_fit, *popt), color=red, linewidth=1.5, label='Fit', alpha=0.7)
# plt.legend()
plt.xlabel('Normalized Fluorescence signal')
plt.ylabel('Probability density')

plt.savefig("atom-counting.pdf", bbox_inches='tight')
plt.close()