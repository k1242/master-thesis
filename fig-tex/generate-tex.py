import os
import subprocess

latex_template = r"""
\documentclass[border=0.1mm]{standalone}
\usepackage{braket}
\usepackage{xcolor}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{bbm}

\definecolor{cred}{rgb}{0.86, 0.08, 0.24}
\definecolor{cblue}{rgb}{0.12, 0.56, 1.0}

\newcommand{\D}{^{\dag}}
\newcommand{\hc}{\mathrm{h.c.}}

\begin{document}

%s

\end{document}
"""

# name = ["ket(1)", "ket(2)", "ket(3)", "ket(4)", "ket(5)", "ket(6)"]
# code = [r"$\ket{1}$", r"$\ket{2}$", r"$\ket{3}$", r"$\ket{4}$", r"$\ket{5}$", r"$\ket{6}$"]

# name = ["MW-flip", "RF-flip"]
# code = [r"MW-flip", r"RF-flip"]

# name = ["mF", "m12", "m32", "32", "12"]
# code = [r"$m_F$", r"$-1/2$", r"$-3/2$", r"$3/2$", r"$1/2$"]

# name = ["F", "F52", "F32", "F12", "D1", "D2", "2S12", "2P12", "2P32"]
# code = [r"$F$", r"$5/2$", r"$3/2$", r"$1/2$", r"D${}_1$", r"D${}_2$", r"$2\, {}^2\mathrm{S}_{1/2}$", r"$2\, {}^2\mathrm{P}_{1/2}$", r"$2\, {}^2\mathrm{P}_{3/2}$"]

# name = ["ket(g)", "ket(e)", "Omega1", "Omega2", "momentumhbark", "Gamma"]
# code = [r"$\ket{\mathrm{g}}$", r"$\ket{\mathrm{e}}$", r"${\color{cblue} \Omega_1}$", r"${\color{cred} \Omega_2}$", "Momentum, $\hbar k$", r"$\Gamma$"]

# name = ["ket(x0)", "ket(x1)", "ket(xm)", "Udag", "U", "ket(0)", "ket(f(x))"]
# code = [r"$\ket{x_0}$", r"$\ket{x_1}$", r"$\ket{x_m}$", r"$U\D$", r"$U$", r"$\ket{0}$", r"$\ket{f(x)}$"]

# name = ["mathbbm(1)", "f(x)", "checkmark"]
# code = [r"$\mathbbm{1}$", r"$f(x)$", r"\checkmark"]

# name = ["loc-therm-a", "loc-therm-b", "loc-therm-c", "loc-therm-d"]
# code = [r"$U=1,\, V=1$", r"$U=0,\, V=10$", r"$U=0.1,\, V=10$", r"$U=1,\, V=10$"]

name = ["Delta-E", "80muW"]
code = [r"$\Delta E$", r"80$\mu$W"]

for (n, c) in zip(name, code):
    tex_filename = f"{n}.tex"
    
    with open(tex_filename, "w", encoding="utf-8") as f:
        f.write(latex_template % f"{c}")

    res = subprocess.run(["pdflatex", tex_filename])
    print(res)
    
    # aux_file = tex_filename.replace(".tex", ".aux")
    # log_file = tex_filename.replace(".tex", ".log")
    # for temp_file in [aux_file, log_file]:
    #     if os.path.exists(temp_file):
    #         os.remove(temp_file)

print("Ok.")
