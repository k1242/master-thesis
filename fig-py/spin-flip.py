import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue, purple
from scipy.optimize import curve_fit

data = np.load("../data/spin-flip/data.npz")
x1, y1, x2, y2, xd, yd, xr, yrm, yrs = data['x1'], data['y1'], data['x2'], data['y2'], data['xd'], data['yd'], data['xr'], data['yrm'], data['yrs']

# Lorentzian centers
C1, C2, C3 = 823.59, 900.59, 986.61

def lorentzian(x, x0, gamma, amp):
    return amp * gamma**2 / ((x - x0) ** 2 + gamma**2)

def triple_lorentzian(x, g1, g2, g3, A1, A2, A3):
    return (lorentzian(x, C1, g1, A1) +
            lorentzian(x, C2, g2, A2) +
            lorentzian(x, C3, g3, A3))

def exp(t, A, B, G):
    return A + B * np.exp(-G * t)

def damped_cos(t, A, B, G, Ω):
    return A + B * np.exp(-G * t) * np.cos(Ω * t)


g1 = (13.3, 13.3, 20, 0.79, 0.77, 0.024)
g2 = (13.3, 13.3, 13.3, 0.759, 0.1, 1.03)
gd = (0.28, 1.23, 0.034)
gr = (0.5, 0.75, 0.04, 0.5)

p1, _ = curve_fit(triple_lorentzian, x1, y1, p0=g1)
p2, _ = curve_fit(triple_lorentzian, x2, y2, p0=g2)
pd, _ = curve_fit(exp, xd, yd, p0=gd)
pr, _ = curve_fit(damped_cos, xr, yrm, p0=gr)


fig, axs = plt.subplots(1, 3, figsize=(6, 1.9))

s = 4
axs[0].scatter(x1, y1, color=blue, s=s)
axs[0].scatter(x2, y2, color=red, s=s)
axs[1].scatter(xd, yd, color=purple, s=s)
axs[2].errorbar(xr, yrm, yrs, color=purple, fmt=',', linewidth=1)
axs[2].scatter(xr, yrm, color=purple, s=s)
# axs[2].plot(xr, yrm, color=purple, linewidth=1)


xx1 = np.linspace(x1.min(), x1.max(), 400)
axs[0].plot(xx1, triple_lorentzian(xx1, *p1), color=blue, lw=1, alpha=0.7)
xx2 = np.linspace(x2.min(), x2.max(), 400)
axs[0].plot(xx2, triple_lorentzian(xx2, *p2), color=red, lw=1, alpha=0.7)
xxd = np.linspace(0, xd.max(), 400)
axs[1].plot(xxd, exp(xxd, *pd), color=purple, lw=1, alpha=0.7)
xxr = np.linspace(0, xr.max(), 400)
axs[2].plot(xxr, damped_cos(xxr, *pr), color=purple, lw=1)

for ax in (axs[0],):
	ax.set_xticks([C1, C2, C3])
	# ax.set_xticklabels([r"$|1\rangle$", r"$|2\rangle$", r"$|3\rangle$"]))
	ax.set_xticklabels([f"{round(C1-C1)}", f"{round(C2-C1)}", f"{round(C3-C1)}"])
	for C in (C1, C2, C3):
		ax.axvline(x=C, linestyle='--', color='k', alpha=0.3, linewidth=0.5)
	ax.set_ylim(0, 1.1)
	ax.set_xlabel('Frequency, MHz')
	ax.set_ylabel(r'Fluorescence, a.u.')

axs[1].set_ylim(-0.05, 1.05)
axs[2].set_ylim(-0.05, 1.05)

axs[1].set_xticks([0, 50, 100])
axs[1].set_xlabel('Sweep time, ms')
axs[1].set_ylabel('Population')

axs[2].set_xlabel('Pulse time, ms')
axs[2].set_ylabel(r'Population')

axt = axs[0].twiny()
axt.cla()
axt.set_xticks([C1, C2, C3])
axt.set_xlim(axs[0].get_xlim())
axt.set_xticklabels([r"$|1\rangle$", r"$|2\rangle$", r"$|3\rangle$"])

plt.tight_layout()
# plt.savefig("spin-flip.pdf", bbox_inches='tight')

for i in range(3):
    for j, ax in enumerate(axs):
        ax.set_visible(i == j)
        axt.set_visible(i == 0)
    plt.savefig(f"spin-flip-{i+1}.pdf", bbox_inches='tight')

plt.close()
