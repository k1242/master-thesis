import torch
import math
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from matplotlib.gridspec import GridSpec
from colors import red, blue, uBlues

device = torch.device('cpu')

# Grid parameters
nx   = 1024          # number of spatial points
lx   = 5.0         # box length
dx   = lx / nx
x    = (torch.arange(nx, device=device) - nx//2) * dx          # centered grid
k    = 2 * math.pi * torch.fft.fftfreq(nx, d=dx, device=device)

x_ho = math.sqrt(1 / math.pi)

# Physical constants (dimensionless units: ħ = 1)
mass  = 1.25
omega = math.pi
rep = 4
dt    = 5/30/rep

# Initial Gaussian packets (zero mean momentum, opposite centres)
sigma = lx / 15
x0    =  lx / 4
psi = torch.zeros((2, nx), dtype=torch.complex64, device=device)
psi[0] = torch.exp(- (x - x0)**2 / (2 * sigma**2))
psi[1] = torch.exp(- (x + x0)**2 / (2 * sigma**2))

# Normalise each orbital to unity
for i in range(2):
    norm = torch.sum(torch.abs(psi[i])**2) * dx
    psi[i] /= torch.sqrt(norm)

# Pre-computed split-step propagators
T    = k**2 / (2 * mass)                            # kinetic energy
V    = 0.5 * mass * omega**2 * x**2                 # harmonic potential
expK = torch.exp(-1j * T * dt / 2)                  # half-step kinetic
expV = torch.exp(-1j * V * dt)                      # full-step potential

def propagate(batch_psi: torch.Tensor) -> torch.Tensor:
    """One time step for a batch of orbitals (shape: n_orb, nx)."""
    batch_psi = torch.fft.fft(batch_psi, dim=-1)
    batch_psi *= expK
    batch_psi = torch.fft.ifft(batch_psi, dim=-1)
    batch_psi *= expV
    batch_psi = torch.fft.fft(batch_psi, dim=-1)
    batch_psi *= expK
    batch_psi = torch.fft.ifft(batch_psi, dim=-1)
    return batch_psi


n_steps         = 3
frames          = []
frames_rho = []
frames_psi = []

psi_t = psi.clone()
for step in range(n_steps + 1):
    # Move data to CPU once per snapshot for cheaper analysis
    psi1, psi2 = psi_t.cpu()
    frames_psi.append(psi_t.cpu().numpy())

    # One-particle density ρ(x)
    rho = torch.abs(psi1)**2 + torch.abs(psi2)**2

    # Two-particle g2 (anti-symmetrised) and normalisation
    g2 = 0.5 * torch.abs(
            torch.outer(psi1, psi2) - torch.outer(psi2, psi1)
         )**2
    g2_norm = g2  # / (rho[:, None] * rho[None, :] + 1e-3)
    frames.append(g2_norm.numpy())
    frames_rho.append(rho.numpy())

    for _ in range(rep):
        psi_t = propagate(psi_t)

# ------------------------------ Visualisation ----------------------------- #
m = len(frames)
fig = plt.figure(figsize=(7, 2.5), dpi=400)
gs = GridSpec(2, m, height_ratios=[2, 1], hspace=0.25, wspace=0.1)
extent = (-lx/2/x_ho, lx/2/x_ho, -lx/2/x_ho, lx/2/x_ho)

for j, d in enumerate(frames):
    ax = fig.add_subplot(gs[0, j])
    ax.imshow(d, origin='lower', extent=extent, cmap=uBlues)
    ax.set_title(fr'$t/T = {j*dt/2*rep:.2f}$')
#     ax.set_xlabel(r'$x$')
    ax.plot([-lx/2/x_ho, lx/2/x_ho], [-lx/2/x_ho, lx/2/x_ho], 'k--', alpha=0.5, linewidth=1)
    ax.set_aspect('equal', adjustable='box')
    (ax.set_ylabel(r"$x' / x_\mathrm{ho}$") if j == 0 else ax.set_yticks([]))

for j, d in enumerate(frames_rho):
    ax = fig.add_subplot(gs[1, j])
    ax.plot(x/x_ho, d, color=blue)
    ax.set_xlabel(r'$x / x_\mathrm{ho} $')
    ax.set_ylim(-0.1, 2)
    (ax.set_ylabel(r'$n$') if j == 0 else ax.set_yticks([]))

# plt.tight_layout()
plt.savefig("interference.pdf", bbox_inches='tight')
plt.close()