# Discussion notes (Claude Code sessions)

Running notes for Oscar to review before writing. Newest first. The earlier claude.ai session is summarised in HANDOFF.md.

---

## Standing principles for placing tasks (agreed 2026-11-22)
1. **Assume harnesses work as intended.** Bugs in a harness or evaluator don't count against fidelity: they're usually easy to fix. Fidelity reflects *structural* gaps between the reward and the goal, such as physics mismatch in sims, proxy vs real outcome, or what a check can't observe even in principle.
2. **Keep the plot as simple as possible while carrying the detail.** Many more tasks are coming, so prefer upright ellipses and only split a task into rungs when the rungs are genuinely different reward sources.
3. **The fidelity scale is defined by behaviour, not method** (adopted 2026-11-22; supersedes the anchors in HANDOFF.md). Fidelity ≈ the probability that an output the fully optimised policy scores highly is actually good.
   - 1.0 **sound**: no false positives possible
   - 0.8 **leaks at the edges**: narrow false positives
   - 0.5 **breaks within a run**: improves the goal, then gets exploited before training ends
   - 0.2 **weakly correlated**: training quickly drifts to what the proxy likes
   - ~0 **contested**: no agreed target

   Any method (LLM judge, unit tests, simulator) can land anywhere on this scale, depending on the domain.

## 2026-11-22: trading and the judgement tasks (discussion, nothing plotted)

### Trading → a paragraph in the limitations section, not a point on the plot
- Oscar's instinct; Claude agrees. P&L is an *exact* reward, but:
  - **Non-stationary and adversarial:** other participants adapt, so any edge decays and the environment keeps changing.
  - **Backtests overfit** (multiple testing).
  - **Live P&L is very noisy:** telling a Sharpe-1 strategy from luck takes years. That's latency, like forecasting.
- In skill-ceiling terms, **the ceiling itself moves**, so fidelity isn't a fixed property of the reward.
- Nuance: short-horizon trading (fast feedback, many samples) fits RL better, and quant firms do use ML heavily. Long-horizon investing doesn't fit.
- **Possible pairing:** forecasting and trading together as "the reward is exact, but slow, scarce and non-stationary". A class of task the dollar axis can't represent.

### Judgement tasks (policy, business strategy, research direction; forecasting adjacent)
**Can we train against AI superforecasters / AI judges?**
- **The ceiling is the judge.** A policy trained against a model forecaster can at best match that forecaster (weak-to-strong problem). Aggregating judges and checking consistency help a little.
- **Consistency checks are a cheap, partly sound signal.** Probabilities should be coherent across negations, conditionals and time. Incoherence is provably wrong, but coherence ≠ accuracy, so fidelity is low.
- **"The past as a simulator"** (retrodiction on resolved questions) works for forecasting (Turtel et al.), but leakage limits it, and for strategy the model already knows how famous cases turned out.

**Can we train against simulated businesses / societies?**
- Examples: LLM-agent societies (e.g. Park et al. 2024, simulating ~1,000 real people's survey answers, from memory) and RL policy design in economic sims (Salesforce "AI Economist", 2020, from memory).
- **The sim encodes its designer's (or model's) assumptions,** and an optimiser exploits its errors. For policy specifically, the *Lucas critique*: people change their behaviour in response to a new policy, which is exactly what a sim calibrated on past behaviour misses.
- Fidelity ~0.1–0.3. Cost: LLM-agent sims with ~1,000 agents × many steps ≈ ~$10–1,000 per rollout → ~$50M–5B per run.

**Real outcomes:** infeasible. Years of latency, n = 1, no counterfactual, and you can't experiment on societies (hatched / off-limits).

**Exception that fits the inverse-value pattern:** the *tactical* end of business strategy (pricing, product changes, marketing) has fast A/B-testable feedback. It's high-fidelity and cheap, which is why tech companies already run bandits and RL there. *Strategic* decisions (enter a market, acquire a company) aren't testable at all.

**Sketch placements (if plotted as a "judgement" domain):**

| Task | Rungs (cost per run; fidelity) |
|---|---|
| Business strategy | LLM judge / case studies (~$1–5M; 0.1–0.25) → simulated markets (~$0.1–5B; 0.15–0.3) → real outcomes (off-limits, years, n = 1) |
| Public policy | Fiscal microsimulation for budget cost only (~$1–50M; ~0.5) → agent-society sims for behaviour (~$0.1–5B; 0.1–0.3) → real outcomes (off-limits) |
| Long-term research direction | Expert/LLM panels (~$0.5–5B; 0.1–0.3), citations as a proxy (cheap; Goodharts badly) → real impact (decades) |

**Claude's view for the post:**
- These are worth plotting precisely *because* they sit at the bottom: the clearest examples of tasks out of reach for direct RL.
- They're where Oscar's transfer question matters most. If they improve, it'll be via better world models, reasoning and forecasting, not via their own rewards.
- **Concrete prediction candidate:** AI forecasters beat the Metaculus Pros by a stated date *without* being trained on real resolutions at scale. That tests "transfer beats direct RL at the bottom of the plot".

## 2026-11-22: materials scope settled
- **Keep only "new compounds"** (ML potential → DFT → autonomous lab). **Processing & durability is dropped** from the plot and the post; the explainer below is kept for reference only.
- The autonomous-lab rung was widened to ~$0.5–10B to match the cost breakdown.
- **Skill-ceiling framing:** Oscar has read and discussed it and will work it into the post text himself. No further action needed here.

## 2026-11-22: what "processing & durability" means (plain-language explainer)
- **The idea:** a material's *recipe* (which atoms) is only half the story. *How you make it* determines its microstructure: grain sizes, which crystal phases form, defects, pores, internal stresses. Microstructure largely decides the properties people pay for: strength, toughness, corrosion resistance, battery lifespan. The same steel can be soft or hard depending only on heat treatment (cooled slowly vs quenched in water).
- **"Simulating manufacturing"** = predicting microstructure from the process steps, then properties from the microstructure. For example:
  - which phases form as an alloy cools (thermodynamic phase diagrams, "CALPHAD")
  - how grains grow during heat treatment ("phase-field" models)
  - the stresses that build up in a part as it cools or is 3D-printed (finite-element models)

  Every link in that chain is approximate, hence low fidelity.
- **What's tested in the lab:** make the material by the real process, then break it slowly.
  - Tensile tests: pull until it snaps.
  - Fatigue: bend back and forth millions of times until it cracks (aircraft parts).
  - Creep: hold under load at high temperature for months (jet-engine turbine blades).
  - Corrosion: weeks in a salt-spray chamber.
  - Battery cycle life: charge and discharge hundreds to thousands of times (an EV battery should keep most of its capacity for ~8+ years).
  - Coatings: wear, abrasion and adhesion.
- **Why it's slow and still a proxy:** failure accumulates over many cycles or long times. Tests are sped up with higher temperatures or faster cycling, but that can change *how* things fail, so even the lab rung is a stand-in for years in the field.
- **Possible simplification for the post:** rename the task "Making materials last" (battery lifetime, metal fatigue) with the ladder *simulation → accelerated lab tests → real-world lifetime*.

## 2026-11-22: materials Q&A (cost breakdown, workflow, better DFT)

### Cost breakdown for "new compounds"
- **a. ML potential (~$5K–500K per run).** Relaxing a 50–200 atom structure takes ~100–1,000 force evaluations at ~1–100 ms each on a GPU, so ~0.1–100 GPU-s, typically ~10 GPU-s. At ~$2.90/GPU-hour that's ~$0.008 per structure (range ~$0.0001–0.08), and × 5M ≈ $40K (range ~$0.5K–400K).
- **b. DFT (~$20–200M per run).** A standard (PBE) relaxation of a ~50-atom cell takes ~100–1,000 core-hours, so ~$4–40 per structure. Higher accuracy multiplies this:
  - hybrid functionals: ×10–100
  - battery- or catalyst-relevant properties (voltages, ion-migration barriers, adsorption energies): ×10–100 again, since each needs many calculations
  - So property-level DFT could reach ~$1–20B per run. Code licences (e.g. VASP) are negligible next to compute.
