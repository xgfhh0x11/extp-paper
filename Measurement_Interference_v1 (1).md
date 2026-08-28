# Measurement Interference

## 1. Background and Scope

### 1.1 Position within property hierarchy

Three formal properties precede MI in the EXTp framework:

- **Capability Separation** (Capability_Separation_Theorem.md)
  bounds the authority delegation between exploit-time and
  replay-time execution; replay capability sets are disjoint from
  the original exploit's, and this disjointness is preserved across
  every replay event.
- **Strong Observational Equivalence** (Strong_Observational_Equivalence.md)
  establishes that on the four-component observable surface
  (rip, exit_reason, exit_qual, rax), original-trace and replay-trace
  trajectories agree event-by-event with score_S = 1.0000 across
  N=34 cross-boot replays (Cross_Boot_Stability_N34.md).
- **Measurement Interference (this entry)** characterizes the
  detectability bound for timing-domain perturbations under the
  EXTp framework's measurement instruments. Timing is **not**
  part of the SOE observable surface (Section 1.1 of the SOE
  entry); MI quantifies the scope boundary of the dimension SOE
  deliberately excludes.

The fourth property, **Counterfactual Soundness Theorem (CST)**,
is forthcoming;
it consumes MI's detection threshold as the lower bound for
intervention-effect significance.

### 1.2 Motivation

Replay verdicts on the SOE observable surface achieve score_S =
1.0000, including across boot boundaries. However, an exploit's
behaviour may also exhibit a **timing signature** — micro-
architectural latency patterns that the SOE surface deliberately
suppresses. Without a quantitative bound on the EXTp framework's
measurement instruments' sensitivity, two failure modes are
possible:

1. **False negative.** A real timing-domain divergence falls below
   the noise floor of the instrument and is mistaken for replay
   determinism in the timing dimension as well.
2. **False positive.** Instrument noise exceeds the threshold of
   significance and a "divergence" is reported where none exists.

MI characterizes the detectability boundary that separates these
regimes. The property's empirical antecedents (TSC noise floor,
sigmoid detection curve, slope-mediated workload-class scaling)
collectively dimension this boundary for the workload classes
and instruments characterized in this work.

### 1.3 What MI claims and does not claim

**MI claims.** Under the EXTp framework's measurement instruments,
on hardware and workload classes characterized in §4, the P=0.5
detection inflection for timing-domain perturbations is given by
the formal expression in §3.1 (per-iteration units), and the
§3.2 cycle-unit conjecture is hypothesized as a forward-looking
direction (Q3b validation pending) within the bare-RDTSC
measurement regime.

**MI does not claim.** MI does not extend SOE — it does not
introduce timing into the SOE observable surface. The SOE
score_S = 1.0000 result is unaffected by MI's findings; MI
operates in the **complement** of SOE's observable surface.

**Scope qualifier (cycle-invariance conjecture).** The cycle-
invariance conjecture stated in §3.2 is **hypothesized within
S2 (bare-RDTSC) measurement regime, forward-looking**; see §3.2
and §6.2 for citation discipline. Cross-instrument generalization
to S1 (LFENCE-RDTSC) is not established; the 28% (CPUID-VMCALL
vs L2-pchase) and 17% (L1-pchase vs L2-pchase) gaps observed in
§4.3 between S1 and S2 detection thresholds are consistent with
joint contributions of instrument variation, sampling-regime
variation (§2.3 non-confounding assumption), and guest-workload
covariance (§3.2 prior counter-evidence). Decoupling these
contributions is the explicit task of Q3 (§5.2). Readers should
not interpret the conjecture as instrument-invariant.

---

## 2. Definitions

**Notation note (scope flag).** Two instruments are characterized
in this entry: S1 (LFENCE-RDTSC sandwich) and S2 (bare RDTSC).
Unless explicitly qualified, claims in Sections 3–5 apply to S2.
S1↔S2 generalization is deferred to the future work item in
Section 5.2.

### 2.1 Instrument

The **instrument** is the instruction sequence used to obtain a
timestamp value at a given trace event. Two instruments are
distinguished:

**S1 — LFENCE-RDTSC sandwich.**
```
LFENCE
RDTSC
LFENCE
```
RDTSC reads TSC without architectural serialization. The
flanking LFENCE pair carries the entire serialization burden:
on Intel post-Spectre microcode, LFENCE is a full execution
barrier, so (i) the leading LFENCE drains prior in-flight ops
before the RDTSC dispatches, and (ii) the trailing LFENCE
gates subsequent op dispatch until RDTSC retires. RDTSC was
chosen over RDTSCP to avoid the ENABLE_RDTSCP secondary-exec
VMCS dependency in VMM context (cf. `extp_tsc_sandwich()` in
`projects/sel4test/apps/extp-vmm/include/trace/timing.h`).
Microcode-dispatch cost of LFENCE under post-Spectre microcode
adds variable latency. Range-estimator inference (§4.1)
suggests S1 elevates σ_baseline by ~3× relative to S2 under
matched workload; direct paired empirical measurement is
pending Q3c (§5.2).

**S2 — bare RDTSC.**
```
RDTSC
```
Single-instruction read of TSC, no architectural serialization
guarantee. Reorder window is open: prior loads may not have
retired, subsequent ops may dispatch before the read commits.
Empirically yields lower σ_baseline than S1 on the workloads
characterized here.

The choice between S1 and S2 affects σ_baseline magnitude but
not the slope `b` of the perturbation primitive (Section 2.5),
since `b` is determined by per-iteration cycle cost of the
guest-side workload, not the instrument cost. The window
distinction underlying this claim is formalized in §2.2.

**Joint contribution disclaimer.** The σ_baseline difference
between S1 and S2 is treated as a **joint contribution** of
instrument cost (deterministic mean shift) and instrument-induced
jitter (variance overlay). Quantitative decomposition between
these two components requires paired S1/S2 measurement on
identical workload, which is not available in this work.
Decomposition is deferred; it is automatically obtained as a
by-product of the Q3 future work item (Section 5.2), which
introduces a paired bare-RDTSC measurement under the Sweep
workload.

### 2.2 Measurement window

Two distinct notions of "window" are at play; conflating them
collapses the analytical separation between instrument choice
and event semantics. We introduce paper-specific notation to
keep them apart: $W_L$ for the logical window, $W_M$ for the
measured window.

**Logical window ($W_L$).** The instruction sequence bracketed
by two instrument invocations: t_start (instrument call before
guest event) and t_end (instrument call after guest event).
$W_L$'s span is determined by **event semantics** — for VM-exit
timing in EXTp, it spans `extp_event_from_vmenter` to the
corresponding handler return. $W_L$ is **identical** under S1
and S2; the same guest event is being bracketed.

