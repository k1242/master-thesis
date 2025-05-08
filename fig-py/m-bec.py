import numpy as np
from scipy.optimize import curve_fit
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.style.use('thesis.mplstyle')
from colors import red, blue



data = np.load("../data/m-bec/data.npz")
PSD, T, X, Y, x, y = data['PSD'], data['T'], data['X'], data['Y'], data['x'], data['y']

px2mum = 5.7


def rb_c(alpha):
    return tuple(alpha*np.array(red) + (1-alpha)*np.array(blue))
plot_colors = [rb_c(t) for t in (T - T.min()) / (T.max() - T.min())]


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(6.3,2.1))


# ---------- I ----------

ax1.scatter(T, PSD, color=plot_colors, s=15)
ax1.set_xlabel("Temperature, nK")
ax1.set_ylabel("Phase Space Density")
ax1.set_xlim(0, 300)
ax1.set_ylim(-5.3, 65)


# ---------- II ----------

for j in range(Y.shape[0]):
    # scale = Y.max()
    scale = Y[j].sum()
    ax2.plot(X*px2mum/1000, gaussian_filter(Y[j], 1) / scale, alpha=0.8, color=plot_colors[j], label=T[j])
# ax2.legend()
ax2.set_xlabel(r"Position, mm")
ax2.set_ylabel(r"Atom density, a.u.")

cmap = mpl.colors.LinearSegmentedColormap.from_list('rb', [blue, red])
norm = mpl.colors.Normalize(vmin=T.min(), vmax=T.max())
sm   = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])
cax = ax1.inset_axes([0, 0, 1, 0.075], transform=ax1.transAxes)
cbar = fig.colorbar(sm, cax=cax, orientation='horizontal')
cbar.set_ticks([0, 100, 200, 300])
cbar.ax.xaxis.set_ticks([])


# ---------- III ----------

def fit_gauss(x, x0, a, b, c):
    return a * np.exp(- b * (x - x0)**2) + c


def plot_bec_fraction(ax, X, Y, b):
    """
    Draws experimental data, its Gaussian + BEC fit and fills the BEC contribution.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Existing axes where the plot will be drawn.
    X, Y : np.ndarray
        1‑D data arrays.
    b : float
        Threshold parameter used to cut out the central peak before Gaussian fit.
    """

    # ----------- helpers & defaults -----------
    yscale = Y.sum()
    fit_r = fit_gauss

    # ----------- central‑peak cut -----------
    x0 = np.argmax(Y)
    x1 = np.argmax(Y - b * Y.max() > 0)
    x2 = x0 + (x0 - x1)          # symmetric right edge

    X2fit = np.r_[X[:x1],  X[x2 + 1:]]
    Y2fit = np.r_[Y[:x1],  Y[x2 + 1:]]

    # ----------- Gaussian fit -----------
    popt, _ = curve_fit(fit_gauss, X2fit, Y2fit, p0=[0, 5, 0.01, 0.17])

    # ----------- residual fit -----------
    Yr = Y - fit_gauss(X, *popt)
    poptr, _ = curve_fit(fit_r, X, Yr, p0=[0, 9, 0.01, 0.03])

    # ----------- plotting -----------
    X2plot = np.linspace(X.min(), X.max(), 400)

    # data points
    ax.scatter(X[x1:x2 + 1]*px2mum / 1e3, Y[x1:x2 + 1]/yscale, s=10, color="k", zorder=10, linewidths=0, alpha=0.5)
    ax.scatter(X2fit*px2mum / 1e3, Y2fit/yscale, s=10, color=red, zorder=10, alpha=0.5, linewidths=0)

    # filled BEC area
    gauss_part = fit_gauss(X2plot, *popt) / yscale
    resid_part = fit_r(X2plot, *poptr) / yscale
    ax.fill_between(X2plot / 1e3 * px2mum,
                    gauss_part + resid_part,
                    gauss_part,
                    color="b", alpha=0.25, label="mBEC", linewidth=0)

    # Gaussian fit curve
    ax.plot(X2plot * px2mum / 1e3, gauss_part, ls="--", c="k", zorder=20, linewidth=1)

    x_half_span = px2mum * max(abs(X.min()), abs(X.max())) / 1e3
    ax.set_xlim(-x_half_span, x_half_span)


plot_bec_fraction(ax3, x, y, 0.09)
ax3.set_xlabel(r"Position, mm")
ax3.set_ylabel(r"Atom density, a.u.")
ax3.set_ylim(ax2.get_ylim())
# ax3.legend(frameon=False)


plt.tight_layout()
# plt.savefig("m-bec.pdf", bbox_inches='tight')

for i in range(3):
    for j, ax in enumerate((ax1, ax2, ax3)):
        ax.set_visible(i == j)
    plt.savefig(f"m-bec-{i+1}.pdf", bbox_inches='tight')