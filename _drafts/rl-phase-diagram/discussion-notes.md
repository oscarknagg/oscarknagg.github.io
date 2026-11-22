# Discussion notes (Claude Code sessions)

Running notes for Oscar to review before writing. Newest first. The earlier claude.ai session is summarised in HANDOFF.md.

---

## Standing principles for placing tasks (agreed 2026-11-22)
1. **Assume harnesses work as intended.** Bugs in a harness or evaluator don't count against fidelity: they're usually easy to fix. Fidelity reflects *structural* gaps between the reward and the goal, such as physics mismatch in sims, proxy vs real outcome, or what a check can't observe even in principle.
2. **Keep the plot as simple as possible while carrying the detail.** Many more tasks are coming, so prefer upright ellipses and only split a task into rungs when the rungs are genuinely different reward sources.

## 2026-11-22: SWE extended, earlier proposals revisited
- **Software eng. now spans 0.65–0.90 fidelity.** The top end covers SWE tasks with an *oracle*: reverse-engineering an existing program (match its behaviour), or visual feedback where a target image or reference render is the check. Oscar suspects many of Fable's one-shot JavaScript painting results come from this kind of training.
- **Proposals from the section below, revisited under the principles above:**
  - *Extend kernel optimisation down:* **dropped.** The Sakana case was a harness bug (reusing results, skipping accuracy checks), which principle 1 excludes.
  - *Tilt ellipses:* **dropped** for simplicity (principle 2). The idea that "within a task you can buy fidelity" can still go in the text.
  - *Split computer use into scripted and LLM-judged rungs:* **not done.** It may be worth revisiting if more computer-use-like tasks are added.
  - *Open:* computer use's height was partly justified by OSWorld evaluator bugs, which principle 1 now excludes. The structural reasons remain: end-state checks don't see side effects, and some tasks need an LLM judge. Consider nudging it up slightly (e.g. 0.65–0.80).
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