**Measured window ($W_M$).** Also: instrument-extended window.
The interval Δ = TSC(trailing) − TSC(leading), where each TSC
value is captured at the RDTSC retirement point of the
respective instrument invocation. Under S1, the LFENCE pair
flanking each RDTSC contributes pipeline-drain latency that is
absorbed into the leading-side TSC (post-drain) and the
trailing-side TSC (after the next-LFENCE-induced gating);
$W_M$ therefore includes the cost of LFENCE-induced
serialization in addition to the bracketed event. Under S2,
no flanking LFENCE is present, so $W_M$ collapses to the bare
TSC-to-TSC interval. $W_M$ is **wider under S1** than S2 due
to LFENCE-induced drain.

The observed delta Δ = t_end − t_start corresponds to $W_M$,
not $W_L$. When σ_baseline differs between S1 and S2 (Section
4.1), this difference is attributable to **$W_M$ variation**,
while $W_L$ remains fixed by event semantics. The §4.3
cross-instrument comparison thus isolates instrument variation,
not event-semantic variation.

### 2.3 Sampling regime

The **sampling regime** specifies how raw measurements are
aggregated:

- **N** — total outer-run count per condition
- **inner warmup discard** — first 20 samples per outer run
  excluded from aggregation (calibrated in TSC Reorder Noise
  Floor entry)
- **trim policy** — for σ characterization: untrimmed (raw σ) and
  5/95 trimmed (tail-robust σ) both reported; for sigmoid fit:
  untrimmed (preserves tail behavior)
- **mod-K interleaving** — across K conditions, samples drawn in
  round-robin order to avoid temporal drift confounds

**Within-experiment vs cross-experiment.** N is held fixed
**within** each experiment in this work. **Cross-experiment** N
varies by design: §4.1 uses flat N=1000 (single-condition noise
floor characterization); §4.3 uses stratified 9 conditions × 111
samples (cross-condition coverage). The two designs are not
interchangeable — flat N=1000 estimates a single-stratum σ;
stratified 9×111 estimates within-stratum σ that pools across
conditions.

**Cross-experiment σ comparisons** (e.g., σ_S1 = 6,383 from §4.1
vs σ_S2 = 4,604 from §4.3) assume the sampling regime is
**non-confounding** — i.e., that within-stratum σ in stratified
design is comparable to single-stratum σ in flat design. This
assumption is **not independently validated** in this work. The
S1-vs-S2 gaps in §4.3 may include a residual sampling-regime
contribution alongside instrument and guest-workload
contributions.

The Q3 future work item (Section 5.2) addresses this by
replicating §4.2 under S2 with a sampling regime aligned to
§4.3's stratified design, eliminating sampling regime as a
cross-experiment confound.

### 2.4 Baseline noise

The **baseline noise** σ_baseline is the standard deviation of
the measured delta Δ under no-perturbation condition, for a
fixed (instrument, workload, sampling regime) tuple.

**Per-experiment calibration.** σ_baseline is computed
**within** each experiment from the iter=0 (no-perturbation)
condition. We do not borrow σ_baseline from a separate
experiment, because instrument and workload may differ; cross-
experiment σ comparisons are reported with explicit qualification
(§2.3, §4.3).

**Estimator.** Within-experiment σ̂_baseline is the sample standard
deviation of post-warmup deltas in iter=0:
$$\hat{\sigma}_{\text{baseline}} = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (\Delta_i - \bar{\Delta})^2}$$
with n the number of post-warmup samples in the iter=0 condition.

**Trim policy.** Trimming would lower σ̂ and thereby reduce the
detection threshold, raising false-positive rate against unmodeled
baseline outliers. Without independent artifact-vs-signal
calibration at the tails (§5.4), raw σ̂ is retained as the
conservative bound. The 5/95-trimmed estimator is reported in
§4.1 (TSC Reorder Noise Floor entry) for descriptive
comparability but is not used in property formalism.

**What σ_baseline is not.** σ_baseline is not the population σ
of any underlying physical process — it is an instrument- and
workload-conditioned estimator. Treating it as a population
parameter would be a category error; cross-instrument or
cross-workload σ comparisons are explicitly empirical claims,
not analytical identities.

### 2.5 Workload class and slope

A **workload class** is characterized by the per-iteration cycle
cost `b` of the perturbation primitive when executed in the
guest under the EXTp VMM. Two workload classes are
characterized in this work:

- **L1-resident** (32 KB working set): pointer-chase chain fits
  in L1 data cache; per-iter cost b ≈ 4.481 cycle (§4.2)
- **L2-resident** (512 KB working set): chain exceeds L1, fits
  in L2; per-iter cost b ≈ 15.194 cycle (§4.3)

**Slope estimation.** `b` is estimated from the calibration phase
of each experiment via linear regression of mean Δ on iteration
count, across multiple iter conditions:
$$\hat{b} = \frac{\sum_i (n_i - \bar{n})(\bar{\Delta}_i - \bar{\bar{\Delta}})}{\sum_i (n_i - \bar{n})^2}$$
We require R² ≥ 0.99 for slope fit acceptance. We adopt this
as a conservative round-number threshold; both characterized
workload classes satisfy it (L1: R² = 0.9929, §4.2; L2:
R² = 0.99994, §4.3). The threshold approximately corresponds
to ≤ 10% RMS deviation in the cycle-unit expression Δ = b·δ
(§2.6) under standard regression assumptions; the exact
relationship depends on SST and is not matched mathematically
by R² alone. Below R² = 0.99, per-iter quantification (δ) is
preferred over cycle-unit conversion.

**What workload class is not.** Workload class is not a property
of the cache hierarchy in isolation — it is a property of the
**primitive's interaction** with the cache hierarchy under the
specific guest binding. A different perturbation primitive
(non-pointer-chase) on the same working-set size would constitute
a different workload class.

**Coverage.** Only L1-resident and L2-resident classes are
characterized in this work. LLC-resident (8 MB) and DRAM-resident
(64 MB) classes are deferred (§5.3).

### 2.6 Perturbation magnitude

The **perturbation magnitude** is the controlled timing shift
injected into the guest workload, expressed in two equivalent
units:

**Iteration units (δ).** The number of iterations of the
pointer-chase primitive injected before the trace event. δ is
the **primary control variable** in the Sweep (§4.2) and
Workload Class (§4.3) experiments.

**Cycle units (Δ).** The mean cycle shift induced by δ
iterations, computed from the workload-class slope:
$$\Delta = b \cdot \delta$$
Δ is the **derived expression** in cycle space, used for cross-
workload comparisons under the cycle-invariance conjecture
(§3.2).

