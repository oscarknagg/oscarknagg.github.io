"""Reward fidelity vs reward cost phase diagram (November 2026).

x = log10(USD to verify one R1-scale RL run of ~5M rollouts), reward/verification
    cost only: policy generation cost and success rates are ignored.
y = reward fidelity under optimisation pressure (0 = contested target,
    1 = sound by construction).

Every number below is a rough judgement call. Edit TASKS and re-run:
    python3 phase_diagram.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Patch
from matplotlib.lines import Line2D
import numpy as np

N_ROLLOUTS = 5e6  # DeepSeek-R1-Zero: 10,400 steps x 512 rollouts ~= 5.3M

# ---- palette (validated categorical slots 1-3, light surface) ---------------
SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
CATS = {
    "digital": ("Digital / formal", "#2a78d6"),
    "physical": ("Physical world", "#eb6834"),
    "human": ("Human judgement & real-world outcomes", "#1baf7a"),
}

# ---- tasks -----------------------------------------------------------------
# Each rung: (x_centre, x_halfwidth, y_centre, y_halfwidth, rung_label[, (badge_dx, badge_dy)])
# x is log10(USD per run). Ladders are drawn as rungs joined by a dashed line.
# The optional offset nudges a rung's number badge off-centre where badges collide.
# label_at / ha / size / note / rung_label_offset are only used by alternatives.py.
# forbidden: indices of rungs whose reward exists but where RL exploration
# isn't allowed (public roads, patients). Drawn hatched.
TASKS = [
    dict(name="Chess / Go", cat="digital", label_at=(0.0, 1.035),
         rungs=[(0.0, 0.5, 0.985, 0.015, "")]),
    dict(name="Math (Lean)", cat="digital", label_at=(2.7, 0.95),
         rungs=[(2.7, 1.0, 0.95, 0.05, "")]),
    dict(name="Software eng.\n(to a spec)", cat="digital", label_at=(4.35, 0.775),
         rungs=[(4.35, 0.65, 0.775, 0.125, "")]),
    dict(name="Kernel\noptimisation", cat="digital", label_at=(5.05, 1.0),
         rungs=[(5.05, 0.4, 0.90, 0.045, "")]),
    dict(name="Computer\nuse", cat="digital", label_at=(5.55, 0.725), size=9.5,
         rungs=[(5.55, 0.45, 0.725, 0.075, "")]),
    dict(name="Exploit finding", cat="digital", label_at=(5.5, 0.97),
         rungs=[(5.5, 0.5, 0.90, 0.05, "")]),
    dict(name="Small-scale pretraining research", cat="digital", label_at=(9.2, 0.725),
         rungs=[(7.3, 0.4, 0.42, 0.07, "100M"), (9.2, 0.4, 0.62, 0.07, "1B")]),
    dict(name="Digital chip design", cat="digital", label_at=(6.9, 0.99),
         rungs=[(4.5, 1.0, 0.775, 0.075, "RTL + open synth", (0.3, -0.035)),
                (6.9, 0.7, 0.90, 0.05, "signoff", (-0.35, 0.03))]),
    dict(name="Analog chip design", cat="physical", label_at=(11.05, 1.02),
         rungs=[(4.7, 2.0, 0.625, 0.125, "SPICE"), (6.85, 0.85, 0.885, 0.035, "post-layout", (-0.3, -0.03)),
                (11.05, 0.65, 0.95, 0.03, "silicon")],
         rung_label_offset=-0.07),
    dict(name="Locomotion (sim)", cat="physical", label_at=(1.2, 0.725),
         rungs=[(1.2, 0.5, 0.82, 0.06, "")]),
    dict(name="Robotic\nmanipulation", cat="physical", label_at=(2.7, 0.45),
         rungs=[(2.7, 1.0, 0.42, 0.13, "sim"), (7.2, 0.5, 0.90, 0.05, "real", (0.3, 0.0))],
         rung_label_offset=-0.06),
    dict(name="Self-driving", cat="physical", label_at=(8.45, 0.935), ha="left",
         rungs=[(1.5, 0.45, 0.18, 0.07, "object\nsim"), (6.7, 0.45, 0.60, 0.10, "sensor\nsim"),
                (8.0, 0.35, 0.935, 0.04, "real")],
         forbidden=[2], arcs={0: 0.2},  # bend under the manipulation ellipse
         note=((8.45, 0.885), "real rung: exploring on\npublic roads isn't allowed")),
    dict(name="Robotic surgery (autonomous)", cat="physical",
         rungs=[(4.2, 0.5, 0.22, 0.08, "sim"), (8.9, 0.5, 0.55, 0.08, "ex vivo tissue"),
                (10.2, 0.5, 0.75, 0.05, "live animal"), (12.0, 0.4, 0.95, 0.03, "patients")],
         forbidden=[3]),
    dict(name="Writing a great novel", cat="human", label_at=(8.75, 0.215),
         rungs=[(6.7, 0.35, 0.22, 0.08, "LLM\njudge"), (9.9, 0.3, 0.48, 0.08, "human\nreaders")],
         beyond=((11.9, 0.70), "\u201cstands the test of time\u201d:\ndecades away, off the chart")),
    dict(name="Drug efficacy\n(Phase 3 trials)", cat="human", label_at=(14.6, 0.845),
         rungs=[(14.6, 0.6, 0.93, 0.04, "")]),
]

# Law tasks: first pass, shown on their own in law_preview.png until reviewed.
# Materials tasks: first pass, shown in materials_preview.png until reviewed.
MATERIALS_TASKS = [
    dict(name="Materials: new compounds", cat="physical",
         rungs=[(4.7, 1.0, 0.40, 0.10, "ML potential"),
                (7.8, 0.5, 0.575, 0.075, "DFT"),
                (9.35, 0.65, 0.775, 0.075, "autonomous lab")]),
]

# Judgement tasks: first pass, shown in judgement_preview.png until reviewed.
JUDGEMENT_TASKS = [
    dict(name="Strategy (business, policy, research direction)", cat="human",
         rungs=[(7.85, 1.85, 0.10, 0.10, "")],
         beyond=((11.6, 0.30), "real outcomes: years,\nn = 1, no counterfactual")),
]

# beyond: an arrow from the last rung to a point off to the right, for a true
# test that can't be put on the chart.
LAW_TASKS = [
    dict(name="Document review / diligence", cat="human",
         rungs=[(4.6, 0.9, 0.70, 0.10, "")]),
    dict(name="Research memos", cat="human",
         rungs=[(6.2, 0.5, 0.525, 0.075, "rubric judge + citations", (-0.25, 0.02)),
                (9.1, 0.5, 0.75, 0.05, "lawyer grading")]),
    dict(name="Contract drafting", cat="human",
         rungs=[(6.2, 0.5, 0.475, 0.075, "rubric / playbook judge", (0.25, -0.02)),
                (10.0, 0.3, 0.70, 0.05, "partner review")],
         beyond=((12.0, 0.85), "true test: does it hold up in\na dispute years later?")),
    dict(name="Litigation", cat="human",
         rungs=[(5.2, 0.5, 0.375, 0.075, "historical rulings"),
                (10.2, 0.5, 0.55, 0.05, "mock trial")],
         beyond=((12.2, 0.64), "real rulings: can't experiment\non live cases; years of latency")),
]


def money(x):
    v = 10 ** x
    for unit, div in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if v >= div:
            return f"${v / div:g}{unit}"
    return f"${v:g}"


def edge_point(c, d, xw, yw):
    """Point where the ray from ellipse centre c in direction d exits the ellipse."""
    t = 1.0 / np.sqrt((d[0] / xw) ** 2 + (d[1] / yw) ** 2)
    return c + t * d


def flat(text):
    return text.replace("\n", " ")


def draw(tasks, out, title, subtitle, footnote=None):
    """Faint uncertainty ellipses, a numbered badge at each centre, names in a key."""
    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(SURFACE)
    ax = fig.add_axes([0.085, 0.10, 0.645, 0.76])
    key = fig.add_axes([0.755, 0.03, 0.24, 0.83])
    key.axis("off")
    ax.set_facecolor(SURFACE)
    xmin, xmax, ymin, ymax = -1.0, 16.0, 0.0, 1.08

    # Rough "already fallen" region (judgement, not data)
    bx = [xmin, 5.4, 5.9, 6.1, 6.2, 6.22, 6.22]
    by = [0.58, 0.58, 0.60, 0.66, 0.75, 0.85, ymax]
    ax.add_patch(Polygon(list(zip(bx, by)) + [(xmin, ymax)], closed=True,
                         facecolor="#2a78d6", alpha=0.045, edgecolor="none", zorder=0))
    ax.plot(bx, by, ls=(0, (6, 4)), lw=1.4, color=INK2, zorder=1)
    ax.text(6.35, 1.055, "\u2190 Rough frontier, Nov 2026: tasks inside have largely fallen to RL",
            fontsize=9, color=INK2, va="center", style="italic")

    # Budget reference lines
    for x, lab in ((9.0, "$1B: a very large\nRL run"), (np.log10(1.1e14), "World GDP\n(~$110T)")):
        ax.axvline(x, color=AXIS, lw=1, ls=(0, (2, 3)), zorder=0)
        ax.text(x + 0.1, 0.02, lab, fontsize=8, color=MUTED, va="bottom")

    # Number tasks by category, then by cost of their cheapest rung
    cats = list(CATS)
    order = sorted(tasks, key=lambda t: (cats.index(t["cat"]), t["rungs"][0][0]))
    entries = []
    for n, t in enumerate(order, start=1):
        _, color = CATS[t["cat"]]
        rungs = t["rungs"]
        multi = len(rungs) > 1
        forbidden = t.get("forbidden", ())
        for k, (r0, r1) in enumerate(zip(rungs, rungs[1:])):
            c0, c1 = np.array([r0[0], r0[2]]), np.array([r1[0], r1[2]])
            d = c1 - c0
            p0 = edge_point(c0, d, r0[1], r0[3])
            p1 = edge_point(c1, -d, r1[1], r1[3])
            ax.annotate("", xy=p1, xytext=p0, zorder=2,
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.2, alpha=0.75,
                                        linestyle=(0, (4, 3)), shrinkA=0, shrinkB=2,
                                        connectionstyle=f"arc3,rad={t.get('arcs', {}).get(k, 0)}"))
        parts = []
        for i, r in enumerate(rungs):
            x, xw, y, yw, lab = r[:5]
            dx, dy = r[5] if len(r) > 5 else (0, 0)
            if i in forbidden:
                ax.add_patch(Ellipse((x, y), 2 * xw, 2 * yw, facecolor="none", hatch="////",
                                     edgecolor=color, lw=0, alpha=0.35, zorder=3))
                ax.add_patch(Ellipse((x, y), 2 * xw, 2 * yw, facecolor="none", edgecolor=color,
                                     lw=1.0, alpha=0.6, zorder=4, ls=(0, (3, 2))))
            else:
                ax.add_patch(Ellipse((x, y), 2 * xw, 2 * yw, facecolor=color, alpha=0.06,
                                     edgecolor="none", zorder=3))
                ax.add_patch(Ellipse((x, y), 2 * xw, 2 * yw, facecolor="none", edgecolor=color,
                                     lw=1.0, alpha=0.55, zorder=4))
            tag = f"{n}{'abcd'[i]}" if multi else f"{n}"
            open_badge = i in forbidden
            ax.text(x + dx, y + dy, tag, fontsize=8, fontweight="bold", ha="center", va="center",
                    color=color if open_badge else "white", zorder=8,
                    bbox=dict(boxstyle="round,pad=0.25", fc=SURFACE if open_badge else color,
                              ec=color, lw=1.2))
            if multi:
                parts.append(f"{'abcd'[i]} {flat(lab)}" + (" *" if open_badge else ""))
        if "beyond" in t:
            (ex, ey), etext = t["beyond"]
            lx, lxw, ly, lyw = rungs[-1][:4]
            c = np.array([lx, ly])
            start = edge_point(c, np.array([ex, ey]) - c, lxw, lyw)
            ax.annotate("", xy=(ex, ey), xytext=start,
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.2, alpha=0.75,
                                        linestyle=(0, (4, 3))))
            ax.text(ex + 0.1, ey, etext, fontsize=8, color=INK2, va="center")
            parts.append("off chart")
        if "stub" in t:
            # Overview: short arrow towards the task's next (costlier) rung
            (x0, xw0, y0, yw0), (x1, y1) = t["rungs"][0][:4], t["stub"]
            d = np.array([x1 - x0, (y1 - y0) * 12])
            d /= np.linalg.norm(d)
            d = np.array([d[0], d[1] / 12])
            start = edge_point(np.array([x0, y0]), d, xw0, yw0)
            ax.annotate("", xy=start + 0.9 * d, xytext=start, zorder=2,
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.3, alpha=0.8))
        name = flat(t["name"]) + ("  \u2192" if "stub" in t else "")
        entries.append((t["cat"], n, name, " \u2192 ".join(parts)))

    # Axes
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ticks = list(range(0, 16, 3))
    ax.set_xticks(ticks)
    ax.set_xticklabels([money(x) for x in ticks])
    ax.set_xticks(range(-1, 17), minor=True)
    ax.set_yticks([0, 0.2, 0.5, 0.8, 1.0])
    ax.set_yticklabels(["0  contested", "0.2  weakly\ncorrelated", "0.5  breaks\nwithin a run",
                        "0.8  leaks at\nthe edges", "1.0  sound"])
    ax.grid(True, which="major", color=GRID, lw=0.7, zorder=0)
    ax.tick_params(colors=INK2, labelsize=9, length=0)
    ax.tick_params(which="minor", length=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
    ax.set_xlabel("Reward cost: dollars to verify one R1-scale RL run (~5M rollouts), log scale",
                  fontsize=10.5, color=INK, labelpad=10)
    ax.set_ylabel("Reward fidelity under optimisation pressure", fontsize=10.5, color=INK, labelpad=10)

    # Key: shrink spacing and type if there are many entries
    ncat = len({e[0] for e in entries})
    need = 0.034 * sum(2 if e[3] else 1 for e in entries) + 0.08 * ncat + 0.12
    k = min(1.0, 1.0 / need)
    fk = max(k, 0.72)
    y, cur = 1.0, None
    for cat, n, name, sub in entries:
        if cat != cur:
            cur = cat
            y -= (0.015 if n == 1 else 0.035) * k
            key.text(0, y, CATS[cat][0], fontsize=10 * fk, fontweight="bold", color=CATS[cat][1],
                     transform=key.transAxes, va="top")
            y -= 0.045 * k
        key.text(0, y, f"{n:>2}", fontsize=9.5 * fk, color=CATS[cat][1], fontweight="bold",
                 transform=key.transAxes, va="top")
        key.text(0.08, y, name, fontsize=9.5 * fk, color=INK, transform=key.transAxes, va="top")
        y -= 0.034 * k
        if sub:
            key.text(0.08, y, sub, fontsize=8.5 * fk, color=INK2, transform=key.transAxes, va="top")
            y -= 0.034 * k
    key.text(0, y - 0.03 * k, footnote if footnote else "Letters are rungs of a ladder: a cheap proxy reward \u2192 the\n"
             "expensive real one. * Hatched, open badge: the reward exists,\n"
             "but RL exploration isn't allowed.", fontsize=8, color=INK2,
             transform=key.transAxes, va="top")

    fig.suptitle(title,
                 x=0.065, ha="left", fontsize=15, color=INK, fontweight="bold", y=0.97)
    fig.text(0.065, 0.925, subtitle, fontsize=9.5, color=INK2, ha="left")

    for ext in ("png", "svg"):
        fig.savefig(f"{out}.{ext}", dpi=200, facecolor=SURFACE)
    plt.close(fig)


SUBTITLE = ("Each ellipse is a rough judgement with its uncertainty; the badge marks its centre. "
            "Generation cost and success rates are ignored.")


def overview_tasks(tasks):
    """One ellipse per task: its cheapest rung, with a stub towards the next rung."""
    out = []
    for t in tasks:
        r = t["rungs"]
        o = dict(name=t["name"], cat=t["cat"], rungs=[r[0]])
        if len(r) > 1:
            o["stub"] = (r[1][0], r[1][2])
        out.append(o)
    return out


OVERVIEW_NOTE = ("Each task is shown at its cheapest reward. \u2192 marks a ladder: costlier,\n"
                 "higher-fidelity rewards exist (see the per-domain plots).")


def main():
    draw(TASKS + LAW_TASKS + MATERIALS_TASKS + JUDGEMENT_TASKS, "phase_diagram_2026",
         "Where RL can reach: reward fidelity vs reward cost, November 2026", SUBTITLE)
    novel = [t for t in TASKS if t["name"].startswith("Writing a great novel")]
    draw(JUDGEMENT_TASKS + novel, "judgement_preview",
         "Judgement tasks against the frontier (first pass, Nov 2026)", SUBTITLE)
    draw(MATERIALS_TASKS, "materials_preview",
         "Materials tasks against the frontier (first pass, Nov 2026)", SUBTITLE)
    draw(LAW_TASKS, "law_preview", "Law tasks against the frontier (first pass, Nov 2026)", SUBTITLE)


if __name__ == "__main__":
    main()
