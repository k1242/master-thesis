import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, bwr, uBlues
from matplotlib.patches import FancyArrowPatch

data = np.load("../data/crosstalk/data.npz")
residuals = data['residuals_camera']

x = residuals * 100


mu, std = norm.fit(x)

fig, ax = plt.subplots(1, 1, figsize=(1.5, 1.5))

ax.hist(x, bins=30, density=True, alpha=0.6, color=blue)
ax.set_xlabel(r"Relative residuals, \%")

x_fit = np.linspace(x.min(), x.max(), 100)
plt.plot(x_fit, norm.pdf(x_fit, mu, std), 'k', linewidth=1, alpha=0.7)



y_arrow = norm.pdf(mu+std, mu, std)
arrow = FancyArrowPatch(
    (mu - std, y_arrow),
    (mu + std, y_arrow),
    arrowstyle="<|-|>",
    mutation_scale=5,
    lw=1,
    color='k',
    shrinkA=0,
    shrinkB=0
)
ax.add_patch(arrow)
ax.text(mu, y_arrow + y_arrow*0.02, r"$2\sigma$", ha="center", va="bottom", alpha=0.7)


plt.savefig("crosstalk-camera-res.pdf", bbox_inches='tight')
plt.close()