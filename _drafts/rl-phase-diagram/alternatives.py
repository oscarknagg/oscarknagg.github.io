"""Alternative layouts of the phase diagram, to compare readability.

Uses TASKS and the palette from phase_diagram.py. Run from this folder:
    python3 alternatives.py
Writes alternatives/alt_*.png.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
import numpy as np

from phase_diagram import TASKS, CATS, SURFACE, INK, INK2, MUTED, GRID, AXIS, money

XMIN, XMAX, YMIN, YMAX = -1.0, 16.0, 0.0, 1.08
OUT = "alternatives"


def rung(r):
    x, xw, y, yw, label = r[:5]
    return x, xw, y, yw, label


def setup(ax, fs=1.0, frontier_text=True, axis_labels=True):
    ax.set_facecolor(SURFACE)
    bx = [XMIN, 5.4, 5.9, 6.1, 6.2, 6.22, 6.22]
    by = [0.58, 0.58, 0.60, 0.66, 0.75, 0.85, YMAX]
    ax.add_patch(Polygon(list(zip(bx, by)) + [(XMIN, YMAX)], closed=True,
                         facecolor="#2a78d6", alpha=0.045, edgecolor="none", zorder=0))
    ax.plot(bx, by, ls=(0, (6, 4)), lw=1.2, color=INK2, zorder=1)
    if frontier_text:
        ax.text(6.35, 1.055, "← Rough frontier, Nov 2026", fontsize=9 * fs, color=INK2,
                va="center", style="italic")
    for x, lab in ((9.0, "$1B"), (np.log10(1.1e14), "World GDP")):
        ax.axvline(x, color=AXIS, lw=1, ls=(0, (2, 3)), zorder=0)
        ax.text(x + 0.1, 0.02, lab, fontsize=8 * fs, color=MUTED, va="bottom")
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(YMIN, YMAX)
    ticks = list(range(0, 16, 3))
    ax.set_xticks(ticks)
    ax.set_xticklabels([money(x) for x in ticks])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.grid(True, color=GRID, lw=0.7, zorder=0)
    ax.tick_params(colors=INK2, labelsize=9 * fs, length=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    if axis_labels:
        ax.set_xlabel("Reward cost per R1-scale RL run (log scale)", fontsize=10 * fs, color=INK)
        ax.set_ylabel("Reward fidelity under optimisation pressure", fontsize=10 * fs, color=INK)


def edge_point(c, d, xw, yw):
    t = 1.0 / np.sqrt((d[0] / xw) ** 2 + (d[1] / yw) ** 2)
    return c + t * d


def ladder_arrows(ax, t, color, lw=1.3, alpha=1.0, to_centres=False):
    rungs = [rung(r) for r in t["rungs"]]
    for k, (r0, r1) in enumerate(zip(rungs, rungs[1:])):
        c0, c1 = np.array([r0[0], r0[2]]), np.array([r1[0], r1[2]])
        d = c1 - c0
        if to_centres:
            p0, p1 = c0, c1
        else:
            p0 = edge_point(c0, d, r0[1], r0[3])
            p1 = edge_point(c1, -d, r1[1], r1[3])
        ax.annotate("", xy=p1, xytext=p0, zorder=2,
                    arrowprops=dict(arrowstyle="->", color=color, lw=lw, alpha=alpha,
                                    linestyle=(0, (4, 3)), shrinkA=4 if to_centres else 0,
                                    shrinkB=4 if to_centres else 2,
                                    connectionstyle=f"arc3,rad={t.get('arcs', {}).get(k, 0)}"))


def ellipse(ax, t, i, r, color, fill_alpha=0.2, lw=1.8, edge_alpha=1.0):
    x, xw, y, yw, _ = rung(r)
    if i in t.get("forbidden", ()):
        ax.add_patch(Ellipse((x, y), 2 * xw, 2 * yw, facecolor="none", hatch="////",
                             edgecolor=color, lw=0, alpha=0.5 * edge_alpha, zorder=3))
        ax.add_patch(Ellipse((x, y), 2 * xw, 2 * yw, facecolor="none", edgecolor=color,
                             lw=lw, alpha=edge_alpha, zorder=4, ls=(0, (3, 2))))
    else:
        if fill_alpha:
            ax.add_patch(Ellipse((x, y), 2 * xw, 2 * yw, facecolor=color, alpha=fill_alpha,
                                 edgecolor="none", zorder=3))
        ax.add_patch(Ellipse((x, y), 2 * xw, 2 * yw, facecolor="none", edgecolor=color,
                             lw=lw, alpha=edge_alpha, zorder=4))


def flat(name):
    return name.replace("\n", " ")


# ---- A: numbered badges + key ----------------------------------------------
def alt_numbered():
    fig = plt.figure(figsize=(16, 8.5))
    fig.patch.set_facecolor(SURFACE)
    ax = fig.add_axes([0.06, 0.09, 0.66, 0.80])
    setup(ax)
    key = fig.add_axes([0.745, 0.09, 0.25, 0.80])
    key.axis("off")
    order = sorted(range(len(TASKS)), key=lambda i: (list(CATS).index(TASKS[i]["cat"]),
                                                     TASKS[i]["rungs"][0][0]))
    lines = []
    for n, ti in enumerate(order, start=1):
        t = TASKS[ti]
        color = CATS[t["cat"]][1]
        ladder_arrows(ax, t, color)
        multi = len(t["rungs"]) > 1
        parts = []
        for i, r in enumerate(t["rungs"]):
            ellipse(ax, t, i, r, color, fill_alpha=0.12, lw=1.4)
            x, _, y, _, lab = rung(r)
            tag = f"{n}{'abcd'[i]}" if multi else f"{n}"
            ax.text(x, y, tag, fontsize=8, color="white", fontweight="bold", ha="center",
                    va="center", zorder=8,
                    bbox=dict(boxstyle="round,pad=0.25", fc=color, ec="none"))
            if multi:
                parts.append(f"{'abcd'[i]} {flat(lab)}")
        lines.append((t["cat"], f"{n}  {flat(t['name'])}", " → ".join(parts)))
    y = 1.0
    cur = None
    for cat, title, sub in lines:
        if cat != cur:
            cur = cat
            y -= 0.02
            key.text(0, y, CATS[cat][0], fontsize=10, fontweight="bold", color=CATS[cat][1],
                     transform=key.transAxes, va="top")
            y -= 0.045
        key.text(0, y, title, fontsize=9.5, color=INK, transform=key.transAxes, va="top")
        y -= 0.035
        if sub:
            key.text(0.04, y, sub, fontsize=8.5, color=INK2, transform=key.transAxes, va="top")
            y -= 0.035
    key.text(0, y - 0.03, "Hatched: reward exists, but RL\nexploration isn't allowed",
             fontsize=8.5, color=INK2, transform=key.transAxes, va="top")
    fig.suptitle("A. Numbered badges with a key", x=0.06, ha="left", fontsize=14,
                 fontweight="bold", color=INK, y=0.965)
    fig.savefig(f"{OUT}/alt_a_numbered.png", dpi=150, facecolor=SURFACE)


# ---- B: small multiples by category ----------------------------------------
def alt_small_multiples():
    fig, axes = plt.subplots(1, 3, figsize=(19, 7), sharey=True)
    fig.patch.set_facecolor(SURFACE)
    for ax, cat in zip(axes, CATS):
        setup(ax, fs=0.9, frontier_text=False, axis_labels=False)
        ax.set_title(CATS[cat][0], fontsize=12, fontweight="bold", color=CATS[cat][1], loc="left")
        for t in TASKS:
            if t["cat"] == cat:
                continue
            for i, r in enumerate(t["rungs"]):
                ellipse(ax, t, i, r, MUTED, fill_alpha=0, lw=0.8, edge_alpha=0.35)
        for t in TASKS:
            if t["cat"] != cat:
                continue
            color = CATS[cat][1]
            ladder_arrows(ax, t, color)
            for i, r in enumerate(t["rungs"]):
                ellipse(ax, t, i, r, color)
                x, _, y, _, lab = rung(r)
                if lab and len(t["rungs"]) > 1:
                    ax.text(x, y, flat(lab), fontsize=7.5, color=INK2, ha="center", va="center",
                            zorder=7, bbox=dict(boxstyle="round,pad=0.1", fc=SURFACE, ec="none",
                                                alpha=0.7))
            lx, ly = t["label_at"]
            ax.text(lx, ly, t["name"], fontsize=9.5, color=INK, ha=t.get("ha", "center"),
                    va="center", zorder=8, fontweight="bold")
    axes[0].set_ylabel("Reward fidelity under optimisation pressure", fontsize=10, color=INK)
    axes[1].set_xlabel("Reward cost per R1-scale RL run (log scale)", fontsize=10, color=INK)
    fig.suptitle("B. Small multiples: one panel per category, others greyed",
                 x=0.04, ha="left", fontsize=14, fontweight="bold", color=INK, y=0.99)
    fig.subplots_adjust(left=0.05, right=0.99, top=0.88, bottom=0.1, wspace=0.06)
    fig.savefig(f"{OUT}/alt_b_small_multiples.png", dpi=150, facecolor=SURFACE)


# ---- C: centre dots, faint outlines, direct labels --------------------------
def alt_dots():
    fig, ax = plt.subplots(figsize=(14, 8.5))
    fig.patch.set_facecolor(SURFACE)
    setup(ax)
    for t in TASKS:
        color = CATS[t["cat"]][1]
        ladder_arrows(ax, t, color, lw=1.1, alpha=0.8, to_centres=True)
        multi = len(t["rungs"]) > 1
        for i, r in enumerate(t["rungs"]):
            ellipse(ax, t, i, r, color, fill_alpha=0.05, lw=0.9, edge_alpha=0.45)
            x, _, y, _, lab = rung(r)
            forb = i in t.get("forbidden", ())
            ax.plot(x, y, "o", ms=8, color=SURFACE if forb else color,
                    mec=color, mew=1.8, zorder=6)
            if multi and lab:
                ax.text(x + 0.18, y - 0.012, flat(lab), fontsize=7.5, color=INK2, va="top",
                        zorder=7)
        lx, ly = t["label_at"]
        ax.text(lx, ly, t["name"], fontsize=9.5, color=color, ha=t.get("ha", "center"),
                va="center", zorder=8, fontweight="bold")
    ax.text(15.8, 0.04, "Open dot: reward exists, but RL exploration isn't allowed",
            fontsize=8.5, color=INK2, ha="right")
    fig.suptitle("C. Centre dots with faint uncertainty outlines, labels coloured by category",
                 x=0.06, ha="left", fontsize=14, fontweight="bold", color=INK, y=0.97)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.09)
    fig.savefig(f"{OUT}/alt_c_dots.png", dpi=150, facecolor=SURFACE)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    alt_numbered()
    alt_small_multiples()
    alt_dots()
