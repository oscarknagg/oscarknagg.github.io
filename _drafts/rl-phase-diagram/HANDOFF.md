# Handoff: "AI progress through the reward fidelity / reward cost lens"

Context carried over from a claude.ai session (22 Nov 2026) for continuing in Claude Code.
Files alongside this note: `phase_diagram.py` (regenerates the figure), `phase_diagram_2026.png`, `phase_diagram_2026.svg`.

## Working agreements with the author
- The post's words are the author's own. Claude helps with analysis and is credited for that. Don't draft prose unless asked.
- Keep each turn low-bandwidth: go deep on a few tasks, not many unfamiliar domains at once.
- The plot starts with tasks the author knows well. Others (law, chips, materials, surgery) get added later, mostly on Claude's judgement.
- British spelling ("optimisation").

## Planned post structure (from the author)
1. A crisp statement that RL-driven learning drives progress now (pretraining necessary but not sufficient).
2. Introduce the two axes and the phase diagram as of November 2026, with each task as an ellipse showing uncertainty.
3. What it looked like in the past (a pre-LLM year, ~2019).
4. How it might change as models and hardware improve.
5. Opportunities: tasks that become amenable if money goes into better reward fidelity/cost (simulators, automated labs, formalisation).
6. Gaps and failures of the method (forecasting is the lead example).
7. Concrete predictions.
Sections 3–7 were deliberately deferred. The current focus is understanding the tasks on the plot.

## The framework as agreed
- **y: reward fidelity under optimisation pressure, 0–1.** Not average correlation with the true goal, but whether the reward holds up when an optimiser searches for its gaps. False positives (accepting bad outputs) matter; false negatives mostly waste signal.
  Anchors: 1.0 sound by construction (Lean, game rules) · 0.8 strong but hackable (unit tests) · 0.5 a proxy that breaks under pressure (LLM judge, docking, backtests) · 0.2 a weak proxy · ~0 a contested target.
- **x: reward cost, log10 of USD to verify one R1-scale RL run of ~5M rollouts.** Verification/environment cost only.
  - The author decided to **ignore policy generation cost** (the floor for a frontier run is ~$10^5–10^6 anyway; cheap rewards still matter because they make experimentation cheap).
  - The author decided to **ignore success rate** (partial rewards and curricula make it hard to estimate).
  - The 5M figure comes from DeepSeek-R1-Zero: 10,400 steps × 512 rollouts (32 questions × 16 samples) ≈ 5.3M. The top open model now (Kimi K3.1 Pro) doesn't publish rollout counts.
  - Multiplying by a fixed N is just a constant shift on a log axis. Its value is readability: budget lines can be drawn ($1B ≈ a very large RL run, a rough guess; world GDP ≈ $110T).
- **Ladders:** many tasks have a cheap proxy rung and an expensive real rung (sim → real robot, LLM judge → human readers). These are drawn as separate ellipses joined by a dashed arrow.
- **Place tasks, not fields** (medicine spans the whole plot).
- **Bootstrappability was considered and dropped** as an axis. The author's point: formal math fell fast despite little formal data (Mathlib ~2M lines; all formal libraries ~10M lines, roughly 0.001% of a pretraining corpus), because the bootstrap came from informal math via autoformalisation (AlphaProof autoformalised ~80M statements). It folds into cost; it explains the games-before-math timing but mostly matters historically.
- **Latency is not dollars.** You can parallelise dollars but not wall-clock time. This shows up most in forecasting and in materials durability testing.
- The **off-diagonal corners** suggest what is needed. Cheap but unsound needs better verifiers (formalisation, robust reward models). Sound but expensive needs cheaper rungs (simulators, surrogates, automated labs).
- The cost axis is **model- and time-dependent**: compute prices, lab budgets and model quality all move tasks over time.