**Why both units appear.** The primary form of the property
(§3.1) is in iteration units because δ is what the experimenter
controls. The conjecture (§3.2) is in cycle units because cross-
workload comparison requires unit normalization to b. If the
slope fit fails the §2.5 acceptance criterion (R² < 0.99), the
cycle-unit expression Δ = b·δ is approximate and per-iter
quantification δ should be used as the primary observable.

### 2.7 Detection criterion

The **detection criterion** is the per-sample decision rule for
classifying an observed delta Δ_i as "detected" or "not
detected":
$$\text{detect}(\Delta_i) = \begin{cases} 1 & \text{if } \Delta_i > \hat{\mu}_{\text{baseline}} + z_{1-\alpha} \cdot \hat{\sigma}_{\text{baseline}} \\ 0 & \text{otherwise} \end{cases}$$
with μ̂_baseline and σ̂_baseline computed within-experiment from
the iter=0 condition only.

**Parameterization.** The detection criterion is parameterized
over α ∈ (0,1). All numerical results in §3–§5 use α = 0.05
(one-sided z_{1-α} = 1.645) as the convention. Application at
alternative α requires recomputation of: (i) the threshold
Δ* = z_{1-α} · σ̂_baseline per experiment, and (ii) sigmoid
fit parameters (x_0, k) per workload class (§4.2). The
framework's structural claims are α-invariant; only quantitative
thresholds shift.

**Why one-sided.** Perturbation injection adds positive cycle
cost to Δ; only positive shifts are tested. Symmetric or
negative-direction perturbation tests would require two-sided or
inverse criteria, which are out of scope (§5.4).

**Why baseline-σ, not pooled-σ.** The criterion tests against the
baseline distribution because the property's claim is "this delta
exceeds what the instrument produces under no perturbation."
Pooled σ across all conditions inflates the threshold (§4.2
records the 4σ-pooled equivalent for completeness), but the
empirical onset point at α=0.05 is the operationally meaningful
detection threshold.

**Approximation under asymmetric tails.** The z-test relies on a
near-normal baseline distribution. The asymmetric-tail
observation (§5.4) implies the z-test is approximate; the
nominal α=0.05 does not exactly match the realized false-positive
rate when the lower tail is heavier than the upper. Non-parametric
or quantile-based alternatives (e.g., empirical 95th percentile
of iter=0 distribution) are deferred; the z-test is retained for
analytical tractability and consistency with the §3.1 closed-form
δ* expression.

**Detection rate.** For a given condition with n samples, the
**detection rate** is the fraction of samples satisfying
detect(·) = 1. Detection rates are aggregated per condition and
fitted to a sigmoid function of δ (§4.2) to extract x_0 (P=0.5
inflection) and k (steepness).

**Per-event α vs trace-level FWER.** The detection criterion's
α is **per-event**: each event-indexed comparison carries
nominal false-positive rate α (default 0.05). For a trace
containing N events, the expected number of false detections
under no perturbation is N·α (nominal), or N·α_realized using
the §5.4 direct-count values. MI does **not** prescribe a
family-wise correction (Bonferroni, FDR) for trace-level
aggregation; this is delegated to the downstream consumer
(replay verdict pipeline, §6.1; CST admissibility framework,
§6.3). Consumers aggregating per-event verdicts to trace-level
attribution must apply the appropriate correction for their
use case. MI claims per-event detection-threshold validity;
trace-level FWER is the consumer's aggregation responsibility.

---

## 3. Property Statement

### 3.1 Detection threshold (primary form, iteration units)

Let:
- σ̂_baseline = baseline distribution standard deviation estimator
  (cycles), per-experiment calibration (§2.4)
- b = workload-class slope (cycles per perturbation iteration,
  §2.5)
- α = confidence level (default 0.05)
- z_{1-α} = one-sided normal quantile

**MI Detection Threshold (formal claim):**

Under the per-sample detection criterion (§2.7), the
**probability of detection** as a function of perturbation
magnitude δ is:

  P(detect | δ) = 1 − Φ(z_{1-α} − (b·δ) / σ̂_baseline)

assuming homoscedasticity (σ_perturbation ≈ σ̂_baseline) and
near-normal Δ distribution. Under these assumptions:

- δ = 0 yields P = α (by construction of the criterion)
- δ such that b·δ = z_{1-α} · σ̂_baseline yields P = 0.5

The **MI detection threshold** δ* is defined as the
P=0.5 inflection point:

  δ*(α, σ̂_baseline, b) = (z_{1-α} · σ̂_baseline) / b

This is **workload-class dependent** — different workload classes
exhibit different b and may exhibit different σ̂_baseline regimes.
Below δ*, detection probability per sample is < 0.5; above δ*,
> 0.5. The threshold is operationally the perturbation magnitude
at which the mean induced delta b·δ matches the per-sample
detection threshold z_{1-α} · σ̂_baseline.

**Empirical correspondence.** In the L1-resident pchase workload
under S1 (§4.2), with σ̂_baseline_L1_pchase_S1 = 5,518 cycle
(Sweep iter=0 condition, boot_log12, n=108, directly measured
under same instrument and same workload as the sigmoid fit), the
analytical δ* = (1.645 · 5,518) / 4.481 = 2,026 iter; the
sigmoid fit's x_0 = 2,520 iter. The nominal gap is 24%
(predicted basis).

**σ̂ sampling uncertainty (n=108).** The χ² 95% confidence
interval on σ for n=108 is asymmetric:
σ ∈ [4,867, 6,371] cycle (-11.8% / +15.5% on the point estimate).
Propagating to δ*:
δ* ∈ [1,787, 2,339] iter.
The gap between sigmoid x_0 = 2,520 and δ* therefore spans:
- 7.7% (if σ true value is at upper CI bound 6,371)
- 41.0% (if σ true value is at lower CI bound 4,867)

with 24% as the point-estimate-based gap.

**Interpretation.** The gap is **dominated by σ̂ sampling
uncertainty**, not by functional-form effects (logistic vs probit)
or homoscedasticity violation. At n=108, the confidence interval
on σ̂ is wide enough that functional-form contributions cannot
be separately resolved. Two consequences:

1. The "20–24% gap" reading as evidence of functional-form
   mismatch is **not supported** by this dataset at this sample
   size; the gap may be entirely attributable to σ̂ sampling
   noise.
2. Resolving the functional-form contribution would require N
   substantially larger (e.g., N ≥ 500 under matched conditions),
   at which the σ̂ CI tightens to ~±5% and gap interpretation
   becomes meaningful.

Both partitions — functional-form attribution and quantitative
decomposition of homoscedasticity violation — are **deferred**
beyond the scope of the current sample size.

### 3.2 Cycle-unit threshold (empirical regularity, conjecture)

