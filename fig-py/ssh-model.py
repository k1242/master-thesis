import torch
from cmath import exp, pi
import matplotlib.pyplot as plt
plt.style.use('thesis.mplstyle')
from tqdm import tqdm
from colors import red, blue
from matplotlib.patches import FancyArrow

n = 101   # number of momentums
N = 2 * n 


# init hamiltonians
h0 = torch.zeros((n, n), dtype=torch.complex64)
h1 = torch.diag(torch.ones(n - 1, dtype=torch.complex64), diagonal=-1)
h2 = torch.diag(torch.ones(n - 1, dtype=torch.complex64), diagonal=+1)

H1 = torch.cat((torch.cat((h0, h1), dim=1), torch.cat((h0, h0), dim=1)), dim=0)
H2 = torch.cat((torch.cat((h0, h2), dim=1), torch.cat((h0, h0), dim=1)), dim=0)

H1 = H1 + torch.conj(H1.T)
H2 = H2 + torch.conj(H2.T)


# define function for rk4 evolution
def L(ρ):
    Lρ = torch.zeros((N, N), dtype=torch.complex64)
    Lρ[n:, n:] = - ρ[n:, n:]
    Lρ[n:, :n] = - ρ[n:, :n] / 2
    Lρ[:n, n:] = - ρ[:n, n:] / 2
    Lρ.diagonal()[:n] += ρ.diagonal()[n:]    
    return Lρ

def f(t, ρ):
    if τ is not None:
        if round(t//τ) % 2:
            return - 1j * Ω * (H1 @ ρ - ρ @ H1) + γ * L(ρ)
        else:
            return - 1j * Ω * (H2 @ ρ - ρ @ H2) + γ * L(ρ)
    else:
        return - 1j * Ω * ((H1+H2) @ ρ - ρ @ (H1+H2)) + γ * L(ρ)

def rk_step(t, ρ):
    k1 = f(t, ρ)
    k2 = f(t + dt/2, ρ + dt/2 * k1)
    k3 = f(t + dt/2, ρ + dt/2 * k2)
    k4 = f(t + dt, ρ + dt * k3)
    return ρ + dt/6 * (k1 + 2 * k2 + 2 * k3 + k4)

def evol():
    # initial condition
    ρ = torch.zeros((N, N), dtype=torch.complex64)
    ρ.diagonal()[n//2] = 1
    
    # evolution
    nsteps = int(T//dt)
    ρs = torch.zeros((nsteps, N, N), dtype=torch.complex64)
    t = 0
    for j in range(nsteps):
        ρs[j] = ρ
        ρ = rk_step(t, ρ)
        t += dt
    
    p = ρs.diagonal(dim1=1, dim2=2).real
    p = p[:, :n] + p[:, n:]
    return p


# evolve
dt = 0.1 # time step
T = 13 # time
Ω = 2 # Rabi freq
γ = 0.1 # decay

τ = T+1; p1 = evol();
τ = None; p2 = evol();
τ = 3; p3 = evol();

p_log = [torch.log(p + 1e-3) for p in (p1, p2, p3)]


# plot
titles = [
	'Single beam\n', 
	'Two beams\ncontinuous',
	'Two beams\nalternating'
]

fig, axs = plt.subplots(1, 3, figsize=(5.4,1.5), sharey=True)

vmin = min(pl.min().item() for pl in p_log)
vmax = max(pl.max().item() for pl in p_log)

for (ax, p, title) in zip(axs, p_log, titles):
	im = ax.imshow(
        p, cmap='Blues', extent=(-n//2, n//2, T, 0), 
        aspect='auto', vmin=vmin, vmax=vmax
    )
	ax.set_title(title)

# [left, bottom, width, height]
cbar = fig.colorbar(im, cax=fig.add_axes([0.88, 0.1, 0.01, 0.78]))
cbar.ax.text(
    0.5, 1.04, 'log($p$)',
    ha='center', va='bottom',
    transform=cbar.ax.transAxes
)

for j in range(T//τ):
    # axs[2].axhline(y = (j + 1) * τ, color='k', alpha=0.25)
    sign = (-1)**j
    arrow = FancyArrow(
        x=-18*sign, y=(j+1/2)*τ, dx=3*sign, dy=0, width=0.2, 
        length_includes_head=True, head_width=0.5, head_length=1, 
        color=red
    )
    axs[2].add_patch(arrow)

axs[0].set_ylabel(r'Time, $\tau$')
for ax in axs:
    ax.set_xlabel(r'Momentum, $\hbar k$')
    # ax.axvline(x = 0, color='k', alpha=0.25, linestyle='-')
    ax.set_xlim(-20, 20)
    ax.set_xticks([-20, -10, 0, 10, 20])

plt.subplots_adjust(wspace=0.3, right=0.85)
plt.savefig("ssh-model.pdf", bbox_inches='tight')
plt.close()