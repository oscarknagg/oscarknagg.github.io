# Discussion notes (Claude Code sessions)

Running notes for Oscar to review before writing. Newest first. The earlier claude.ai session is summarised in HANDOFF.md.

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
2. **Possible plot changes (not done yet):** mark forbidden rungs differently (e.g. a hatched or greyed ellipse with "exploration not allowed"). The same treatment would later apply to surgery (patients) and drugs (Phase 3). The sim rung also needs splitting or widening: object-level sims (~$30, low fidelity for perception) vs sensor-level sims (~$5M, higher fidelity).

### Open points from Claude's first critique (not yet discussed)
1. **Is fidelity measured against the sim or the real goal?** The plot implicitly uses the real goal, so sim rungs absorb the sim-to-real gap. That explains locomotion (0.82) vs manipulation (0.42). The axis label should probably say so.
2. **The real robot rungs may be too high (0.90–0.94).** Someone still has to decide whether an attempt succeeded, typically a human labeller or a learned classifier, and that detector is gameable.
3. **Ignoring success rate flatters sparse-reward tasks.** Real-world driving is the clearest case.

### Housekeeping
- Regenerating the figure locally fell back to matplotlib's default font (DejaVu Sans). The claude.ai version used a different sans-serif. Pick a font explicitly before publishing.