Re-expressing in cycle units (multiplying both sides by b):

  Δ*(α, σ̂_baseline) = z_{1-α} · σ̂_baseline

This motivates a stronger conjecture — that cycle-unit thresholds
are **workload-class invariant within a fixed instrument**. With
the empirical antecedents available in this work, this conjecture
**cannot yet be tested** in its narrow form: the available
cross-workload σ data under S2 (Workload Class mini-probe,
boot_log14) is at fixed iter=4500, not at the iter=0 condition
required by σ̂_baseline (§2.4). Direct same-instrument cross-
workload Δ* comparison under S2 is the explicit task of Q3b
(§5.2).

**Prior counter-evidence (guest-workload covariance with σ).**
We define **guest-workload type** as the type of guest activity
bracketed by the measurement window — e.g., pchase loop vs
CPUID-VMCALL VM-exit. This is **not** a property of the window
$W_L$ or $W_M$ themselves (which are bracket definitions, §2.2);
it is a property of what executes inside the bracket.

§4.1 reports two σ̂_baseline values under the **same instrument**
S1, **paired by direct measurement** (no methodology asymmetry):
- 5,518 cycles (L1-pchase guest-workload, Sweep iter=0,
  boot_log12, n=108)
- 6,383 cycles (CPUID-VMCALL guest-workload, noise floor
  experiment, n=978)

The 15.7% spread under fixed instrument with paired direct
measurement suggests **σ̂_baseline covaries with guest-workload
type**, not purely with cache tier. This is **prior evidence
against** unrestricted workload-class invariance. (The
range-estimator inferred value 2,189 in §4.1 is not used for
this counter-evidence claim, since its methodology is
non-paired.)

The conjecture's testable form is therefore narrowed to:

  Δ* invariance across **cache tiers** (L1 vs L2 vs LLC vs DRAM)
  **within a fixed guest-workload type** (e.g., pchase) under a
  fixed instrument.

Generalization across guest-workload types (e.g., pchase vs
CPUID-VMCALL) is **not** part of the conjecture; the §4.1 spread
is consistent with that generalization being false.

The conjecture is therefore stated as **forward-looking**:
hypothesized within S2, within fixed guest-workload type, pending
Q3b validation. Cross-instrument generalization (S1 ↔ S2)
additionally requires Q3c.

### 3.3 Premises

The MI property holds for a given (hardware, workload, instrument)
configuration iff the following premises are empirically
established:

- **P1.** Instrument noise floor characterization: σ_baseline
  empirically measured under no-perturbation condition; freq drift
  and other confounders falsified.
- **P2.** Detection curve sigmoid form validated for the workload
  class: detection rate exhibits monotonic sigmoid with sub-detection,
  transition, and saturation regimes.
- **P3.** Slope-mediated workload class scaling validated: for at
  least one cross-class comparison, threshold ratio in iter units
  matches z·σ/b prediction at the point estimate. Observed
  deviations across the characterized workload classes are 24%
  (§3.1 single-workload point estimate) and 22% (§4.3
  cross-workload point estimate); these are reported as a
  **descriptive central-tendency** for the L1/L2 cases studied,
  not as an a priori statistical guarantee band. At n=108
  (§3.1), the σ̂ sampling uncertainty alone produces a 95% CI on
  the gap spanning approximately 7.7%–41% (§3.1 analysis); the
  observed point-estimate deviations are well within this range.
  Larger N would be required to validate a tighter band.
  Extrapolation to LLC/DRAM workload classes (§5.3) requires
  per-class re-measurement; deviations under those classes are
  not bounded by the L1/L2 observations.

Section 4 establishes P1, P2, P3 with separate empirical evidence
each.

---

## 4. Evidence for Premises

### 4.1 Evidence for P1 — Instrument noise floor characterization

[TSC_Reorder_Noise_Floor entry, N=1000 single-boot:
- σ_baseline = 6,383 cycle (sandwich, S1; CPUID-VMCALL
  guest-workload; directly measured)
- σ_baseline = 5,518 cycle (sandwich, S1; L1-pchase
  guest-workload; Sweep iter=0 condition, boot_log12, n=108,
  directly measured. This is the σ used in §3.1 empirical
  correspondence — same instrument and same guest-workload as
  the sigmoid fit.)
- σ_baseline = 4,604 cycle (bare RDTSC, S2; from Workload Class
  S2 calibration boot — separate experiment, sampling regime
  differs from S1 measurement, see §2.3)
- σ_baseline ≈ 2,189 cycle (bare RDTSC, S2; range-estimator
  inference under Gaussian-approximation, from
  Cross_Boot_Stability_N34 per-boot 98-sample range,
  $\hat{\sigma} \approx \text{range} / 2\sqrt{2\ln n}$ with
  range = 13,266). The §4.1 entry itself observes asymmetric
  tails; the Gaussian-approximation range estimator is biased
  under asymmetric distributions, so this σ value carries
  larger uncertainty than the directly measured σ values.
  The S1/S2 ratio under this inference is ~3× — but this is a
  range-estimator inference under a different guest-workload
  with a Gaussian-approximation qualifier, not a paired
  same-condition measurement.
- Frequency drift hypothesis falsified: APERF/MPERF quintile
  stratification shows no σ-modulation
- P-state locked at 4.9 GHz turbo throughout
- Asymmetric tails (low extends further than high) — cycle-unit
  threshold formulation should treat this as upper bound

**Four σ_S2 values, four regimes:**
- 4,604 (S2 calibration, L2-pchase workload, iter=0 baseline,
  stratified sampling)
- 4,747 (S2 mini-probe, L1-pchase workload, iter=4500 fixed
  perturbation, n=109; not σ_baseline since iter≠0, see §2.4
  category constraint)
- 7,723 (S2 mini-probe, L2-pchase workload, iter=4500 fixed
  perturbation, n≈109; directly measured; gives the §4.3
  mini-probe ratio L2/L1 = 7,723/4,747 = 1.63. Same iter≠0
  category constraint as σ_L1(mini-probe).)
- 2,189 (range-estimator inference, no-perturbation 18.6M-cycle
  CPUID-VMCALL window, flat sampling, Gaussian-approximation)
- The S1/S2 ratio is **~1.39× under the calibration-boot
  comparison** (cross-experiment, sampling-regime confound per
  §2.3), and **~3× under the range-estimator inference**
  (cross-window, single-source). Direct paired measurement of
  σ_S1/σ_S2 ratio is not available; Q3c (§5.2) provides this.]

### 4.2 Evidence for P2 — Detection curve sigmoid form

