# Counterfactual Soundness Theorem

## 1. Background and Scope

### 1.1 Position within property hierarchy

The Counterfactual Soundness Theorem (CST) is the **fourth and
final formal property** in the EXTp framework, completing the
property hierarchy:

| # | Property | Type | Function |
|---|----------|------|----------|
| 1 | Capability Separation Theorem | observable | Bounds intervention authority surface |
| 2 | Strong Observational Equivalence (SOE) | observable | Establishes 4-tuple replay determinism (score_S = 1.0000, N=34) |
| 3 | Measurement Interference (MI) | observable | Quantifies timing-domain noise floor and detection threshold $\Delta^*$ |
| 4 | **Counterfactual Soundness Theorem (CST)** | **binding** | **Composes P1–P3 into causal-attribution sufficiency** |

The first three properties are **observable**: each makes
empirically testable claims about a specific dimension of the
replay framework (authority, observability, timing noise). They
are independently meaningful — each can be stated, validated,
and cited on its own.

CST is **structurally different**: it is a **binding** (or
meta-) property. CST does not make a new empirical claim about
the replay framework; it asserts that the three observable
properties, in composition, are **sufficient to ground
counterfactual causal attribution claims** within explicitly
enumerated epistemic bounds. CST's content is the **composition
closure** of the property hierarchy.

This positional difference matters for how CST is read:

