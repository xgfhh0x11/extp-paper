# EXTp Formal Properties — Pure Mathematical Formalization

Notation and primitive symbols only. Each property tagged by layer.

---

## Primitives

Let:
- $S$ = system state space
- $\Sigma$ = observable surface, $\Sigma \subseteq S$
- $\mathcal{K} = \mathcal{K}_\text{verified} \cup \mathcal{K}_\text{extended}$ = capability set, with $\mathcal{K}_\text{verified} \cap \mathcal{K}_\text{extended} = \emptyset$
- $\mathcal{K}_\text{int} \subseteq \mathcal{K}$ = intervention machinery authority set
- $\mathcal{K}_\text{fwk} \subseteq \mathcal{K}$ = framework-internal authority set
- $T_\text{orig}, T_\text{cf}$ = event sequences $[e_0, e_1, \ldots, e_n]$ where each $e_i \in \Sigma \times \mathbb{N}$
- $\text{do}(X = x')$ = Pearl intervention operator on variable $X$ at event $e_i$
- $D : T_\text{orig} \times T_\text{cf} \times \mathbb{N} \to \{\text{true}, \text{false}\}$ = divergence detection function
- $\Delta^\star \in \mathbb{N}$ = empirical timing threshold (calibration-derived)
- $\hat\sigma_\text{baseline} \in \mathbb{N}$ = baseline timing standard deviation
- $\alpha \in (0, 1)$ = significance level

[Layer: notation]

---

## P1 — Capability Separation (CapSep)

$$
\mathcal{K}_\text{int} \cap \mathcal{K}_\text{fwk} = \emptyset
$$

with two-layer strength:

- $\forall k \in \mathcal{K}_\text{verified}$: separation holds **unconditionally** (inherited from L4.verified functional correctness)
- $\forall k \in \mathcal{K}_\text{extended}$: separation holds **empirically**, bounded by Clopper-Pearson one-sided $(1-\alpha)$ confidence interval on observed zero-failure trials:

$$
P(\text{failure}) \leq 1 - \alpha^{1/N}
$$

for $N$ trials with zero observed failures.

[Layer: structural-empirical hybrid]

---

## P2 — Strong Observational Equivalence (SOE)

For counterfactual replay under intervention $\text{do}(X = x')$ at event $e_i$:

$$
\text{SOE}(T_\text{orig}, T_\text{cf}, i) \iff \forall j < i:\ \pi_\Sigma(T_\text{orig}[j]) = \pi_\Sigma(T_\text{cf}[j])
$$

where $\pi_\Sigma$ projects an event onto its observable surface tuple.

The 4-tuple surface: $\pi_\Sigma(e) = (\text{exit\_reason}, \text{guest\_rip}, \text{exit\_qualification}, \text{guest\_linear\_address})$.

[Layer: structural]

---

## P3 — Measurement Interference (MI)

Define intervention signature:

$$
\text{sig}(\text{do}(X = x')) := \overline{T_\text{cf}} - \overline{T_\text{orig}}
$$

where $\overline{T}$ denotes per-event timing mean over $N$ samples.

**A1-modulo (apparatus-bounded) bound:**

$$
|\text{sig}(\text{do}(X = x'))| < \Delta^\star
$$

with threshold:

$$
\Delta^\star := z_{1-\alpha} \cdot \hat\sigma_\text{baseline}
$$

where $z_{1-\alpha}$ is the $(1-\alpha)$ quantile of the standard normal.

Calibration validity: $\hat\sigma_\text{baseline}$ estimated under $\chi^2$ confidence interval, requires $N \geq N_\text{min}$ samples for statistical adequacy.

[Layer: empirical-statistical]

---

## P4 — Counterfactual Soundness Theorem (CST), atomic case

**Theorem 1.** Let $T_\text{orig}, T_\text{cf}$ be counterfactual replays under single intervention $\text{do}(X = x')$ at event $e_i$. Define:

$$
\text{Admissible}(T_\text{orig}, T_\text{cf}, i) \iff
\begin{cases}
D(T_\text{orig}, T_\text{cf}, i) = \text{true} \\
\land\ A_1(T_\text{orig}, T_\text{cf}) \\
\land\ A_2(\Sigma) \\
\land\ A_3(\mathcal{S}_\text{in}, X, x') \\
\land\ A_4(i)
\end{cases}
$$

where antecedents:

- $A_1$: MI clause holds — $|\text{sig}(\text{do}(X=x'))| < \Delta^\star$ (apparatus-bounded)
- $A_2$: validity envelope $\mathcal{E}$ — observable surface tuple is well-defined and consistently captured
- $A_3$: $X \in \mathcal{S}_\text{in}$ — intervention target lies in validated intervention surface
- $A_4$: SOE holds — $\forall j < i: \pi_\Sigma(T_\text{orig}[j]) = \pi_\Sigma(T_\text{cf}[j])$

**Claim:** admissibility ⟺ the counterfactual claim $\langle \text{do}(X = x') \rightsquigarrow_i D \mid A; \mathcal{E} \rangle$ satisfies Halpern-Pearl actual cause conditions (AC1, AC2(a), AC3) within scope $A$.

[Layer: meta-property; conjunction of P1–P3 + Pearl alignment]

---

## P5 — Sequential Composition Closure

**Proposition 1.** For ordered intervention sequence $[\text{do}(X_1 = x_1'), \text{do}(X_2 = x_2'), \ldots, \text{do}(X_n = x_n')]$ producing trace $T_\text{cf}$:

$$
\text{Admissible}(T_\text{orig}, T_\text{cf}, [i_1, \ldots, i_n]) \iff
\bigwedge_{k=1}^{n} \text{Admissible}(T_\text{orig}^{(k-1)}, T_\text{cf}^{(k)}, i_k)
$$

where $T_\text{cf}^{(k)}$ is the trace after applying the first $k$ interventions, and $T_\text{cf}^{(0)} = T_\text{orig}$.

**Commutativity not assumed:** $\text{do}(X_1 = x_1') \to \text{do}(X_2 = x_2')$ may produce different divergence patterns than $\text{do}(X_2 = x_2') \to \text{do}(X_1 = x_1')$.

[Layer: structural induction over P4]

---

## P6 — Q4 Modularity (Intervention Surface Composability)

For validated intervention surface $\mathcal{S}_\text{in}$ partitioned into classes $\mathcal{S}_\text{in} = \mathcal{C}_\text{nopcount} \cup \mathcal{C}_\text{regwrite} \cup \mathcal{C}_\text{inputvalue} \cup \mathcal{C}_\text{cache}$:

$$
\forall X \in \mathcal{C}_i, \forall x' \in \text{dom}(X): \text{Admissible-class}(\mathcal{C}_i) \implies \text{Admissible}(\text{do}(X = x'))
$$

i.e., class-level admissibility lifts to instance-level admissibility within validated classes.

[Layer: structural — type-level invariant]

---

## P7 — Pearl/Halpern-Pearl Alignment

Pearl SCM intervention semantics:

$$
P(Y = y \mid \text{do}(X = x')) = \sum_{z} P(Y = y \mid X = x', Z = z) \cdot P(Z = z)
$$

where $Z$ are non-descendants of $X$. EXTp operationalizes this via fresh-boot discipline ensuring $Z$ independence across replay sessions.

Halpern-Pearl actual cause conditions for claim $\langle X = x' \text{ caused } \varphi \rangle$:

- **AC1:** $X = x'$ and $\varphi$ both occurred in the actual world
- **AC2(a):** $\exists$ partition $(\mathcal{Z}, \mathcal{W})$ and value $x''$ such that under $\text{do}(X = x'', \mathcal{W} = w^*)$, $\varphi$ does not hold
- **AC3:** $X$ is minimal — no proper subset of $X$ satisfies AC1–AC2

EXTp's mapping:

$$
\text{AC1} \leftrightarrow D(T_\text{orig}, T_\text{cf}, i) = \text{true} \text{ observed in } T_\text{cf}
$$

$$
\text{AC2(a)} \leftrightarrow \pi_\Sigma(T_\text{cf}[i]) \neq \pi_\Sigma(T_\text{orig}[i]) \text{ under counterfactual variation of } X
$$

$$
\text{AC3} \leftrightarrow \text{per-event intervention scope: } X \text{ set exactly at } e_i
$$

[Layer: semantic mapping — Pearl ↔ EXTp]

---

## P8 — Scope Conditioning (Validity Envelope $\mathcal{E}$)

All claims are conditioned on configuration tuple:

$$
\mathcal{E} = (h, m, v, \kappa)
$$

where:
- $h$ = hardware revision (CPU model + microcode revision)
- $m$ = microcode patch state
- $v$ = VMM build hash
- $\kappa$ = calibration parameters $(\hat\sigma_\text{baseline}, \Delta^\star, N_\text{calibration})$

Claims do not transfer across $\mathcal{E}' \neq \mathcal{E}$ without recalibration:

$$
\text{Admissible}(T_\text{orig}, T_\text{cf}, i; \mathcal{E}) \not\implies \text{Admissible}(T_\text{orig}, T_\text{cf}, i; \mathcal{E}')
$$

Recalibration cost: $N_\text{recal} \geq 200$ cross-boot trials to re-establish MI $\hat\sigma_\text{baseline}$ and CapSep Clopper-Pearson bounds.

[Layer: meta — conditioning frame on P1–P7]

---

## Property Dependency Graph

```
P1 (CapSep) ─────┐
                 ├──> P4 (CST) ──> P5 (Sequential Composition)
P2 (SOE) ────────┤        │
                 │        └──> P6 (Q4 Modularity)
P3 (MI) ─────────┘        │
                          │
P7 (Pearl/HP) ────────────┘
                          
P8 (Scope Conditioning) ──> conditions all of P1–P7
```

[Layer: meta — structural dependency map]
