# Determinantal Monte-Carlo sampling for two fermions in a 1D harmonic trap

import math, torch, matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from colors import red, blue, uBlues
plt.style.use('thesis.mplstyle')

# ------------------------------------------------------------------
# Grid and physical parameters
# ------------------------------------------------------------------
device = torch.device('cpu')

nx, lx = 64, 5.0
dx = lx / nx
x = (torch.arange(nx, device=device) - nx // 2) * dx
k = 2 * math.pi * torch.fft.fftfreq(nx, d=dx, device=device)
x_ho = math.sqrt(1 / math.pi)

mass, omega = 1.25, math.pi
rep = 2
dt = 5/30 / rep

# Initial Gaussian orbitals
sigma, x0 = lx / 15, lx / 4
psi = torch.stack([
    torch.exp(-(x - x0) ** 2 / (2 * sigma ** 2)),
    torch.exp(-(x + x0) ** 2 / (2 * sigma ** 2))
]).to(torch.complex64)
psi /= torch.sqrt((psi.abs() ** 2).sum(-1, keepdim=True) * dx)  # normalise

# Split-operator propagators
T = k ** 2 / (2 * mass)
V = 0.5 * mass * omega ** 2 * x ** 2
expK = torch.exp(-1j * T * dt / 2)
expV = torch.exp(-1j * V * dt)

def propagate(phi):
    """One split-operator time step."""
    phi = torch.fft.fft(phi, dim=-1) * expK
    phi = torch.fft.ifft(phi, dim=-1) * expV
    phi = torch.fft.fft(phi, dim=-1) * expK
    return torch.fft.ifft(phi, dim=-1)

# ------------------------------------------------------------------
# Basic projection-DPP sampler (Kulesza & Taskar, 2012)
# ------------------------------------------------------------------
def sample_projection_dpp(K):
    """Return indices drawn from a projection DPP with kernel K."""
    evals, evecs = torch.linalg.eigh(K)
    V = [evecs[:, j].clone() for j in (evals > 0.5).nonzero(as_tuple=True)[0]]
    Y = []
    while V:
        Vmat = torch.stack(V)                          # (m, nx)
        p = (Vmat.abs() ** 2).sum(0)                   # selection probabilities
        i = torch.multinomial(p, 1).item()
        Y.append(i)
        w = torch.tensor([abs(v[i]) ** 2 for v in V], device=K.device)
        v = V[torch.multinomial(w, 1).item()]
        new_V = []
        for u in V:
            if torch.allclose(u, v):                   # drop selected vector
                continue
            u = u - (u[i] / v[i]) * v                  # Gram–Schmidt step
            n = u.norm()
            if n > 1e-12:
                new_V.append(u / n)
        V = new_V
    return Y

# ------------------------------------------------------------------
# Monte-Carlo evolution
# ------------------------------------------------------------------
n_steps, n_mc = 3, 10_000
frames_g2, frames_rho = [], []
phi_t = psi.clone()

for step in range(n_steps + 1):
    # Build projection kernel K(x_i,x_j)
    phi = (phi_t * math.sqrt(dx)).cpu()               # (2, nx)
    K = (phi.conj().T @ phi).to(torch.complex64)      # (nx, nx)

    g2 = torch.zeros((nx, nx))
    rho = torch.zeros(nx)

    for _ in range(n_mc):
        i, j = sample_projection_dpp(K)
        rho[i] += 1
        rho[j] += 1
        g2[i, j] += 1
        g2[j, i] += 1

    frames_rho.append((rho / (2 * n_mc * dx)).numpy())
    frames_g2.append((g2 / n_mc).numpy())

    for _ in range(rep):
        phi_t = propagate(phi_t)

# ------------------------------------------------------------------
# Visualisation
# ------------------------------------------------------------------
m = len(frames_g2)
fig = plt.figure(figsize=(7, 2.5), dpi=400)
gs = gridspec.GridSpec(2, m, height_ratios=[2, 1], hspace=0.25, wspace=0.1)
extent = (-lx / (2 * x_ho), lx / (2 * x_ho), -lx / (2 * x_ho), lx / (2 * x_ho))

for j, g2 in enumerate(frames_g2):
    ax = fig.add_subplot(gs[0, j])
    ax.imshow(g2, origin='lower', extent=extent, cmap=uBlues)
    ax.plot([extent[0], extent[1]], [extent[2], extent[3]],
            '--', color='k', alpha=0.5, linewidth=1)
    ax.set_aspect('equal')
    ax.set_title(f'$t/T = {j * dt / 2:.2f}$')
    if j == 0:
        ax.set_ylabel(r"$x' / x_\mathrm{ho}$")
    else:
        ax.set_yticks([])

for j, rho in enumerate(frames_rho):
    ax = fig.add_subplot(gs[1, j])
    ax.plot(x.cpu() / x_ho, rho * 2, color=blue)
    ax.set_xlabel(r"$x / x_\mathrm{ho}$")
    ax.set_ylim(-0.1, 2)
    if j == 0:
        ax.set_ylabel(r"$n$")
    else:
        ax.set_yticks([])

fig.savefig('interference_dpp.pdf', bbox_inches='tight')
plt.close()
