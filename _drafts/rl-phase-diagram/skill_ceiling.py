"""Schematic: reward fidelity as a skill ceiling. Illustrative curves, not data.

Left: real-task skill vs optimisation pressure for rewards of different fidelity
(the shape follows reward over-optimisation results such as Gao et al. 2022).
Right: a ladder, where you train on a cheap rung until it saturates, then switch
to an expensive, higher-fidelity rung.

    python3 skill_ceiling.py   ->  skill_ceiling.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from phase_diagram import SURFACE, INK, INK2, MUTED, GRID, AXIS

t = np.linspace(0, 10, 400)


def skill(f, t):
    """Rises towards a ceiling that grows with f, then degrades at a rate that grows with 1 - f."""
    if f >= 1:
        return 0.95 * (1 - np.exp(-t / 3.0))
    ceiling = 0.95 * f ** 0.8
    rise = ceiling * (1 - np.exp(-t / (1.0 + 2.5 * f)))
    peak_t = 1.5 + 6.0 * f
    fall = 0.06 * (1 - f) * np.clip(t - peak_t, 0, None) ** 1.6
    return np.clip(rise - fall, 0, None)


def style(ax, xlabel):
    ax.set_facecolor(SURFACE)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.05)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    ax.set_xlabel(xlabel, fontsize=10.5, color=INK)
    ax.set_ylabel("Skill on the real task", fontsize=10.5, color=INK)


def main():
    fig, (a, b) = plt.subplots(1, 2, figsize=(14, 5.6))
    fig.patch.set_facecolor(SURFACE)

    # Left: one curve per fidelity
    style(a, "Optimisation pressure against the reward (training) →")
    shades = {1.0: "#0b0b0b", 0.8: "#2a78d6", 0.5: "#7a5bd0", 0.2: "#eb6834", 0.0: MUTED}
    labels = {1.0: "1.0 sound: no ceiling but the task's own",
              0.8: "0.8 leaks at the edges: high ceiling, reached late",
              0.5: "0.5 breaks within a run: peaks, then exploited",
              0.2: "0.2 weakly correlated: low ceiling, reached fast",
              0.0: "0 contested: optimising doesn't help"}
    for f, c in shades.items():
        y = skill(f, t) + (0.01 if f == 0 else 0)
        a.plot(t, y, color=c, lw=2.2, label=labels[f])
    a.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False, fontsize=8.5,
             labelcolor=INK2, handlelength=1.5)
    a.axhline(0.55, color=INK2, lw=1, ls=(0, (4, 3)))
    a.text(0.1, 0.57, "today's model skill", fontsize=8.5, color=INK2)
    a.set_title("Fidelity sets the skill ceiling", loc="left", fontsize=12, fontweight="bold",
                color=INK)
    a.text(0.1, 0.99, "Rewards whose ceiling sits below today's skill can't teach anything.\n"
           "As models improve, that line rises, and so does the fidelity a task needs.",
           fontsize=8.5, color=INK2, va="top")

    # Right: ladder = switch rungs when the cheap one saturates
    style(b, "Training spend →")
    cheap = skill(0.5, t)
    switch = 3.2
    i = np.searchsorted(t, switch)
    cont = cheap.copy()
    after = t >= switch
    base = cheap[i]
    tt = t[after] - switch
    hi = base + (0.85 - base) * (1 - np.exp(-tt / 2.2))
    b.plot(t, cheap, color=MUTED, lw=1.6, ls=(0, (4, 3)))
    b.plot(t[: i + 1], cheap[: i + 1], color="#eb6834", lw=2.4)
    b.plot(t[after], hi, color="#2a78d6", lw=2.4)
    b.axvline(switch, color=AXIS, lw=1, ls=(0, (2, 3)))
    b.text(0.2, 0.30, "cheap rung\n(e.g. LLM judge, sim)", color="#eb6834", fontsize=9)
    b.text(5.6, 0.86, "expensive rung\n(e.g. lawyers, real robots)", color="#2a78d6", fontsize=9)
    b.text(6.4, 0.12, "staying on the cheap rung:\nplateau, then decline", color=MUTED, fontsize=8.5)
    b.text(switch + 0.1, 0.03, "switch when the\ncheap rung saturates", color=INK2, fontsize=8.5)
    b.set_title("Ladders: buy most of the skill cheaply, the rest dearly", loc="left", fontsize=12,
                fontweight="bold", color=INK)

    fig.suptitle("Reward fidelity as a skill ceiling (schematic, not data)", x=0.04, ha="left",
                 fontsize=14, fontweight="bold", color=INK, y=0.99)
    fig.subplots_adjust(left=0.04, right=0.80, top=0.86, bottom=0.1, wspace=0.12)
    # right panel sits after the left panel's labels
    b.set_position([0.66, 0.1, 0.32, 0.76])
    a.set_position([0.04, 0.1, 0.33, 0.76])
    fig.savefig("skill_ceiling.png", dpi=170, facecolor=SURFACE)


if __name__ == "__main__":
    main()
