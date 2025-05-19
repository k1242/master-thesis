from scipy.linalg import eigh_tridiagonal
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from colors import red, blue

# Grid
Nz = 1000
z = np.linspace(-10, 10, Nz)
dz = z[1] - z[0]

# Dimensionless coefficients
c0 = 1e-2*4
c1 = 1      # trap curvature
c2 = 0.2    # magnetic tilt

# Potential
U = -1 / (1 + (z / c1)**2) - c2 * z

# Kinetic energy (tridiagonal Laplacian)
main = c0 / dz**2 + U
off = -0.5 * c0 / dz**2 * np.ones(Nz - 1)

# Diagonalize Hamiltonian
E, psi = eigh_tridiagonal(main, off)
psi /= np.sqrt(np.sum(psi**2 * dz, axis=0))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(2,3))
ax1.plot(z, U, color='k')
    
mask_mean = (z[:, None] * np.abs(psi)**2).mean(axis=0) < 0.1
mask_std = (z[:, None] * np.abs(psi)**2).std(axis=0) < 0.5
mask = mask_mean & mask_std

for e in E[mask][:2]:
    ax1.axhline(y=e, color='k', linewidth=1, alpha=0.5)
for j in mask.nonzero()[0][:2]:
    ax2.plot(z, np.abs(psi[:, j])**2, color=blue)

ax1.set_xlim(-5,5)
ax1.set_ylim(-1.2,0)
ax2.set_xlim(-5,5)
plt.tight_layout()
plt.savefig("preparation-curves.pdf")
plt.close()