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
	pcovs.append(np.diag(pcov)**0.5)
	y_fit = sigmoid2(x_fit, *popt)
	y_fits.append(y_fit)
popts = np.array(popts)
pcovs = np.array(pcovs)
y_fits = np.array(y_fits)


fig, ax = plt.subplots(1, 1, figsize=(2,2))


center = popts[:, 2]
center = center / center.mean()
center = center - center.mean()
center *= 100
err = pcovs[:, 2] * 100
ax.errorbar(np.arange(16), center, err, fmt=',', color=blue, alpha=0.7)
ax.scatter(np.arange(16), center, color=blue, s=10, alpha=1, edgecolor='none')
ax.axhline(y=0, color=(0.5, 0.5, 0.5), linestyle='--', linewidth=1)

# n = 1000
# est = np.random.randn(n, 16) * err
# est += center[None]
# est = est - est.mean(axis=1)[:, None]
# print(est.std(axis=1).std())
# print(est.std(axis=1).mean())
# # print(err.mean())
# print(center.std())

ax.set_ylim(-5, 5)
ax.set_xlabel('Tweezer')
ax.set_ylabel('Deviation, \\%')

plt.savefig("step-plot-balance.pdf", bbox_inches='tight')
plt.close()



N = 16

# Unbiased sample variance of the noisy measurements
s_obs2 = np.var(center, ddof=1) # (N−1) in denominator

# Mean squared measurement error
mean_err2 = np.mean(err ** 2)

# Bias-corrected variance of the true centres
s_true2 = s_obs2 - mean_err2
sigma_hat = np.sqrt(s_true2)

# Standard error via delta method
sigma_se = s_obs2 / (np.sqrt(2 * (N - 1)) * sigma_hat)


M = 10000 # number of MC repeats

# draw new noisy measurements: each row is one synthetic experiment
noisy = center + np.random.normal(scale=err, size=(M, N))

# sample variance of each experiment (unbiased, noisy)
s_obs2_mc = noisy.var(axis=1, ddof=1)

# bias-corrected variance of true centres per experiment
s_true2_mc = s_obs2_mc - mean_err2
s_true2_mc[s_true2_mc < 0] = 0   # truncate negative variances

sigma_mc = np.sqrt(s_true2_mc)   # σ̂ for every experiment

# summary statistics
sigma_mean = sigma_mc.mean()                     # MC estimate of σ̂
sigma_std  = sigma_mc.std(ddof=1)                # its standard error
ci_low, ci_high = np.percentile(sigma_mc, [2.5, 97.5])  # 95 % CI

print(f"{center.std() = :.2f}")
print(f"{err.mean()    = :.2f}")
print(f"Delta-method  : {sigma_hat:.2f} ± {sigma_se:.2f}")
print(f"Monte-Carlo   : {sigma_mean:.2f} ± {sigma_std:.2f}  (95% CI {ci_low:.2f}-{ci_high:.2f})")


# N = 16

# print(f"{center.std() = :.2f}")
# print(f"{err.mean() = :.2f}")
# print(f"{sigma_hat:.2f} +- {sigma_se:.2f}")