## Key analysis points (for later sections)
- **RL drives progress.** R1 used ~5% of compute on post-training. RL compute rose >10× from o1 to o3. SemiAnalysis attributes recent gains to scaling RL. A 2026 paper finds post-RL performance is predicted by pretraining loss (pretraining sets the ceiling). Counterpoint: Toby Ord argues RL scales poorly (≈10,000× RL compute to match 100× inference).
- **RL on small-scale pretraining experiments** (a slice of recursive self-improvement). A 100M Chinchilla-optimal run is ~1.2e18 FLOPs, ≈1 H100-hour, ≈$3. Cost per reward scales with N², so 1B ≈ $300 and 10B ≈ $30k. FLOP/$ doubles every ~2 years (Epoch), so the affordable inner-loop scale grows only √2 every 2 years. Lab budgets grow faster, so consider normalising cost to lab compute.
  Fidelity issues: small-scale gains often don't transfer to large models (Narang et al. 2021, from memory); seed noise; hacking (validation leakage, tokenizer changes, so use bits-per-byte and a locked harness with metered compute); latency. Mitigation: reward a fitted scaling trend over a size ladder (20M/50M/100M costs ~30% more than 100M alone).
- **Forecasting as the gap case.** The true reward is free and perfect but latency is months and supply is ~10^4–10^5 resolved questions per year. It is still RL-trained using the past as a simulator (Turtel et al.: RL on 110k questions matched o1 accuracy with better calibration); temporal leakage limits fidelity. Much of the gain is probably transfer from RL'd reasoning and search. Main caveat for the whole method: the plot measures *direct* trainability; capability also arrives by transfer.
  State in 2026: FRI says AI has likely reached parity with superforecasters on ForecastBench (superforecasters dispute what the benchmark shows); Metaculus Pros still beat bots as of May 2026.