[MI_Detection_Threshold_Sweep entry, L1-resident pointer-chase,
S1 instrument, 9 condition × 111 sample:
- Slope fit (mean Δ on iter count, S1 calibration): b_L1 = 4.481
  cycle/iter, R² = 0.9929 (slope-fit; distinct from sigmoid-fit
  R² below)
- Logistic sigmoid fit: x0 = 2,520 iter, k = 635 iter, R² = 0.9984
- Three regimes empirically distinguished: sub-detection (< 1.5K),
  transition (1.5K–6K), saturation (> 6K)
- α=0.05 detection criterion (per-sample one-sided Z-test against
  baseline distribution, σ from iter=0 only, n=110)
- 4σ-pooled equivalent crossing at 5,779 iter as alternative
  strong-evidence threshold]

### 4.3 Evidence for P3 — Slope-mediated workload class scaling

[MI_Workload_Class_Sensitivity entry, L1+L2 cross-class, S2:
- L1 slope (Sweep, S1): b_L1 = 4.481 cycle/iter
- L2 slope (Workload Class, S2): b_L2 = 15.194 cycle/iter
- σ ratio L2/L1 (mini-probe, fixed iter): 1.63
- slope ratio L2/L1: 3.39
- threshold ratio (iter): predicted (z·σ/b model) = 0.246,
  observed = 0.192 — 22% relative deviation (point estimate).

**Predicted ratio derivation.** δ*_L2/δ*_L1 = (σ_L2·b_L1) /
(σ_L1·b_L2), with σ_L1 = 5,518 (S1, L1-pchase iter=0,
boot_log12, n=108) and σ_L2 = 4,604 (S2, L2-pchase iter=0,
boot_log15, n≈108 per condition), b_L1 = 4.481, b_L2 = 15.194.
Computation: (4,604·4.481) / (5,518·15.194) = 20,634 / 83,840
= 0.246.

**Cross-instrument σ confound.** This prediction uses σ_L1
from S1 instrument and σ_L2 from S2 instrument — a
cross-instrument σ pair. The §4.3 P3 validation is therefore
**not strictly within-instrument**; the prediction holds
quantitatively but interprets the slope-mediated scaling claim
under a cross-instrument σ hybrid. Within-instrument
validation (σ_L1 and σ_L2 both under S2, both at iter=0)
requires Q3a (§5.2).

**σ̂ sampling uncertainty.** Both σ̂ inputs to this prediction
carry n≈108 sampling uncertainty. At n=108, χ² 95% CI on σ
spans ±~12–16% (§3.1 detailed analysis); the propagated CI on
the predicted ratio is **comparable in magnitude to the 22%
observed deviation**. The 22% gap is therefore **also
σ̂-noise-dominated**, like the §3.1 24% gap — not necessarily
evidence of homoscedasticity violation or functional-form
mismatch. Larger N under matched conditions (Q3a target)
would tighten this CI substantially.
- Slope dominates threshold scaling under fixed σ-ratio:
  point-estimate observation (predicted 0.246, observed 0.192)
  within σ̂ CI; stronger validation pending Q3a.

**S2-only cross-workload Δ* consistency** is **not directly
computable** from current data: σ_baseline_L1(S2) requires an
iter=0 measurement under S2 with L1-resident workload, which
the Sweep experiment (S1 instrument) and Workload Class
mini-probe (fixed iter=4500, no iter=0) do not provide.
Validation pending Q3a/Q3b (§5.2).

**Cross-instrument cycle-unit comparison (illustrates non-invariance
across instruments):**
- Δ*_(S1, CPUID-VMCALL) (α=0.05) = z·σ_S1_CPUID = 1.645 × 6,383
  = 10,500 cycle (σ_S1 measured under CPUID-VMCALL guest-workload,
  §4.1)
- Δ*_(S1, L1-pchase) (α=0.05) = z·σ_S1_pchase = 1.645 × 5,518
  = 9,077 cycle (σ_S1 measured under L1-pchase guest-workload,
  Sweep iter=0, §4.1)
- Δ*_(S2, L2-pchase) (α=0.05) = z·σ_S2 = 1.645 × 4,604 = 7,574
  cycle (σ_S2 measured under L2-pchase guest-workload, §4.3)
- Difference (S1 CPUID-VMCALL vs S2 L2-pchase): 28%
- Difference (S1 L1-pchase vs S2 L2-pchase): 17%

**Confound analysis.**

The **28% gap (S1 CPUID-VMCALL vs S2 L2-pchase)** is consistent
with the joint contribution of three confounds:

1. **Instrument variation** — S1 vs S2 (the §4.1 noise floor
   difference)
2. **Sampling regime variation** — flat N=1000 (§4.1) vs
   stratified 9×111 (§4.3); §2.3 non-confounding assumption
3. **Guest-workload variation** — CPUID-VMCALL (§4.1) vs
   L2-pchase (§4.3); §3.2 prior counter-evidence on
   guest-workload covariance with σ.

The **17% gap (S1 L1-pchase vs S2 L2-pchase)** is consistent
with the joint contribution of two confounds (the
guest-workload-type confound is partially eliminated since both
are pchase; cache tier still differs):

1. **Instrument variation** — S1 vs S2
2. **Cache-tier variation within pchase family** — L1 vs L2
   pchase (this would itself be evidence against the §3.2
   conjecture if instrument were held fixed; but instrument is
   not held fixed here, so contributions are entangled)

In neither comparison is sampling-regime or instrument
contribution separately quantified in this work. Q3c (§5.2)
isolates the instrument contribution under matched workload and
aligned sampling regime; Q3d separately bounds the
sampling-regime contribution. Together they decompose the gaps
into instrument, regime, and residual contributions
attributable to guest-workload covariance and cache-tier
covariance (§3.2 prior counter-evidence).

This comparison illustrates the necessity of the S2-only
restriction in §3.2, not a test of it; cross-instrument
generalization pending Q3c (§5.2).]

---

## 5. Concession Footnote

### 5.1 Capability concession (read-only RDMSR)

The empirical antecedents (Sections 4.1–4.3) depend on the
read-only `SysX86DangerousRDMSR` debug syscall (`KernelX86DangerousMSR=ON`
build flag). This syscall is not capability-mediated. The
read-only nature of the use does not violate the write-side
authority delegation claims of the Capability Separation Theorem
(see footnote in that entry); production builds disable the flag.

**Read-side information-disclosure.** A read-only RDMSR
nevertheless constitutes a side-channel surface (TSC, performance
counters, MSR-resident state). Information-disclosure semantics
are out of scope of capability separation in EXTp's threat model;
production builds disable the flag, eliminating the disclosure
surface entirely. Research builds accept the disclosure surface
as a measurement instrument cost.

### 5.2 Instrument confound between Sweep and Workload Class

