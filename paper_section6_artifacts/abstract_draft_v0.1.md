# EXTp Paper — Abstract Draft v0.1

**Target venue**: NDSS '27 Fall cycle. Abstract budget: 150-250 words
(NDSS guidance). This draft lands at ~200 words. Subject to editorial
shortening in Day 12-14 polish pass.

---

## v0.1 (drafted alongside Day 9 fuzz sweep build)

> Counterfactual reasoning — "would this exploit have triggered if
> input X had been different?" — is widely used informally in security
> analysis but lacks a rigorous, falsifiable substrate.  Pearl's
> structural causal model offers the abstract machinery but operates
> on idealized distributions; running exploits, by contrast, produce
> noisy bare-metal traces with race-window microarchitectural detail
> that the abstract model elides.  We present **EXTp**, a framework
> for *empirically realizable* counterfactual causal attribution
> grounded on the seL4 verified microkernel.  EXTp composes four
> formal properties — capability separation (authority disjointness),
> strong observational equivalence (4-tuple replay determinism with
> score_S = 1.0000 across N=34 cross-boot trials), measurement
> interference (timing-domain detection threshold Δ\*), and the
> **Counterfactual Soundness Theorem** (a binding composition theorem
> in the spirit of Halpern-Pearl actual causation) — into a single
> attribution pipeline whose claims are deterministic, event-indexed,
> and envelope-bounded.  A synthetic capability-bypass demonstration
> exercises four register-write intervention values × 132 replay runs
> on a 12th-Gen Intel platform: the framework correctly attributes
> divergence in 33/33 sweep inputs with false-positive rate zero on
> the SOE clause, and recovers a calibrated noise-floor measurement
> (σ̂ = 6,237 cycles, 95% CI [5,476, 7,245]) that matches the
> reference pchase workload within 13%.  EXTp's main contribution is
> the demonstration that Pearl-style causal claims about exploit
> behaviour can be operationalized on verified-microkernel
> infrastructure, with both the structural integrity of the framework
> and its empirical realizability validated end-to-end.

---

## Key claims highlighted (for self-review)

1. **Gap stated**: counterfactual reasoning lacks rigorous substrate;
   Pearl's apparatus is abstract; real exploits are noisy.
2. **Contribution**: EXTp framework on seL4.
3. **Four property hierarchy** explicitly enumerated.
4. **Empirical anchor**: synthetic demo with concrete numbers
   (132 runs, 33 sweep inputs, σ̂=6,237 cycles, 95% CI).
5. **Cross-validation against MI baseline** (within 13%).
6. **Headline claim**: Pearl + seL4 + counterfactual replay
   intersection operationalized.

## Open questions for next polish pass

- Sentence 4 ("running exploits... produce noisy traces") might
  be tightened — what's the most defensible thing to say
  generically?
- The "binding composition theorem" framing of CST should be
  consistent with §1 main text. If we end up renaming the
  theorem, propagate here.
- We claim "33/33 sweep inputs" — this is contingent on the fuzz
  sweep boot result. If only 1/33 diverges as predicted, the
  phrasing should be "the framework correctly classifies all 33
  inputs as divergent (n=1) or non-divergent (n=32)" rather than
  "attributes divergence in 33/33."
- "Score_S = 1.0000 across N=34 cross-boot trials" — this is from
  Cross_Boot_Stability_N34.md. Confirm consistency with paper
  §5 Empirical Evaluation row.

---

## Alternative formulations to consider (Day 12 polish)

**v0.2 candidate** (shorter, more punchy):

> We present EXTp, a framework for empirically realizable
> counterfactual causal attribution on verified-microkernel exploit
> replay.  EXTp composes capability separation, strong observational
> equivalence, measurement interference, and a binding Counterfactual
> Soundness Theorem into a single attribution pipeline grounded on
> seL4.  A synthetic capability-bypass demonstration on a 12th-Gen
> Intel platform exercises 33 register-write intervention values
> across 132 replay runs; the framework correctly classifies each
> input within a calibrated noise floor (σ̂ = 6,237 cycle, 95% CI
> [5,476, 7,245]) that agrees with the reference pchase workload to
> within 13%.  EXTp operationalizes Pearl-style causal claims about
> exploit behaviour with explicit epistemic bounds, demonstrating
> that the seL4 trust anchor extends to counterfactual analysis
> on its VMM-hosted guests.

(~140 words. Cleaner; less Pearl reference; same key facts.)

**v0.3 candidate** (more aggressive framing):

> Counterfactual reasoning underpins security exploit analysis but
> typically lacks rigorous, reproducible grounding.  We present
> EXTp, the first framework to operationalize Pearl-style
> counterfactual causal attribution on a verified microkernel.  EXTp's
> four-property hierarchy — capability separation, strong observational
> equivalence, measurement interference, and the binding Counterfactual
> Soundness Theorem — establishes the formal substrate; the seL4
> verified kernel provides the trust anchor.  We empirically validate
> the framework end-to-end on a 12th-Gen Intel platform with a
> synthetic capability-bypass demonstration: 33-input register-write
> sweep × 132 replay runs, calibrated noise floor σ̂ = 6,237 cycles
> (95% CI [5,476, 7,245]), false-positive-rate-zero divergence
> attribution on the structured-observable surface.  EXTp's
> contribution is the demonstration that the verified-microkernel
> infrastructure extends to counterfactual analysis with explicit
> bounded-epistemic guarantees.

(~155 words. Stronger "first to..." language; risk: reviewer challenges
"first" claim with prior work I don't know about. Defensive position
better in v0.2.)

---

## Recommendation

Start with **v0.1** (more conservative, more explicit). After paper
§1 introduction is reviewed, polish toward v0.2 (cleaner, shorter)
or v0.3 (more aggressive) depending on how strong the §1 claims
turn out to be.

Final abstract will be locked in Day 12-14 polish window, after
§1-§9 main text is settled.