- **Law:** verifiability runs inversely to billing rate (document review is verifiable; partner judgement is not). Harvey is already RL-training a Kimi K3-based legal model (via Fireworks).
- **Novel:** "greatness" partly means departing from current taste, so proxies calibrated on today's readers penalise it. That puts a fidelity ceiling below 1 at any spend.
- **Surgery:** the top rung (patients) is forbidden, not just expensive (as is the Phase 3 rung for drugs). Current state is imitation learning (SRT-H, ex vivo cholecystectomy).
- **Materials:** split by verification structure (computable crystal properties vs processing/durability). Cautionary tale: A-Lab claimed 41 novel compounds; a critique found ~2/3 were likely known disordered versions, and the critics concluded none were new. The automated characterisation (the reward) was the weak link.
- **Analog/RF:** good ladder (SPICE → manufacturing-variation sweeps → post-layout/EM → silicon). The bottleneck is bootstrap/data access (proprietary designs, NDA'd PDKs, closed tools), not verification.

## Tasks currently plotted
See `TASKS` in `phase_diagram.py`: Chess/Go, Math (Lean), Software eng., Kernel optimisation, Computer use, Small-scale pretraining research (100M → 1B), Locomotion (sim), Robotic manipulation (sim → real), Self-driving (sim → real), Forecasting (dashed: misplaced by the cost axis), Writing a great novel (LLM judge → human readers → off chart), Drug efficacy (Phase 3).
The "rough frontier" line (fidelity > ~0.6, cost < ~$1M) is Claude's judgement, not data.

## Not yet plotted: first-pass placements (verification-only axis, unreviewed)
Format: log10($ per 5M-rollout run) (fidelity). Arrows are ladder rungs.
- Math/science with checkable answers: 1.7–2.7 (0.7–0.85)
- Law, document review/diligence: 2.7–4.7 (0.75–0.85)
- Law, research memos: 4.7 citation check (0.5) → 9.2–9.7 expert grading (0.7)
- Law, drafting agreements: 5.7 playbook check (0.6) → 9.7–10.2 partner review (0.65); true test unobservable
- Law, negotiation (self-play): 5.7 (0.3–0.5)
- Law, litigation: 4.7–5.7 historical dockets (0.5) → off chart, real rulings (0.7)
- Law, strategic counsel: 9.7–10.7 expert panels (0.1–0.3)
- Surgery: 3.7–4.7 sim (0.2) → 8.4–9.4 ex vivo (0.55) → 9.7–10.7 live animal (0.75); patients forbidden
- Analog/RF: 4.7–6.7 SPICE + variation sweeps (0.75–0.9) → 7.7–8.7 post-layout/EM → 10.7–11.7 silicon (0.95)
- Materials, computable properties: 4.7–8.7 (0.5–0.7) → 8.7–9.7 automated lab (0.75)
- Materials, processing/durability: 6.7–8.7 (0.2–0.4) → 9.7–10.7 lab tests, months (0.85)
- Protein binder design: 4.7–6.7 in silico (0.4) → 8.7–9.7 assay (0.85)
- Small-molecule drugs: 4.7 docking (0.1) → 8.7–9.7 assay (0.6) → ~14.7 Phase 3 (0.95)
- Trading: 4.7–5.7 backtest (0.15) → 9.7–10.7 live (0.9)
- Long-term research direction: 12+ (0.1–0.3)
- Business strategy: 11+ (0.1–0.3)
- Public policy: 6.7–7.7 fiscal microsimulation (0.55) → off chart, behavioural effects (0.3)

## Sources found during the session
- DeepSeek-R1: https://arxiv.org/abs/2501.12948 (5.3M rollouts per a secondary summary; check the Nature supplement)
- RL share of compute: https://arxiv.org/pdf/2504.12501 · https://arxiv.org/pdf/2510.13786 · https://newsletter.semianalysis.com/p/rl-environments-and-rl-for-science
- Pretraining loss predicts post-RL performance: https://huggingface.co/papers/2607.16097.md
- Toby Ord on RL scaling: https://ora.ox.ac.uk/objects/uuid:cc69b4e2-968c-41d6-91d0-a9afbb27b766/files/s1r66j354n
- Mathlib size: https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/2.20million.html · Mizar/AFP: https://arxiv.org/html/2508.21593v2
- AlphaProof 80M autoformalised statements: https://www.natureasia.com/en/info/press-releases/detail/9147
- Epoch GPU price-performance: https://epoch.ai/blog/trends-in-gpu-price-performance
- H100 rental prices 2026: https://tech-insider.org/?p=46019 · https://fourweekmba.com/ai-nvidia-h100-rent-hits-2-88-an-hour-up-44-since-december/
- Forecasting: https://forecastingresearch.substack.com/p/ai-models-have-likely-reached-parity · https://goodjudgment.com/category/good-judgment-inc/page/1 · https://forum.effectivealtruism.org/posts/Spyz3wESZu2eeqhDj/ai-forecasting-in-2026-what-11-analyses-say · https://arxiv.org/abs/2505.17989 · https://arxiv.org/html/2604.18576v2
- Formal Conjectures benchmark: https://arxiv.org/html/2605.13171v1
- Open-model ranking (Kimi K3.1 Pro top, Nov 2026): https://benchlm.ai/best/open-source-llm-comparison · Kimi K3 report: https://www.emergentmind.com/papers/2607.24653
- Harvey / Kimi K3 RL: https://fireworks.ai/research/kimi-k3-on-fireworks-fast-rl-at-frontier-scale
- A-Lab and critique: https://pmc.ncbi.nlm.nih.gov/articles/PMC10700133 · https://par.nsf.gov/servlets/purl/10532478 · https://chemistryworld.com/news/new-analysis-raises-doubts-over-autonomous-labs-materials-discoveries/4018791.article
- SRT-H autonomous surgery: https://arxiv.org/abs/2505.10251
- From memory, needs checking before citing: Narang et al. 2021 (transformer modifications don't transfer); UVA/Padova diabetes simulator accepted by the FDA in place of animal trials; world GDP ≈ $110T; "$1B ≈ a very large RL run".