- *Reading CST as if it were observable* (looking for "the
  empirical measurement CST makes") leads to confusion — CST
  does not measure anything new.
- *Reading CST as binding* (looking for "how P1, P2, P3 combine
  to ground causal claims") gives the correct mental model — CST
  is the formal statement of what P1+P2+P3, together, license.

In the property-stack analogy: P1, P2, P3 are *layers* providing
specific guarantees; CST is the *header* that types those layers
into a coherent causal-attribution interface. Without CST, P1–P3
remain three independent guarantees with no formal statement of
their combined epistemic content.

### 1.2 Motivation

Counterfactual reasoning in systems security — "if input X had
been different, would exploit E have triggered?" — is widely
used informally but lacks a rigorous foundation in most
empirical work. The standard practice is to *re-run* an exploit
with modified inputs and observe whether the outcome changes,
treating any observed difference as causal attribution. This
practice has three well-known gaps:

1. **Coincidence.** The observed difference may be due to
   spontaneous noise (non-deterministic replay), not the input
   change.
2. **Confounding.** The replay machinery itself may produce
   side-effects on shared resources, conflating the input
   change's causal effect with the replay machinery's
   side-effects.
3. **Silent processes.** The actual causal pathway may be a
   microarchitectural process not visible at the gross
   observable surface (e.g., a cache state change that
   produces the same output but for a different reason).

Pearl's structural causal model (Pearl 2009) and Halpern-Pearl's
actual-causation framework (Halpern and Pearl 2005) provide
philosophical and mathematical machinery for addressing these
gaps — *do*-calculus, modularity, faithfulness, AC1/AC2/AC3
conditions. But Pearl's apparatus is *probabilistic and
abstract*: it operates on distributions over latent variables
and idealized structural equations, not on concrete
microarchitectural traces with measurable noise floors.

The gap between Pearl's apparatus and practical exploit analysis
is large enough that, in practice, the former is rarely cited
and the latter is rarely rigorous. CST closes this gap by
providing a **technical substrate** that makes Pearl-style
causal claims *empirically realizable* on bare-metal exploit
replay:

- The *do*-calculus operator $do(X = x')$ is realized by EXTp's
  intervention machinery (§2.2).
- Modularity (Pearl's effectiveness + composition axioms) is
  realized by Capability Separation (P1) bounding intervention
  authority.
- Observational completeness (HP's AC2) is realized by SOE
  4-tuple agreement (P2) extended with MI's timing surface (P3),
  modulo an explicit silent-leak scope-out.
- Faithfulness is *replaced* by determinism (A4): under EXTp's
  deterministic replay (score_S = 1.0000, N=34), Pearl's
  probabilistic faithfulness is strictly weakened — trajectory-
  level reproducibility is stronger and more directly verifiable.
- Confounder boundedness (Pearl's noise/latent-variable
  treatment) is realized by MI's quantified detection threshold
  $\Delta^*$ with empirically validated realized FPR
  (0.6%–2.8%, MI §5.4).

CST formally states that this composition is *sufficient* to
ground causal-attribution claims about exploit traces, within
explicit epistemic bounds. The motivation, in one line: CST is
the formal bridge between Pearl's causal apparatus and EXTp's
operational machinery.

### 1.3 What CST claims and does not claim

This subsection enumerates CST's positive and negative claims at
the highest level, for reviewer orientation. Detailed scope
restrictions are in §3.4.

**CST claims:**

- Under assumptions A1–A4 (Modularity, Observational completeness
  modulo silent leak, Confounder boundedness, Replay
  determinism) holding for a specific (hardware, microcode,
  instrument, workload class, guest-workload type)
  configuration, atomic interventions $do(X = x')$ in EXTp's
  validated intervention surface produce divergences on the SOE
  4-tuple + MI timing surface that constitute **sound
  deterministic actual-causation assertions** within the
  enumerated epistemic envelope $\mathcal{E}$.
- Pearl's effectiveness and composition axioms (modulo A1
  validation status) and Halpern-Pearl's AC1 and AC2 conditions
  are **satisfied** by every CST-admissible atomic claim.
- Compositional claims (chains of atomic interventions) preserve
  admissibility under per-step independent verification.
- CST is **strictly stronger than Pearl's faithfulness** in the
  determinism dimension; trajectory-level reproducibility
  substitutes for probabilistic conditional-independence testing.

**CST does not claim:**

- A mitigation efficacy framework. "Mitigation M would have
  prevented exploit E" is a downstream application, not a CST
  claim; CST establishes the *substrate* for such claims, not
  their content.
- A sensitivity characterization. "Exploit E is robust to
  input parameter variation in range [a, b]" is a downstream
  application (systematic intervention sweep with admissibility-
  bounded results); CST grounds it but does not perform it.
- A complete causal-modeling framework. CST yields **causal-link
  claims**, not causal-explanation claims (§2.4.4 chain-vs-
  mechanism distinction). Halpern-Pearl AC3 minimality is out
  of CST v1.0 scope.
- Cross-configuration soundness. CST is single-configuration by
  construction (§2.1); cross-microcode, cross-VMM,
  cross-kernel-version comparisons require a separate property.
- Multi-VCPU coverage. Concurrent execution breaks A4
  determinism; CST v1.0 covers single-threaded VM-exit traces
  only.
- Silent microarchitectural divergence detection. Cache, branch
  predictor, TLB state changes without 4-tuple or timing
  manifestation are explicitly scope-excluded; CMD (§5.2) is
  scheduled future work.
- Strict modularity without empirical validation. A1 is
  currently asserted modulo bounded side-effects below
  $\Delta^*$; Q4 future experiment (§5.1) addresses this gap.

**Scope qualifier (CST v1.0).** Every CST claim is stamped with
envelope version v1.0 (§3.4.5). Future versions expand coverage
as Q4 resolves, CMD is developed, additional intervention
surfaces are validated, and workload classes are calibrated.
Paper text citing CST must declare the envelope version per
§6.2 citation discipline.

CST is **the binding theorem of EXTp's property hierarchy**, not
a complete account of counterfactual causal inference in
systems security. The bounds are the price of empirical
realizability; the soundness within those bounds is what CST
claims.

---

## 2. Definitions

### 2.1 Counterfactual replay

A **counterfactual replay** is the re-execution of an exploit
trace with a controlled modification (an **intervention**) to one
or more parameters of the trace, under EXTp's deterministic
replay guarantee (SOE).

Two traces are involved:

- **Original trace** $T_{\text{orig}}$ — captured execution of the
  exploit on the bare-metal seL4 VMM, recorded as a sequence of
  observable events on the SOE 4-tuple surface (rip, exit_reason,
  exit_qual, rax) plus per-event timing $\Delta$ (MI §2.2).
- **Counterfactual trace** $T_{\text{cf}}$ — re-execution of
  $T_{\text{orig}}$ in a fresh boot session, with one or more
  parameters perturbed by an intervention $do(X=x')$ (defined
  formally in §2.2).

Under EXTp's framework, in the absence of intervention,
$T_{\text{cf}}$ matches $T_{\text{orig}}$ event-by-event on the
SOE surface (score_S = 1.0000 across N=34 cross-boot trials,
Cross_Boot_Stability_N34). Any divergence between $T_{\text{cf}}$
and $T_{\text{orig}}$ is therefore attributable to the
intervention, modulo the scope restrictions enumerated in §3.4.

**Trace indexing.** A trace $T$ is a finite sequence of events
$[e_0, e_1, \ldots, e_n]$ where each $e_i$ carries the SOE
4-tuple $(\text{rip}_i, \text{exit\_reason}_i, \text{exit\_qual}_i, \text{rax}_i)$
and the per-event timing $\Delta_i$. The index $i$ refers to
event position within the trace; divergence detection is
**per-event** (event-level resolution), required because causal
attribution claims target specific events ("intervention $X$
affected event $i$").

**Divergence detection function.** The observable surface for
divergence detection is the combined SOE 4-tuple plus MI Δ*
timing surface:

$$D(T_{\text{orig}}, T_{\text{cf}}, i) = \underbrace{\big(\text{4-tuple}_i^{\text{orig}} \neq \text{4-tuple}_i^{\text{cf}}\big)}_{\text{SOE clause (deterministic)}} \;\;\lor\;\; \underbrace{\big(|\Delta_i^{\text{orig}} - \Delta_i^{\text{cf}}| > \Delta^*\big)}_{\text{timing clause (probabilistic)}}$$

where $\Delta^*$ is the MI detection threshold (MI §3.1)
calibrated for the (instrument, workload class, guest-workload
type) admissibility tuple (MI §6.3).

**OR-clause asymmetry.** The two clauses of $D$ have distinct
statistical natures:

- **SOE clause is deterministic.** Under SOE's score_S = 1.0000
  guarantee (Cross_Boot_Stability_N34), in the absence of
  intervention, the 4-tuple matches exactly event-by-event;
  non-zero 4-tuple delta is a genuine divergence with
  **false-positive rate zero** under A4 (§3.2).
- **Timing clause is probabilistic.** $\Delta^*$ corresponds to
  the $P(\text{detect}) = 0.5$ inflection (MI §3.1). Above
  $\Delta^*$, detection probability exceeds 0.5 but is bounded
  below 1; below $\Delta^*$, detection probability exceeds
  nominal $\alpha$ but is bounded below 0.5. The timing clause
  carries the false-positive rate of $\alpha$ (default 0.05;
  empirically realized 0.6–2.8% per MI §5.4 direct-count
  measurements).

**False-positive rate of $D$.** $D$ inherits its false-positive
rate **exclusively from the timing clause**; the SOE clause adds
none. Under default $\alpha = 0.05$, $D$'s nominal FPR is 0.05
per event; empirical realized FPR is substantially lower per MI
§5.4 (0.61% for CPUID-VMCALL workload, 2.78% for L1-pchase
workload — both well below nominal).

**Per-event vs trace-level FPR.** The $\alpha$ bound is
**per-event**: each event-indexed comparison carries the
specified false-positive rate. For a trace containing $N$
events, the expected number of false detections under no
intervention is $N \cdot \alpha$ (nominal) or $N \cdot
\alpha_{\text{realized}}$ using §5.4's direct-count values.
CST does **not** apply a family-wise correction (Bonferroni,
FDR) to per-event $D$ assertions; per-event atomic claims are
the primitive unit (§2.3). Trace-level aggregation —
combining per-event claims into a "trace-wide attribution" or
"exploit-as-a-whole was caused by intervention X" — is the
**consumer's responsibility** under the verdict interpretation
pipeline (§6.1 evolving aggregation strategy), and requires
applying the appropriate correction for the consumer's use
case (Bonferroni for strict family-wise control, FDR for
discovery-mode aggregation, or per-event-independent
attribution under the §2.3 compositional claim format).

**Single-configuration discipline.** Counterfactual replay is
**single-configuration by definition**: $T_{\text{orig}}$ and
$T_{\text{cf}}$ execute under the same hardware, microcode, VMM
build, and seL4 kernel version. Cross-configuration comparisons
(e.g., different microcode revisions, different kernel versions,
different VMM builds) fall **outside CST's epistemic envelope**
because assumptions A1–A4 are configuration-conditioned (§3.2):

- A4 (replay determinism) is configuration-conditioned —
  different microcode produces different deterministic
  trajectory; SOE's score_S = 1.0000 guarantee does not hold
  cross-config without separate validation.
- A2/A3 (observational completeness, confounder boundedness)
  depend on MI's $\Delta^*$, which is configuration-calibrated
  (different hardware $\rightarrow$ different $\hat{\sigma}_{\text{baseline}}$,
  different $b$).
- A1 (modularity) derives from Capability Separation, which is
  bound to the specific seL4 configuration's authority manifest.

Cross-configuration counterfactual reasoning would require a
separate property (e.g., "Cross-Configuration Soundness"), not
covered by CST.

**Fresh-boot discipline.** Each counterfactual replay
$T_{\text{cf}}$ executes in a **fresh boot session**, independent
from $T_{\text{orig}}$'s boot. This is a conservative
simplification:

- Within-boot counterfactuals would require validating that
  microarchitectural state (cache, branch predictor, TLB,
  MSR-resident state) is fully reset between intervention runs.
  VMCS reload alone does not reset SMM-level or microcode-level
  state; full reset machinery is not validated in this work.
- Cross-boot stability is established by Cross_Boot_Stability_N34
  (score_S = 1.0000, N = 34), which validates A4 (replay
  determinism) across boot boundaries. CST inherits this
  guarantee.
- Within-boot relaxation is **future work**, pending state-reset
  machinery validation.

**What counterfactual replay is not.** Counterfactual replay is
not exploit re-execution under different system conditions or
within-boot perturbation. The original and counterfactual traces
share all framework conditions except the explicitly controlled
intervention, and execute in separate boot sessions; under this
discipline, divergence isolates the intervention's causal effect.

### 2.2 Intervention model

An **intervention** $do(X=x')$ is a controlled modification to a
specific parameter $X$ of the trace, executed during the fresh
boot session of $T_{\text{cf}}$ (§2.1). This subsection defines
the intervention surface, scope, timing, and the relation to
Pearl's $do()$ operator.

**Intervention surface.** The set of parameters available for
intervention under EXTp's framework — i.e., the values of $X$
that the framework can perturb. Four classes are validated in
this work, organized along a **state-versus-temporal taxonomic
split**:

*State interventions* (modify framework or guest state directly):

- **Cache state** ($X = \text{cache\_state}$). Initial cache line
  occupancy (which lines are warm/cold) before a trace event.
  Requires EPT manipulation and explicit cache pre-loading.
- **Input value** ($X = \text{input}_j$). Value of the $j$-th
  input parameter passed from the guest to the hypercall or
  VM-exit handler.
- **Register state** ($X = \text{reg}_r$). Value of register $r$
  in the guest VMCS at a designated pre-event point.

*Temporal interventions* (modify the temporal profile of execution):

- **Iteration count** ($X = \text{nopcount}$). Number of pchase
  primitive iterations injected before a trace event. This is
  the perturbation primitive used in MI §4.2 (Sweep) and §4.3
  (Workload Class).

The state-temporal split matters for downstream analysis: state
interventions are expected to produce 4-tuple deltas (SOE clause
of $D$); temporal interventions are expected to produce timing
deltas (timing clause of $D$). Both clause types may fire for
either intervention class, but the **primary expected signal**
differs.

Each class has a distinct intervention machinery within the EXTp
VMM; the machinery is itself capability-mediated under
Capability Separation, ensuring intervention scope bounded
authority (foundation for A1, §3.2).

**Future-extension intervention surfaces.** Three additional
intervention classes are identified as future implementation
work, not part of CST v1.0:

- **Interrupt injection** — controlled timing and source of
  interrupt delivery to the guest.
- **EPT mapping flip** — modifying guest physical-to-host
  physical mappings mid-trace.
- **MSR write** — modifying model-specific register state
  visible to the guest.

CST's validity envelope (§3.4) covers the four current classes;
extension to future surfaces requires re-validation of A1
(modularity) on the new intervention machinery, since each new
machinery introduces a new authority surface that Capability
Separation must bound.

**Intervention scope (available scopes).** The granularity at
which $X$ is perturbed. **Per-event scope** is the only scope
validated in CST v1.0:

- **Per-event scope (validated).** $X$ is set to $x'$ exactly at
  event $e_i$ in the trace and reverts after the event. Smallest
  perturbation granularity. This is the scope at which MI's
  empirical antecedents (Sweep, Workload Class) operate.

The following scopes are **future work**, not part of CST v1.0:

- **Per-window scope (future).** $X$ is set to $x'$ across a
  contiguous range of events $[e_i, e_j]$. Used for
  cumulative-effect interventions (e.g., sustained cache
  pressure). Requires validation that per-window state
  maintenance does not violate A1 modularity.
- **Global scope (future).** $X$ is set to $x'$ for the entire
  trace duration. Used for environmental interventions (e.g.,
  elevated baseline noise floor). Requires validation that the
  global setting does not perturb framework-internal state
  beyond the intervention target.

CST v1.0 applies to **per-event interventions only**; the
validity envelope (§3.4) makes this restriction explicit.

**Intervention timing.** When during execution the intervention
takes effect:

- **Pre-trace.** Intervention is applied before $T_{\text{cf}}$'s
  execution begins (e.g., setting initial register state).
- **Mid-trace, pre-event.** Intervention is applied between
  event $e_{i-1}$ and event $e_i$ (e.g., injecting pchase
  iterations into the dispatch path).
- **Post-event.** Intervention is applied after event $e_i$
  retires, affecting only subsequent events.

The intervention model assumes interventions are **atomic**: a
single $do(X=x')$ operation completes before any observable
event is recorded.

**Compound interventions.** Multiple interventions in the same
$T_{\text{cf}}$ are modeled as an **ordered atomic sequence**:
$do(X_1=x_1')$ executes first to completion, then $do(X_2=x_2')$,
within the same fresh boot session.

**Commutativity is not assumed.** In general,
$do(X_1=x_1') \rightarrow do(X_2=x_2')$ may produce different
trace outcomes than $do(X_2=x_2') \rightarrow do(X_1=x_1')$,
because intervention $X_1$ may modify the state on which
intervention $X_2$ subsequently operates (e.g., a cache_state
preload followed by a nopcount injection sees a different
starting cache than the reverse order).

A specific pair $(X_1, X_2)$ may be **demonstrably commutative**
under EXTp — e.g., two register-state interventions on
non-overlapping registers — but commutativity is a property to
be established case-by-case, not a default. CST v1.0 reports
all compound interventions in their executed order; reordering
analysis is a per-case investigation, not a CST-wide guarantee.

**Relation to Pearl's $do()$ operator.** Pearl's $do(X=x')$
denotes an external action that forcibly sets $X$ to $x'$,
severing all incoming causal connections to $X$ in the underlying
causal model (Pearl 2009, p. 23–24, 70). EXTp's intervention
machinery operationalizes this severance through the four-class
surface above:

- For $X = \text{nopcount}$: the intervention overrides the
  iteration count that would have been determined by guest
  control flow. Guest's "intent" to execute $n$ iterations is
  severed; the framework imposes $n'$.
- For $X = \text{cache\_state}$: the intervention overrides the
  natural cache state evolution from prior events. The "what
  the cache would have been" is severed by explicit preloading.
- For $X = \text{input}_j$: the intervention overrides the input
  value the guest passed. The "what the guest sent" is severed
  by VMM-level rewrite.
- For $X = \text{reg}_r$: the intervention overrides the register
  state the guest would have established. The "what the guest
  computed" is severed by VMCS-level write.

In each case, the severance is realized via Capability
Separation's authority discipline: the intervention machinery
holds capabilities to modify $X$ that the guest does not, and
the modification is invisible to the guest's normal causal model
(guest reads the modified value as if it were natural).

**Effect propagation.** A $do(X=x')$ intervention produces two
classes of observable effects on $T_{\text{cf}}$:

- **Deterministic effects on the SOE 4-tuple surface.** Changes
  in rip, exit_reason, exit_qual, or rax at events causally
  downstream of $X$. These are detected by the SOE clause of
  $D$ (§2.1) with false-positive rate zero.
- **Probabilistic effects on the timing surface.** Changes in
  per-event $\Delta_i$ beyond $\Delta^*$. These are detected by
  the timing clause of $D$ with false-positive rate $\alpha$.

This effect-class distinction maps directly to the OR-clause
asymmetry in $D$ (§2.1) and grounds the assumption set in §3.2:
A2 (observational completeness) requires both classes to be
captured; A3 (confounder boundedness) addresses the timing
class's $\alpha$-bound.

**Intervention parameter space.** $X$ ranges over parameters
defined **within a single configuration** (per §2.1
single-configuration discipline). Cross-configuration parameters
(microcode revision, kernel version) are not valid intervention
targets under CST; they would require a separate property
addressing cross-configuration soundness.

**What intervention is not.** EXTp's intervention is not
input fuzzing in the classical sense — there is no random
mutation operator. Each $do(X=x')$ is a **specific, named
modification** with a known target parameter and a known new
value, executed deterministically. Random/stochastic intervention
strategies are downstream applications, not part of CST's
primitive intervention model.

CST-grounded counterfactual fuzzing — using sequences of CST
interventions to systematically explore exploit input space with
causal-attribution-aware feedback — is a **natural downstream
application** of CST, distinct from primitive intervention. The
hook for this application is documented in §6.3 (demonstration
case requirements); the application itself is out of scope for
CST v1.0's formal claims.

### 2.3 Causal claim space

A **causal claim** under CST is a statement about the causal
relationship between an intervention $do(X=x')$ and an observed
divergence in the counterfactual trace. This subsection defines
the format of admissible claims, the distinction between atomic
and compositional claims, the validity scope notation, and the
explicit boundaries of what CST does and does not count as
"caused by".

**Atomic claim format.** The primitive unit of CST is the
**atomic causal claim**, written:

$$\mathcal{C}_{\text{atomic}} = \big\langle do(X=x') \rightsquigarrow_i D \;\big|\; A_1, A_2, A_3, A_4;\;\mathcal{E} \big\rangle$$

The components:

- $do(X=x')$ — the intervention performed on the counterfactual
  trace (§2.2)
- $\rightsquigarrow_i$ — the causal-implication operator at event
  index $i$ (read: "causally produces, at event $i$")
- $D$ — the divergence detection function output (§2.1):
  specifically, $D(T_{\text{orig}}, T_{\text{cf}}, i) = \text{true}$
- $A_1, A_2, A_3, A_4$ — the four assumptions (§3.2) that must
  hold for the claim to be valid
- $\mathcal{E}$ — the **validity envelope** (§3.4), parameterizing
  the configuration under which the claim is asserted
  (instrument, workload class, guest-workload type, scope, plus
  the validity-envelope inclusions/exclusions)

The atomic claim reads in English: "Under assumptions $A_1$
through $A_4$ holding within validity envelope $\mathcal{E}$,
intervention $do(X=x')$ causally produces the observed divergence
$D$ at event $i$."

**Operator distinction.** The $\rightsquigarrow_i$ operator is
CST-specific and must be distinguished from two adjacent operators
in the causality literature:

- **Lewis's counterfactual conditional** $\square\!\!\to$
  (Lewis 1973): "if $X$ had been $x'$, then $D$ would have
  occurred." Lewis's operator is **modal**, quantifying over
  possible worlds (closest world where antecedent holds).
  $\rightsquigarrow_i$ is **operational**: there is no quantifier
  over possible worlds; instead, $T_{\text{cf}}$ is the actual
  counterfactual trace produced by EXTp's intervention machinery,
  observed event-by-event. The "closest possible world" problem
  (which world counts as closest) is replaced by an empirical
  procedure (the fresh-boot replay of §2.1).
- **Pearl's distributional $do(\cdot)$** as in
  $P(D \mid do(X=x'))$ (Pearl 2009, ch. 3): a probability
  distribution over outcomes under the intervention. Pearl's
  expression averages over latent variables and stochastic
  variation. $\rightsquigarrow_i$ is **deterministic and
  trajectory-level**: under A4 (deterministic replay), there is
  no distribution to average over; $D$ either holds at event $i$
  or it does not, in the single observed counterfactual trace.

This operator distinction is the formal expression of the
restriction discussed at the end of this subsection
("CST's restriction is the price of empirical realizability"):
modal quantification and probabilistic distribution are both
replaced by direct empirical observation under EXTp's
deterministic replay.

**Compositional claim format.** Atomic claims compose into
**compositional causal claims** by sequential chaining:

$$\mathcal{C}_{\text{compound}} = \big\langle do(X_1=x_1') \rightsquigarrow_{i_1} do(X_2=x_2') \rightsquigarrow_{i_2} \cdots \rightsquigarrow_{i_n} D \;\big|\; A_1, A_2, A_3, A_4;\;\mathcal{E} \big\rangle$$

Each step of the chain is an atomic claim; the chain asserts a
**causal path** from the initial intervention $do(X_1=x_1')$
through intermediate effects to the terminal divergence $D$ at
event $i_n$.

**Important constraint.** Each chain step's atomic claim must be
**independently verifiable** — i.e., the compositional claim is
admissible only if every atomic claim in the chain is admissible
under its own validity envelope. Chains do not "inherit"
admissibility from each other; commutativity within the chain is
not assumed (§2.2).

**Validity envelope notation.** $\mathcal{E}$ is a tuple:

$$\mathcal{E} = (\text{instr}, \text{wl-class}, \text{gw-type}, \text{scope}, \mathcal{S}_{\text{in}}, \mathcal{S}_{\text{out}})$$

where:
- $\text{instr} \in \{S_1, S_2\}$ — MI instrument
- $\text{wl-class} \in \{L_1\text{-pchase}, L_2\text{-pchase}\}$ —
  MI workload class
- $\text{gw-type} \in \{\text{pchase}, \text{CPUID-VMCALL}, \ldots\}$
  — guest-workload type (MI §3.2)
- $\text{scope} \in \{\text{per-event}\}$ — intervention scope
  (CST v1.0: per-event only, §2.2)
- $\mathcal{S}_{\text{in}}$ — explicit in-scope conditions
  (§3.4 inclusions)
- $\mathcal{S}_{\text{out}}$ — explicit out-of-scope conditions
  (§3.4 exclusions)

A claim is **structurally invalid** if any component of $\mathcal{E}$
falls outside CST's coverage (e.g., $\text{wl-class} = \text{LLC-pchase}$
is outside CST v1.0's coverage per MI §5.3).

**What counts as "caused by" under CST.** A causal claim
$\langle do(X=x') \rightsquigarrow_i D \;|\; A_1, \ldots, A_4; \mathcal{E} \rangle$
is admissible iff:

1. Intervention $do(X=x')$ was performed per §2.2's intervention
   model (valid surface class, validated scope, atomic
   execution)
2. Divergence $D(T_{\text{orig}}, T_{\text{cf}}, i) = \text{true}$
   was observed on the §2.1 surface
3. Assumptions $A_1, A_2, A_3, A_4$ all hold for the
   configuration (§3.2)
4. Validity envelope $\mathcal{E}$'s in-scope conditions hold and
   out-of-scope conditions do not apply (§3.4)

If all four hold, the claim is **CST-admissible**: the divergence
$D$ is causally attributable to intervention $do(X=x')$ within
the explicit epistemic bounds of $\mathcal{E}$.

**Chain versus mechanism — important distinction.** The
compositional claim format (above) introduces a syntactic
construct that superficially resembles mechanism attribution
("$do(X=x') \rightsquigarrow_{i_1} \cdots \rightsquigarrow_{i_n} D$"
looks like "$X$ causes $D$ via intermediate events"). The
distinction matters and is sharp:

- **Chain (CST in-scope).** A compositional claim is a sequence
  of atomic claims, each of which is independently observable on
  the SOE 4-tuple + timing surface. Each $\rightsquigarrow_{i_k}$
  step asserts a divergence at event $i_k$ that is itself
  CST-admissible. The "intermediate effects" in a chain are
  **events**, observable, indexable, with their own atomic
  claims. A chain is an **observable causal pathway** through
  the trace.
- **Mechanism (CST out-of-scope).** A mechanism claim asserts
  that $X$ causes $D$ via an **unobservable process** —
  microarchitectural state evolution, control-flow internals
  between events, branch predictor updates, cache line evictions
  that do not register on the 4-tuple or exceed $\Delta^*$.
  Mechanism intermediaries are not events on CST's observable
  surface and are not addressable by atomic claims.

The compositional claim format captures **observable causal
pathways**, not mechanistic processes. A chain through events
$(i_1, i_2, \ldots, i_n)$ is admissible under CST; a mechanism
claim asserting an unobservable trajectory between events is not.
This distinction maps to the A2 scope-out (§3.2): silent
microarchitectural state evolution is precisely the class of
mechanism that CST cannot address.

**What does NOT count as "caused by" under CST.** The following
are **outside** CST's claim space:

- **Probabilistic causation.** Statements of the form "$do(X=x')$
  raises the probability of $D$" are not CST claims. CST operates
  on deterministic replay; probability statements would require
  ensemble averaging across stochastic trials, which contradicts
  A4 (deterministic replay).
- **Contributing causes.** Statements of the form "$do(X=x')$ is
  one of several factors causing $D$" are not CST claims. CST's
  atomic claim format attributes $D$ to a specific intervention;
  multi-factor attribution requires compositional chaining
  (§2.3 compositional claim format), not implicit aggregation.
- **Joint causation without explicit composition.** Statements of
  the form "$do(X_1=x_1')$ and $do(X_2=x_2')$ jointly cause $D$"
  are not CST claims unless reformulated as a compositional claim
  with explicit ordering and each atomic step admissible.
- **Mechanism claims.** Per the chain-vs-mechanism distinction
  above: statements of the form "$do(X=x')$ causes $D$ via
  mechanism $M$" where $M$ refers to an unobservable process
  (microarchitectural, control-flow internal) are not CST
  claims. CST captures observable causal pathways (chains), not
  mechanistic intermediates.
- **Counterfactual conditionals beyond intervention space.**
  Statements of the form "if $X$ had been $x'$, then $D$ would
  have occurred" where $X$ is not in CST's intervention surface
  (§2.2) — e.g., "if the kernel version had been different" —
  are not CST claims. CST's claim space is bounded by its
  intervention surface, and the intervention surface is bounded
  by Capability Separation's authority discipline.
- **Silent causation.** Effects of $do(X=x')$ that do not
  manifest on the SOE 4-tuple or exceed $\Delta^*$ in timing are
  **not detected** by $D$ and therefore are **not claimed** by
  CST. The A2 assumption (§3.2) explicitly scopes out silent
  microarchitectural divergence (cache state without timing
  manifestation, etc.); CST is **silent on silent effects**, not
  asserting their absence.

**Silent causation — three-threat decomposition (forward
reference).** A natural reviewer concern: "perhaps all observed
divergences are caused by silent processes, and CST is
mis-attributing them to the named interventions." This concern
decomposes into three distinct threats, each addressed
separately:

1. **Coincidence.** The divergence at event $i$ happens to
   correlate with $do(X=x')$ but is causally independent of it
   (e.g., a spontaneous timing fluctuation). Addressed by
   **A4 (deterministic replay)**: if the divergence were
   spontaneous, deterministic replay of $T_{\text{cf}}$ would
   not reproduce it; cross-boot stability (score_S = 1.0000,
   N=34) rules out this class of coincidence at the per-event
   resolution.
2. **Silent mechanism.** The divergence is caused by an
   unobservable microarchitectural process that $do(X=x')$
   happens to trigger, but the causal pathway is mechanistic
   rather than event-level. Addressed by **scope-honesty**:
   CST does not claim mechanism attribution, only event-level
   causal attribution (chain-vs-mechanism distinction above).
   If the silent mechanism does not produce an observable
   divergence (4-tuple or timing > $\Delta^*$), CST is silent;
   if it does produce one, the chain captures it as an
   observable pathway regardless of the underlying mechanism.
3. **Confounder.** The divergence is caused by a third factor
   correlated with both $do(X=x')$ and the observed outcome
   (e.g., a framework-internal state change triggered by the
   intervention machinery but not the intervention itself).
   Addressed by **A1 (modularity, modulo Q4 gap)**: Capability
   Separation bounds intervention authority, but the gap between
   "authority bounded" and "side-effect free" is a known
   limitation (§4.1 modularity gap, §5.1 Q4 future experiment).
   Until Q4 is resolved, the confounder threat is **partially
   addressed** rather than fully eliminated.

The full sketch proof in §3.3 addresses these three threats in
sequence under the A1–A4 assumption set.

**Claim space and Pearl correspondence.** The CST claim space is
a restricted subset of Pearl-style causal claim space (Pearl
2009, ch. 7). CST claims are deterministic, intervention-specific,
event-indexed, and envelope-bounded; Pearl claims may be
probabilistic, distribution-level, ungoverned by an explicit
envelope, or quantified over latent variables. CST's restriction
is the **price of empirical realizability**: every CST claim
corresponds to a concrete intervention with an observable
outcome, no latent variables, no probabilistic ensembles. This
restriction is detailed in §2.4 (Pearl correspondence).

### 2.4 Pearl do-calculus correspondence

CST's claim notation $\langle do(X=x') \rightsquigarrow_i D \mid A_1, A_2, A_3, A_4;\;\mathcal{E} \rangle$
uses Pearl's intervention operator $do(\cdot)$ as a syntactic
anchor, but operates in a regime that diverges from Pearl's
classical structural causal model (SCM, Pearl 2009) in two
structural respects:

1. **Determinism** — under A4 (replay determinism, §3.2),
   trajectories are fully determined by intervention and
   configuration; there is no probabilistic structure to apply
   Pearl's distributional machinery $P(y \mid do(x))$ directly.
2. **Linear-time execution** — interventions are forward-only
   and replays are non-rewindable within a single execution.
   Pearl's structural-model reasoning is *timeless* in the
   sense that intervention semantics are defined at the level
   of structural equations, not over a temporal trace.

This section maps Pearl's axiomatic apparatus (Pearl 2009,
Chapter 7.3) and his three rules of do-calculus (Pearl 2009,
Chapter 3.4) onto EXTp's machinery, identifying which
correspondences hold, which hold vacuously under determinism,
and which fail structurally. We further map the Halpern-Pearl
actual-causation framework (Halpern and Pearl 2005) onto CST's
claim form, since CST's atomic claim $\langle do(X=x') \rightsquigarrow_i D \mid A;\;\mathcal{E} \rangle$
is most naturally read as an actual-causation assertion rather
than a distributional intervention statement.

#### 2.4.1 Pearl's axioms of atomic intervention

Pearl 2009 (Definition 7.3.1) formulates three axioms governing
atomic interventions in the structural causal model:

- **Effectiveness.** For every variable $X$ and value $x$, the
  intervention $do(X = x)$ yields $X = x$ in the post-intervention
  state. The intervention is *successful* at setting the targeted
  variable.
- **Composition.** Holding a variable $W$ at its natural value
  $w$ while intervening to set $X = x$ produces the same outcome
  as just $do(X = x)$ alone, provided $W$'s value would naturally
  be $w$ under $do(X = x)$:
  $$Y_{x,w}(u) = Y_x(u) \quad \text{if} \quad W_x(u) = w$$
- **Reversibility.** For atomic interventions, if setting $X = x$
  and holding $W = w$ gives $Y = y$, and setting $X = x$ and
  holding $Y = y$ gives $W = w$, then setting $X = x$ alone gives
  $Y = y$ and $W = w$:
  $$Y_{x,w}(u) = y \;\text{ and }\; W_{x,y}(u) = w \;\Longrightarrow\; Y_x(u) = y,\; W_x(u) = w$$

#### 2.4.2 EXTp correspondence — atomic-intervention axioms

**Effectiveness — holds.** EXTp's intervention machinery (§2.2)
is designed to set the targeted parameter $X$ to the specified
value $x'$ at the intervention point. For the four validated
intervention classes (nopcount, register, input, cache),
$do(X = x')$ is operationally a value assignment: the value at
event $i$ is observed to be $x'$ after the intervention.
Effectiveness is the *value-setting* component of the
intervention. Note that effectiveness alone does not guarantee
that *no other variable* is affected — that is the modularity
claim (A1), captured separately in §3.2. Pearl's effectiveness
axiom and CST's A1 are *orthogonal*: effectiveness says the
intervention reaches its target; modularity says it reaches
*only* its target.

**Composition — holds modulo A1.** Pearl's composition axiom
requires that intervening on $X$ produces the same effect on $Y$
whether $W$ is explicitly held at its natural value $w$ or
allowed to evolve under $do(X = x)$. In EXTp, A1 (modularity)
directly underwrites this: if $do(X = x')$ is side-effect-free
on $W$ (A1 holds), then $W$ evolves to its natural value $w$
under $do(X = x')$ whether we externally pin it or not.
Composition therefore *inherits the validation status of A1*:
under A1 it holds; under A1's empirical-validation gap (§5.1
Q4 future experiment), composition is approximate.

**Reversibility — does not apply (structural divergence).**
EXTp's execution is *linear-time and irreversible*: once event
$i$ has occurred, the trajectory before $i$ cannot be rewound
within a single replay. Counterfactual replays generate
alternative trajectories by re-running from a fresh boot (§2.1),
but this is *not* equivalent to Pearl's reversibility, which
permits algebraic reversal of intervention semantics within a
single structural model. EXTp's machinery does not support the
"set $W = w$ to back out $Y = y$ and verify $X = x'$" reasoning
that reversibility presupposes. We therefore declare
reversibility **inapplicable** rather than satisfied: CST claims
do not invoke reversibility-style reasoning, and the absence of
reversibility in EXTp does not invalidate the framework — it
restricts CST's expressive scope to forward-time interventions
only.

This is a *concrete divergence point* from Pearl's classical
SCM. Authors familiar with Pearl 2009 should read CST claims as
operating in a **linear-time deterministic structural model**
rather than the static algebraic structural model of Pearl 2009.

#### 2.4.3 EXTp correspondence — do-calculus rules

Pearl's three rules of do-calculus (Pearl 2009, Theorem 3.4.1)
govern the manipulation of probability expressions involving
$do(\cdot)$:

- **Rule 1** (insertion/deletion of observations):
  $P(y \mid do(x), z, w) = P(y \mid do(x), w)$ if
  $Z \perp\!\!\!\perp Y \mid X, W$ in the manipulated graph
  $G_{\bar{X}}$.
- **Rule 2** (action/observation exchange):
  $P(y \mid do(x), do(z), w) = P(y \mid do(x), z, w)$ if
  $Z \perp\!\!\!\perp Y \mid X, W$ in $G_{\bar{X}\underline{Z}}$.
- **Rule 3** (insertion/deletion of actions):
  $P(y \mid do(x), do(z), w) = P(y \mid do(x), w)$ if
  $Z \perp\!\!\!\perp Y \mid X, W$ in $G_{\bar{X}\underline{Z(W)}}$.

Under A4 determinism, $P(y \mid do(x), z, w)$ collapses to a
$\{0,1\}$ indicator (the event $Y = y$ either occurs
deterministically under the intervention or does not). The
do-calculus rules apply in this degenerate-probabilistic form,
but the operational content is reduced:

- **Rule 1** holds *trivially*: under determinism, observations
  independent of $D$ in the post-intervention graph cannot
  change $D$'s deterministic value. EXTp's per-event
  observability surface (4-tuple + timing, §2.1) makes the
  relevant independence checks decidable at the trace level:
  events causally downstream of $D$ cannot affect $D$'s value.
- **Rule 2** maps to A1 + A4 jointly. Pearl's rule says
  observation can be exchanged with intervention under
  independence. In EXTp, A1 guarantees $do(Z = z')$ is
  side-effect-free, and A4 guarantees the resulting trajectory
  is the same as the trajectory in which $Z = z'$ is naturally
  observed (because no probabilistic divergence). Under A4, the
  conditional-independence requirement of Rule 2 collapses to
  trace-level independence: variables not on the trajectory
  dependency graph of $X$ and $Z$ are independent of $Y$ by
  determinism. The graph-theoretic check is replaced by
  trajectory-level forward-causality precedence (similar to
  Rule 3). The rule holds in a strong form: observation and
  intervention coincide under A1+A4.
- **Rule 3** holds under forward-time causal precedence. An
  intervention at event $j > i$ cannot affect event $i$ because
  event $i$ is fully determined by events $\leq i$ (A4
  trajectory determinism). The rule is satisfied without
  requiring a graphical independence check; it follows directly
  from temporal causal precedence.

Summary: do-calculus rules carry over to CST in a
*degenerate-deterministic form*. The rules are not the primary
inference apparatus for CST (CST operates by direct trajectory
comparison, not by algebraic manipulation of probability
expressions), but the correspondence ensures consistency:
operations that are valid under do-calculus in Pearl's framework
remain valid under CST's deterministic restriction.

do-calculus is an identification apparatus for inferring causal
effects from observational distributions; CST operates by direct
intervention, not by identification, so do-calculus rules serve
a different role in CST — consistency anchor, not inference rule.

#### 2.4.4 Halpern-Pearl 2005 actual-causation correspondence

CST's atomic claim form $\langle do(X = x') \rightsquigarrow_i D \mid A;\;\mathcal{E} \rangle$
reads more naturally as an *actual-causation* assertion than a
distributional one. Halpern and Pearl (2005) formalize actual
causation through three conditions (restated in their notation,
simplified for atomic interventions):

- **AC1.** The candidate cause $X = x'$ and the effect $\varphi$
  (here, the observable $D$ at event $i$) both hold in the
  actual world. In CST: the *actual world* for the claim is
  the counterfactual trace $T_{\text{cf}}$ — the world in which
  the intervention $do(X = x')$ was performed. $T_{\text{cf}}$
  exhibits the intervention condition $X = x'$ at the
  intervention point (by construction of §2.2) and $D = \text{true}$
  at event $i$ (when measured against the natural-baseline trace
  $T_{\text{orig}}$, in which $X = x_{\text{natural}}$ at the
  same point). Note the directionality: $T_{\text{orig}}$ is the
  *baseline* (no intervention, natural $X$); $T_{\text{cf}}$ is
  the *actual world* of the CST claim (intervention applied).
  AC1's "both hold" condition is satisfied jointly in
  $T_{\text{cf}}$: the intervention condition is set, and the
  divergence $D$ relative to baseline is observed.
- **AC2.** There exists an alternative assignment to $X$ such
  that, under counterfactual intervention, $\neg \varphi$ holds.
  In CST: the counterfactual replay $T_{\text{cf}}$ (with
  $do(X = x_{\text{natural}})$ substituted) exhibits divergence
  at event $i$ — i.e., the SOE 4-tuple or timing observable on
  $T_{\text{cf}}$ at event $i$ differs from $T_{\text{orig}}$'s.
  This is the *counterfactual sensitivity* condition.
- **AC3.** Minimality: no proper subset of the cause can be
  removed while preserving AC2. In CST: the intervention
  $do(X = x')$ is treated as an atomic cause; AC3 is not
  directly addressed at the primitive level. Compound
  interventions (§2.2) introduce sequenced causes, and
  minimality across the sequence requires separate consideration
  — flagged as future work in §5.

Under this mapping, the CST claim $\langle do(X = x') \rightsquigarrow_i D \mid A;\;\mathcal{E} \rangle$
asserts AC1 (effect observed) and AC2 (counterfactual
sensitivity) under the assumption envelope $A$. AC3 minimality
is *not* part of the CST atomic claim; it is a *post-hoc
analytical refinement* for compound chains.

This is consistent with CST's positioning as a binding theorem
rather than a complete causal-modeling framework: CST grounds
the *operational validity* of actual-causation assertions
(AC1 and AC2) under EXTp's machinery; it does not undertake the
additional minimality analysis that distinguishes "this is *the*
cause" from "this is *a* cause among several". Reviewer-level
distinction: **CST yields causal-link claims, not
causal-explanation claims.** The latter would require AC3
machinery, which is out of CST v1.0's scope.

Multi-cause scenarios under CST are addressed by compositional
claim enumeration (§2.3): each atomic step is independently
CST-admissible, and the chain explicitly enumerates causal
links rather than asserting minimality of a single cause.

**Chain enumeration vs link necessity.** Chain enumeration
captures the observable causal pathway; per-link necessity
(which of the enumerated links are required for the terminal
effect, and which are redundant) is a downstream analysis
requiring per-link counterfactual probe — running the chain
with each link individually removed and re-checking
admissibility. This is a *compositional refinement* analysis,
not part of CST v1.0's atomic claim. Reviewers asking
"which of the enumerated causes is the necessary cause?"
should be directed to per-link probe; CST itself does not
distinguish necessary from redundant links within a chain.

#### 2.4.5 Correspondence table

| Pearl/HP construct | EXTp correspondence | Status |
|--------------------|---------------------|--------|
| Effectiveness (Pearl 2009 Def. 7.3.1) | Intervention machinery (§2.2) sets target | **Holds** |
| Composition (Pearl 2009 Def. 7.3.1) | Inherits A1 modularity | **Holds modulo A1 gap** |
| Reversibility (Pearl 2009 Def. 7.3.1) | Not supported — linear-time execution | **Inapplicable (concrete divergence)** |
| do-calculus Rule 1 | Vacuous under A4 determinism | **Holds trivially** |
| do-calculus Rule 2 | A1 + A4 joint | **Holds in strong form** |
| do-calculus Rule 3 | Forward-time causal precedence | **Holds in strong form** |
| HP 2005 AC1 (effect occurs) | $D$ observed in $T_{\text{orig}}$ at event $i$ | **Direct** |
| HP 2005 AC2 (counterfactual sensitivity) | $D$ differs in $T_{\text{cf}}$ at event $i$ | **Direct — foundation of $\rightsquigarrow_i$** |
| HP 2005 AC3 (minimality) | Not addressed; compound chain future work | **Out of CST v1.0 scope** |

#### 2.4.6 Implications for CST claim space

The Pearl correspondence is **partial-and-concrete**: a subset
of Pearl's machinery (effectiveness, composition, do-calculus
rules) maps cleanly onto CST under A1–A4; a structural component
(reversibility) does not map at all and represents an explicit
scope restriction of CST relative to classical SCM; and the
Halpern-Pearl actual-causation conditions (AC1, AC2) underwrite
the *meaning* of $\rightsquigarrow_i$ while a third condition
(AC3 minimality) is deferred.

CST claims are therefore best understood as **deterministic,
forward-time, actual-causation assertions under a bounded
epistemic envelope** — a restricted but mechanically well-defined
subset of Pearl's broader causal-modeling apparatus. This
restriction is not a weakness but the price of empirical
realizability: CST trades Pearl's expressive generality for
direct operational validation against EXTp's machinery.

§3.1 will state CST's composition closure theorem within this
correspondence: under A1–A4, the atomic claim form
$\langle do(X = x') \rightsquigarrow_i D \mid A;\;\mathcal{E} \rangle$
satisfies Pearl-style effectiveness + composition and HP-style
AC1 + AC2, yielding a **sound (within enumerated bounds)
actual-causation assertion** about the EXTp trajectory.

### 2.5 Epistemic bounds notation

This subsection consolidates the notational conventions for
expressing causal claim validity envelopes — the bookkeeping
machinery that tracks under what conditions a CST claim is
admissible.

**Atomic claim form** (consolidates §2.3):

$$\mathcal{C}_{\text{atomic}} = \big\langle do(X = x') \rightsquigarrow_i D \;\big|\; A_1, A_2, A_3, A_4;\;\mathcal{E} \big\rangle$$

The angle-bracket notation $\langle \cdot \mid \cdot ; \cdot \rangle$
separates three layers:

- *Operational content* (before $\mid$): the intervention,
  causal-implication operator, and divergence
- *Assumption layer* (between $\mid$ and $;$): the four
  assumptions A1–A4 under which the claim is admissible
- *Envelope layer* (after $;$): the validity envelope
  $\mathcal{E}$ scoping the claim to a specific configuration

**Validity envelope tuple** (consolidates §3.4.1):

$$\mathcal{E} = (\text{instr}, \text{wl-class}, \text{gw-type}, \text{scope}, \mathcal{S}_{\text{in}}, \mathcal{S}_{\text{out}})$$

Six components, each constraining a different dimension of the
claim's coverage. Per §3.4 admissibility check, every component
must match CST v1.0's enumerated coverage.

**Bound parameter notation.**

When a claim's admissibility depends on a calibrated parameter
(MI's R², $\Delta^*$, $\hat{\sigma}_{\text{baseline}}$), the
parameter is named in $\mathcal{S}_{\text{in}}$ with its
calibration source. Examples:

- R² ≥ 0.99 — slope-fit acceptance criterion (MI §2.5)
- $\Delta^* = 9{,}077$ cycle — detection threshold for L1-pchase
  S1 (MI §3.1, calibrated against boot_log12)
- $\Delta^* = 7{,}574$ cycle — detection threshold for L2-pchase
  S2 (MI §4.3, calibrated against boot_log15)
- $\hat{\sigma}_{\text{baseline}} = 5{,}518$ cycle — noise
  floor for L1-pchase S1 (MI §4.1)
- $\hat{\sigma}_{\text{baseline}} = 4{,}604$ cycle — noise
  floor for L2-pchase S2 (MI §4.1)

The naming discipline allows reviewers to verify that the
claim's parameters match the calibration source.

**Assumption qualifier notation.**

When an assumption is asserted in a non-strict form, the
qualifier is attached to the assumption tag:

- $A_1^{\text{modulo}}$ — modularity asserted modulo bounded
  side-effects below $\Delta^*$ (current empirical status,
  §4.1.3)
- $A_2^{\text{modulo-silent-leak}}$ — observational completeness
  asserted modulo the enumerated silent leak class (§4.2.4)
- $A_3^{\text{empirical}}$ vs $A_3^{\text{nominal}}$ — which
  FPR bound is being cited (empirical 0.6%–2.8% vs nominal 5%,
  §4.3.4)
- $A_4^{\text{strict}}$ — replay determinism asserted in
  trajectory-level form (current status from
  Cross_Boot_Stability_N34)

Qualified tags are paper-text-citable: "the claim holds under
$(A_1^{\text{modulo}}, A_2^{\text{modulo-silent-leak}}, A_3^{\text{empirical}}, A_4^{\text{strict}})$"
gives a reviewer the complete assumption status at-a-glance.

**Failure-mode flagging convention.**

When a claim's admissibility check (§6.1) fails at a specific
stage, the failure is flagged with a structured tag:

- *envelope-mismatch error*: $\mathcal{E}$'s tuple components
  outside CST v1.0's coverage. Claim is *structurally invalid*.
- *assumption-incomplete error*: assumption validation reference
  missing or stale.
- *surface-empty error*: $D = \text{false}$ at the claimed
  event. Empty claims are structurally forbidden per
  Theorem 3.1's biconditional.
- *intervention-surface-mismatch error*: $X$ outside the four
  validated intervention classes.

These tags are used by the verdict interpretation pipeline (§6.1)
and should appear in paper text whenever a claim's
non-admissibility is discussed.

**Envelope version stamp.**

Every claim carries an envelope version stamp:
$\mathcal{E}_{\text{v1.0}}$ for CST v1.0 (current),
$\mathcal{E}_{\text{v1.1}}$ after Q4 resolution (§3.4.5), etc.
Paper text citations must use the versioned form per §6.2.

---

## 3. Theorem Statement

### 3.1 Composition closure (formal statement)

**Theorem 3.1 (CST Composition Closure, atomic case).**

Let $T_{\text{orig}}$ and $T_{\text{cf}}$ be counterfactual
replays under a single configuration (§2.1), with $T_{\text{cf}}$
generated by atomic intervention $do(X = x')$ (§2.2). Let $i$ be
a trace event index. Let $A = (A_1, A_2, A_3, A_4)$ be the
assumption envelope (§3.2). Let $\mathcal{E}$ be the validity
envelope (§3.4).

Under $A$ satisfied and $\mathcal{E}$ admitted, the atomic CST
claim

$$\big\langle do(X = x') \rightsquigarrow_i D \;\big|\; A;\;\mathcal{E} \big\rangle$$

holds iff $D(T_{\text{orig}}, T_{\text{cf}}, i) = \text{true}$,
where $D$ is the divergence predicate of §2.1.

Furthermore, the claim satisfies:

  (i)   Pearl's effectiveness axiom (§2.4.2): $do(X = x')$ sets
        $X$ to $x'$;
  (ii)  Pearl's composition axiom modulo A1 (§2.4.2): inheriting
        modularity validation status;
  (iii) Halpern-Pearl AC1 (§2.4.4): the effect $D$ occurs in
        $T_{\text{orig}}$;
  (iv)  Halpern-Pearl AC2 (§2.4.4): the effect $D$ differs in
        $T_{\text{cf}}$, establishing counterfactual sensitivity.

The CST claim therefore constitutes a sound deterministic
actual-causation assertion within the bounded epistemic envelope
$(A, \mathcal{E})$.

---

**Reading.** Theorem 3.1 states the **atomic case** of CST: a
single intervention $do(X = x')$ produces an observable
divergence $D$ at event $i$, and this divergence is causally
attributable to the intervention under the four-assumption set
and validity envelope.

The biconditional ("iff") establishes both directions of
attribution:

- **Necessary direction** (claim $\Rightarrow D = \text{true}$):
  a CST claim cannot be asserted without an observed divergence;
  empty claims ("$do(X = x')$ caused divergence" without
  divergence) are structurally forbidden.
- **Sufficient direction** ($D = \text{true} + A + \mathcal{E}
  \Rightarrow$ claim): an observed divergence, under the
  satisfied assumption set within an admitted envelope, suffices
  to ground the causal claim.

The four conformity conditions (i)–(iv) are the Pearl/HP
correspondence guarantees from §2.4: any claim admissible under
Theorem 3.1 simultaneously satisfies Pearl-style effectiveness +
composition (atomic-intervention axioms) and HP-style AC1 + AC2
(actual-causation conditions). This is the formal sense in which
CST is "Pearl-conformant under bounded epistemic envelope":
EXTp's machinery does not introduce causal-attribution moves
that violate Pearl's axiomatic apparatus; it restricts to a
deterministic, forward-time subset of that apparatus.

**Theorem 3.1 covers the atomic case only.** Compositional
claims — chains of atomic interventions producing a terminal
divergence (§2.3) — are addressed by an extension theorem in
§3.3 (sufficiency proposition and sketch proof). The
compositional extension does not introduce new assumptions; it
shows that A1–A4 carry through sequential composition under the
ordered-atomic-sequence discipline of §2.2.

**Forward references:**

- §3.2 — formal statement of assumptions A1, A2, A3, A4
- §3.3 — sufficiency proposition (extending Theorem 3.1 to
  compositional claims) and semi-formal sketch proof
- §3.4 — validity envelope $\mathcal{E}$ (in-scope / out-of-scope
  enumeration)
- §4 — evidence for each assumption, derived from upstream
  property entries
- §5 — concessions (modularity gap, silent leak, Pearl alignment,
  Isabelle deferral)

### 3.2 Assumptions

Theorem 3.1 is conditional on four assumptions, $A_1$ through
$A_4$. Each assumption is stated formally below, with its
upstream EXTp-property derivation indicated and a forward
reference to its evidence subsection in §4. The assumptions are
**configuration-conditioned**: they hold for a specific
(hardware, microcode, instrument, workload class, guest-workload
type) configuration; violations of any assumption invalidate the
CST claim within that configuration.

#### A1 — Modularity

**Statement.** For an atomic intervention $do(X = x')$ executed
under EXTp's intervention machinery, the intervention modifies
only the targeted parameter $X$ and its causal descendants in
the trace; framework-internal state outside $X$'s capability
authority scope is invariant under the intervention.

Formally: let $\mathcal{S}$ denote the framework-internal state
(VMM scheduler state, EPT structures, capability registers not
under $X$'s authority scope, MSR-resident state outside the
intervention surface). Then for any atomic intervention
$do(X = x')$:

$$\mathcal{S}(T_{\text{cf}}) = \mathcal{S}(T_{\text{orig}})$$

at every event $i$ in the trace, modulo the propagation of $X$'s
own causal effects through legitimate state-update paths.

**Pearl correspondence (§2.4.2).** A1 is the structural
realization of Pearl's modularity principle: $do(X = x')$ severs
incoming causal connections to $X$ without modifying the
structural equations governing variables outside $X$'s descendant
set.

**Upstream property.** Derived from Capability Separation Theorem
— intervention machinery operates within explicitly bounded
capability authority; values modifiable under intervention are
exactly those covered by the intervention machinery's capability
set, which is disjoint from framework-internal state.

**Known gap.** Capability Separation establishes authority
disjointness, not strict side-effect freedom. The intervention
machinery's *execution* (e.g., nopcount injection invoking VMM
scheduler time for the injection itself) may introduce bounded
side-effects on framework-internal observables. Empirical
validation of this gap is the subject of Q4 future experiment
(§5.1). Until Q4 is resolved, A1 is asserted **modulo bounded
side-effects of magnitude below $\Delta^*$ on framework
observables** — a scope restriction explicit in $\mathcal{E}$
(§3.4).

**Evidence:** §4.1.

---

#### A2 — Observational completeness modulo silent leak

**Statement.** Every causal effect of intervention $do(X = x')$
on the trace either:

  (i)  manifests on the SOE 4-tuple surface
       $(\text{rip}, \text{exit\_reason}, \text{exit\_qual}, \text{rax})$
       at some event $i$, **or**

  (ii) produces a timing deviation $|\Delta_i^{\text{cf}} - \Delta_i^{\text{orig}}| > \Delta^*$
       at some event $i$, **or**

  (iii) falls within the explicitly enumerated **silent leak
        class** (microarchitectural state changes — cache state,
        branch predictor state, TLB state — that produce neither
        4-tuple delta nor timing deviation above $\Delta^*$).

Formally, define the *observed effect set* of $do(X = x')$:

$$\mathcal{O}(do(X = x')) = \big\{\, i \,:\, D(T_{\text{orig}}, T_{\text{cf}}, i) = \text{true} \,\big\}$$

and the *true causal effect set* $\mathcal{C}(do(X = x'))$ as the
set of all events $i$ where $do(X = x')$ is a causal antecedent
of state change at event $i$. Then:

$$\mathcal{C}(do(X = x')) \setminus \mathcal{O}(do(X = x')) \subseteq \text{SilentLeak}$$

— the unobserved portion of true causal effects is contained
within the silent leak class.

**Pearl correspondence (§2.4.4).** A2 underwrites Halpern-Pearl
AC2 (counterfactual sensitivity): a counterfactual claim's
detectability requires that the effect manifests on the
observable surface. Pearl's classical AC2 assumes complete
observability; A2 weakens this to observability-modulo-silent-leak,
which is honest about EXTp's instrument set.

**Upstream property.** Derived from SOE entry (4-tuple surface
guarantee under fresh-boot determinism, score_S = 1.0000) and
MI entry (timing surface extension with quantified noise floor
$\Delta^*$). The union of these two surfaces is the *observable
surface* of CST.

**Known scope-out.** Silent microarchitectural divergence (cache
state, branch predictor state, TLB state) without timing
manifestation is **explicitly excluded** from A2's coverage.
Addressing this class requires microarchitectural counter
instrumentation (LLC miss rate, branch misprediction counters,
TLB miss counters) outside MI's current instrument set. Future
work pointer: **Counterfactual Microarch Divergence (CMD)** —
a separate property class scheduled for future development
(§5.2).

**Evidence:** §4.2.

---

#### A3 — Confounder boundedness

**Statement.** Measurement noise on the observable surface is
bounded:

  (i)  SOE clause: 4-tuple delta is detected with **zero
       false-positive rate** under SOE's deterministic agreement
       guarantee (score_S = 1.0000 across N=34 cross-boot
       trials, Cross_Boot_Stability_N34).

  (ii) Timing clause: timing delta is detected with
       **false-positive rate bounded by $\alpha$** (nominal 0.05,
       empirically realized 0.6%–2.8% per MI §5.4 direct-count
       measurements), within the calibrated workload class.

Formally, the divergence detection function $D$ (§2.1) satisfies:

$$\Pr[D = \text{true} \mid \text{no intervention effect}] \leq \alpha + 0 = \alpha$$

(the SOE clause contributes 0; the timing clause contributes
$\alpha$).

**Pearl correspondence.** A3 corresponds to Pearl's confounder-
boundedness requirement: causal claims require that observed
divergence is distinguishable from background noise.
$\Delta^*$ provides the quantified noise floor; $\alpha$ provides
the quantified false-positive bound.

**Upstream property.** Derived from MI entry: $\hat{\sigma}_{\text{baseline}}$
characterization per workload class (MI §4.1), $\Delta^* = z_{1-\alpha} \cdot \hat{\sigma}_{\text{baseline}}$
detection threshold (MI §3.1), empirical realized FPR per direct
count (MI §5.4).

**Known scope dependency.** $\Delta^*$ is calibrated for specific
workload classes (L1-pchase, L2-pchase) and guest-workload types
(pchase). Cross-class extrapolation (LLC/DRAM workloads) requires
$\hat{\sigma}_{\text{baseline}}$ re-measurement (MI §5.3).
Cross-guest-workload-type extrapolation (e.g., from pchase to
CPUID-VMCALL handler) is subject to the §3.2 conjecture (MI's
prior counter-evidence on $\hat{\sigma}_{\text{baseline}}$
guest-workload covariance) and requires per-type recalibration.

**Evidence:** §4.3.

---

#### A4 — Replay determinism (stronger than faithfulness)

**Statement.** EXTp's counterfactual replay machinery reproduces
the observable trajectory deterministically: for fixed
configuration and fixed input (including the intervention
parameter assignment), the trace is uniquely determined event by
event on the SOE 4-tuple surface.

Formally: let $T(c, \iota)$ denote the trace produced under
configuration $c$ and intervention assignment $\iota$. Then for
any fixed $(c, \iota)$:

$$\forall i: \text{4-tuple}_i\big(T_1(c, \iota)\big) = \text{4-tuple}_i\big(T_2(c, \iota)\big)$$

where $T_1, T_2$ are independent replay executions. Empirical
support: score_S = 1.0000 over N=34 cross-boot trials
(Cross_Boot_Stability_N34).

**Pearl correspondence (§2.4.4).** A4 is **strictly stronger
than** Pearl's probabilistic faithfulness axiom. Pearl's
faithfulness states: every conditional independence in the
observed distribution corresponds to a d-separation in the
underlying DAG, validated through probabilistic CI testing.
A4 dispenses with the distribution entirely: there is no
distribution because trajectories are reproduced exactly. CST's
sufficiency proposition (§3.3) requires only that the
counterfactual trace and original trace differ exclusively due
to the intervention — which deterministic replay guarantees
directly, without recourse to probabilistic structure.

**Upstream property.** Derived from SOE entry (score_S = 1.0000)
and Cross_Boot_Stability_N34 entry (cross-boot replay
reproducibility across N=34 independent boot sessions).

**Validation status disclosure.** The N=34 empirical foundation
validates A4 specifically under the **no-intervention** case
(reproducibility of the baseline trajectory). Generalization to
**intervention-applied** counterfactual replays (A4 holding for
$T_{\text{cf}}$ with arbitrary $do(X=x')$) rests on a
construction-level argument (§4.4.2): the VMM dispatch logic is
identical across replays, and the intervention machinery's
value-setting operation is deterministic, so combining
deterministic dispatch with deterministic value-setting yields
a deterministic trajectory. This construction argument has
**not** been empirically validated across intervention classes
in CST v1.0. A4's status is therefore:
- *Strong empirical sense for no-intervention case:* established
  by N=34 cross-boot trials.
- *Construction-argument extension for intervention cases:*
  asserted but not empirically validated; logged as Q5 future
  experiment (per-intervention-class cross-boot trials,
  analogous to Cross_Boot_Stability_N34 but with intervention
  injection at each replay).

Additionally, the N=34 sample size yields a Clopper-Pearson
95% upper bound on the per-replay failure rate of **10.4%**
(under 0 observed failures). The "deterministic" framing of A4
is therefore *high-confidence empirical*, not categorical; CST
claims under A4 inherit this bound.

**Known failure mode.** A4 fails under concurrent multi-VCPU
execution: race-induced non-determinism would break the
trajectory-level reproducibility guarantee. This is excluded by
the validity envelope (§3.4): CST v1.0 applies to single-threaded
VM-exit traces with deterministic dispatch. Multi-VCPU
counterfactual replay is future work.

**Note on timing dimension.** A4's determinism guarantee covers
the SOE 4-tuple surface, *not* the per-event timing $\Delta_i$.
Timing varies across replays due to microarchitectural noise (MI
$\hat{\sigma}_{\text{baseline}}$); A4 does not extend to
guaranteeing $\Delta_i^{\text{rep1}} = \Delta_i^{\text{rep2}}$.
This is precisely why A3 (timing-clause confounder boundedness
via $\Delta^*$) is needed as a separate assumption: A4 covers
deterministic 4-tuple agreement; A3 covers probabilistic
timing-clause bound.

**Evidence:** §4.4.

### 3.3 Sufficiency proposition + sketch proof

Theorem 3.1 covers the **atomic case**: a single intervention
$do(X = x')$ producing a single divergence $D$ at event $i$.
This subsection extends the result to **compositional claims** —
chains of atomic interventions producing a terminal divergence —
and provides a semi-formal sketch proof addressing the three
threats to causal attribution decomposed in §2.3
(coincidence, silent mechanism, confounder).

#### 3.3.1 Compositional extension proposition

**Proposition 3.3.1 (CST Composition Closure, compositional case).**

Let $T_{\text{orig}}$ and $T_{\text{cf}}$ be counterfactual
replays under a single configuration. Let $T_{\text{cf}}$ be
generated by an *ordered atomic sequence* of interventions:

$$\sigma = \big( do(X_1 = x_1'),\; do(X_2 = x_2'),\; \ldots,\; do(X_n = x_n') \big)$$

executed in the specified order during $T_{\text{cf}}$'s
fresh-boot replay (§2.2 compound intervention discipline). Let
$i_1 < i_2 < \cdots < i_n$ be the event indices at which each
intervention's effect first manifests on the observable surface.
Let $A = (A_1, A_2, A_3, A_4)$ be the assumption envelope (§3.2)
and $\mathcal{E}$ the validity envelope (§3.4).

Under $A$ satisfied and $\mathcal{E}$ admitted, the compositional
CST claim

$$\mathcal{C}_{\text{compound}} = \big\langle do(X_1=x_1') \rightsquigarrow_{i_1} do(X_2=x_2') \rightsquigarrow_{i_2} \cdots \rightsquigarrow_{i_n} D \;\big|\; A;\;\mathcal{E} \big\rangle$$

is admissible **iff** every atomic step

$$\big\langle do(X_k=x_k') \rightsquigarrow_{i_k} D_k \;\big|\; A;\;\mathcal{E} \big\rangle, \quad k = 1, 2, \ldots, n$$

is admissible under Theorem 3.1, where $D_k$ is the per-step
divergence at event $i_k$.

**Per-step independence requirement.** Each atomic step's
admissibility is checked *independently* under Theorem 3.1; the
compositional claim does not inherit admissibility from prior
steps. Commutativity is not assumed (§2.2): reordering $\sigma$
generally yields a different chain with different admissibility.

#### 3.3.2 Sketch proof — atomic case

The atomic case is proven by addressing the three threats to
causal attribution decomposed in §2.3.

**Setup.** Suppose $D(T_{\text{orig}}, T_{\text{cf}}, i) = \text{true}$
under intervention $do(X = x')$, with $A_1, A_2, A_3, A_4$
satisfied and $\mathcal{E}$ admitted. We show that the observed
divergence is causally attributable to $do(X = x')$ within the
bounded epistemic envelope $(A, \mathcal{E})$.

**Threat 1 — Coincidence.** *The divergence at event $i$
correlates with $do(X = x')$ but is causally independent — e.g.,
a spontaneous timing fluctuation or framework-internal state
flicker.*

Addressed by **A4 (replay determinism)**: under A4, a spontaneous
non-intervention-driven divergence would fail to reproduce across
independent replays of $T_{\text{cf}}$. The empirical foundation
of A4 — score_S = 1.0000 across N = 34 cross-boot trials
(Cross_Boot_Stability_N34) — establishes that the absence of
intervention yields exact 4-tuple reproducibility at every event.
Therefore a 4-tuple divergence in $T_{\text{cf}}$ relative to
$T_{\text{orig}}$ cannot be spontaneous; it requires a
trace-distinguishing input difference, which under the
single-configuration discipline (§2.1) is exactly the
intervention $do(X = x')$. The SOE clause of $D$ rules out
coincidence at false-positive rate zero.

The timing clause of $D$ admits a residual coincidence rate of
$\alpha$ (nominal 0.05, empirically realized 0.6%–2.8% per MI
§5.4). This residual is **explicitly admitted as $\alpha$-bounded
noise** and incorporated into A3 (confounder boundedness); it is
not a defeater of attribution but a quantified bound on
attribution confidence.

**Threat 2 — Silent mechanism.** *The divergence is caused by an
unobservable microarchitectural process that $do(X = x')$ happens
to trigger, but the causal pathway is mechanistic rather than
event-level.*

Addressed by **scope-honesty** (the chain-vs-mechanism
distinction of §2.3) combined with **A2 (observational
completeness modulo silent leak)**. Two cases:

- *The silent mechanism does not produce a 4-tuple delta or
  timing > $\Delta^*$.* Then $D = \text{false}$ at event $i$
  (no observed divergence), contradicting the premise. The silent
  mechanism is detected by neither clause of $D$; CST is
  **silent on this case**, neither claiming nor refuting causal
  attribution. This is the explicit A2 scope-out: silent
  microarchitectural divergence outside CST's observable surface
  is deferred to CMD (§5.2 future work).
- *The silent mechanism does produce a 4-tuple delta or timing
  $> \Delta^*$.* Then $D = \text{true}$ at event $i$, and the
  divergence is captured on CST's observable surface. The
  underlying mechanism is unobservable, but the *observable
  causal pathway* — the chain of events through which the effect
  propagates — is captured. CST attributes causation at the
  event-level (chain), not at the microarchitectural level
  (mechanism); the attribution is admissible regardless of the
  underlying mechanism.

Threat 2 therefore does not defeat CST's atomic claim: in the
first case CST is silent (scope-honest); in the second case CST
attributes correctly at the chain level (mechanism-agnostic).

**Threat 3 — Confounder.** *The divergence is caused by a third
factor correlated with both $do(X = x')$ and the observed
outcome — e.g., a framework-internal state change triggered by
the intervention machinery but not the intervention itself.*

Addressed by **A1 (modularity)** — modulo the known gap. A1
asserts that the intervention machinery's execution does not
modify framework-internal state outside $X$'s capability
authority scope. Two cases:

- *A1 holds in its strict form (Q4 future experiment validates
  side-effect freedom).* Then no framework-internal state change
  is correlated with $do(X = x')$; the only difference between
  $T_{\text{orig}}$ and $T_{\text{cf}}$ is the intervention
  parameter $X$. Confounder attribution is ruled out.
- *A1 holds modulo bounded side-effects below $\Delta^*$ (current
  empirical status, pre-Q4).* In this state, the framework-internal
  side-effect class is **hypothesized** bounded below $\Delta^*$;
  this hypothesis is the load-bearing assumption of A1-modulo, and
  it is **not** empirically validated until Q4 (§5.1) executes.
  Conditional on the A1-modulo hypothesis holding, attribution
  proceeds as follows: any divergence $D = \text{true}$ at event
  $i$ must arise from an effect *above* $\Delta^*$, which by the
  hypothesized bound is not attributable to the side-effect class.
  Attribution to $do(X = x')$ is therefore admissible **within
  the A1-modulo bound, conditional on the hypothesis**.

  The honest framing: CST v1.0 claims do not categorically rule
  out confounder attribution; they assert that **if** the A1-modulo
  hypothesis holds (validated by Q4), confounder attribution is
  excluded. Pre-Q4, the threat is **partially addressed by
  hypothesis**, with the residual side-effect class explicitly
  flagged in $\mathcal{E}$ (§3.4) and Q4 resolution scheduled
  (§5.1). Q4 falsification of A1-modulo would invalidate all
  CST claims under v1.0 envelope.

Threat 3 is therefore **partially addressed**: fully eliminated
under strict A1, partially eliminated under A1-modulo. CST claims
under the current empirical state carry an explicit
"A1-modulo-bound" qualifier in their validity envelope.

**Pearl/HP conformity (sketch).** The atomic claim's conformity
to Pearl's effectiveness + composition axioms and HP's AC1 + AC2
conditions, asserted as conditions (i)–(iv) of Theorem 3.1,
follows directly from the threat analysis:

  (i)   **Effectiveness** — $do(X = x')$ sets $X$ to $x'$ by the
        intervention machinery's design (§2.2); this is
        established by construction, not by proof.
  (ii)  **Composition modulo A1** — follows from Threat 3
        analysis: under A1 (or A1-modulo), the variables outside
        $X$'s descendant set evolve to their natural values
        whether explicitly pinned or not, satisfying Pearl's
        composition axiom.
  (iii) **HP AC1 (effect occurs in actual world)** — the
        divergence $D = \text{true}$ is observed in
        $T_{\text{cf}}$ at event $i$; by premise.
  (iv)  **HP AC2 (counterfactual sensitivity)** — the divergence
        differs from $T_{\text{orig}}$ at event $i$; this is the
        operational meaning of $D$, established by construction.

Thus the atomic claim is *sound* in the precise sense of
Theorem 3.1: it satisfies the four conformity conditions under
$(A, \mathcal{E})$ and addresses the three coincidence/silent/
confounder threats within bounded epistemic guarantees. $\square$
(atomic case)

#### 3.3.3 Sketch proof — compositional case

The compositional case (Proposition 3.3.1) follows by **induction
on the chain length** $n$:

**Base case** ($n = 1$). Single atomic step — reduces to
Theorem 3.1 directly.

**Inductive step.** Assume the compositional claim is admissible
for chains of length $n - 1$. Consider a chain of length $n$:

$$\big\langle do(X_1=x_1') \rightsquigarrow_{i_1} \cdots \rightsquigarrow_{i_{n-1}} do(X_n=x_n') \rightsquigarrow_{i_n} D \;\big|\; A;\;\mathcal{E} \big\rangle$$

By the inductive hypothesis, the prefix chain (length $n-1$,
terminating at $do(X_n = x_n')$ at event $i_{n-1}$) is
admissible: the state at event $i_{n-1}$ is causally attributable
to the chain $(X_1, \ldots, X_{n-1})$ within bounded epistemic
envelope.

The final atomic step $do(X_n=x_n') \rightsquigarrow_{i_n} D$
is admissible by Theorem 3.1 directly: it is an atomic
intervention producing a divergence at event $i_n$, with
assumptions $A_1$–$A_4$ and envelope $\mathcal{E}$ verified for
this single step.

**Comparison-baseline clarification.** In the compositional
case, the per-step divergence $D_k$ at event $i_k$ is defined
relative to a **step-wise baseline**: the state at $i_k$ that
would have resulted from the prefix-chain interventions
$(X_1, \ldots, X_{k-1})$ **without** intervention $X_k$. Under
A1 (modularity), $X_k$'s intervention only affects $X_k$ and
its causal descendants; prior interventions' downstream effects
compose linearly with $X_k$'s effects. The per-step attribution
at $i_k$ is therefore well-defined: $D_k = \text{true}$ iff
$T_{\text{cf}}$'s state at $i_k$ differs from the step-wise
baseline, attributable to $X_k$ alone modulo A1's validity.
Theorem 3.1's atomic-case framework ($T_{\text{orig}}$ vs
$T_{\text{cf}}$ with single intervention) generalizes to this
step-wise baseline because A1+A2 guarantee that intermediate
state evolution remains observable on the §2.1 surface, and
because the per-step independence requirement (§2.3) ensures
each step's claim is independently verifiable against its
step-wise baseline.

Crucially, the two admissibility claims are **independent**: the
prefix chain's admissibility does not impose constraints on the
final atomic step beyond $A_1$–$A_4$ themselves. Per the
*per-step independence requirement* of Proposition 3.3.1, each
step is checked under Theorem 3.1's premises, not under
prior-step inheritance.

Therefore the full chain of length $n$ is admissible if and only
if every atomic step is admissible under Theorem 3.1.
$\square$ (compositional case)

#### 3.3.4 Notes on proof rigor

This is a **semi-formal sketch proof** at the level appropriate
for paper-text inclusion (per §5.4 Isabelle formalization
deferral): the structure is rigorous (threat decomposition,
case analysis under A1 / A2 / A4, induction on chain length),
but mechanical formalization of state-evolution semantics and
exhaustive case enumeration is deferred to future Isabelle/HOL
formalization leveraging seL4's existing proof harness.

The sketch establishes:

- Each of the three threats (coincidence, silent mechanism,
  confounder) is addressed by a specific assumption (A4, A2, A1
  respectively), or explicitly deferred where the addressing is
  partial (A1-modulo, A2 silent-leak scope-out).
- Pearl/HP conformity conditions (i)–(iv) of Theorem 3.1 follow
  from the threat analysis plus construction.
- The compositional extension preserves admissibility under
  per-step independent verification.

What the sketch does **not** establish:

- Mechanical state-evolution semantics at the bit-precise level
  (deferred to Isabelle formalization).
- Closure under intervention scopes beyond per-event (per-window,
  global — §2.2 future work).
- Cross-configuration soundness (§2.1 single-config scope
  excludes this).

These gaps are intentional: CST v1.0 is a **soundness theorem
within enumerated bounds**, not a complete causal-modeling
framework. The bounds are the price of empirical realizability;
the soundness is what CST claims and what the sketch proof
establishes.

### 3.4 Validity envelope

The **validity envelope** $\mathcal{E}$ enumerates the
configurations, scopes, and conditions under which CST claims
are admissible (in-scope) and those under which CST claims are
structurally inapplicable or excluded (out-of-scope). $\mathcal{E}$
is the formal record of CST v1.0's epistemic boundaries; any
claim asserted with $\mathcal{E}$ outside its enumerated coverage
is **structurally invalid**, not merely empirically weak.

#### 3.4.1 Envelope tuple structure

Per §2.3, the validity envelope is a 6-tuple:

$$\mathcal{E} = (\text{instr}, \text{wl-class}, \text{gw-type}, \text{scope}, \mathcal{S}_{\text{in}}, \mathcal{S}_{\text{out}})$$

with components:

- $\text{instr}$ — MI instrument ($S_1$ sandwich-LFENCE-RDTSC or
  $S_2$ bare-RDTSC)
- $\text{wl-class}$ — MI workload class ($L_1$-pchase or
  $L_2$-pchase in CST v1.0)
- $\text{gw-type}$ — guest-workload type (pchase, CPUID-VMCALL,
  per MI §3.2 prior counter-evidence on covariance with
  $\hat{\sigma}_{\text{baseline}}$)
- $\text{scope}$ — intervention scope (per-event in CST v1.0;
  per-window and global are §2.2 future work)
- $\mathcal{S}_{\text{in}}$ — explicit in-scope conditions
  (§3.4.2)
- $\mathcal{S}_{\text{out}}$ — explicit out-of-scope conditions
  (§3.4.3)

A claim is admissible only if **all six components** match CST
v1.0's enumerated coverage.

#### 3.4.2 In-scope conditions ($\mathcal{S}_{\text{in}}$)

CST v1.0 claims are admissible for:

- **Single-threaded VM-exit traces with deterministic dispatch.**
  The trace is generated by a single VCPU under deterministic
  VMM event-handling order. Race-free execution is required for
  A4 (replay determinism).
- **Per-event intervention scope.** $X$ is set to $x'$ exactly at
  event $e_i$ and reverts after the event (§2.2). Per-window and
  global scopes are future work.
- **Atomic intervention surface.** $X$ is one of the four
  validated classes: $\text{nopcount}$, $\text{cache\_state}$,
  $\text{input}_j$, $\text{reg}_r$ (§2.2). Future-extension
  surfaces (interrupt injection, EPT mapping flip, MSR write)
  are not yet covered.
- **Calibrated workload classes.** $\text{wl-class}$ is either
  $L_1$-pchase or $L_2$-pchase, with R² ≥ 0.99 slope-fit
  satisfied (MI §2.5 acceptance criterion).
- **Calibrated guest-workload types.** $\text{gw-type}$ matches a
  type for which $\hat{\sigma}_{\text{baseline}}$ and $\Delta^*$
  have been directly measured (MI §4.1, §4.3) under the same
  $\text{instr}$ and $\text{wl-class}$.
- **Single-configuration execution.** $T_{\text{orig}}$ and
  $T_{\text{cf}}$ share hardware, microcode revision, VMM build,
  and seL4 kernel version (§2.1).
- **Fresh-boot replay.** Each $T_{\text{cf}}$ executes in a
  fresh boot session independent from $T_{\text{orig}}$'s boot
  (§2.1).
- **Intervention magnitudes within calibrated range.** The
  intervention magnitude (in iter units or cycle units) is
  within the range for which the workload class's slope-fit
  satisfies R² ≥ 0.99 (MI §2.5); extrapolation beyond the
  calibrated range is not covered.

#### 3.4.3 Out-of-scope conditions ($\mathcal{S}_{\text{out}}$)

CST v1.0 claims are **structurally inapplicable** for:

- **Concurrent multi-VCPU traces.** Race-induced non-determinism
  breaks A4. Multi-VCPU counterfactual replay requires a
  separate property addressing race-aware determinism — future
  work, not part of CST v1.0.
- **Workload classes outside L1/L2 pchase.** LLC/DRAM pchase and
  non-pchase workload classes (e.g., branch-heavy code, FPU
  workloads) require per-class recalibration of
  $\hat{\sigma}_{\text{baseline}}$ and $b$ (MI §5.3); claims
  under uncalibrated classes are structurally invalid.
- **Silent microarchitectural divergences.** Cache state, branch
  predictor state, TLB state changes that produce neither
  4-tuple delta nor timing deviation above $\Delta^*$ are
  outside CST's observable surface. Addressing this class
  requires CMD (§5.2 future).
- **Interventions on framework-internal state.** Modifications to
  capability sets, seL4 scheduler state, EPT structures outside
  the intervention surface, or MSR-resident state outside the
  validated MSR write surface — these are outside Capability
  Separation's intervention authority and therefore outside
  CST's intervention surface.
- **Bidirectional or negative-direction interventions.** MI's
  $\Delta^*$ is one-sided (positive shifts only, MI §2.7).
  Interventions designed to *reduce* per-event timing (e.g.,
  cache prefetch reducing latency) require independent
  threshold derivation; CST v1.0 does not cover this case.
- **Cross-configuration comparisons.** Claims comparing
  $T_{\text{orig}}$ and $T_{\text{cf}}$ across different
  hardware, microcode revisions, VMM builds, or kernel versions
  are structurally invalid under §2.1 single-configuration
  discipline.
- **Probabilistic causation claims.** Claims of the form
  "$do(X = x')$ raises the probability of $D$" require
  ensemble-level distribution, contradicting A4 (§2.3 claim
  space exclusions).
- **Mechanism claims.** Claims attributing causation through
  unobservable microarchitectural processes ($M$ in
  "$do(X = x') \rightarrow D$ via mechanism $M$") are outside
  CST's chain-level observable pathway scope (§2.3 chain-versus-
  mechanism distinction).
- **AC3 minimality claims.** Claims asserting that $do(X = x')$
  is *the* minimal cause of $D$ require Halpern-Pearl AC3
  analysis (§2.4.4), not covered by CST v1.0.

#### 3.4.4 Negative-framing rules (paper-text citation discipline)

The following framings are **forbidden** in paper text citing
CST claims:

- ❌ "EXTp proves $X$ is the cause of $Y$" — missing envelope
  qualifier; minimality not established. Use:
  "EXTp's CST-admissible claim attributes $Y$ at event $i$ to
  $do(X = x')$ under envelope $\mathcal{E}$".
- ❌ "EXTp shows $X$ causes $Y$ across configurations" — cross-
  configuration claims are structurally invalid. Use single-
  configuration framing only.
- ❌ "Replay of $X$ proves $Y$ would not have occurred without
  $X$" — modal counterfactual, not CST's deterministic
  trajectory framing. Use:
  "The counterfactual replay with $do(X = x_{\text{natural}})$
  exhibits $\neg D$ at event $i$, satisfying HP AC2".
- ❌ "EXTp's framework eliminates confounders" — A1 modulo Q4 gap
  is partial. Use:
  "A1 modularity is asserted modulo bounded side-effects below
  $\Delta^*$, pending Q4 validation (§5.1)".
- ❌ "CST validates that $X$ caused $Y$ through mechanism $M$" —
  mechanism out of scope. Use chain enumeration only:
  "$do(X = x_1') \rightsquigarrow_{i_1} \cdots \rightsquigarrow_{i_n} D$".
- ❌ "CST's $\Delta^*$ applies to LLC/DRAM workloads" —
  uncalibrated class. Use:
  "CST v1.0 covers L1/L2-pchase; LLC/DRAM extrapolation requires
  per-class recalibration (MI §5.3)".

#### 3.4.5 Envelope evolution and versioning

The validity envelope is **version-stamped**. CST v1.0's
envelope is defined by §3.4.1–§3.4.3. Future versions (v1.1,
v2.0) may expand the envelope by:

- Validating future-extension intervention surfaces (interrupt,
  EPT, MSR) — expands $\mathcal{S}_{\text{in}}$
- Validating per-window or global intervention scopes — expands
  $\text{scope}$ component
- Adding workload classes (LLC, DRAM, non-pchase) — expands
  $\text{wl-class}$ component
- Resolving the Q4 modularity gap (§5.1) — strengthens A1 from
  modulo-bounded to strict, lifting the side-effect qualifier
- Developing CMD for silent microarchitectural divergence —
  expands coverage beyond the silent-leak scope-out

Each envelope expansion is a separate validation effort with its
own evidence and version stamp; claims under an expanded envelope
explicitly cite the version (e.g., "admissible under CST v1.1
envelope, see CST §3.4.1 v1.1").

Paper text citing CST must declare the envelope version under
which the claim is asserted, per §6.2 citation discipline.

---

## 4. Evidence for Assumptions

### §4 Prologue — Dependency table

| Assumption | Pearl-side role | Upstream EXTp property | Scope restriction |
|------------|-----------------|------------------------|-------------------|
| A1 modularity | do(X=x) only affects X and descendants | Capability Separation | full (within authority bounds) |
| A2 obs. completeness | observable trajectory captures all causal effects | SOE 4-tuple + MI Δ* | modulo silent cache divergence |
| A3 confounder bound | bounded measurement noise | MI (Δ*_significance) | guest-workload-type covariant |
| A4 determinism | replay reproduces trajectory exactly | SOE (score_S = 1.0000) | full (single-threaded) |

### 4.1 Evidence for A1 — Modularity from Capability Separation

A1 (modularity, §3.2) asserts that intervention $do(X = x')$
modifies only the targeted parameter $X$ and its causal
descendants; framework-internal state outside $X$'s capability
authority scope is invariant under the intervention. This
subsection derives A1 from the Capability Separation Theorem
entry and explicitly characterizes the known gap between
*authority disjointness* (what Capability Separation proves) and
*side-effect freedom* (what A1 strictly requires).

#### 4.1.1 Capability Separation derivation

The Capability Separation Theorem (Capability_Separation_Theorem.md)
proves that EXTp's intervention machinery operates within
explicitly bounded capability authority: the set of values
modifiable by the intervention machinery is exactly the set
covered by the machinery's capability set, which is *disjoint*
from framework-internal state.

Formally, let $\mathcal{K}_{\text{int}}$ denote the capability
set held by the intervention machinery, and $\mathcal{K}_{\text{fwk}}$
the capability set governing framework-internal state (VMM
scheduler, EPT structures outside the validated intervention
surface, capability registers not under intervention authority,
MSR-resident state outside the validated MSR write surface).
Capability Separation establishes:

$$\mathcal{K}_{\text{int}} \cap \mathcal{K}_{\text{fwk}} = \emptyset$$

Under this disjointness, any value modifiable through
$\mathcal{K}_{\text{int}}$ cannot also be modifiable through
$\mathcal{K}_{\text{fwk}}$ (by construction). The intervention
machinery therefore cannot *directly* modify framework-internal
state — there is no capability path from intervention authority
to framework state.

This is the foundational guarantee from which A1's modularity
claim derives.

#### 4.1.2 From authority disjointness to modularity

Authority disjointness establishes that $do(X = x')$ cannot
*directly* modify framework state. To complete the derivation of
A1, we must also establish that $do(X = x')$ does not modify
framework state *indirectly* — e.g., through side-effects of the
intervention's *execution* on shared resources (CPU cycles, VMM
scheduler time, cache lines).

Three sub-paths of potential indirect modification:

- **Execution-time consumption.** The intervention machinery
  itself consumes CPU time during the injection (e.g., nopcount
  injection invokes VMM scheduler dispatch for the injection
  operation). This time consumption is observable in the VMM
  scheduler's timing profile.
- **Cache-line displacement.** The intervention machinery's code
  and data occupy cache lines during execution, potentially
  displacing other cache state.
- **Branch predictor pollution.** The intervention machinery's
  branch instructions train the branch predictor, potentially
  affecting subsequent prediction accuracy.

For strict A1 to hold, all three sub-paths must produce
side-effects below the detection threshold $\Delta^*$ on
framework observables. Capability Separation establishes
disjointness at the *authority* level but does not establish
boundedness at the *execution side-effect* level.

#### 4.1.3 Known gap and current empirical status

**The gap.** Capability Separation proves authority
disjointness (no direct modification path), but not strict
side-effect freedom (no indirect modification via execution
overhead). The three sub-paths in §4.1.2 are *plausibly bounded*
under EXTp's lean intervention machinery (each intervention
class adds minimal instruction count, MI §4.2 nopcount
calibration suggests slope $b \approx 4.48$ cycle/iter for the
pchase loop body — well-quantified per iteration), but
*empirical validation* of side-effect boundedness on
framework-internal observables has not been performed in this
work.

**Two-layer derivation source.** Per Capability_Separation_Theorem.md
§3.4, EXTp's capability operations split into two methodological
layers:

- $K_{\text{verified}} = \{\text{create}, \text{copy}, \text{revoke}, \text{destroy}\}$
  — seL4 cap-table operations within L4.verified's formal scope.
  Authority disjointness on this layer is **formally proven** by
  seL4's Isabelle/HOL proof harness; the modularity gap on
  $K_{\text{verified}}$ is zero by formal proof.
- $K_{\text{extended}} = \{\text{MapEPT}, \text{Unmap}, \text{WriteVMCS}, \text{ReadVMCS}, \ldots\}$
  — seL4's x86-64 VT-x extension operations outside L4.verified's
  formal scope. Authority disjointness on this layer is
  **empirically validated** (Capability_Separation_Theorem.md §3.4
  N=998 + N=34 cross-boot evidence), but execution-overhead
  side-effects remain to be validated by Q4.

A1's modulo qualifier therefore applies **only to
$K_{\text{extended}}$**: indirect modification paths
(execution-time consumption, cache displacement, branch predictor
pollution) arising from $K_{\text{extended}}$ operations are
pending Q4 validation. For $K_{\text{verified}}$ operations,
strict modularity holds by inheritance from L4.verified's
formal proof.

**Current empirical status.** A1 is asserted **modulo bounded
side-effects of magnitude below $\Delta^*$ on framework
observables, scoped to $K_{\text{extended}}$ operations**. Two
scope-clarifications are critical:

(a) **Δ* source.** "Below Δ*" here refers to the *guest-workload*'s
calibrated Δ* (MI §3.1; e.g., 9,077 cycles for L1-pchase under
S1). The framework observables (VMM scheduler dispatch timing,
EPT modification counts, capability register state, etc.) have
their own noise floor which is **uncalibrated** pre-Q4. The
A1-modulo bound is therefore *operationally meaningful only for
side-effects propagating to the guest observable surface*;
framework-internal side-effects that do not propagate to the
guest surface are silent (A2 scope-out applies).

(b) **Hypothesis status.** "Modulo Δ*" is a *hypothesis* pre-Q4,
not an empirically validated bound. Q4 will both calibrate
framework-observable noise floor AND validate side-effect
boundedness against that calibration. Until Q4 executes, A1
operates under the hypothesis; CST claims under v1.0 envelope
inherit this conditionality (see §3.3.2 Threat 3 wording for
the honest framing).

This is a *temporary scope restriction* tracked through to Q4
resolution:

- If Q4 (§5.1) validates strict side-effect freedom (all
  framework observables show no change above $\Delta^*$ under
  intervention), A1 is strengthened to its strict form; the
  modulo qualifier is lifted in the next envelope version.
- If Q4 detects bounded side-effects above $\Delta^*$ on some
  framework observables, A1 must be narrowed: the affected
  observable classes are excluded from $\mathcal{S}_{\text{in}}$,
  and CST's coverage shrinks accordingly.
- If Q4 detects side-effects with magnitude *near* $\Delta^*$ (in
  the marginal-detection regime), the A1-modulo qualifier
  remains but is parameterized by the empirical bound rather
  than the threshold-bound.

In all three outcomes, the envelope version stamp records the
post-Q4 state.

#### 4.1.4 Pearl correspondence cross-reference

Per §2.4.2, Pearl's *effectiveness* axiom is established by
construction (intervention machinery sets $X$ to $x'$),
**orthogonal** to A1. Pearl's *composition* axiom inherits A1's
validation status: under strict A1, composition holds
unconditionally; under A1-modulo, composition holds within the
bounded-side-effect qualifier. This inheritance pattern is the
formal basis for the "Composition modulo A1" status row in
§2.4.5 correspondence table.

#### 4.1.5 Forward references

- §5.1 — Q4 empirical validation experiment design
- §3.4.5 — envelope evolution upon Q4 resolution
- §6.2 — citation discipline for A1-modulo qualifier in paper
  text

### 4.2 Evidence for A2 — Observational completeness from SOE + MI

A2 (§3.2) asserts that every causal effect of intervention
$do(X = x')$ on the trace either (i) manifests on the SOE
4-tuple surface, (ii) produces a timing deviation exceeding
$\Delta^*$, or (iii) falls within the explicitly enumerated
silent leak class. This subsection derives A2 from the
composition of two upstream property entries — SOE
(observational surface) and MI (timing surface with quantified
noise floor) — and characterizes the silent leak scope-out.

#### 4.2.1 SOE 4-tuple surface contribution

The Strong Observational Equivalence entry
(Strong_Observational_Equivalence.md) establishes that the
4-tuple $(\text{rip}, \text{exit\_reason}, \text{exit\_qual}, \text{rax})$
captures the discrete state evolution of the trace event by
event. Two empirical facts ground this:

- **Cross-boot reproducibility.** Cross_Boot_Stability_N34 reports
  score_S = 1.0000 across N = 34 cross-boot trials, meaning the
  4-tuple agrees exactly at every event in every trial pair.
  This establishes that the 4-tuple is a *deterministic surface*
  under fresh-boot single-configuration replay.
- **Coverage of discrete state transitions.** The 4-tuple
  captures the VM-exit dispatch state machine: instruction
  pointer ($\text{rip}$), exit cause ($\text{exit\_reason}$),
  exit detail ($\text{exit\_qual}$), and primary return register
  ($\text{rax}$). Every discrete state transition under a
  VM-exit produces a value change in at least one of the four
  components, by construction of the VM-exit handler protocol.

Under SOE, *discrete causal effects* of $do(X = x')$ — effects
that change which dispatch path executes, which return value is
produced, or which fault is raised — manifest on the 4-tuple
surface. The SOE clause of $D$ (§2.1) detects these effects with
zero false-positive rate (under A4 deterministic replay).

This is the first disjunct of A2.

#### 4.2.2 MI Δ* timing surface contribution

The Measurement Interference entry (Measurement_Interference.md)
extends observability to the timing dimension. Specifically:

- **Quantified noise floor.** MI §4.1 reports
  $\hat{\sigma}_{\text{baseline}}$ values per workload class
  (e.g., 5,518 cycle for L1-pchase S1 at iter=0, 4,604 cycle for
  L2-pchase S2 at iter=0). These quantify the timing measurement
  uncertainty under no-intervention baseline conditions.
- **Detection threshold.** MI §3.1 defines
  $\Delta^* = z_{1-\alpha} \cdot \hat{\sigma}_{\text{baseline}}$
  (with $\alpha = 0.05$, $z = 1.645$). Timing deviations
  exceeding $\Delta^*$ are detectable above the noise floor with
  bounded false-positive rate $\alpha$.
- **Empirical validation.** MI §5.4 reports direct empirical
  realized FPR: 0.61% (boot_log8, n=978) and 2.78% (boot_log12
  iter=0, n=108) — both well below nominal 5%, confirming the
  parametric z-test is conservative in the upper-tail regime.

Under MI, *timing causal effects* of $do(X = x')$ — effects that
change per-event timing without necessarily changing the
4-tuple — manifest on the timing surface when the deviation
exceeds $\Delta^*$. The timing clause of $D$ (§2.1) detects
these effects with false-positive rate $\alpha$ (nominal,
empirically realized 0.6%–2.8%).

This is the second disjunct of A2.

#### 4.2.3 Union surface — combined observability

The union of the SOE 4-tuple surface and the MI timing surface
constitutes CST's *observable surface*:

$$\text{Observable} = \text{4-tuple delta} \;\cup\; \text{timing delta} > \Delta^*$$

This union is the operational meaning of $D$ (§2.1). Under A2,
every causal effect of $do(X = x')$ either lies within the
observable surface (covered by SOE or MI) or lies within the
silent leak class (out of scope, §4.2.4).

**Important note on surface independence.** The SOE and MI
surfaces are *not orthogonal*: a discrete state transition
captured by the SOE 4-tuple may also produce a timing deviation
captured by MI. CST does not require independence; the OR
structure of $D$ admits redundant detection (a single causal
effect detected by both clauses). What CST requires is that
*every* causally relevant effect produces at least *one* of the
two signals (or falls in the silent leak class).

#### 4.2.4 Silent leak scope-out

Three classes of microarchitectural state are *not* captured by
SOE or MI:

- **Cache state changes without timing manifestation.** A cache
  state difference between $T_{\text{orig}}$ and $T_{\text{cf}}$
  that does not produce a per-event timing deviation above
  $\Delta^*$. This can occur when the cache state difference
  affects only lines that are not accessed during the recorded
  trace events, or when the timing deviation falls below
  $\Delta^*$.
- **Branch predictor state changes without observable
  consequence.** A branch predictor state difference that does
  not manifest as a misprediction during the trace, or whose
  misprediction cost falls below $\Delta^*$.
- **TLB state changes without observable consequence.** A TLB
  miss/hit pattern difference that does not produce per-event
  timing deviation above $\Delta^*$.

These three classes constitute the **silent leak scope-out** of
A2. CST is **silent on silent effects, not asserting their
absence** (§2.3): if a causal effect of $do(X = x')$ falls
entirely within the silent leak class, $D = \text{false}$ at
every event, and CST does not assert any claim — neither
attribution nor refutation.

**Future work pointer.** Addressing the silent leak class
requires microarchitectural counter instrumentation:

- LLC miss rate counters (Intel PMU MSR_LLC_MISS or equivalent)
- Branch misprediction counters (Intel PMU
  MSR_BR_MISP_RETIRED.ALL_BRANCHES)
- TLB miss counters (Intel PMU MSR_DTLB_MISS or equivalent)

These counters are accessible via MSR reads at VM-exit but are
not part of MI's current instrument set. The forthcoming
**Counterfactual Microarch Divergence (CMD)** property class
(§5.2) is scheduled to extend the observable surface using these
counters, narrowing the silent leak scope-out.

#### 4.2.5 Pearl correspondence cross-reference

Per §2.4.4, Halpern-Pearl AC2 (counterfactual sensitivity)
requires that the effect manifests on the observable surface.
A2's three-way disjunction (SOE OR MI OR silent-leak-scope-out)
implements AC2 under CST's restricted observability: AC2 is
established whenever the effect lies in the observable union,
and explicitly *not asserted* when the effect lies in the silent
leak class. This is the formal basis for the "AC2 / direct"
status row in §2.4.5 correspondence table, qualified by the
silent leak scope-out.

#### 4.2.6 Forward references

- §5.2 — CMD future work scope, silent leak class addressing
- §3.4.3 — silent microarchitectural divergence in
  $\mathcal{S}_{\text{out}}$
- §6.2 — citation discipline for "modulo silent leak"
  qualifier in paper text

### 4.3 Evidence for A3 — Confounder boundedness from MI

A3 (§3.2) asserts that measurement noise on the observable
surface is bounded: the SOE clause contributes zero
false-positive rate, and the timing clause contributes
false-positive rate bounded by $\alpha$ (nominal 0.05,
empirically realized 0.6%–2.8%). This subsection derives A3
from the Measurement Interference entry's calibrated noise
floor and empirical false-positive rate measurements.

#### 4.3.1 SOE clause — zero false-positive rate

The SOE clause of $D$ (§2.1) tests whether the 4-tuple at event
$i$ differs between $T_{\text{orig}}$ and $T_{\text{cf}}$.
Under A4 (replay determinism), in the absence of intervention,
the 4-tuple agrees exactly at every event:

$$\forall i: \text{4-tuple}_i^{\text{orig}} = \text{4-tuple}_i^{\text{cf}}$$

per Cross_Boot_Stability_N34's score_S = 1.0000 across N = 34
trials. The SOE clause therefore returns true *only* when there
is a genuine 4-tuple difference — by construction, with no
spurious detection. The false-positive rate of the SOE clause
is **zero** (within A4's coverage; A4's failure mode under
concurrent multi-VCPU is excluded by §3.4 envelope).

This is the first component of A3.

#### 4.3.2 Timing clause — α-bounded false-positive rate

The timing clause of $D$ tests whether
$|\Delta_i^{\text{orig}} - \Delta_i^{\text{cf}}| > \Delta^*$.
Under MI's calibration:

- **Threshold derivation.** $\Delta^* = z_{1-\alpha} \cdot \hat{\sigma}_{\text{baseline}}$
  with $z = 1.645$ for $\alpha = 0.05$. For L1-pchase S1:
  $\Delta^* = 1.645 \cdot 5{,}518 = 9{,}077$ cycle (MI §4.1).
- **Parametric assumption.** The threshold derivation assumes a
  z-test with Gaussian-approximated noise distribution. MI §2.7
  notes this approximation; the asymmetric-tail observation
  (MI §5.4) confirms the upper tail is not Gaussian but is
  *thinner* than Gaussian past the 95th percentile.
- **Nominal false-positive rate.** Under the parametric
  assumption, the timing clause produces a false detection with
  probability $\alpha$ per event in the absence of intervention.

This is the nominal component of A3.

#### 4.3.3 Empirical validation — direct-count realized FPR

MI §5.4 reports direct empirical realized FPR from raw delta
counts above $\Delta^*$:

- **boot_log8** (S1, CPUID-VMCALL, n=978 post-warmup):
  6 samples above $\mu + 1.645 \cdot \hat{\sigma}$ →
  **realized α = 0.61%** (vs nominal 5%; **8.2× conservative**).
- **boot_log12 iter=0** (S1, L1-pchase, n=108 post-warmup):
  3 samples above $\mu + 1.645 \cdot \hat{\sigma}$ →
  **realized α = 2.78%** (vs nominal 5%; **1.8× conservative**;
  binomial 95% CI roughly [0.6%, 8%] given small sample).

The empirical realized FPR is **substantially below nominal**
in both cases. The asymmetric upper tail thins rapidly past p95
(MI §5.4 linear-estimate overshoot analysis: 6.6× for boot_log8,
1.2× for boot_log12), with the rate of thinning itself
guest-workload-type covariant (MI §3.2 prior counter-evidence,
extended to tail-shape covariance).

Under MI's empirical bounds, the timing clause's realized FPR
is bounded by $\alpha$ in the **conservative direction**: actual
detection rate ≤ nominal, with the conservative bound
quantified per workload class.

This is the empirical component of A3.

#### 4.3.4 Combined A3 bound

The combined false-positive rate of $D$ is:

$$\Pr[D = \text{true} \mid \text{no intervention effect}] \leq 0 + \alpha_{\text{realized}} = \alpha_{\text{realized}}$$

where $\alpha_{\text{realized}}$ is the empirically measured FPR
per workload class (0.61% for CPUID-VMCALL, 2.78% for
L1-pchase, both below nominal 5%).

A3 is therefore established with:
- *Nominal* bound: $\alpha = 0.05$
- *Empirical* bound: $\alpha_{\text{realized}} \in [0.6\%, 2.8\%]$
  per characterized workload class

CST claims using A3 may cite either the nominal or the empirical
bound; the empirical bound is preferred where the workload class
matches the calibration source (citation discipline per §6.2).

#### 4.3.5 Known scope dependency

A3's bound is **workload-class-conditional** and
**guest-workload-type-conditional**:

- $\hat{\sigma}_{\text{baseline}}$ is calibrated per workload
  class (L1-pchase, L2-pchase, ...); LLC/DRAM extrapolation
  requires re-measurement per MI §5.3.
- $\hat{\sigma}_{\text{baseline}}$ covaries with guest-workload
  type per MI §3.2 prior counter-evidence (paired same-instrument
  measurement: 5,518 cycle for pchase vs 6,383 cycle for
  CPUID-VMCALL under S1).
- The empirical FPR's *tail shape* covaries with guest-workload
  type (MI §5.4: 6.6× linear-overshoot for CPUID-VMCALL vs 1.2×
  for L1-pchase). Tail-shape covariance is a *second-order*
  dependency: not only the magnitude but the functional shape
  of $\alpha_{\text{realized}}$ differs across workload types.

A3 is asserted **for the calibrated workload class and
guest-workload type matching the validity envelope $\mathcal{E}$
of the claim**. Cross-class or cross-type extrapolation
invalidates A3 and therefore invalidates the CST claim, per §3.4
out-of-scope conditions.

#### 4.3.6 Pearl correspondence cross-reference

A3 corresponds to Pearl's confounder-boundedness requirement,
expressed through the quantified noise floor $\Delta^*$ and
realized FPR bound. Under Pearl's classical framework,
confounder boundedness is typically asserted through latent-
variable assumptions; CST's instrument-bounded formulation
substitutes empirical calibration for latent-variable reasoning
(§2.4.2 effectiveness/A1 orthogonality discussion).

#### 4.3.7 Forward references

- MI §4.1 — $\hat{\sigma}_{\text{baseline}}$ per workload class
- MI §3.1 — $\Delta^*$ derivation
- MI §5.4 — direct-count realized FPR, asymmetric tail shape
- §6.2 — citation discipline for nominal vs empirical bound

### 4.4 Evidence for A4 — Determinism from SOE

A4 (§3.2) asserts that EXTp's counterfactual replay machinery
reproduces the observable trajectory deterministically on the
SOE 4-tuple surface: for fixed configuration and fixed input
(including intervention assignment), the trace is uniquely
determined event by event. A4 is strictly stronger than Pearl's
probabilistic faithfulness axiom (§2.4.2). This subsection
derives A4 from the SOE entry and Cross_Boot_Stability_N34 entry
and characterizes the Pearl-stronger framing.

#### 4.4.1 SOE entry derivation

The Strong Observational Equivalence entry establishes that the
4-tuple agreement metric:

$$\text{score}_S = \frac{|\{i : \text{4-tuple}_i^{T_1} = \text{4-tuple}_i^{T_2}\}|}{|T|}$$

evaluates to exactly **1.0000** across N = 34 cross-boot replay
trial pairs (Cross_Boot_Stability_N34.md). This is the empirical
foundation of A4: in the absence of intervention, two
independent replays of the same configuration produce 4-tuple
agreement at every event with no exception across N = 34
trials.

**Score formula scope.** $\text{score}_S$ is defined for trace
pairs of *equal length*; the formula assumes $|T_1| = |T_2|$.
Cross-boot replays under fresh-boot single-config produce traces
of identical length by construction (deterministic trace
boundaries on the SOE 4-tuple surface; the no-intervention case
yields the same event count by virtue of A4 acting on dispatch
logic). Unequal-length traces fall outside the score's defined
domain and are flagged as **structural failures**, not soft
divergences.

**Sample-size CI on A4.** With 0 observed failures in N=34
trials, the Clopper-Pearson 95% upper bound on the per-replay
failure rate is **10.4%**. A4's "exactly 1.0000" framing is
therefore *high-confidence empirical*, not categorical: with
95% confidence, the population failure rate is ≤10.4%. CST
claims invoking A4 inherit this bound; tightening requires
larger N (e.g., N=300 cross-boot trials would yield upper
bound ≤1.0%).

Formally, for the trace produced under configuration $c$ and
intervention assignment $\iota$ (which in the no-intervention
case is the identity assignment $\iota_0$):

$$\forall i: \text{4-tuple}_i\big(T_1(c, \iota_0)\big) = \text{4-tuple}_i\big(T_2(c, \iota_0)\big)$$

where $T_1, T_2$ are independent replay executions. This is the
trajectory-level reproducibility guarantee.

#### 4.4.2 Generalization to intervention assignments

A4 generalizes the no-intervention reproducibility to arbitrary
intervention assignments: for any $\iota$ within CST's
intervention surface (§2.2),

$$\forall i: \text{4-tuple}_i\big(T_1(c, \iota)\big) = \text{4-tuple}_i\big(T_2(c, \iota)\big)$$

This generalization is **not directly validated by N = 34** — the
cross-boot stability trials measure no-intervention
reproducibility only. The generalization rests on a
*construction-level argument*:

- The VMM event-handling dispatch logic is identical across
  replays under the same configuration.
- The intervention machinery's value-setting operation
  (effectiveness, §2.4.2) is deterministic: a specified value
  $x'$ is set, not a stochastic draw.
- Combining the deterministic dispatch logic with deterministic
  value-setting yields a deterministic trace under any
  intervention assignment, by construction.

The construction-level argument is *not* a substitute for
empirical validation across intervention classes. Future work
extending Cross_Boot_Stability_N34 to per-intervention-class
reproducibility (e.g., N=34 cross-boot trials under fixed
$do(\text{nopcount} = 4500)$) would directly validate the
generalization. This is logged as deferred empirical work; CST
v1.0 cites the construction-level argument with this
qualification.

#### 4.4.3 Pearl-stronger framing

Pearl's *faithfulness* axiom states: every conditional
independence in the observed distribution corresponds to a
d-separation in the underlying DAG (Pearl 2009, Definition 2.4.1).
Faithfulness is a *probabilistic* property — it requires:

- A probability distribution over outcomes
- Conditional independence relationships testable via
  statistical conditional independence tests
- Validation through statistical CI testing

A4 (determinism) is **strictly stronger** in the following
precise sense:

- Under determinism, there is no distribution to average over;
  trajectories are reproduced exactly.
- Conditional independence relationships are trivially satisfied
  (a trajectory determined by inputs is conditionally
  independent of any non-input variable given the inputs).
- The CI testing apparatus is unnecessary: there is nothing to
  test because the joint distribution collapses to a point mass.

Formally, faithfulness can be derived from determinism:

> If $T(c, \iota)$ is deterministic given $(c, \iota)$, then for
> any variable $V$ in $T$ and any conditioning set $S$ containing
> $(c, \iota)$, $V \perp\!\!\!\perp W \mid S$ holds trivially for
> any $W$ that is a deterministic function of $S$.

The converse does not hold: faithfulness does not imply
determinism (faithfulness is consistent with stochastic
trajectories, with the CI structure preserved across the
distribution). Therefore A4 (determinism) is a strict
*strengthening* of Pearl's faithfulness requirement.

**Why this matters for CST.** CST's sufficiency proposition
(§3.3) requires only that the counterfactual trace and original
trace differ exclusively due to the intervention — which
deterministic replay guarantees directly, without recourse to
probabilistic CI testing. Pearl's faithfulness would require CST
to demonstrate CI structure across an ensemble of replays
(infeasible — and unnecessary under A4). EXTp's determinism is
the operational substitute that makes CST's empirical
realizability possible.

This is the formal basis for the "A4 / Replay determinism
(strictly stronger than faithfulness)" framing across §2.4.1,
§3.2, and §2.4.5 correspondence table.

#### 4.4.4 Known failure mode — multi-VCPU non-determinism

A4 fails under concurrent multi-VCPU execution:

- Multiple VCPUs share microarchitectural resources (caches, TLB,
  branch predictor) with race-dependent eviction patterns.
- The order in which VCPUs reach VM-exit points depends on
  scheduling decisions that are not deterministic across replays
  (kernel preemption, interrupt timing, I/O delays).
- Race-induced non-determinism would produce trajectory-level
  divergence across replays even in the absence of intervention,
  breaking SOE's score_S = 1.0000 guarantee.

This failure mode is **explicitly excluded** by the validity
envelope (§3.4): CST v1.0 applies to single-threaded VM-exit
traces with deterministic dispatch. Multi-VCPU counterfactual
replay would require a separate property addressing
race-aware determinism (e.g., schedule-canonicalization or
partial-order replay), tagged as future work.

#### 4.4.5 Note on timing dimension exclusion

A4's determinism guarantee covers the **SOE 4-tuple surface**
only — not the per-event timing $\Delta_i$. Per-event timing
varies across replays due to microarchitectural noise (cache
warming effects, TSC jitter, thermal management, frequency
scaling) characterized by MI's $\hat{\sigma}_{\text{baseline}}$.

A4 does *not* extend to:
$$\Delta_i^{T_1(c, \iota)} = \Delta_i^{T_2(c, \iota)}$$

This is precisely why A3 (timing-clause confounder boundedness
via $\Delta^*$) is a separate assumption: A4 covers
deterministic 4-tuple agreement; A3 covers probabilistic timing-
clause bound.

The clean separation — A4 deterministic + A3 probabilistic —
maps to the OR-clause asymmetry of $D$ (§2.1) and underwrites
the divergence detection function's hybrid statistical nature.

#### 4.4.6 Pearl correspondence cross-reference

Per §2.4.5 correspondence table, A4 maps to "Replay determinism
(strictly stronger than faithfulness)". The strict-stronger
relationship is formalized in §4.4.3 above. The mapping is:

- *Pearl faithfulness* (probabilistic CI, distribution-level)
  $\rightarrow$
- *A4 determinism* (trajectory-level, point-mass distribution)

This is the second of the two *concrete divergences* from
Pearl's classical SCM (the first being reversibility,
§2.4.2 — reversibility absent in EXTp, determinism stronger
than faithfulness in EXTp).

#### 4.4.7 Forward references

- §5.4 — Isabelle formalization, A4 mechanical proof leveraging
  seL4's existing proof harness
- §3.4 — multi-VCPU exclusion in $\mathcal{S}_{\text{out}}$
- §6.2 — citation discipline for "stronger than faithfulness"
  framing in paper text

---

## 5. Concession Footnote

### 5.1 Modularity gap empirical validation (Q4 future experiment)

**Context.** A1 (modularity, §3.2 + §4.1) is currently asserted
*modulo bounded side-effects below $\Delta^*$ on framework
observables*. The gap arises because Capability Separation
establishes authority disjointness ($\mathcal{K}_{\text{int}} \cap \mathcal{K}_{\text{fwk}} = \emptyset$,
§4.1.1) but does not establish strict side-effect freedom on
framework-internal state — the intervention machinery's
*execution* may produce side-effects on shared resources (CPU
cycles, VMM scheduler time, cache lines, branch predictor state)
even though it cannot directly modify framework state.

Three sub-paths of potential indirect modification were
identified in §4.1.2: execution-time consumption, cache-line
displacement, and branch predictor pollution. Q4 empirically
validates whether these sub-paths produce side-effects above
$\Delta^*$ on framework-internal observables.

**Design.** For each intervention class $X \in \{\text{nopcount},
\text{cache\_state}, \text{input}, \text{reg}\}$, measure
side-effect magnitudes on a fixed set of framework observables
under a no-trace-effect intervention pattern:

- *Framework observables to measure:*
  - VMM scheduler dispatch timing (per-VM-exit handler entry
    latency)
  - EPT modification counts under intervention (should be zero
    for non-EPT interventions; if non-zero, indicates indirect
    EPT effect)
  - Capability register state outside intervention authority
    (should be invariant; if changes detected, indicates
    authority leakage)
  - LLC miss rate during VMM dispatch (PMU
    MSR_LAST_LEVEL_CACHE_REFERENCES, MISSES)
  - Branch misprediction rate during VMM dispatch (PMU
    MSR_BR_MISP_RETIRED.ALL_BRANCHES)

- *No-trace-effect intervention pattern:* intervention is
  performed but with parameter set to its natural value (e.g.,
  $do(\text{nopcount} = n_{\text{natural}})$ where
  $n_{\text{natural}}$ is the value the guest would have computed
  without intervention). This isolates the intervention
  *machinery's execution overhead* from the intervention's
  causal effect on the trace.

- *Sample size:* per intervention class, $N \geq 200$ across $\geq 5$
  fresh-boot sessions, matching MI's calibration sample size
  conventions.

**Success criteria.**

- *Strict A1 validated.* All framework observables show no
  change above $\Delta^*$ under intervention (compared to
  no-intervention baseline). A1 is strengthened to strict form;
  the modulo qualifier is lifted in envelope version v1.1.
- *Strict A1 falsified, narrow A1 viable.* Some framework
  observables show changes above $\Delta^*$, but the affected
  observable classes are *identifiable and bounded*. A1 is
  narrowed: the affected classes are excluded from
  $\mathcal{S}_{\text{in}}$; CST coverage shrinks accordingly,
  but the remaining envelope remains coherent.
- *Strict A1 falsified, narrow A1 also falsified.* Framework
  observable changes are pervasive (most observables show
  intervention-correlated changes above $\Delta^*$). The
  modularity assumption fails fundamentally; CST v1.0 is not
  applicable in its current form. Revisit Capability Separation
  authority bounds; consider whether intervention machinery
  itself requires capability scope reduction.

**Forward path.** Q4 is scheduled after CST v1.0 documentation
completion. Estimated execution time: ~10 hours wall-clock for
all four intervention classes across $N \geq 200$ per class.
Results feed into CST envelope version v1.1 (§3.4.5).

### 5.2 Silent microarchitectural divergence (CMD future scope)

**Context.** A2 (observational completeness, §3.2 + §4.2) is
asserted *modulo silent leak*: causal effects of $do(X = x')$
that produce neither 4-tuple delta nor timing deviation above
$\Delta^*$ are outside CST's observable surface. Three classes
of silent leak were enumerated in §4.2.4: cache state without
timing manifestation, branch predictor state without observable
consequence, TLB state without observable consequence.

Addressing this scope-out requires extending the observable
surface to include microarchitectural state counters not present
in MI's current instrument set.

**Design.** Develop a separate property class —
**Counterfactual Microarch Divergence (CMD)** — that extends
CST's observable surface using Intel PMU counters:

- *Cache observability:* LLC miss rate
  (MSR_LAST_LEVEL_CACHE_REFERENCES, MSR_LAST_LEVEL_CACHE_MISSES),
  L1/L2 miss rates (MSR_MEM_LOAD_RETIRED.L1_MISS,
  L2_MISS), cache line ownership transitions
  (MSR_L2_RQSTS family).
- *Branch predictor observability:* misprediction rate
  (MSR_BR_MISP_RETIRED.ALL_BRANCHES), conditional vs indirect
  branch misprediction breakdown
  (MSR_BR_MISP_RETIRED.COND, .INDIRECT_CALL).
- *TLB observability:* DTLB/ITLB miss rates
  (MSR_DTLB_LOAD_MISSES.MISS_CAUSES_A_WALK,
  MSR_ITLB_MISSES.MISS_CAUSES_A_WALK), TLB shootdown counts
  (MSR_PERF_COUNT_HW_CACHE_MISSES with DTLB/ITLB cache types).

These counters are accessible via RDMSR at VM-exit or via the
perf_event subsystem (which CST's bare-metal seL4 environment
does not currently expose; PMU access machinery is a separable
infrastructure prerequisite).

**Success criteria.**

- *CMD as additive property class.* CMD's claim form is a
  parallel of CST's atomic claim, with the observable surface
  $D$ extended to include PMU-counter deltas:
  $D_{\text{CMD}} = D_{\text{CST}} \cup \{\text{PMU counter}_k\text{ delta} > \delta_k^*\}$
  where $\delta_k^*$ is a per-counter noise floor calibrated
  analogously to MI's $\Delta^*$.
- *Silent leak narrowing.* Under CMD, the silent leak class
  shrinks from "any cache/branch/TLB state change without
  timing manifestation" to "any cache/branch/TLB state change
  without PMU counter delta above per-counter threshold." This
  is a strict narrowing, not elimination: PMU counters
  themselves have noise floors, and silent leak classes outside
  the validated PMU counter set remain.
- *Composition with CST.* A CMD claim implies the corresponding
  CST claim (the CMD observable surface is a superset of CST's);
  the converse does not hold. Citations of CMD-grounded claims
  must declare CMD envelope, distinct from CST envelope.

**Forward path.** CMD is **deferred future work**, not part of
CST v1.0. Prerequisites:

- PMU access machinery in bare-metal seL4 VMM (RDMSR
  privileged-mode access, MSR allowlisting for perf-event
  counters).
- Per-counter noise floor calibration analogous to MI's
  $\hat{\sigma}_{\text{baseline}}$ characterization, per workload
  class.
- Q4 modularity validation (§5.1) — CMD's intervention machinery
  must satisfy A1; the PMU readout itself is an additional
  side-effect surface to validate.

CMD's relationship to CST is *additive extension*, not
*replacement*: CST v1.0 stands as a valid soundness theorem
within its enumerated bounds; CMD widens the bounds.

### 5.3 Pearl/Woodward literature alignment

**Context.** §2.4 maps Pearl's atomic-intervention axioms and
do-calculus rules onto CST, plus Halpern-Pearl 2005's actual-
causation conditions. This subsection situates CST within the
broader Pearl/Woodward causal inference literature, explicitly
identifying convergences and divergences for paper-defensible
positioning.

**Design.** Document four categories of relationship:

- *Convergences (CST adopts Pearl/Woodward concepts directly):*
  - $do(\cdot)$ operator as the foundational intervention
    primitive (Pearl 2009 ch. 3).
  - Modularity axiom (intervention affects only target and
    descendants) — A1 (§3.2 + §4.1).
  - Sufficiency-by-axiom-composition methodology (theorem
    structure mirrors Pearl 2009 §7.3).
  - Actual-causation AC1/AC2 conditions (Halpern-Pearl 2005)
    underwriting $\rightsquigarrow_i$ operator semantics
    (§2.4.4).

- *Concrete divergences (CST explicitly differs):*
  - *Reversibility absent.* Pearl 2009 Def. 7.3.1's
    reversibility axiom is *inapplicable* under EXTp's linear-
    time irreversible execution (§2.4.2). CST claims do not
    invoke reversibility-style reasoning; this is a scope
    restriction, not a failure.
  - *Determinism stronger than faithfulness.* A4 (§4.4.3)
    formalizes determinism as strictly stronger than Pearl's
    probabilistic faithfulness. CST does not require Pearl's
    CI-testing apparatus; trajectory-level reproducibility
    substitutes.
  - *Observational surface explicit.* Pearl operates on abstract
    DAGs; CST operates on concrete 4-tuple + timing surface with
    explicit scope ($\mathcal{E}$, §3.4). The DAG is implicit in
    EXTp; explicit DAG construction is not a CST primitive.
  - *Confounder framing.* Pearl uses latent-variable formalism;
    CST uses instrument-bounded noise (MI $\Delta^*$, A3 in §4.3).
    Latent variables are replaced by empirical calibration.

- *Partial mappings (CST covers a restricted subset):*
  - *do-calculus rules in degenerate-deterministic form.* The
    three rules of Pearl 2009 Theorem 3.4.1 carry over to CST
    but in a degenerate form under A4 (§2.4.3): they serve as
    consistency anchors, not inference rules.
  - *Halpern-Pearl AC3 minimality absent.* AC3 (minimality)
    is out of CST v1.0 scope (§2.4.4); CST yields causal-link
    claims, not causal-explanation claims.

- *Adjacent frameworks not adopted:*
  - *Woodward (2003) interventionism.* Woodward's manipulability
    framing is largely consonant with EXTp's intervention-based
    causation, but Woodward's emphasis on *invariance under
    intervention* (a relationship is causal if it remains stable
    across a range of interventions) is not a CST primitive —
    CST attributes causation per-claim, not via invariance
    across an intervention range. Future extension (sensitivity-
    range analysis under CST claims) could incorporate
    Woodward-style invariance; flagged as deferred.
  - *Spirtes-Glymour-Scheines (SGS) constraint-based causal
    discovery.* SGS uses observational conditional independence
    constraints to recover causal structure; CST does not
    perform causal discovery, only causal attribution. The two
    frameworks address different problems.

**Success criteria.** This subsection serves as the
*literature-alignment document* for CST: it gives reviewers a
clear map of which Pearl/Woodward apparatus CST adopts, which
it diverges from concretely, and which it does not engage at
all. The map is paper-text-friendly: each category produces
direct citation lines (e.g., "CST adopts Pearl 2009's $do(\cdot)$
operator; diverges from Pearl 2009's reversibility axiom; does
not engage Spirtes-Glymour-Scheines causal discovery").

**Forward path.** Literature alignment is *documentation-only*,
not an experimental concession. The forward path is paper-text
incorporation: §6.2's citation discipline references this
subsection for Pearl/Woodward citations in paper prose. Future
work extending CST to incorporate Woodward-style invariance is
deferred without scheduled timeline.

### 5.4 Isabelle formalization deferred (future work)

**Context.** §3.3 provides a *semi-formal sketch proof* of CST's
sufficiency proposition, at the level appropriate for paper-text
inclusion. Mechanical formalization of state-evolution semantics
and exhaustive case enumeration is deferred. This subsection
documents the leverage available for full formalization and the
prerequisites.

**Design.** Full mechanical proof of CST in Isabelle/HOL would
proceed as follows:

- *Build on seL4's existing proof harness.* The seL4
  microkernel has Isabelle/HOL formalization at the kernel
  layer (functional correctness via spec→C refinement plus
  integrity/confidentiality at the spec level, with coverage
  varying by architecture). **Scope clarification:** CST's
  intervention machinery operates in the VMM layer **above**
  seL4's verified kernel scope. "Building on seL4's proof
  harness" therefore means *leveraging the existing capability
  framework formalization as a foundation*, not directly
  extending verified theorems. The VMM-layer formalization is
  itself non-trivial (intervention machinery predicates,
  capability-mediated authority bounds, trace event semantics
  in HOL); seL4 harness leverage reduces but does not eliminate
  the formalization cost. This is a multi-year effort, not a
  small extension.
- *Formalize §3.2 assumptions as Isabelle predicates.* Each
  assumption A1–A4 becomes a HOL predicate over the trace and
  configuration:
  - $A_1(c, \iota)$: modularity predicate (intervention's
    framework-state-invariance).
  - $A_2(c, \iota)$: observational completeness predicate
    (every causal effect in the observable union or silent
    leak).
  - $A_3(c, \iota)$: confounder boundedness predicate
    ($\Delta^*$-bounded timing FPR).
  - $A_4(c, \iota)$: replay determinism predicate
    (trajectory-level reproducibility).
- *Mechanize §3.3 sketch proof.* The threat decomposition
  (coincidence/silent mechanism/confounder) becomes a structural
  induction on the trace and intervention pair, with each
  threat addressed by the corresponding assumption predicate.
- *Mechanize §3.4 envelope.* The validity envelope
  $\mathcal{E}$ becomes a record type with explicit in-scope /
  out-of-scope sentinels; claim admissibility becomes a
  decidable predicate over $\mathcal{E}$.

**Success criteria.**

- *CST composition closure theorem mechanically proven.* The
  Isabelle theorem matches Theorem 3.1's statement: under A1–A4
  predicates and admissible $\mathcal{E}$, the atomic CST claim
  is sound.
- *Compositional extension mechanically proven.* Proposition
  3.3.1 follows by Isabelle structural induction over chain
  length.
- *Failure modes mechanically encoded.* Each out-of-scope
  condition (§3.4.3) becomes an Isabelle counter-example or
  exclusion lemma.
- *Pearl/HP correspondence mechanically verified.* Conditions
  (i)–(iv) of Theorem 3.1 become Isabelle subtheorems.

**Forward path.** Isabelle formalization is **deferred future
work**, not part of CST v1.0. The deferral is not a weakness:
the *infrastructure exists* (seL4 proof harness, Isabelle/HOL
toolchain), removing the "could this even be formalized?"
reviewer concern. Paper text should explicitly cite this
deferral: "CST's composition theorem is semi-formally
established in [paper]; mechanical Isabelle formalization
leveraging seL4's existing proof harness is deferred to future
work."

This positioning is the canonical pattern for theorem-paper
publications where formal mechanization is desirable but not
within the publication's scope: state the theorem rigorously,
provide semi-formal proof, point to the formalization path with
sufficient detail that future work is clearly chartered.

---

## 6. Implications

### 6.1 For replay verdict interpretation

This subsection specifies how CST is consumed by the **replay
verdict interpretation pipeline** — the system component that
takes a counterfactual replay output (original and counterfactual
traces) and produces a structured causal claim.

**Frozen — verdict format.**

Every replay verdict that asserts a causal attribution must
conform to the CST atomic claim format (§2.3):

$$\big\langle do(X = x') \rightsquigarrow_i D \;\big|\; A_1, A_2, A_3, A_4;\;\mathcal{E} \big\rangle$$

or its compositional extension (§3.3.1) for chains. Specifically,
every verdict must explicitly carry:

- The intervention $do(X = x')$ that was performed
  (with $X$ from §2.2's validated intervention surface)
- The event index $i$ at which the divergence was observed
- The observed divergence $D = \text{true}$ on the SOE 4-tuple
  + MI timing surface
- The four assumptions $A_1, A_2, A_3, A_4$ tagged as satisfied
  (with assumption-specific validation references — e.g.,
  "A4 validated by Cross_Boot_Stability_N34")
- The validity envelope $\mathcal{E}$ as a 6-tuple, with
  $\text{instr}$, $\text{wl-class}$, $\text{gw-type}$,
  $\text{scope}$, $\mathcal{S}_{\text{in}}$,
  $\mathcal{S}_{\text{out}}$ explicit

A verdict missing any of these components is **structurally
incomplete** and must not be reported as a CST claim.

**Frozen — admissibility check pipeline.**

The verdict interpretation pipeline must perform the following
admissibility checks in order:

1. *Envelope match check.* Does $\mathcal{E}$'s tuple components
   match a configuration for which CST v1.0 has validated
   coverage? If any component falls outside the validated set
   (e.g., $\text{wl-class} = $ LLC-pchase), the claim is
   **structurally invalid**, halt with envelope-mismatch error.
2. *Assumption validation check.* For each $A_k$, is the
   validation reference present and current? (E.g., A4
   references Cross_Boot_Stability_N34, A3 references MI §4.1
   for the relevant workload class.) Missing or stale validation
   references halt with assumption-incomplete error.
3. *Surface check.* Was $D(T_{\text{orig}}, T_{\text{cf}}, i) =
   \text{true}$ actually observed? Verdict cannot be issued
   without observed divergence; empty claims are structurally
   forbidden per Theorem 3.1's biconditional.
4. *Intervention surface check.* Is $X$ within §2.2's validated
   intervention surface (one of: nopcount, cache_state, input,
   reg)? If $X$ is from a future-extension surface (interrupt,
   EPT, MSR), the claim is **structurally invalid** under CST
   v1.0, halt with intervention-surface-mismatch error.

Failure of any check produces a *structural-invalidity error*,
not a "weak claim." CST is binary on admissibility: a claim is
either admissible (passes all checks) or structurally invalid
(fails any check). There is no "approximately admissible" or
"low-confidence admissible" category.

**Evolving — verdict aggregation.**

When multiple atomic claims are produced from a single
counterfactual replay (e.g., divergence at multiple events,
each potentially attributable to the same intervention), the
aggregation strategy is not yet locked. Two candidate
approaches:

- *Per-event claim enumeration.* Each $i$ for which $D(\ldots, i) = \text{true}$
  produces a separate atomic claim. The verdict is a *set* of
  atomic claims, one per divergent event.
- *Earliest-divergence atomic claim.* Only the earliest $i^*$
  with $D = \text{true}$ is reported as an atomic claim; later
  divergent events are treated as causal descendants of the
  earliest divergence under A1+A4.

The two approaches differ in how compositional structure is
extracted from the observed divergence pattern. CST v1.0 does
not lock this aggregation; pipeline implementations may use
either, with the choice declared in the verdict metadata.

### 6.2 For paper framing

This subsection specifies the **citation discipline** for CST
claims in paper text. CST's epistemic envelope and Pearl/HP
correspondence are non-trivial; paper text must carry them
faithfully to avoid reviewer misreading.

**Frozen — citation requirements.**

Every paper-text citation of a CST claim must carry:

- *The atomic claim form* — either the full notation
  $\langle do(X=x') \rightsquigarrow_i D \mid A;\;\mathcal{E} \rangle$,
  or a prose form that explicitly names $X$, $x'$, event $i$,
  $D$, the assumption set, and envelope characteristics.
- *Envelope version stamp* — "admissible under CST v1.0
  envelope" or equivalent; future versions (v1.1 after Q4
  resolution, v2.0 with CMD extension) require explicit
  versioning. Unversioned citations are **forbidden** — they
  obscure scope.
- *Assumption qualifier* where relevant — A1-modulo (current
  empirical status), A2-modulo-silent-leak (the silent leak
  scope-out), A3-empirical vs A3-nominal (which FPR bound is
  being cited).
- *Workload class and guest-workload type* — claim citations
  must name the (workload class, guest-workload type) pair
  matching the envelope's calibration, not just a generic
  "the workload."

**Frozen — forbidden framings.**

The §3.4.4 negative-framing rules are reiterated here as paper-
text-specific forbidden formulations:

- ❌ "EXTp proves $X$ is the cause of $Y$" — missing envelope
  qualifier and minimality.
- ❌ "EXTp shows $X$ causes $Y$ across configurations" — cross-
  configuration claims are structurally invalid.
- ❌ "Replay of $X$ proves $Y$ would not have occurred without
  $X$" — modal counterfactual, not CST's deterministic
  trajectory framing.
- ❌ "EXTp's framework eliminates confounders" — A1 modulo Q4
  gap is partial.
- ❌ "CST validates that $X$ caused $Y$ through mechanism $M$" —
  mechanism out of scope.
- ❌ Citing CST without envelope version stamp.

The replacements for each (with admissible formulations) are
specified in §3.4.4.

**Frozen — Pearl/HP citation pattern.**

When paper text invokes Pearl's apparatus, citations must use
the §5.3 literature-alignment map:

- *Pearl 2009 do-operator* — adopted; cite as foundational.
- *Pearl 2009 reversibility axiom* — diverged; cite as
  inapplicable (linear-time execution).
- *Halpern-Pearl 2005 AC1/AC2* — adopted; underwrites
  $\rightsquigarrow_i$ semantics.
- *Halpern-Pearl 2005 AC3* — not adopted; cite as out of CST
  v1.0 scope.
- *Pearl 2009 faithfulness* — diverged; cite as strictly
  weaker than A4 determinism.
- *Pearl 2009 do-calculus rules (1, 2, 3)* — partial mapping
  in degenerate-deterministic form; cite as consistency anchor,
  not inference rule.
- *Woodward 2003 invariance* — adjacent, not engaged in CST
  v1.0.

Citations of Pearl/HP work that misrepresent CST's relationship
to them are paper-defect-class issues; reviewer pushback on
these citations should be addressed by deferring to this
subsection's map.

**Evolving — notation conventions in paper text.**

CST's notation $\langle \cdot \mid \cdot ; \cdot \rangle$ is
verbose for inline paper text; an abbreviated form is needed
for readability. Two candidates:

- *Subscript-clause form:* $\text{CST}_{(\mathcal{E})}[do(X) \to D]$
  — compact but loses assumption tags.
- *Inline-comma form:* $do(X=x') \rightsquigarrow_i D$ (assumed
  $A_1$–$A_4$ under $\mathcal{E}_{\text{v1.0}}$) — verbose but
  carries full information.

CST v1.0 does not lock the abbreviated form; paper text may
use either, with the convention declared at first use.

### 6.3 For demonstration cases (requirements only)

This subsection specifies the **requirements** that a CST
demonstration case must satisfy. Demonstration cases — toy
exploits, CVE-based scenarios, synthetic divergence examples —
are *parallel artifacts*, not embedded within this CST entry.
Each demonstration is a separate vault entry (e.g.,
`CST_Demonstration_<case>.md`); this subsection locks what they
must show, not which specific cases are selected.

**Frozen — minimum demonstration requirements.**

A CST demonstration case must show:

(i) **Intervention performed.** The intervention $do(X = x')$
is performed using EXTp's intervention machinery under §2.2's
intervention model. The intervention class, scope, and timing
are explicit. The intervention surface ($X$) is one of the four
validated classes.

(ii) **Divergence observed.** The divergence $D = \text{true}$
is observed on the SOE 4-tuple + MI Δ* surface at a specified
event $i$. The observation is reported with raw delta values
(4-tuple component-by-component, timing delta with MI Δ*
threshold).

(iii) **Causal attribution defensible within envelope.** The
attribution of divergence to intervention is defensible within
CST's §3.4 validity envelope. The envelope tuple is explicit;
the assumptions A1–A4 are validated against their evidence
references.

(iv) **Admissibility tuple matched.** The (hardware, instrument,
workload class, guest-workload type) admissibility tuple matches
the calibration conditions for $\hat{\sigma}_{\text{baseline}}$
and $\Delta^*$ used in the demonstration. Citation to MI's
calibration source (§4.1 / §4.3) is explicit.

**Frozen — fuzzing-application hook.**

CST-grounded counterfactual fuzzing — sequences of CST
interventions used to systematically explore input space with
causal-attribution-aware feedback — is a **natural downstream
application** flagged in §2.2. A demonstration case may
incorporate fuzzing-style multi-intervention sweep, *provided*
each atomic intervention in the sweep is independently
CST-admissible (per §3.3.1 per-step independence requirement).

A fuzzing-style demonstration must additionally show:

- *Per-intervention CST admissibility.* Each intervention in the
  sweep produces a CST-admissible atomic claim under its own
  envelope.
- *Sweep aggregation strategy.* How the per-intervention claims
  combine to produce a fuzzing-level observation (e.g., "12 of
  20 interventions in the input-byte sweep produced
  CST-admissible divergence at event $i_{42}$").
- *Causal-attribution-aware feedback.* The fuzzing strategy uses
  CST verdicts (admissibility, not just divergence) to guide
  subsequent interventions — distinguishing CST-grounded
  fuzzing from classical random-mutation fuzzing.

The fuzzing-application hook is a *requirements anchor*, not a
prescription. Specific fuzzing strategies (mutation operators,
feedback heuristics, coverage metrics) are implementation
choices for individual demonstration cases.

**Frozen — demonstration metadata.**

Each demonstration case entry must declare in its frontmatter:

- *Case type:* toy / CVE-based / synthetic
- *Intervention class(es) used:* subset of {nopcount,
  cache_state, input, reg}
- *Envelope version:* CST v1.0 (or later as envelope evolves)
- *Validation references:* the assumption-evidence chain
  (§4.1–§4.4) cited per assumption
- *Replay artifacts:* raw delta logs, traces, configuration
  identifier (matching CST §3.4.1 envelope tuple)

**Evolving — case selection.**

Which specific demonstration cases are pursued is **out of CST
v1.0 entry scope** — case selection happens in parallel artifact
planning. Plausible candidates currently under consideration
(non-binding, listed for context):

- *Toy exploit:* a synthetic exploit pattern constructed for
  demonstration purposes, with full control over input/output
  surface. Lowest risk for first demonstration.
- *CVE-based:* an existing CVE (e.g., from the user's prior
  vault entries — CVE-2025-38352 "Chronomaly" or AppArmor
  "CrackArmor" cluster) recast in the EXTp counterfactual replay
  framework.
- *Synthetic divergence injection:* no real exploit, but a
  controlled divergence pattern injected via the intervention
  machinery to validate the CST attribution pipeline end-to-end.

Selection criteria and execution sequence are tracked in
parallel artifact planning documents, not in this CST entry.

---

## 7. Files

**Adjacent property entries (cross-referenced).** CST derives
its four assumptions from upstream property entries; each
derivation is cross-referenced in §4:

- `Capability_Separation_Theorem.md` — A1 (Modularity)
  derivation per §4.1. Provides authority disjointness
  $\mathcal{K}_{\text{int}} \cap \mathcal{K}_{\text{fwk}} = \emptyset$;
  the side-effect-freedom gap is addressed by Q4 future
  experiment (§5.1).
- `Strong_Observational_Equivalence.md` — A2 (Observational
  completeness, 4-tuple surface) per §4.2.1 and A4 (Replay
  determinism, score_S=1.0000 baseline) per §4.4.1.
- `Cross_Boot_Stability_N34.md` — A4 empirical support
  (score_S = 1.0000 across N=34 cross-boot trials) per §4.4.1.
- `Measurement_Interference.md` — A2 (timing surface extension,
  $\Delta^*$) per §4.2.2 and A3 (Confounder boundedness,
  $\hat{\sigma}_{\text{baseline}}$ and empirical realized FPR)
  per §4.3.

**Raw delta logs and analysis scripts.** Calibration data
referenced by A3 evidence are stored in the MI entry's §7;
CST does not duplicate these references. The relevant logs
(boot_log8, boot_log12, boot_log14, boot_log15) and analysis
pipeline (analyze_noise_floor.py, Workload Class analysis
script) are cited per MI §7.

**Forward references (forthcoming artifacts).**

- **CMD entry** (Counterfactual Microarch Divergence) —
  silent microarch divergence addressing per §5.2.
  Prerequisite: PMU access machinery in bare-metal seL4 VMM
  (RDMSR privileged-mode access, MSR allowlisting for
  perf-event counters); per-counter noise floor calibration
  analogous to MI's $\hat{\sigma}_{\text{baseline}}$
  characterization, per workload class; Q4 modularity
  validation for the PMU readout itself.
- **CST_Demonstration_*.md** (forthcoming) — demonstration
  case entries per §6.3 requirements. Candidate cases
  (toy / CVE-based / synthetic) selected in parallel artifact
  planning.
- **Q4 modularity validation experiment** (forthcoming) —
  empirical validation of A1 strict-vs-modulo status per §5.1.
- **Isabelle/HOL formalization** (deferred, §5.4) — mechanical
  proof of Theorem 3.1 and Proposition 3.3.1, leveraging seL4's
  existing Isabelle proof harness.
- **Paper text** (forthcoming) — citation conventions per §6.2;
  Lemma 3.1.1 (Pearl-conformity) extraction from Theorem 3.1's
  conditions (i)–(iv) for paper-text formal presentation.

**Configuration identifier.** CST v1.0 envelope is calibrated
against the configuration documented in MI §7 Reproducibility:
Intel 12th Gen Core (Alder Lake), microcode 0x3e, ASUS Z690 with
UEFI, bare-metal seL4 VMM (no Linux host), serial console
infrastructure (DIGITUS USB-Serial FT232RL, Digitus DS-30000-1
PCIe Serial, RS-232 null modem). Claims under different
configurations require envelope recalibration per §3.4.5.

---

**Vault localization pending.** CST entry is written in pure
English; other vault entries (MI, SOE, Capability Separation)
use Turkish-English mixed prose for explanatory annotations.
A localization pass — adding Turkish annotation layer for
explanatory paragraphs while preserving English for formal
statements, axiom names, and mathematical notation — is
scheduled after CST §1–§7 reach final v1.0 state. Formal
content stays English-only; annotations gain Turkish layer in
post-completion pass.

---

**CST v1.0 status: complete.** All assumptions derived, sketch
proof in place, validity envelope explicit, concessions
enumerated with forward paths, implications locked. Pending
work (Q4 modularity validation, CMD development, Isabelle
formalization, demonstration cases, paper-text curation) is
tracked above as forward references.