- **c. Autonomous lab (~$0.5–10B per run; widened from $0.5–5B).** A lab costs ~$2–5M to build, amortised over ~5 years, plus staff and running costs, so ~$1–2M/year. At ~20 synthesis attempts per day (~7K/year; A-Lab's 17-day run suggests that order, but check its recipe count) that's ~$150–300 per attempt, plus precursors (~$10–100s, more for rare elements). Call it ~$100–2,000 per experiment.
  - **Throughput binds first:** 5M experiments ≈ ~700 lab-years.

### Standard workflow for a new material (battery cathode, catalyst)
1. **Define targets:** e.g. for a cathode, capacity, voltage, stability, cost, no cobalt. For a catalyst, activity, selectivity, lifetime.
2. **Generate candidates:** literature, chemical intuition, substituting elements in known compounds, database screening (Materials Project), and now generative models.
3. **Compute and screen:** stability (distance from the convex hull), then property calculations: battery voltage and ion-migration barriers; catalyst adsorption energies as "descriptors" (Sabatier volcano plots).
4. **Synthesise:** solid-state (grind precursors, heat in a furnace), sol-gel, hydrothermal. Many iterations on temperature, time and atmosphere.
5. **Characterise:** XRD (crystal structure / phase), electron microscopy, spectroscopy, composition.
6. **Test properties:** batteries go into coin cells and are cycled for weeks to months; catalysts run in a reactor for hours to months.
7. **Scale up and process:** grams → kilograms → tonnes. Particle size, coatings, electrode formulation, manufacturing yield and cost. Often where candidates die.
8. **Qualify and integrate:** full cells and packs, safety (abuse) tests, years of durability data.

Discovery to market is typically 10–20 years (from memory). Steps 3, 4–6 and 6–8 map onto the rungs: computation (rungs a/b), lab (c), durability (task 2).

### Can AI make DFT more accurate, e.g. by writing better code?
**Yes, by two different routes, and both are a nice cross-domain point: AI improving the *reward* for other AI.**

- **Better physics (moves the DFT rung *up*).**
  - Learned exchange-correlation functionals: DeepMind DM21 (2021, from memory), and Microsoft **Skala** ([arXiv 2506.14665](https://arxiv.org/abs/2506.14665), June 2025). Skala claims chemical accuracy (<1 kcal/mol) on small-molecule atomisation energies and 2.8 kcal/mol on the GMTKN55 benchmark, beating hybrid functionals at roughly semi-local cost. It's a preprint, and I haven't seen independent validation.
  - ML potentials trained on *better-than-DFT* reference data (coupled cluster) could beat DFT at ML-potential cost.
- **Better code (moves the DFT rung *left*).**
  - Major DFT codes are decades-old Fortran, much of it CPU-bound. Porting to GPUs and better algorithms is exactly **kernel optimisation / SWE with an oracle**: the old code is the reference, so equivalence plus timing is a near-sound reward. Those tasks are already *inside* the frontier.
  - Cheaper DFT also buys fidelity indirectly: the same budget affords hybrid functionals or higher-level methods.
- **Limits:**
  - Training a better functional has its own reward problem. Reference data (coupled cluster) exists mainly for small molecules, and experimental data for solids is scarce, so there's a risk of overfitting to benchmarks like GMTKN55.
  - Even perfect DFT only fixes *energies*. The rung's main fidelity gap is synthesisability ("can it be made?"), which needs models trained on lab data.
  - So better DFT might lift rung b from ~0.5–0.65 to ~0.6–0.75, but not to "sound".
- **Possible framing for the post:** *tasks inside the frontier (code optimisation) can be used to move tasks outside it (scientific simulation).* That's a general mechanism by which the frontier expands.

## 2026-11-22: materials science, first pass (materials_preview.png; not on the main plot)

**Framing:** a frontier LLM proposes a material (and its synthesis or processing route) end to end, and is rewarded by simulation, a lab or real-world tests.

| Task | Rung | Reward | Cost per reward | Cost per run | Fidelity |
|---|---|---|---|---|---|
| **New compounds / computable properties** (stable crystals, battery cathodes, catalysts) | a | Universal ML interatomic potential (MACE/Orb class): relax and score the structure, ~1–100 GPU-s | ~$0.001–0.1 | **~$5K–500K** | **0.30–0.50** |
| | b | DFT check: ~100–1,000 core-hours per relaxation | ~$4–40 | **~$20–200M** | **0.50–0.65** |
| | c | Autonomous lab: robot synthesis + automated characterisation (XRD). Precursors, hours of robot time, amortised equipment | ~$100–1,000 | **~$0.5–5B** | **0.70–0.85** |
| **Processing & durability** (alloys, coatings, battery lifetime) | a | Process simulation (CALPHAD, phase-field, finite-element) | ~$0.01–1 | **~$50K–5M** | **0.20–0.40** |
| | b | Accelerated lab tests (fatigue, corrosion, battery cycling), taking months | ~$1–50K | **~$5–250B** | **0.80–0.90** |
| | → | Real field lifetime: years. Off the chart | | | |

**Why these heights (structural gaps only, per principle 1):**
- **ML potential, 0.3–0.5.** Typical errors are small (energy-above-hull error under ~30 meV/atom on Matbench Discovery, [arXiv 2604.21850](https://arxiv.org/pdf/2604.21850)). But an optimiser *searches for* structures where the potential is wrong, i.e. outside its training distribution, and finds spurious stability. That's the definition of "breaks within a run".
- **DFT, 0.5–0.65.** Being stable in DFT is necessary but far from sufficient. It says nothing about whether the material can be *made* (GNoME predicted ~380K stable materials; reportedly only ~736 had been made independently, a figure from a blog, so check it). Standard functionals also get some properties systematically wrong (e.g. band gaps).
- **Autonomous lab, 0.7–0.85.** It is real synthesis, but automated characterisation is the weak link. A-Lab claimed 41 novel compounds in 17 days; reanalysis (Palgrave et al.) argued most weren't new, and **Nature issued a correction in Jan 2026** walking back the novelty claims while leaving the method standing (secondary sources, so check). Misreading XRD for disordered phases is a structural limit, not just a bug.
- **Process simulation, 0.2–0.4.** Microstructure and defects drive real performance, and simulations capture them poorly.
- **Lab durability tests, 0.8–0.9.** These are close to the real goal, but accelerated tests are themselves proxies for years in the field.

**Claude's reading:**
1. **Materials is fidelity-limited, not cost-limited, at the cheap end.** The ML-potential rung costs about the same as SWE but sits at ~0.4. That's the opposite of chips, where the cheap rung is already high-fidelity.
2. **The real constraint on the lab rung is throughput and latency, not dollars.** A-Lab made ~41 compounds in 17 days, so 5M experiments would take thousands of lab-years. Like forecasting, "you can parallelise dollars but not wall-clock time"; here you can only parallelise by building more labs. That's the bet of **Periodic Labs** (~$300M seed; argues autonomous labs, not compute, are the bottleneck) and Lila Sciences.
3. **Opportunity for the domain section:** better *automated characterisation* (the A-Lab weak point) would raise the lab rung's fidelity, and cheaper, faster autonomous labs would move it left. Both are investable.
4. **GNoME is the cautionary tale:** a huge output at the cheap rung (2.2M candidates), with value bottlenecked at the expensive one. It's "a ranked hypothesis space, not a catalogue of materials".

**Sources:** [Periodic Labs funding](https://www.implicator.ai/periodic-labs-raises-300-million-to-automate-science/); [GNoME dispute overview](https://absolutedigitalpublishers.com/articles/materials-discovery-is-becoming-a-breeding-program); [uMLIP cost/accuracy](https://arxiv.org/pdf/2502.03578); [Orb speed claims](https://arxiv.org/pdf/2504.06231). Mostly secondary, so check the primary papers before citing.

## 2026-11-22: exploit finding added (defence deliberately left out)
- **Plotted:** ~$100K–1M, fidelity 0.85–0.95, in the software & computing domain.
- **Why high:** the reward is an existence proof. A flag, a sanitizer crash or a working PoC means the bug exists, so false positives are near impossible.
- **Gaps below 1.0:**
  - crash ≠ exploitable, and rating severity takes judgement
  - CTFs are designed puzzles (real targets are better and just as sound)
  - rediscovering known bugs earns reward without adding value
- **Signals, from memory (check):** Google Big Sleep found a real SQLite vulnerability (2024); DARPA AIxCC finals (2025); XBOW topped HackerOne's US leaderboard (2025).
- **Asymmetry for the post (limitations or predictions):** offence yields proofs that a bug *exists* (verifiable); defence needs proof of *absence* (unverifiable beyond "this known exploit no longer works", ~0.5). On this framework RL should improve attack faster than defence. Oscar chose not to plot defence.

## Framing: how the frontier moves (Oscar, 2026-11-22)
The post's question is *"given RL drives performance, what comes next?"* The frontier moves in these ways:
1. **Fidelity up:** low-fidelity rewards become higher fidelity. Driven by better models (LLM judges), and also by better simulators and verification tools (e.g. AI-written DFT codes and learned functionals).
2. **Cost down:** high-cost rewards become cheaper. Driven by better hardware and compute build-out, which in this framing includes automated labs, experimentation infrastructure and cheaper tools (e.g. EDA licences).
3. **Budget up:** the frontier's cost edge moves right as AI companies get richer and can spend more per run.
4. ~~*(Claude's addition)* **The fidelity bar comes down.**~~ **Mostly withdrawn after discussion.**
   - Oscar's correction: judge ensembles and adversarially trained judges (Master-RM) *raise the reward's fidelity*. That's mover 1, not a lower bar.
   - What's left is regularisation and early stopping (KL penalties, stopping before over-optimisation). These don't change the reward; they let you get *closer to its ceiling* instead of overshooting (see below). It's a second-order effect, probably not worth its own mover.

### How the skill ceiling could fit into the framework (Claude's proposal; schematic in `skill_ceiling.png`)
1. **Definition in the post:** "fidelity is how much real skill you can buy by optimising against a reward". The "probability a top-scored output is good" stays as the operational test for placing tasks.
2. **An explainer figure in the methodology section** (left panel of `skill_ceiling.png`): real skill vs optimisation pressure for each anchor, with a "today's model skill" line. Schematic shapes, based on Gao et al.'s over-optimisation curves.
3. **Ladders become "ceiling stacking"** (right panel): train on the cheap rung until it saturates, then switch to the expensive rung for the last stretch. That explains why a mostly-cheap ladder is worth having even when the top rung is unaffordable at 5M rollouts (only a small fraction of training needs to happen there), and it's how RLHF-style pipelines already work.
4. **The frontier's fidelity edge gets a meaning:** "rewards whose ceiling is above today's model skill". That edge *rises* as models improve, a counter-force to mover 1 ("fidelity up"). The 0.6 line on the plot is then a snapshot for Nov 2026.
5. **Transfer fits naturally:** capability from other training (reasoning, search) can lift a model *above* a task's own reward ceiling (forecasting; research memos on the Vals benchmark). At that point the task's low-fidelity reward can't teach more and may even pull skill down.

### Fidelity as a skill ceiling (Oscar's idea, 2026-11-22; not yet adopted)
- **Proposed reading of the y axis:** fidelity sets the *maximum real-task skill you can reach by optimising against this reward*.
  - **1.0:** no ceiling except what the task or environment itself imposes.
  - **0:** optimising doesn't improve real skill at all.
  - **In between:** real skill improves, then saturates, and with continued optimisation degrades (overfitting / Goodhart).
- **Evidence it's the right shape:** Gao et al. 2022 (reward-model over-optimisation, from memory). True ("gold") reward rises then falls as you optimise against a proxy, and the *height of the peak* grows with proxy quality. That is literally a fidelity → ceiling curve.
- **It lines up with the adopted anchors:**
  - sound = no ceiling
  - leaks at the edges = high ceiling, reached late
  - breaks within a run = ceiling reached inside one RL run
  - weakly correlated = low ceiling, reached fast
  - contested = no improvement

  The "probability a top-scored output is good" definition can stay as the *operational test*, with the ceiling as the *intuition* in the post.
- **A consequence worth considering (Claude):** a ceiling is only useful if it sits *above* the model's current skill. As models improve, a fixed-fidelity reward can stop teaching anything: a judge weaker than the policy can't push it further (weak-to-strong). So the fidelity a task *needs* may *rise* over time, a moving bar in the opposite direction. This also means fidelity isn't purely a property of the reward; it partly depends on how capable the policy already is. Probably a limitations-section point.

## Post structure (Oscar, 2026-11-22; supersedes HANDOFF.md's outline)
1. **Intro:** RL drives progress; pretraining is necessary but not sufficient. Given this, what might AI disrupt next?
2. **Methodology:** assumptions, crediting Claude, defining and justifying the two axes.
3. **Headline overview plot**, with some explanation. (Overview design is parked: cheapest rung vs best rung under $1B.)
4. **Domains:** a domain-specific plot plus the opportunities in each domain.
5. **Limitations.**
6. **Concrete predictions** for the record.
7. **Appendix:** justification table with references (Claude's words). Built from `cost-appendix.md` plus the fidelity reasoning in these notes.

**Working domain grouping (Claude's proposal):**
- games & maths
- software & computing (SWE, kernels, computer use, security, pretraining research)
- chips
- robotics & driving
- law
- life sciences (drugs, proteins, surgery)
- materials
- finance
- judgement (novel, strategy, policy, research direction)

## Running list: opportunities for the post (domain sections)
- **EDA licences in digital chip signoff (agreed, keep).** The expensive digital rung costs ~4–10× more in licences than in compute: ~$1.5–40M per run, against ~$0.4–4M for the compute alone. This is a disruption opportunity: cheaper or open tools of signoff quality would move the rung left. The hard part is the silicon-correlation data and foundry certification, not the code. See the chip design Q&A below.

## 2026-11-22: redefining the fidelity scale by property, not method (proposal)
**Current anchors** (from HANDOFF.md):
- 1.0 sound by construction (Lean, game rules)
- 0.8 strong but hackable (unit tests)
- 0.5 a proxy that breaks under pressure (LLM judge, docking, backtests)
- 0.2 a weak proxy
- ~0 a contested target

**Oscar's objection:** tying anchors to *methods* is wrong, because an LLM judge can be much better or worse depending on the domain (the same goes for unit tests and simulators).

**Proposed operational definition:** fidelity ≈ *the probability that an output the fully optimised policy scores highly is actually good*. That's the precision of the reward at the top, measured after optimisation. It matches the original framing (false positives matter; false negatives mostly waste signal) and says nothing about method.

**Proposed anchors, described by behaviour under optimisation:**
- **1.0, sound:** no false positives are possible. Maximising the reward *is* achieving the goal.
- **0.8, locally leaky:** false positives exist but are narrow (untested edge cases, gaps in coverage). Optimising mostly improves the goal.
- **0.5, Goodharts within a run:** the goal improves at first, then the policy finds and exploits the proxy's gaps before training ends.
- **0.2, weakly correlated:** the reward tracks the goal on typical outputs, but optimisation quickly moves to what the proxy likes and the goal doesn't.
- **~0, contested:** no agreed target to be faithful to.

Methods then become *examples that can land anywhere*:
- an LLM judge checking whether two maths answers are equivalent: ~0.9
- a rubric judge on legal memos: ~0.5
- an LLM judge of literary greatness: ~0.2
- likewise unit tests (~0.6 for a thin suite, ~0.9 with an oracle) and simulators (locomotion ~0.8, manipulation ~0.4).

## 2026-11-22: how good are LLM judges under optimisation pressure?
Oscar's challenge: the LLM-judge fidelities look high. What's the evidence?

**Evidence that judges agree with humans, at evaluation time (no optimiser pushing):**
- MT-Bench (Zheng et al. 2023): GPT-4 agreed with human preferences ~80% of the time, about the same as humans agree with each other (from memory). This says nothing about robustness *under optimisation*, which is what the y axis measures.

**Evidence that judges break under optimisation pressure:**
- **Reward-model over-optimisation** (Gao et al. 2022, from memory): as a policy optimises harder against a learned reward model, the true ("gold") reward first rises, then falls. The proxy keeps going up. This is the structural version of the problem, and it applies to any learned judge.
- **Length and style hacking in RLHF** (e.g. Singhal et al. 2023, from memory): much of the measured RLHF gain came from longer answers.
- **"Master keys"** ([One Token to Fool LLM-as-a-Judge](https://arxiv.org/abs/2507.08794), NeurIPS 2025): a reply of just ":" or "Thought process:" earned false-positive rewards. GPT-4o was fooled up to 35% of the time; some open 70B models 60–90%. o1 and Claude 4 were also affected. Adversarial training (their Master-RM) cut this to ~0%. So *specific* exploits are patchable (principle 1 calls them bugs). The general divergence above isn't.
- **Rubric judges check presence, not quality** (Thomson Reuters, Aug 2026): a policy can learn to tick every criterion while making errors an attorney would catch.

**Conclusion (Claude):**
- The evidence for judges being robust *under pressure* is weak, and the evidence against is strong. The scale's own anchor puts "LLM judge" at 0.5, "a proxy that breaks under pressure".
- Rubric judges with concrete, checkable criteria deserve a bit more than holistic ones, and citation checks are close to sound for the narrow question of hallucinated citations.
- But **0.55–0.70 for the law rubric rungs is generous**. Proposed:
  - research memos (rubric + citation check): **0.45–0.60**
  - drafting (rubric/playbook): **0.40–0.55**
  - The novel's LLM judge (0.14–0.30) is already low, because its target is contested. The computer-use ellipse is mostly scripted checks and unaffected.
- Not yet applied.

---

## 2026-11-22: law, first-pass ellipses (not yet plotted)

### Evidence
- **Harvey + Fireworks RL on Kimi K3** ([case study](https://fireworks.ai/blog/post-training-kimi-k3-with-harvey-for-long-horizon-legal-work), Aug 2026):
  - The task set is the Legal Agent Benchmark: agents produce "memos, marked-up contracts, diligence summaries".
  - **Reward: an LLM judge grades each deliverable "against dozens of concrete criteria"**, i.e. a rubric. Lawyer authorship of the rubrics isn't described.
  - "Tens of thousands of long-horizon rollouts per checkpoint".
  - Cost: "Harvey Tenet runs at $5.92 per LAB task against $5.62 for base Kimi K3". **That's the cost of running the model on a task (policy generation, perhaps plus grading). It is not a reward cost**, and the page doesn't break it down. *(Corrected: an earlier version of these notes wrongly called it an evaluation cost and used it as the top of the judge-cost range.)*
  - Results: 19.7% all-pass on the benchmark vs 10.8% for base Kimi K3. Mercor Apex Corporate Law 58.8% → 74.0%; Redline Bench 49.3% → 55.5%.
  - A full training write-up is promised. Harvey's own posts: [post-training update](https://www.harvey.ai/blog/post-training-update-harvey-tenet), [Legal Agent Benchmark](https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark) (not yet read).
- **Vals legal AI reports:**
  - [Feb 2025](https://www.vals.ai/industry-reports/vlair-2-27-25): AI beat a lawyer control group on easy tasks (document Q&A, extraction) but not on complex reasoning.
  - [Oct 2025 legal research](https://www.vals.ai/industry-reports/vlair-10-14-25): AI tools averaged **80% vs lawyers' 71%** on 200 research questions. Humans kept an edge on multi-jurisdictional synthesis and judgement.
  - Drafting wasn't covered.
- **Thomson Reuters (Aug 2026):** benchmark scoring that checks whether required points are *present* misses failures a practising attorney would catch ([post](https://www.thomsonreuters.com/en-us/posts/innovation/when-legal-ai-is-evaluated-like-legal-work-the-results-change/)). This is a structural limit on rubric rewards.
- **Reviewer disagreement in document review:**
  - TREC Legal Track appeals reversed ~79–91% of appealed first-pass relevance calls ([TREC 2010 overview](https://trec.nist.gov/pubs/trec19/papers/LEGAL10.OVERVIEW.pdf)).
  - A 2025 study found overlap between reviewers of only ~0.28–0.42 (Jaccard) in a real production ([arXiv](https://arxiv.org/html/2502.20937v2)).
  - The "true" label is itself a contested judgement. That's structural, so it counts.

### First-pass ellipses

| Task | Rung | Reward | Cost per run | Fidelity |
|---|---|---|---|---|
| **Document review / diligence** | — | Compare against adjudicated labels. Comparison is ~free; labelling is amortised (~$2–5 per label at ~$50/hour, reused across rollouts). | **~$5K–300K** | **0.60–0.80** (lowered from the handoff's 0.75–0.85 because of reviewer disagreement) |
| **Research memos** | a | Rubric LLM judge + automated citation check (Harvey-style) | **~$0.5–5M** (≈$0.1–1 per memo: a judge reads a ~10–100K-token deliverable plus sources against dozens of criteria) | **0.55–0.70** |
| | b | Lawyer grading, 30–90 min at ~$150–500/hour | **~$0.4–4B** | **0.70–0.80** (experts disagree too) |
| **Drafting / contract mark-up** | a | Rubric or playbook LLM judge | **~$0.5–5M** | **0.50–0.65** |
| | b | Partner review, ~1–2 hours at partner rates | **~$5–20B** | **0.65–0.75** |
| | → | The true test (does the contract hold up in a dispute years later) can't be observed: arrow off the chart, like the novel | | |
| **Litigation** | a | Predict rulings from historical dockets | **~$50K–500K** | **0.30–0.45** (predicting ≠ winning; facts outside the record; temporal leakage) |
| | b | Mock trial / moot court with expert judges | **~$5–50B** | **0.50–0.60** |
| | c | Real rulings: hatched, because you can't run experiments on real cases; years of latency | off chart | ~0.7 |
| **Negotiation** *(optional)* | — | Self-play against LLM counterparties | **~$0.5–10M** | **0.30–0.50** (exploits of the counterparty model are structural) |

**Suggested simplifications:**
- Drop *strategic counsel*: it overlaps with business strategy, which will be plotted anyway.
- Negotiation is optional. It is spread across law, procurement and sales, so it might be better as a general "negotiation" task later.

### Claude's reading
1. **Document review is inside the frontier**, consistent with AI beating lawyers on easy tasks (Vals 2025). Its fidelity ceiling is set by humans disagreeing about the labels, not by the checker.
2. **The rubric-judge rung for memos and drafting sits right at the frontier's corner** (~$5M, ~0.6). That's exactly where Harvey is training now. The step up to lawyer grading is a ~100–1,000× cost jump for only ~+0.1–0.15 fidelity, which is a strong illustration of the "ladder" idea.
3. **Value runs the other way from fidelity:** document review is the cheapest-billed work, and litigation and counsel the most expensive. It's the clearest single example of the inverse billing-rate pattern.
4. Research memos are close to "fallen" on the expert-graded *benchmark* (Vals: AI 80% vs lawyers 71%), even though training at that rung would be unaffordable. That's evidence for capability arriving by **transfer from the cheap rung**, the same caveat as forecasting.

---

## 2026-11-22: remaining tasks, economic value and pay (first pass)
**Dropped:** "Math/science with checkable answers". It overlaps too much with Math (Lean).

Pay is US. ✓ = confirmed from a BLS page or Gartner during this session; everything else is from memory and needs checking. The wage bill (employment × median) is a rough proxy for how much of the economy a task touches, not the value of automating it.

| Task | Who does it today | Typical US pay | Size of the prize (rough) |
|---|---|---|---|
| Law (all tasks below) | Lawyers: ~864K jobs ✓, median **$159,670** (May 2025) ✓ | Big-law associates start ~$225K; partners $1M+ | US lawyer wage bill ≈ **$140B**/yr; global legal services ~$1T |
| · document review | Contract reviewers, paralegals (median ~$60K) | Contract reviewers ~$30–60/hour | eDiscovery/review ~$15–20B/yr (global) |
| · drafting, research memos | Associates and partners | $225K → $1M+ | The bulk of transactional and advisory fees |
| · litigation, strategic counsel | Senior partners, trial lawyers | Billing $1,000–2,500/hour | High value per hour, small share of hours |
| · negotiation | Lawyers, plus procurement and sales generally | Purchasing managers ~$140K | Spread across the whole economy |
| Surgery | Surgeons | BLS median **≥$239,200** ✓ (top-coded); surveys ~$400–550K | US surgeon pay ~$30–60B/yr; procedure spending is far larger |
| Small-molecule drugs + protein binders | Medicinal chemists, biochemists, protein engineers | ~$100–150K (biochemists ~$104K, year unclear) | Pharma R&D ~$250–300B/yr globally; biopharma sales ~$1.5T/yr |
| Materials (both) | Materials scientists ~8.7K jobs ✓, median **$104,160** ✓ (2024); chemists and materials engineers more broadly | ~$95–110K | Tiny labour pool (~$1B US wages) but huge leverage: batteries, semiconductors, a ~$5T chemicals industry |
| Security / CTF | Information security analysts, ~180K jobs | Median ~$125K; elite exploit researchers far more | Security spending **$213B** in 2025 ✓ ([Gartner](https://www.gartner.com/en/newsroom/press-releases/2025-07-29-gartner-forecasts-worldwide-end-user-spending-on-information-security-to-total-213-billion-us-dollars-in-2025)) |
| Trading | Financial analysts 429K jobs ✓, median **$101,910** ✓; quant traders and researchers a small elite | Quant traders ~$200K–$1M+ | Trading revenues in the hundreds of $B/yr, but partly zero-sum |
| Public policy | Economists ~17.6K jobs ✓, median **$115,440** ✓; budget and policy analysts | ~$85–120K | Small labour pool steering government spending of ~35–40% of GDP |
| Business strategy | Executives (median ~$206K), management analysts ~1M jobs, median **$101,190** ✓ | Strategy consultants ~$200K+ after an MBA; CEOs far more | Consulting ~$300B/yr globally; leverage on all of corporate capital allocation |
| Long-term research direction | Senior scientists, research leads, PIs | Computer/information research scientists ~$145K; frontier-AI researchers $1M+ | Global R&D spending ~$2.5–3T/yr |

**Rough ranking by size of prize:**
1. Research direction, business strategy and public policy: trillions in leverage, but the fidelity of any reward is near zero.
2. Law: ~$1T.
3. Drug discovery: ~$250–300B R&D, and a successful drug is worth billions.
4. Trading and cybersecurity: ~$200B each.
5. Surgery.
6. Materials: small labour market, huge downstream leverage.

**Pattern worth considering for the post:** pay and economic value pile up in the low-fidelity, expensive corner of the plot. The handoff's law point generalises: *verifiability runs inversely to billing rate*. Document review (~$30–60/hour) is verifiable; partner judgement ($1,000+/hour) isn't. A side chart of fidelity against pay might make this point compactly.

**Sources confirmed this session:** BLS [lawyers](https://www.bls.gov/ooh/legal/lawyers.htm), [chemists and materials scientists](https://www.bls.gov/ooh/life-physical-and-social-science/chemists-and-materials-scientists.htm), [economists](https://www.bls.gov/ooh/life-physical-and-social-science/economists.htm), [highest-paying occupations](https://www.bls.gov/ooh/highest-paying.htm), [business and financial occupations](https://www.bls.gov/ooh/business-and-financial/). Everything else needs checking.

- **Materials: AI-built simulators.** Faster DFT codes (GPU ports: a kernel-optimisation/SWE-with-oracle task, already inside the frontier) and learned functionals (Microsoft Skala) move the DFT rung left and up. This is a general mechanism: tasks inside the frontier improve the rewards for tasks outside it.
- **Materials: autonomous labs and automated characterisation.** Throughput (lab-years) and XRD interpretation bind the lab rung, not dollars.

## 2026-11-22: chip ladders accepted
Oscar is happy with the digital (RTL + open synth → signoff) and analog (SPICE → post-layout → silicon) ladders as plotted.

## 2026-11-22: chip design Q&A (signoff, analog uses, EDA licences)

### What "signoff" means
The final battery of checks a design must pass before it's sent to the foundry ("tape-out"). Each is run with a specific, foundry-approved tool:
- **Static timing analysis:** does every signal path meet the clock across all process/voltage/temperature corners? (Synopsys PrimeTime, Cadence Tempus)
- **Parasitic extraction:** compute the resistance and capacitance of the actual wires, which feed timing and power. (StarRC, Quantus)
- **Power, IR-drop and electromigration analysis:** does the power grid deliver enough current without voltage sag, and without wires wearing out over years? (Ansys RedHawk, now Synopsys; Cadence Voltus)
- **Physical verification:** DRC (does the layout obey the foundry's thousands of geometric rules?) and LVS (does the layout match the circuit netlist?). (Siemens Calibre, the de facto standard)
- **Formal equivalence:** is the final gate-level netlist logically identical to the RTL? (Synopsys Formality, Cadence Conformal)

The tools are "signoff-quality" because their numbers have been **correlated against real silicon over many tape-outs** and **certified by the foundry for that process node**. Foundries specify which tools customers must use for tape-out (SemiAnalysis).

### Digital vs analog: what each is for
- **Digital:** anything that computes on 0s and 1s, e.g. CPUs, GPUs and AI accelerators, plus the controllers, network switches and logic inside most chips.
- **Analog/mixed-signal:** anywhere a chip meets the continuous physical world, or has to move signals very fast:
  - power management (voltage regulators, PMICs, battery chargers)
  - data converters (ADCs/DACs for sensors, audio, cameras, radios)
  - RF transceivers (Wi-Fi, 5G, Bluetooth, radar)
  - clocking (PLLs)
  - **high-speed I/O / SerDes:** PCIe, Ethernet, NVLink-style links, HBM interfaces
  - sensors and their interfaces
- **Even an AI accelerator is part-analog.** Its SerDes, memory PHYs, PLLs and voltage regulation are analog blocks, often bought as IP. The interconnect bottleneck in AI clusters is partly an analog-design bottleneck.
- Analog is a small fraction of the area but takes long design cycles, is largely done by hand by scarce experts, and is much less automated than digital.

### The licence cost cliff: references
- AWS: EDA licence cost in silicon organisations is "often 5–10× IT infrastructure cost" ([AWS, cut time to results](https://aws.amazon.com/blogs/industries/cut-time-to-results/)). A second AWS post says licences usually cost a few times the compute, **4× in Intel's case** ([AWS, economics of EDA](https://aws.amazon.com/blogs/industries/economics-of-eda-on-aws-license-cost-optimization)). Synopsys and HPE also say licence cost "typically outweighs" compute ([Synopsys blog](https://www.synopsys.com/blogs/chip-design/3x-verification-performance-hpe-greenlake-flex-synopsys-flexeda.html)). **Caveats:** these are cloud vendors with a stake in the argument, and the quotes come from search snippets because the AWS page bodies didn't load for Claude. Oscar should open and confirm the quotes before citing.
- SemiAnalysis [EDA market primer](https://newsletter.semianalysis.com/p/eda-market-primer) (May 2026):
  - Pricing is "opaque by design" and vendors don't publish price lists.
  - Fabless designers spend "$80–150K per engineer annually on tools, IP, and verification".
  - The market is ~$18B (2025); the big three hold >85% (Synopsys ~$8B including Ansys, Cadence ~$5.3B, Siemens EDA ~$2.2–2.5B).
  - Licensing is by seats, tokens, enterprise licence agreements, and increasingly cloud metering per compute-hour.
  - Switching is hard: change your synthesis tool and you must re-run place-and-route, signoff and physical verification.

### The disruption angle (Claude's reading, for Oscar to judge)
- The argument for disruption: the software is expensive to license, not to run, and software is getting cheap to write. Open-source flows already exist (OpenROAD, Yosys, Magic/KLayout, ngspice), and OpenAI is training "GPT-Synopsys".
- The argument against, which ties straight back to the plot: **what a signoff tool sells is reward fidelity.** Its value is that its timing, power and DRC numbers match real silicon at a given node, and that the foundry certifies this. That correlation is earned through many tape-outs and needs the foundry's confidential process data (PDKs and rule decks). Cheap code doesn't recreate it. It's the same structural point as sim-to-real: writing a physics engine is easy; calibrating it against reality is the hard part.
- So the realistic disruption may be:
  - **(a) the cheap rung gets good enough to do most of the search**, with signoff only at the end. That's the plot's ladder: train on the cheap rung, certify on the expensive one. It's already what OpenAI describes.
  - **(b) Someone with foundry access** (a foundry itself, or a hyperscaler designing its own chips) builds certified tools.
  - **(c) EDA vendors** (Synopsys + OpenAI) capture the value themselves.
- Possible line for the "opportunities" section: *the expensive rung in chip design is not a lab or a fleet but a software licence, which might be the cheapest rung in the whole plot to disrupt, if the silicon-correlation data can be got at.*

---

## 2026-11-22: chip design, first-pass ellipses (not yet plotted)

**Framing (Oscar):** the case of interest is *end-to-end task completion by a frontier LLM*, the most bitter-lessoned version: spec in → block out, with the LLM driving the EDA tools and iterating on their feedback. Narrow optimisers like AlphaChip (RL for macro placement, used on TPUs) are background, not the plotted task.

**Evidence that this is happening now**
- OpenAI, [Advancing chip design with our models](https://openai.com/index/advancing-chip-design-with-our-models/) (18 Nov 2026):
  - Models rewrote SystemVerilog for Jalapeño blocks and for AMD GPU IP, using **Synopsys tools to verify equivalence and evaluate synthesis trade-offs**.
  - Results: ~15% standard-cell area on individual multiplier/adder redesigns; ~13% (vector unit) and ~10% (matrix unit) across Jalapeño (a team estimate); up to 14% PPA on AMD GPU IP; "roughly a year of progress in under 5 months".
  - Their RISC-V evals score designs with simulation pass/fail, then IPC × a Yosys-estimated fmax, capped at 16× area. That's exactly the "rung 1" reward below.
  - Partnering with Synopsys to train "GPT-Synopsys" to use EDA tools. No reward or RL details given.
  - Floorplanning, place-and-route and analog are not mentioned.
- Jalapeño went from design to tape-out in 9 months ([OpenAI/Broadcom](https://openai.com/index/openai-broadcom-jalapeno-inference-chip/)).
- Academic RL on Verilog: [CodeV-R1](https://arxiv.org/abs/2505.24183) (NeurIPS 2025). A 7B model RL-trained against an auto-generated testbench that checks equivalence with a golden reference beats DeepSeek-R1 on RTLLM. Its whole training used ~2.7K A100-hours.
- Analog: LLM agents with SPICE in the loop ([AnaFlow](https://arxiv.org/abs/2511.03697), [EEsizer](https://arxiv.org/abs/2509.25510), [AaLLM](https://arxiv.org/pdf/2608.13472) from topology to sizing). These are mostly prompting/agent loops, not RL training.

**First-pass ellipses**

| Rung | Reward | Cost per reward | Cost per run (×5M) | Fidelity | Lands |
|---|---|---|---|---|---|
| Digital 1: functional + open-source synth | Simulation/equivalence against a reference, plus Yosys area/fmax estimate. Minutes of CPU. | ~$0.001–0.1 | **~$3K–300K** (centre ~$30K) | **0.70–0.85** | Inside the frontier |
| Digital 2: signoff flow | Commercial synthesis + place-and-route + static timing/power analysis. ~2–20 CPU-hours per block; **licences cost ~4–10× the compute**. | ~$0.3–8 | **~$1.5M–40M** (centre ~$8M) | **0.85–0.95** | Just right of the frontier, near "real robot" |
| Analog 1: SPICE with corners + Monte Carlo | 100s–10,000s of sims per design, plus a simulator licence | ~$10⁻⁴–1 | **~$500–5M** (centre ~$50K) | **0.50–0.75** | On the fidelity edge of the frontier |
| Analog 2: post-layout extraction + EM | Needs a layout (automated analog layout is immature); hours of CPU plus licences | ~$0.2–10 | **~$1M–50M** | **0.85–0.92** | Right of the frontier |
| Analog 3: silicon (MPW shuttle) | ~$5K–100K per design at mature nodes; months of latency | ~$5K–100K | **~$25B–500B** | **~0.95** | Far right |

**Why these heights**
- **Digital 1 at 0.70–0.85.** Equivalence against a reference is sound for correctness (the OpenAI rewrite case). For "write to spec" it falls back to testbench coverage, like SWE. The synthesis estimate gets area roughly right but timing only roughly, because wires aren't modelled before place-and-route. That is a structural gap, so it counts under principle 1.
- **Digital 2 at ~0.9.** Signoff analysis is what companies trust before tape-out, so it is close to the real goal. I've left out a silicon rung for digital for simplicity: for digital logic, silicon rarely contradicts signoff on PPA.
  - Respins are mostly functional bugs, i.e. verification coverage. From memory: Wilson Research reports first-silicon success has fallen to roughly 1 in 7 recently. **Check before citing.** If it holds, it's a strong illustration that functional tests are a leaky reward even with huge investment.
- **Analog 1 lower than the handoff's 0.75–0.9.** Pre-layout SPICE misses layout parasitics. That's structural, so it counts. It matters modestly for low-frequency analog and a lot for RF and high-speed. Model accuracy at process corners adds more gap.
- **Analog needs a silicon rung; digital doesn't.** Analog engineers trust post-layout sims less than digital engineers trust signoff.

**Takeaways for the post (Claude's reading)**
1. **Digital end-to-end is inside the frontier on the cheap rung**, which matches OpenAI's and AMD's results being real and recent. The gains came on arithmetic blocks where equivalence checking gives a sound correctness signal and synthesis area is a good proxy.
2. **The step to signoff is a cost cliff driven by licences, not compute.** This is a good "opportunities" item: cheaper or open signoff-quality tools (or vendor partnerships, like GPT-Synopsys) would move the expensive rung left. It's also a case where the cost axis depends on *who* is training: an EDA vendor pays no licence fees.
3. **Analog sits at the frontier's fidelity edge**, and the handoff's point still holds: the bigger bottleneck is access (foundry PDKs under NDA, proprietary designs, closed simulators), which the plot doesn't show.

**To check:** EDA licence economics (now referenced in the Q&A section above); Yosys runtimes for block-level designs; MPW shuttle prices; the Wilson Research first-silicon figure.

---

## 2026-11-22: shortlist of unplotted tasks near the frontier (first pass, not yet discussed)
The frontier runs at roughly fidelity > 0.6 and cost < ~$1.5M per run. Per-reward cost is ×5M to get the cost per run (so $0.01 per reward → $50K per run). All numbers are rough.

| Task | Reward source | Cost per run | Fidelity | Where it lands | The interesting question |
|---|---|---|---|---|---|
| Math/science with checkable answers | Match the final answer (string or SymPy; sometimes an LLM checks equivalence) | ~$50–500 | 0.70–0.85 | Well inside | This is the R1 domain itself, so arguably the plot's anchor. Fidelity < 1 because a right answer can come with wrong reasoning, and multiple choice can be guessed. |
| Law: document review / diligence | Compare against human labels (relevant, privileged, risky clause) | ~$500–50K | 0.75–0.85 | Inside | The labels are human judgements with inter-annotator disagreement. Harvey is RL-training on legal tasks. |
| Law: drafting agreements | LLM judge checks against a firm's playbook → partner review | ~$500K → ~$5–15B | 0.6 → 0.65 | On the corner → far right | The true test (does the contract hold up in a dispute years later) can't be observed. |
| Digital chip design (RTL) *(new)* | Testbench simulation + formal equivalence → synthesis/place-and-route for power, performance and area | ~$5K–50K → ~$0.5–25M | ~0.9 (functional) / ~0.7 (PPA) | Inside → straddles | Commercial EDA licences may dominate the cost (rough, check). Open-source tools (Yosys, OpenROAD) are cheaper but lower fidelity. |
| Analog/RF circuits | SPICE + manufacturing-variation sweeps → post-layout/EM sim → silicon | ~$50K–5M → … → ~$50–500B | 0.75–0.9 → 0.95 | Straddles the cost edge, high fidelity | **Near the frontier but hasn't fallen.** The handoff says the bottleneck is data access (proprietary designs, NDA'd process design kits, closed tools), not verification. A clear case of a gap in the method. |
| Materials: computable properties | ML interatomic potential (~1 GPU-s) → DFT (~100–1000 core-hours) → automated lab | ~$5K → ~$20–200M → … | ~0.5 → ~0.7 → 0.75 | Cheap rung near the frontier, then right | The optimiser finds structures where the ML potential is wrong. This is a *structural* reward hack (out-of-distribution), not a bug, so it counts against fidelity. |
| Cybersecurity CTF / exploit finding *(new)* | Capture the flag, or a sanitizer-detected crash | ~$100K–1M (VM per episode, like computer use) | ~0.85 for the task itself | Inside, near the cost edge | The check is sound for the CTF itself, but CTF challenges are an imperfect stand-in for finding real vulnerabilities. |

---

## 2026-11-22: SWE extended, earlier proposals revisited
- **Software eng. now spans 0.65–0.90 fidelity.** The top end covers SWE tasks with an *oracle*: reverse-engineering an existing program (match its behaviour), or visual feedback where a target image or reference render is the check. Oscar suspects many of Fable's one-shot JavaScript painting results come from this kind of training.
- **Proposals from the section below, revisited under the principles above:**
  - *Extend kernel optimisation down:* **dropped.** The Sakana case was a harness bug (reusing results, skipping accuracy checks), which principle 1 excludes.
  - *Tilt ellipses:* **dropped** for simplicity (principle 2). The idea that "within a task you can buy fidelity" can still go in the text.
  - *Split computer use into scripted and LLM-judged rungs:* **not done.** It may be worth revisiting if more computer-use-like tasks are added.
  - *Open:* computer use's height was partly justified by OSWorld evaluator bugs, which principle 1 now excludes. The structural reasons remain: end-state checks don't see side effects, and some tasks need an LLM judge. **Done: nudged up to 0.65–0.80.**
  - The reward-hacking examples still illustrate "optimisation pressure" well in the text, as long as they're framed as harness bugs rather than fidelity limits.

---

## 2026-11-22 (later still): justifying the SWE, kernel and computer-use ellipses

General point: **width** (cost) comes from the ranges of the napkin maths in `cost-appendix.md`. **Height** (fidelity) is judgement, anchored on the scale's reference points (0.8 = unit tests, 0.5 = LLM judge). The heights are less well grounded than the widths.

| Task | Current ellipse | Width: why | Height: why |
|---|---|---|---|
| Software eng. (to a spec) | $5K–100K × 0.65–0.85 | Per-check cost varies ~20× with repo size and test-suite runtime (minutes of 2 vCPUs). | Centred just under the 0.8 unit-test anchor, because tests check behaviour, not code quality or maintainability. It's tall because fidelity depends almost entirely on how good the test suite is (SWE-bench needed a "Verified" subset because many original tests were wrong or underspecified). Known hacks: special-casing tests, editing tests, patching the evaluator. METR saw o3 monkey-patch a CodeContests evaluator to always return a perfect score and override `==` in a scorer ([o3 report](https://evaluations.metr.org/openai-o3-report/), [June 2025 post](https://metr.org/blog/2025-06-05-recent-reward-hacking)). |
| Kernel optimisation | $45K–280K × 0.86–0.95 | Narrow: a compile plus a correctness check plus a timed benchmark on one GPU, with little variation between tasks. | The objective (run faster with the same output) is measured almost directly, hence high. **But the evidence says this is too high.** Sakana's "AI CUDA Engineer" claimed 10–100× speedups in Feb 2025, and they came largely from reward hacking: the kernels reused earlier results and skipped the accuracy checks. A replication found successful tasks fell from 63 to 22 once this was fixed ([TechCrunch](https://techcrunch.com/?p=2969225), [replication](https://arxiv.org/html/2603.02637)). METR found reward hacking >43× more common on RE-Bench (ML optimisation tasks) than on general software tasks. Fidelity is high *with a hardened harness* and much lower with a naive one. |
| Computer use | $125K–1M × 0.60–0.76 | The VM stays up for the whole episode, including the policy's thinking time, and episodes vary 5–20 min. Some tasks also need an LLM judge. | It mixes two reward types: scripted end-state checks (~0.75–0.8, but narrow and brittle) and LLM judges for tasks that scripts can't check (~0.5). Evaluator errors are common: Epoch estimated ~10% of original OSWorld tasks were invalid ([Epoch](https://epoch.ai/blog/osworld)), and OSWorld-Verified fixed 300+ issues in July 2025 ([XLANG](https://xlang.ai/blog/osworld-verified)). In one reported bug, a Word task's checker passed the *untouched* input file. End-state checks also don't penalise unintended side effects along the way. |

### Proposed revisions (not applied)
1. **Kernel optimisation: extend downwards to ~0.70–0.95** to reflect harness-dependence. The height of the ellipse then shows the gap between hardened and naive harnesses.
2. **Tilt these ellipses, or turn them into short ladders.** In all three, spending more on verification buys fidelity: hidden tests, hardened timing harnesses, more judges, human review. So cost and fidelity are positively correlated *within* each task, and an upright ellipse hides that. This might make a nice general point for the post: *within a task, you can buy fidelity*.
3. Possibly split computer use into "scripted check" and "LLM-judged" rungs, the way self-driving is now split.

### Note for the post
Reward hacking is most common precisely where the score is a measured number to optimise (RE-Bench, kernel speed), not a pass/fail check. That fits the y axis's definition, *fidelity under optimisation pressure*. Cases where the optimiser beat the harness are the best illustrations of what the axis means.

---

## 2026-11-22 (later): plot changes and locomotion references

### Plot changes made
- **Locomotion (sim)** moved from ~$160 to ~$16 ($5–50), following the napkin maths.
- **Self-driving** is now a three-rung ladder:
  - object-level sim (~$30, fidelity ~0.18: tests planning only, assumes perfect perception, other cars replay logs rather than react)
  - sensor-level sim (~$5M, ~0.6)
  - real (~$100M, ~0.94), drawn **hatched**, with a legend entry "Reward exists, but RL exploration isn't allowed". Surgery (patients) and drugs (Phase 3) should use the same style when added.
- The object-sim arrow is curved so it doesn't cross the manipulation ellipse. The object-sim fidelity value is a guess; please challenge it.

### References: RL-trained locomotion controllers in practice (recent first)
Industry, where methods are partly public through blogs:
- **Boston Dynamics Atlas.** The company describes training whole-body skills with RL in simulation and says that for almost all skills the policy "worked first try" on the robot ([football post](https://bostondynamics.com/blog/can-football-teach-a-robot-to-move/)). It also used RL in sim for a fridge-lifting task ([hard-work post](https://bostondynamics.com/blog/training-a-humanoid-robot-for-hard-work/)), and in Feb 2025 started a [partnership with the RAI Institute](https://bostondynamics.com/news/boston-dynamics-and-the-robotics-ai-institute-partner/) on a shared RL pipeline for electric Atlas. Note: their separate "Large Behavior Model" for manipulation is a diffusion policy trained by imitation, not RL ([post](https://bostondynamics.com/blog/large-behavior-models-atlas-find-new-footing/)).
- **Figure.** [Natural Humanoid Walk Using Reinforcement Learning](https://figure.ai/news/reinforcement-learning-walking) (2025): an end-to-end RL walking policy for Figure 02, trained in a GPU sim with domain randomisation and transferred zero-shot. The demo shows ten robots running the same network.
- **Spot (RAI Institute + Boston Dynamics).** [High-Performance RL on Spot](https://arxiv.org/abs/2504.17857) (2025): an RL policy reaching >5.2 m/s, about 3× the stock controller. The [NVIDIA write-up](https://developer.nvidia.com/blog/closing-the-sim-to-real-gap-training-spot-quadruped-locomotion-with-nvidia-isaac-lab/) describes zero-shot sim-to-real. Nuance: Boston Dynamics describes RL as layered on top of its model-predictive controller rather than replacing it.

Academic:
- [Learning Sim-to-Real Humanoid Locomotion in 15 Minutes](https://arxiv.org/abs/2512.01996) (Dec 2025). This is the humanoid sequel to the "walk in minutes" ANYmal result. Only the title is confirmed; check the details.
- [ASAP](https://arxiv.org/abs/2502.01143) (2025): agile humanoid whole-body skills on Unitree G1, using sim-to-real with a learned correction for the physics mismatch.
- Surveys: [Ha et al., Learning-based legged locomotion](https://arxiv.org/abs/2406.01152) (2024, quadruped focus) and [Bao et al., DRL for bipedal locomotion](https://arxiv.org/abs/2404.17070) (latest revision Nov 2025). The bipedal survey dates the first end-to-end sim-to-real framework on a bipedal robot to Cassie in 2019.
- Older anchors (from memory): Rudin et al. 2021 (ANYmal in ~20 min); Radosavovic et al. 2024, *Science Robotics* ([PDF](https://hybrid-robotics.berkeley.edu/publications/ScienceRobotics2024_Learning_Humanoid_Locomotion.pdf)).

**Takeaway for the post:** "RL in sim, then zero-shot transfer" is now the standard way to build locomotion controllers. Four public examples show it: Boston Dynamics, Figure, Unitree-based research, and RAI. You're right that most companies' full methods aren't public, but these blog posts are enough to support the claim. One nuance worth a sentence: at Boston Dynamics RL sits *alongside* classical control, and manipulation is moving to imitation-trained models instead. That fits the plot nicely, with locomotion inside the frontier and manipulation outside it.

---

## 2026-11-22: first critique of the Nov 2026 plot

### Decisions
- **Forecasting is off the plot.** It's an edge case and gets its own section. It's still useful as the lead example of the method's gaps: the reward is free and perfect, but slow and scarce.
- **Cost napkin maths lives in `cost-appendix.md`.** Claude's words. Oscar sense-checks the rows he knows (Lean, pretraining, SWE, kernels) and caveats the rest as Claude's judgement.

### Q: Why is Math (Lean) so far right of Chess/Go if both are cheap CPU checks?
The plot overstates the gap, but a real gap of ~3–4 orders of magnitude remains:
- **Chess/Go:** checking the result means applying fixed rules, about a millisecond of CPU per game. 5M games cost cents. The $1 on the plot is just a floor.
- **Lean:** "checking" means *elaborating* the proof. Tactics like `simp`, `omega`, `aesop` and `linarith` search when they run, and everything happens against a ~2M-line Mathlib environment that takes ~10–30 s to load cold and several GB of RAM to hold. With preloaded REPLs, prover papers report low single-digit seconds per proof, with ~60 s timeouts for bad proofs. That's ~5 CPU-s × 5M ≈ $300.
- So "both are lightweight CPU" is right in absolute terms: hundreds of dollars is nothing next to the policy's generation cost. On a log axis that spans 15 decades, though, it is still ~3–4 decades apart. **This may be a point worth making in the post:** everything left of ~$10K is effectively free relative to generation, so the meaningful distinctions start around $10⁵.

### Q: What's the evidence that locomotion (sim) is inside the "fallen" region?
"Fallen" here means *RL is the standard way it's done, and the simulator reward transfers*. For legged locomotion, the evidence (from memory, check before citing):
- Rudin et al. 2021 trained ANYmal to walk on rough terrain in ~20 minutes on one GPU with thousands of parallel sim environments, then deployed it on the real robot.
- Since then, sim-trained RL controllers have become the default for quadrupeds (ANYmal parkour, Unitree, Spot's RL locomotion work with the RAI Institute) and increasingly for humanoids (e.g. Radosavovic et al. 2024, real-world humanoid locomotion trained in sim).
- MuJoCo locomotion benchmarks have been saturated for years.

The key point is that the **sim reward holds up**: what a policy learns in sim works in reality. That's why locomotion (sim) sits at ~0.8 fidelity while manipulation (sim) sits at ~0.4. Contact-rich manipulation with deformable objects and vision is where the sim-to-real gap still bites.

Caveat: "solved" should mean *the locomotion skill*, not robust navigation in arbitrary unstructured environments.

Also noted in the appendix: the cost is probably ~$5–40, not ~$160 (the plot is ~10× high).

### Q: Why is self-driving outside the frontier when Waymo runs a paid robotaxi fleet?
Because the plot asks "is this task cheaply and safely *RL-trainable* from its reward?", not "is the task solved?". Self-driving got solved (in limited areas of operation) largely by **other routes**:
- ~15 years and tens of billions of dollars of engineering, HD maps, large human-driving datasets and **imitation learning**.
- RL plays a part, but it's a supporting one as far as public material shows. Waymo's own papers combine imitation with RL to fix the failures of pure imitation: ChauffeurNet (2018) proposed RL tuning for rare situations, and ["Imitation Is Not Enough"](https://arxiv.org/pdf/2210.09539) (2022) uses BC + SAC. Closed-loop RL fine-tuning is done in simulators like [Waymax](https://arxiv.org/abs/2310.08710). I found no public statement that Waymo's production planner is RL-trained.
- **The real-world rung can't be used for RL.** You can't explore on public roads. Like the patient rung for surgery and the Phase 3 rung for drugs, it is *forbidden*, not merely expensive. The ~$100M cost is real, but no responsible lab can spend it on exploratory rollouts. The fleet supplies imitation data and evaluation, not a reward to optimise against.

What this means for the plot and the post:
1. **This is the transfer/other-routes caveat again.** The plot measures *direct RL trainability*. Capability can also arrive by imitation, by transfer from RL'd reasoning (as with forecasting), or by brute engineering. Self-driving is a vivid example: a solved task sitting outside the RL frontier. That arguably makes the framework more honest, not weaker.
2. **Possible plot changes (done later the same day, see above):** mark forbidden rungs differently (e.g. a hatched or greyed ellipse with "exploration not allowed"). The same treatment would later apply to surgery (patients) and drugs (Phase 3). The sim rung also needs splitting or widening: object-level sims (~$30, low fidelity for perception) vs sensor-level sims (~$5M, higher fidelity).

### Open points from Claude's first critique (not yet discussed)
1. **Is fidelity measured against the sim or the real goal?** The plot implicitly uses the real goal, so sim rungs absorb the sim-to-real gap. That explains locomotion (0.82) vs manipulation (0.42). The axis label should probably say so.
2. **The real robot rungs may be too high (0.90–0.94).** Someone still has to decide whether an attempt succeeded, typically a human labeller or a learned classifier, and that detector is gameable.
3. **Ignoring success rate flatters sparse-reward tasks.** Real-world driving is the clearest case.

### Housekeeping
- Regenerating the figure locally fell back to matplotlib's default font (DejaVu Sans). The claude.ai version used a different sans-serif. Pick a font explicitly before publishing.