The Detection Threshold Sweep (Section 4.2) was conducted with
LFENCE-RDTSC sandwich (S1); the Workload Class Sensitivity
experiment (Section 4.3) was conducted with bare RDTSC (S2).
Cross-experiment σ comparison yields S1/S2 ≈ 1.39× under
calibration-boot data (sampling-regime confound per §2.3); a
separate range-estimator inference suggests S1/S2 ≈ 3× under
matched workload (§4.1). The two ratios are not paired, and
neither rests on direct same-condition S1/S2 measurement.
Consequently, observed Δ* values across the two experiments
cannot be unambiguously attributed to workload class versus
instrument.

In addition, the two experiments use different sampling regimes
(§4.1 flat N=1000; §4.3 stratified 9×111). Cross-experiment σ
comparisons therefore carry a residual sampling-regime
non-confounding assumption (§2.3) that is not independently
validated in this work.

**Future work — Q3 sub-experiments (shared platform).**

Q3 is a future experimental campaign comprising four
sub-experiments. They share platform (same bare-metal hardware,
same pchase primitive, same seL4 build with sweep mode runtime
parameter, same serial logging) but each sub-experiment has
its own design optimized for the specific question.

**Q3a — Workload-class isolation.**
Replicate §4.2 (Sweep) under S2 with sampling regime aligned to
§4.3 (9 conditions × 111 samples, stratified, mod-9 interleaved).
**Boot design:** Q3a re-collects both L1 and L2 measurements
within the same boot identity (same boot session, sequential
mode-switching). This avoids the boot-stability confound that
would arise from comparing Q3a's new L1 measurement (e.g.,
multi-boot) to §4.3's L2 measurement (single-boot). Estimated
wall-clock: ~10 hours (≈6 hours for an L1-only single-boot
replication of §4.2 plus ~4 hours added by re-collecting L2
within the same boot identity), justified by removing the
boot-identity confound from Q3b's downstream re-analysis.
Resolves: workload-class effect vs instrument effect decomposition.
Q3a is designed to support both workload-class isolation (its
primary outcome) and the Q3b cycle-invariance re-analysis
(pre-registered secondary use); Q3d's stratification frame is
also derivable from Q3a's design (pre-registered tertiary use).

**Q3b — Cycle-unit invariance generalization within S2.**
Q3b re-analyzes the Q3a dataset alongside §4.3's L2 data: compare
Δ*_L1(S2) vs Δ*_L2(S2) in cycle units. No additional measurement
needed. Resolves: cycle-unit invariance within S2 instrument.
Cross-instrument cycle invariance (S1 vs S2) requires Q3c, not
Q3b.

**Q3c — Paired S1/S2 instrument decomposition.**
Separate paired measurement: Sweep workload, fixed condition
(e.g., iter=4500), N=500 samples each under S1 and S2
instruments. **Boot design (pre-registered):** N_boot = 3 boots,
S1 and S2 measurements interleaved within each boot to control
boot-identity confound (each boot collects ~167 S1 + ~167 S2
samples, mode-switched in mid-boot). Total wall-clock ~3 hours
including boot setup overhead. Yields two outputs: (i) directly
measured σ_S1/σ_S2 ratio under matched workload (resolving the
ambiguity between the cross-experiment ~1.39× and the range-
estimator-inferred ~3×, see §4.1); (ii) quantitative decomposition
of σ_S1 vs σ_S2 into mean-shift and variance-overlay components
(§2.1 joint contribution disclaimer). Required as separate
experiment because paired same-condition S1/S2 design is not
extractable from Q3a.

