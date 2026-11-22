# Discussion notes (Claude Code sessions)

Running notes for Oscar to review before writing. Newest first. The earlier claude.ai session is summarised in HANDOFF.md.

---

## Standing principles for placing tasks (agreed 2026-11-22)
1. **Assume harnesses work as intended.** Bugs in a harness or evaluator don't count against fidelity: they're usually easy to fix. Fidelity reflects *structural* gaps between the reward and the goal, such as physics mismatch in sims, proxy vs real outcome, or what a check can't observe even in principle.
2. **Keep the plot as simple as possible while carrying the detail.** Many more tasks are coming, so prefer upright ellipses and only split a task into rungs when the rungs are genuinely different reward sources.

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
