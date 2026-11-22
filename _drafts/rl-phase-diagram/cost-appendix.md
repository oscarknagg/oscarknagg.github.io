# Appendix draft: napkin maths for the reward-cost axis

*Written by Claude as working notes. Oscar sense-checks the rows he knows well and caveats the rest.*

The x axis is the cost to compute rewards for one R1-scale RL run: **5M rollouts** (DeepSeek-R1-Zero: 10,400 steps × 512 rollouts ≈ 5.3M). The policy's own generation cost is excluded. So each row is

> cost per reward × 5M

## Shared price assumptions (Nov 2026)

| Resource | Price used | Note |
|---|---|---|
| CPU | ~$0.04 per vCPU-hour | cloud on-demand, order of magnitude |
| GPU (H100) | ~$2.90 per hour | rental, Nov 2026 (sources in HANDOFF.md) |
| LLM judge tokens | ~$1–3 per M input tokens | frontier-ish judge |
| Skilled human time | ~$30–50/hour (readers, robot operators); far more for experts | |

## Per-task workings

"Plot" is the ellipse centre currently in `phase_diagram.py`. ⚠ marks a row where my napkin maths and the plot disagree by roughly 10× or more.

| Task | What the reward computation is | Cost per reward | × 5M | Plot | Confidence |
|---|---|---|---|---|---|
| Chess / Go | Apply the game rules to decide who won. A rules engine plays out a ~200-move game in about 1 ms of CPU. | ~1 ms CPU ≈ $10⁻⁸ | ~$0.06 | ~$1 | High. Effectively free, and the plot's $1 is a generous rounding. In AlphaZero-style training the dominant cost is search by the policy, which we exclude. |
| Math (Lean) | Lean type-checks the proof against Mathlib. Tactics such as `simp`, `omega` and `aesop` do real search when they run, which makes checking much heavier than checking a chess result. With Mathlib preloaded in a reused REPL, a check typically takes low single-digit seconds. A cold Mathlib import adds ~10–30 s. Timeouts on bad proofs are often set at ~60 s. | ~1–60 CPU-s, typically ~5 ≈ $5×10⁻⁵ | ~$50–3K, typically ~$300 | ~$500 | Medium. Timing comes from prover-paper reports, not my own measurement. |
| Software eng. (to a spec) | Start a container, apply the patch, run the test suite. SWE-bench-style. | ~2 vCPU × 2–15 min ≈ $0.001–0.02 | ~$5K–100K | ~$22K | Medium. Heavy repos with long-running test suites can be far more expensive. |
| Kernel optimisation | Compile, check correctness against a reference, benchmark on a GPU. | ~10–60 GPU-s ≈ $0.01–0.05 | ~$50K–250K | ~$110K | Medium |
| Chip design, digital (functional + open synth) *(not yet plotted)* | Simulate or check equivalence against a reference, then Yosys synthesis for an area/fmax estimate. Minutes of CPU for a block. | ~$0.001–0.1 | ~$3K–300K | — | Medium |
| Chip design, digital (signoff) *(not yet plotted)* | Commercial synthesis + place-and-route + static timing/power: ~2–20 CPU-hours per block (~$0.08–0.8). Licences reportedly cost ~4–10× the compute (AWS; 4× at Intel; see notes), giving ~$0.3–8 in total. | ~$0.3–8 | ~$1.5M–40M | — | Low. Licence pricing isn't public, and an EDA vendor training its own model would pay nothing for it. |
| Chip design, analog (SPICE) *(not yet plotted)* | 100s–10,000s of SPICE runs across process corners and Monte Carlo samples, at 0.1–10 s each, plus a simulator licence. | ~$10⁻⁴–1 | ~$500–5M | — | Low (very design-dependent) |
| Chip design, analog (post-layout + EM) *(not yet plotted)* | Parasitic extraction and re-simulation, plus electromagnetic sims for RF: hours of CPU plus licences. | ~$0.2–10 | ~$1M–50M | — | Low |
| Chip design, analog (silicon) *(not yet plotted)* | A multi-project-wafer shuttle slot at a mature node, ~$5K–100K per design. Months of latency. | ~$5K–100K | ~$25B–500B | — | Low |
| Law: document review *(not yet plotted)* | Compare model labels with adjudicated gold labels. The comparison is ~free; labelling costs ~$2–5 per document (contract reviewer at ~$50/hour, ~3–6 min) and is reused across many rollouts. | ~$0.001–0.06 amortised | ~$5K–300K | — | Medium-low (depends on how often labels are reused) |
| Law: memos / drafting, rubric judge *(not yet plotted)* | An LLM judge reads a ~10–100K-token deliverable (plus sources) and grades it against dozens of rubric criteria, with automated citation checks: ~$0.1–1 at ~$1–3 per M input tokens, allowing for several passes. (Harvey/Fireworks's $5.92 per task is the cost of running the model, not the reward, so it isn't used here.) | ~$0.1–1 | ~$0.5–5M | — | Medium-low |
| Law: memos, lawyer grading *(not yet plotted)* | A lawyer reads and grades the memo: 30–90 min at ~$150–500/hour. | ~$75–750 | ~$0.4–4B | — | Medium |
| Law: drafting, partner review *(not yet plotted)* | A partner reviews the mark-up: ~1–2 hours at ~$1,000–2,000/hour. | ~$1–4K | ~$5–20B | — | Medium |
| Law: litigation, historical dockets *(not yet plotted)* | Predict rulings from past cases and score against what happened. Cheap lookup plus an optional LLM judge. | ~$0.01–0.1 | ~$50K–500K | — | Medium |
| Law: litigation, mock trial *(not yet plotted)* | Expert judges or practitioners score arguments: hours of senior time per case. | ~$1–10K | ~$5–50B | — | Low |
| Materials: ML potential *(not yet plotted)* | Relax and score a proposed structure with a universal ML interatomic potential, ~1–100 GPU-seconds. | ~$0.001–0.1 | ~$5K–500K | — | Medium |
| Materials: DFT *(not yet plotted)* | DFT relaxation and energy, ~100–1,000 core-hours at ~$0.04 per core-hour. | ~$4–40 | ~$20–200M | — | Medium (depends on system size) |
| Materials: autonomous lab *(not yet plotted)* | Robot synthesis plus XRD characterisation: precursors, hours of robot time, amortised equipment. Throughput (~tens of compounds per lab per month) binds long before dollars. | ~$100–2,000 | ~$0.5–10B | — | Low |
| Strategy (business, policy, research direction) *(not yet plotted)* | Anything from an LLM judge grading a strategy against historical cases (~$0.2–1 per rollout) up to LLM-agent simulations of markets or societies (~$20–1,000 per rollout) or expert panels (~$100–1,000). | ~$0.2–1,000 | ~$1M–5B | — | Low. The point is the fidelity (0–0.2), not the cost. |
| Exploit finding | The target runs in a VM/container for the whole episode while the agent probes it; the reward is a captured flag, a sanitizer-detected crash or a working proof-of-concept. Checking is ~free; the cost is keeping the environment up (like computer use). | ~$0.02–0.2 | ~$100K–1M | ~$300K | Medium |
| Computer use | A VM or browser stays up for the whole episode, including the time the policy spends thinking. A scripted state check, or sometimes an LLM judge, gives the reward. | ~5–20 min VM at ~$0.1/h, plus up to ~$0.05 judge ≈ $0.02–0.2 | ~$100K–1M | ~$350K | Medium-low. The VM cost depends on policy latency, so it isn't purely a verification cost. |
| Small-scale pretraining, 100M | Train a Chinchilla-optimal 100M model and evaluate it. 6ND = 6 × 1e8 × 2e9 ≈ 1.2e18 FLOPs. At ~40% MFU on an H100 (~4e14 FLOP/s) that is ~50 min. | ~$2.5–3 | ~$12–15M | ~$20M | High for the arithmetic. Fitting a scaling trend across a size ladder adds ~30%. |
| Small-scale pretraining, 1B | Cost scales with N², so 100× the 100M run. | ~$250–300 | ~$1.3–1.5B | ~$1.6B | High (same arithmetic) |
| Locomotion (sim) | Run a GPU-parallel physics sim (Isaac Gym/Lab class). One rollout is an episode of ~20 s at 50 Hz = 1,000 steps. One GPU does ~10⁵–10⁶ steps/s across thousands of parallel envs. 5M × 1,000 = 5e9 steps ≈ 1.5–14 GPU-hours. | ~$10⁻⁶–10⁻⁵ | ~$5–40 | ~$16 (moved from ~$160) | Medium. Caveat: here a "rollout" is a control episode, not an LLM sample, so the units are only loosely comparable. |
| Robotic manipulation (sim) | Contact-rich physics is slower than locomotion, and vision policies need camera rendering. With rendering: ~1,000 frames per episode, ~10⁴ frames/s per GPU, which gives 5e9 frames ≈ 140 GPU-hours ≈ $400. State-only would be ~10× cheaper. | ~$10⁻⁵–10⁻³ | ~$20–5K | ~$500 | Medium |
| Robotic manipulation (real) | A physical robot plus a human or automated reset, ~1 minute per episode. Robot depreciation, operator time and space come to ~$50–200/hour. 5M minutes ≈ 83K robot-hours. (For scale, from memory: QT-Opt (2018) collected ~580K real grasps with 7 robots over several weeks.) | ~$1–3 | ~$4–17M | ~$16M | Medium |
| Self-driving (sim) | Depends heavily on the sim type. An object-level, data-driven sim like Waymax (accelerator-based) is ~90 steps per 9 s scenario, giving ~$30 for 5M scenarios. A sensor-level sim with camera/lidar rendering or neural reconstruction is perhaps ~$0.05 per simulated second; 20 s scenarios give ~$5M. | ~$10⁻⁵–1 | ~$30 / ~$5M | ~$30 (object) and ~$5M (sensor), now separate rungs | Low. The fidelity trade-off between the two sim types is the real story. |
| Self-driving (real) | A test vehicle with a safety driver, ~$100/hour all-in, at ~10 min per episode. | ~$17 | ~$85M | ~$100M (hatched) | Medium on cost. But exploring on public roads isn't allowed (see notes), so this rung can't actually be used for RL. |
| Novel, LLM judge | Judge reads a ~100K-word novel (~130K tokens): ~$0.15–0.40 per read. Use ~3–5 judges to reduce noise. | ~$0.5–2 | ~$2.5–10M | ~$5M | Medium. Note that generating the novel costs far more than judging it, and we're ignoring that. |
| Novel, human readers | A reader spends ~6–10 hours at ~$20–50/hour, so ~$150–500 per read. Use 3–5 readers per novel. | ~$500–2.5K | ~$2.5–12B | ~$8B | Medium |
| Drug efficacy (Phase 3) | One Phase 3 trial is one reward. Trials cost ~$20–100M+. Latency is years. | ~$20–100M | ~$100–500T | ~$400T | Medium on cost (published per-trial ranges vary a lot). |

## Removed from the plot
- **Forecasting.** A resolved question is a free and perfect reward, but supply (~10⁴–10⁵ resolved questions per year) and latency (months) are the real limits, and a dollar axis can't show them. Oscar will write about it separately.

## To check before publishing
- Lean timing: [Kimina Lean Server](https://nips.cc/virtual/2025/131063) and [the prover paper with import-overhead figures](https://arxiv.org/html/2504.21230v3). Confirm the per-proof seconds in their tables.
- Isaac Gym throughput and the ~20-minute ANYmal training figure: Rudin et al. 2021, "Learning to Walk in Minutes Using Massively Parallel Deep RL" (from memory). A recent data point: [Learning Sim-to-Real Humanoid Locomotion in 15 Minutes](https://arxiv.org/abs/2512.01996) (2025; only its title is confirmed).
- QT-Opt 580K grasps (from memory).
- Phase 3 cost range: find a single citable source.
- Waymax throughput: [Waymax paper](https://arxiv.org/abs/2310.08710).