**Q3d — Sampling-regime non-confounding validation.**
Q3d re-analyzes Q3a's stratified data alone, comparing
within-stratum σ̂ (from Q3a's iter=0 condition, n≈111) to
flat-pooled σ̂ (Q3a's iter=0 condition treated as a single
stratum, ignoring its place in the 9-condition mod-K
interleaving). If within-stratum σ̂ ≈ flat-pooled σ̂ on the
same data, sampling regime is non-confounding. This is a
clean within-experiment comparison; an earlier draft proposed
re-analyzing §4.1 (flat) alongside Q3a (stratified), but those
two experiments differ on three axes (instrument, guest-workload,
sampling regime), so sampling regime would not be identifiable
from that pair. Resolves: sampling-regime non-confounding
assumption (§2.3). No additional measurement needed.

**Compatibility matrix.**

| Sub-Q | Question | Data source | Additional experiment? |
|-------|----------|-------------|------------------------|
| Q3a | Workload-class isolation | New: Sweep under S2, stratified | Yes |
| Q3b | Cycle invariance within S2 | Q3a output + §4.3 | Re-analyze only |
| Q3c | S1/S2 decomposition | New: paired S1/S2 fixed-condition | Yes |
| Q3d | Sampling-regime validation | Q3a iter=0 within-stratum vs flat-pooled | Re-analyze only |

**Total experimental cost:** two new measurement campaigns (Q3a
~10 hours including boot-identity discipline, Q3c ~3 hours with
N_boot=3). Estimated 13 hours wall-clock. Q3b and Q3d are
analytical re-derivations; no instrument time required.

**Coupling without conflation.** Q3a's output is used by both
Q3b (cycle invariance) and Q3d (regime validation), but these
are distinct analytical questions over the same data, not a
single experiment claimed to resolve four questions. Q3c is
methodologically separate.

### 5.3 Coverage limitations

- Workload classes characterized: L1-resident, L2-resident only.
  LLC (8 MB) and DRAM (64 MB) not yet measured (EPT huge-page
  support required, 1–2 day implementation cost).
- Cross-boot stability for the Workload Class experiment: single-
  boot result; cross-boot generalization (N ≥ 5 boots) not yet
  measured.
- Sigmoid functional form: logistic SSE used; scipy NLS re-fit for
  publication polish pending (R² 0.9984 → 0.999+).

### 5.4 Tail asymmetry observation

The TSC Reorder Noise Floor entry observed asymmetric outlier
tails (low tail extends further than high). The α=0.05
detection criterion tests one-sided shifts above baseline; this
is appropriate for the perturbation-injection direction (positive
shift). The asymmetric tails affect the realized one-sided
false-positive rate even in the positive-direction test (cf.
§2.7 approximation note); for our lower-tail-heavier observation,
the realized rate is conservative (< nominal α=0.05) — the
upper-tail mass beyond μ + 1.645σ is **less** than under a
symmetric Gaussian, so fewer false detections than nominal.

**Empirical 95th percentile vs analytical threshold.** To
quantify the conservatism, we compare the empirical 95th
percentile of the iter=0 baseline distribution to the analytical
z=1.645·σ̂ threshold:

- **boot_log8** (S1, CPUID-VMCALL, n=978 post-warmup):
  - mean = 18,581,659 cycle
  - σ̂ = 6,386 cycle
  - Empirical p95 − μ = 8,493 cycle
  - Analytical 1.645·σ̂ = 10,505 cycle
  - Ratio (empirical/parametric) = 0.808 — **parametric
    threshold is 19% above empirical p95**
- **boot_log12 iter=0** (S1, L1-pchase, n=108 post-warmup):
  - mean = 18,582,928 cycle
  - σ̂ = 5,518 cycle
  - Empirical p95 − μ = 6,165 cycle
  - Analytical 1.645·σ̂ = 9,077 cycle
  - Ratio (empirical/parametric) = 0.679 — **parametric
    threshold is 32% above empirical p95**
  - (Note: at n=108, the 95th percentile sits at rank ≈ 103–104,
    a noisy order-statistic estimate.)

**Realized false-positive rate.** Two estimates compared:

*Direct empirical count* (exact, from raw data):
- boot_log8: 6/978 samples above parametric threshold
  μ + 1.645·σ̂ = 18,592,164 → **realized α = 0.61%**
  (n=978 yields a Clopper-Pearson 95% CI of [0.22%, 1.33%] —
  tight, well below nominal 5%.)
- boot_log12 iter=0: 3/108 samples above parametric threshold
  μ + 1.645·σ̂ = 18,592,005 → **realized α = 2.78%**
  (n=108 yields a Clopper-Pearson 95% CI of roughly
  [0.58%, 7.91%] — noisy but with upper bound still below
  nominal 5%; the point estimate is consistent with
  boot_log8's conservatism.)

*Linear first-order estimate* (0.05 × empirical/parametric ratio):
- boot_log8: 0.05 × 0.808 ≈ 4.04%
- boot_log12 iter=0: 0.05 × 0.679 ≈ 3.40%

**Discrepancy: linear estimate overshoots direct count, especially
for boot_log8 (6.6× overshoot).** The linear estimate assumes
uniform tail density beyond p95, but the actual upper tail
**thins rapidly past p95** — it is not merely shorter than
Gaussian, it is functionally different in shape (rapid drop-off
rather than gentle decay).

The parametric z-test is therefore even more conservative than
the linear estimate suggests: realized α is well below nominal
5%, with boot_log8 indicating the z-test is **~8× conservative**
at this workload (5% / 0.61% ≈ 8.2). For boot_log12 the
conservatism is milder (~1.8×) but still definite.

**Asymmetric-tail shape is itself guest-workload-type
covariant.** The two ratios (0.808 for CPUID-VMCALL, 0.679 for
L1-pchase) differ measurably in p95 magnitude. Additionally, the
**rate at which the tail thins past p95** differs between the
two workloads — CPUID-VMCALL's tail drops off sharply (6.6×
overshoot of linear estimate), L1-pchase's tail drops off more
gently (1.2× overshoot). This is an **ancillary observation
supporting §3.2 prior counter-evidence**: not only does
σ̂_baseline covary with guest-workload type (the §3.2 claim),
not only does the **p95 magnitude** of asymmetric tail covary,
but the **functional shape of the tail past p95** is also
workload-dependent. Pchase's deterministic execution profile
yields a less abrupt upper-tail cutoff than the branchy,
I/O-touching CPUID-VMCALL handler. Detection criterion
conservatism is therefore not uniform across workload types — a
second-order dependency that the §3.2 conjecture's
instrument-invariance narrowing does not yet address.

For symmetric or negative-direction perturbation tests, an
explicit non-Gaussian noise model would be required; deferred.

---

## 6. Implications

This section specifies how MI is consumed by adjacent
artifacts: the replay verdict interpretation pipeline, the
paper text, and the forthcoming Counterfactual Soundness Theorem
(CST). Each subsection distinguishes **frozen** content
(interface contract, stable across downstream evolution) from
**evolving** content (binding points, subject to revision when
downstream artifacts finalize).

### 6.1 For replay verdict interpretation

**Frozen.**

- The detection threshold formula $\Delta^* = z_{1-\alpha} \cdot
  \hat{\sigma}_{\text{baseline}}$ (§3.1, §2.7) is the bound any
  replay-verdict consumer uses to classify a timing-domain delta
  as "above instrument noise (P_detect > 0.5)" or "within
  instrument noise (P_detect < 0.5)" — a probabilistic
  classification at the P=0.5 inflection per §3.1, not a hard
  threshold.
- σ̂_baseline must be calibrated **per-experiment** (§2.4); a
  consumer applying MI cannot borrow σ̂_baseline from a separate
  experiment without re-establishing the antecedents in §3.3.
- Default convention is one-sided α = 0.05 (§2.7); alternative α
  triggers recomputation per §2.7 parameterization.
- **Slope fit admissibility (consumer-side check).** Consumer
  must verify the (instrument, workload class, guest-workload
  type) tuple's slope fit satisfies R² ≥ 0.99 (§2.5) and that
  calibration σ̂_baseline matches the consumer's guest-workload
  type (§3.2 conjecture scope) before applying δ* in iter units.
  Below R² threshold, iter-unit δ* is inadmissible; cycle-unit
  Δ* requires the §3.2 conjecture, which is forward-looking —
  therefore MI is not yet applicable for the workload class
  until either R² ≥ 0.99 is established or Q3b validates the
  conjecture.

**Evolving.**

- The mechanism by which the replay machinery emits
  threshold-relevant signals (per-event delta vector, calibration
  state, instrument identifier) is not yet specified in the EXTp
  trace format. Subject to revision when the replay tool's
  output schema finalizes.

### 6.2 For paper framing

**Frozen — citation conventions.**

- Every single-number MI threshold citation in the paper text
  must carry an instrument label, a workload class label, and a
  guest-workload type label (e.g., "Δ\* ≈ 7,574 cycles (S2,
  L2-resident, pchase)"). Unlabeled or partially labeled
  citations are forbidden.
- The cycle-invariance conjecture (§3.2) must be cited as a
  conjecture, not a theorem; cross-reference to §1.3 scope
  qualifier is required at first paper-text mention.
- Negative-framing rules (forbidden interpretations):
  - MI threshold values shall not be cited without all three of:
    instrument, workload class, and guest-workload type labels.
  - The cycle-invariance conjecture shall not be referenced as
    instrument-invariant.
  - The cycle-invariance conjecture (§3.2) shall not be cited
    as "empirically supported within S2" until Q3b validation;
    its current status is forward-looking.
  - The S1-vs-S2 gaps in §4.3 (28% CPUID-VMCALL vs L2-pchase;
    17% L1-pchase vs L2-pchase) shall not be attributed to a
    single source without invoking the §2.3 non-confounding
    assumption.
  - MI shall not be described as extending SOE; MI dimensions
    SOE's complement (§1.3).

**Evolving.**

- Specific paper section numbers and figure references that cite
  MI results. Subject to revision when the paper outline
  finalizes.
- **Δ notation disambiguation.** The vault entry uses Δ for three
  distinct quantities (raw timestamp delta in §2.2, induced mean
  shift b·δ in §2.6, detection threshold z·σ in §3.1); context
  disambiguates within the entry. Paper text should adopt explicit
  subscripts (e.g., Δ_raw, Δ_shift, Δ*) at first use of each
  quantity to prevent reader confusion.

### 6.3 For Counterfactual Soundness Theorem

**Frozen — interface contract.**

CST will consume the following quantities from MI:

- $\hat{\sigma}_{\text{baseline}}$ (§2.4) — significance floor
  for intervention-effect detection
- $b$ (§2.5) — cycle/iter conversion for any iter-domain
  intervention magnitude
- $\Delta^*$ (§3.1, §3.2) — detection threshold; intervention
  effects below this magnitude are not separable from instrument
  noise
- R² ≥ 0.99 acceptance criterion (§2.5) — workload class
  admissibility test for any CST experiment
- **Admissibility tuple** — (instrument, workload class,
  guest-workload type) all three must match the calibration
  conditions used to derive σ̂_baseline and b. The §3.2 conjecture
  is scoped to fixed guest-workload type; CST interface checking
  only workload class would silently violate this scope.

CST's intervention magnitudes that fall below $\Delta^*$ for the
relevant workload class are, by MI's claim, indistinguishable
from instrument noise; CST must either accept this as a null
result or escalate intervention magnitude.

**Evolving.**

- CST's specific composition formulas (how MI's quantities enter
  CST's significance bound, how multiple intervention points
  combine, how CST handles cross-instrument significance) are
  out of scope here. CST's consumption formulas will be
  specified in the CST entry; this section locks only what MI
  provides, not how CST uses it.
- **Direction caveat.** MI's Δ* is **one-sided** (positive shifts
  only, §2.7). CST interventions in negative direction (e.g.,
  cache prefetch reducing latency) require independent threshold
  derivation; MI's z_{1-α} formula does not directly transfer to
  bidirectional or negative-only tests. CST entry must derive
  its own two-sided or inverse threshold if the intervention
  design requires it.

---

## 7. Files

**Adjacent property entries (cross-referenced):**

- `Capability_Separation_Theorem.md` — §1.1 hierarchy, §5.1
  capability concession reference
- `Strong_Observational_Equivalence.md` — §1.1 hierarchy, §1.3
  observable surface complement
- `Cross_Boot_Stability_N34.md` — §1.1, §1.2 score_S = 1.0000
  across boot boundaries

**Empirical antecedents (this property's premises):**

- `TSC_Reorder_Noise_Floor.md` — Premise P1 (§4.1); σ_baseline
  characterization for S1 instrument, frequency drift
  falsification, asymmetric tail observation
- `MI_Detection_Threshold_Sweep.md` — Premise P2 (§4.2); sigmoid
  detection curve fit, x_0 = 2,520 iter, k = 635 iter, R² = 0.9984
  under S1, L1-resident workload
- `MI_Workload_Class_Sensitivity.md` — Premise P3 (§4.3); L2
  slope = 15.194 cycle/iter, R² = 0.99994, slope-mediated
  scaling validation under S2

**Build configuration:**

- `KernelX86DangerousMSR=ON` — research builds only; production
  builds disable (§5.1)
- `EXTP_NUM_RUNS_OVERRIDE` — per-experiment N control
- `EXTP_INNER_WARMUP_SAMPLES=20` — sampling regime constant (§2.3)

**Modified source paths:**

- `projects/sel4test/apps/extp-vmm/src/trace/event.c` — bare RDTSC
  in production (post-revert); LFENCE-RDTSC sandwich preserved
  as `extp_tsc_sandwich()` opt-in helper
- `projects/sel4test/apps/extp-vmm/src/trace/timing.c` — RDMSR
  wrapper (research mode)
- `projects/sel4test/apps/extp-vmm/src/main.c` — sweep mode runtime
  parameter, mod-K interleaving
- `projects/sel4test/apps/extp-vmm/include/guest/chain.h` —
  pointer-chase primitive

**Forward references:**

- Counterfactual Soundness Theorem entry (forthcoming) —
  interface contract per §6.3
- Paper text (forthcoming) — citation conventions per §6.2

**Reproducibility (hardware identity):**

The σ̂_baseline values in §4.1 and the sigmoid fit parameters in
§4.2 are conditional on the following hardware configuration:

- **CPU:** Intel 12th Gen Core (Alder Lake architecture)
- **Microcode revision:** `0x3e` (early-2022 baseline; Spectre v2
  and pre-Downfall MDS mitigations active; later mitigations
  including Downfall/Reptar/INCEPTION absent. LFENCE
  microcode-dispatch cost under this revision is the basis of
  the S1 σ̂ elevation observed in §4.1.)
- **Motherboard:** ASUS Z690
- **Firmware:** UEFI BIOS
- **Boot environment:** bare-metal seL4 (no Linux host); seL4
  VMM boots directly via UEFI
- **Serial console (out-of-band logging):**
  - DIGITUS USB-Serial Adapter (FTDI FT232RL, USB-C to DB9)
  - Digitus DS-30000-1 PCIe Serial card (MCS9901, 2-port DB9
    add-on)
  - RS-232 null modem cable (DB9 female-to-female)

Microcode revision dependency is non-trivial: σ̂_S1 (sandwich)
elevation in §4.1 depends on the LFENCE dispatch cost under the
specific microcode. Reproduction under newer microcode revisions
(e.g., 0x12B+ with Downfall mitigation) may yield different σ̂_S1
values; σ̂_S2 (bare RDTSC) is less sensitive to microcode
revision since it bypasses the LFENCE microcode dispatch path.

Raw delta logs for the experiments referenced here:

- `boot_log8` — TSC Reorder Noise Floor, S1, CPUID-VMCALL,
  N=1000 (998 post-warmup)
- `boot_log12` — Detection Threshold Sweep, S1, L1-pchase,
  9 conditions × 111 samples (108 post-warmup per condition)
- `boot_log14` — Workload Class Sensitivity mini-probe, S2,
  L1+L2 pchase, iter=4500 fixed, n=109 per condition
- `boot_log15` — Workload Class Sensitivity main, S2,
  L2-pchase, 9 conditions × 111 samples

Analysis pipeline (raw delta extraction, σ computation, sigmoid
fit): `analyze_noise_floor.py` (TSC Reorder Noise Floor), Workload
Class entry's analysis script (forthcoming vault commit).
