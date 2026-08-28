#!/usr/bin/env python3
"""
apply_fixes_v2.py — Apply wave-2 EXTp NDSS revision patches.

PREREQUISITE: extp_revised.tex from wave 1 must exist (default input).
              This script operates on the OUTPUT of apply_fixes.py.

Usage:
    python3 apply_fixes_v2.py [--input extp_revised.tex] [--output extp_revised_v2.tex] [--dry-run]

Patches applied (wave 2):
    P14  Abstract: "1.0000" hedging with Clopper-Pearson bound
    P15a §VIII-A: AID distinction — substrate + enumerated antecedents
    P15b §VII-C: Mechanization difficulty — two specific layers
    P16  §II-C: AC3 / causal-link legitimacy defense
    P17b §VI-D: Workload-class calibration scope reframing
    P18  §VII-A: Chronomaly cross-reference consistency flag

DEPENDENCY ON WAVE 1:
    P15a operates on text that wave-1 E2 produced. Running wave-2
    without wave-1 first will fail P15a's OLD-string match (correctly).
"""

import argparse
import sys
from pathlib import Path

# =====================================================================
# Wave-2 patches
# =====================================================================

# --- P14: Abstract 1.0000 hedging ---
P14_OLD = """Separation (Pearl modularity; Clopper-Pearson bound
${\\leq}0.37\\%$ at $N{=}998$), Strong Observational Equivalence
(replay determinism, $\\scoreS{=}1.0000$ over $N{=}34$ cross-boot
trials), and Measurement Interference (calibrated timing threshold,"""

P14_NEW = """Separation (Pearl modularity; Clopper-Pearson bound
${\\leq}0.37\\%$ at $N{=}998$), Strong Observational Equivalence
(replay determinism: $\\scoreS{=}1.0000$ observed over $N{=}34$
cross-boot trials, Clopper-Pearson one-sided $95\\%$ upper bound on
the per-run failure rate ${\\leq}10.4\\%$), and Measurement
Interference (calibrated timing threshold,"""


# --- P15a: §VIII-A AID distinction (operates on wave-1 E2 output) ---
P15a_OLD = r"""statistical setting; EXTp targets hypervisor exploit execution on a
formally verified microkernel in a deterministic single-configuration
replay setting; and AID does not provide a formal soundness theorem
for its causal attributions. EXTp's CST is the first soundness
theorem for causal exploit attribution grounded in a verified
microkernel substrate (seL4's L4.verified~\cite{klein2014sel4})."""

P15a_NEW = r"""statistical setting; EXTp targets hypervisor exploit execution on a
formally verified microkernel in a deterministic single-configuration
replay setting; and AID does not provide a formal soundness theorem
for its causal attributions. EXTp's CST is the first soundness
theorem for causal exploit attribution that combines two
ingredients absent from AID: a formally verified computational
substrate (seL4's L4.verified~\cite{klein2014sel4}), and admissibility
conditioned on an enumerated antecedent envelope $(A_1, A_2, A_3, A_4)$
with bounds propagated per-claim through the validity envelope
$\mathcal{E}$. The distinction is not mechanization (CST's proof
remains semi-formal pending the Isabelle pathway of
\S\ref{sec:discussion-isabelle}) but the conditioning structure:
AID issues bounded probabilistic attributions; CST issues
attributions whose bounds are conditioned on a named, falsifiable
set of structural and empirical antecedents."""


# --- P15b: §VII-C mechanization specificity ---
P15b_OLD = r"""The primary
technical challenge is formalizing EXTp's deterministic replay
semantics in Isabelle's term language at an abstraction level that
interfaces with seL4's existing machine model --- specifically,
defining the equivalence relation $\approx_S$ over VM-exit
trajectories such that A4's empirical $\scoreS{=}1.0000$ lifts to
a structural determinism predicate. The empirical components (A3
confounder bound, A4 cross-boot determinism) remain empirical in
the mechanized proof: Isabelle establishes the conditional
soundness theorem; calibration data supplies the antecedents."""

P15b_NEW = r"""The primary
technical challenge has two specific layers, neither
reducible to a missing tactic.

First, an \emph{abstraction-layer gap}. seL4's existing Isabelle
machine model~\cite{klein2014sel4} is defined over abstract event
traces at the kernel-API level; EXTp's VM-exit trace surface is
defined over VT-x microarchitectural state (VMCS fields, EPT
mappings, register file contents). Bridging the two requires a
lifting from the seL4 abstract machine state to EXTp's
concrete VM-exit observable surface --- a mapping that does not
currently exist in the L4.verified harness and would constitute a
standalone contribution. The equivalence relation $\approx_S$ over
VM-exit trajectories must be defined at the granularity of this
lifting, not at the granularity of seL4's existing trace
abstractions.

Second, an \emph{empirical-to-structural lifting} question. A4's
empirical content is a probability bound ($\scoreS{=}1.0000$
observed; Clopper-Pearson per-run failure rate $\leq 10.4\%$ at
$N{=}34$); lifting this into a structural determinism predicate
in Isabelle/HOL requires a choice of modal context for representing
empirical probability mass. Standard HOL is set-theoretic and does
not carry a probability monad natively; whether to use a
probabilistic HOL extension (e.g., HOL-Probability), an axiomatic
empirical-envelope layer, or a hybrid construction is an open
research design choice. CST's empirical antecedents (A3
confounder bound, A4 cross-boot determinism) remain empirical in
any mechanized proof: Isabelle establishes the conditional
soundness theorem; calibration data supplies the antecedents.
The open question is the \emph{interface format} between empirical
calibration and Isabelle's term language, not whether Isabelle can
express conditional soundness."""


# --- P16: §II-C AC3 / causal-link defense ---
P16_OLD = r"""EXTp's CST establishes AC1 and AC2 for every
admissible atomic claim. AC3 (minimality) is outside CST v1.0 scope:
CST produces \emph{causal-link} claims, not \emph{causal-explanation}
claims in the Halpern-Pearl sense."""

P16_NEW = r"""EXTp's CST establishes AC1 and AC2 for every
admissible atomic claim. AC3 (minimality) is outside CST v1.0 scope:
CST produces \emph{causal-link} claims, not \emph{causal-explanation}
claims in the Halpern-Pearl sense. The distinction is consequential
but the omission is principled: CST's downstream applications
(mitigation verification and counterfactual fuzzing,
\S\ref{sec:discussion-fuzz}) require attribution at individual
intervention points --- ``did $\dox{x'}$ cause the divergence?'' ---
not identification of minimal sufficient cause sets. A
mitigation-verification workflow needs to know whether patching
parameter $X$ severs the causal pathway; whether $\{X\}$ is the
minimal such set is operationally irrelevant. AC3 minimality
becomes essential only when CST claims are used to construct
human-readable explanations, a separate use case that EXTp does
not target in v1.0."""


# --- P17b: §VI-D Workload-class scope reframing ---
P17b_OLD = r"""\textbf{Single workload class.} All $\sigbase$ and FPR calibration
is against $L_1$-pchase and $L_2$-pchase guest workloads.
LLC-resident and DRAM-resident workload classes are not yet
characterized; $\Dstar$ portability to these classes is not
established."""

P17b_NEW = r"""\textbf{Workload-class calibration scope.} All $\sigbase$ and FPR
calibration in this paper is established for the $L_1$-pchase and
$L_2$-pchase guest workload classes (plus the synthetic-guest
class used in \S\ref{sec:eval-demo}). LLC-resident and
DRAM-resident workload classes constitute a separate experimental
track --- $\Dstar$ calibration for these classes is mechanically
straightforward (re-running the MI calibration protocol of
\S\ref{sec:mi} with the new workload binary) but has not been
performed for this submission. CST claims issued in this paper
are scoped to the calibrated workload classes via the validity
envelope $\mathcal{E}$'s \texttt{wl-class} field
(\S\ref{sec:framework}); a claim issued under
\texttt{wl-class = L1-pchase} carries no implicit transportability
guarantee to \texttt{wl-class = LLC-resident}. Adding LLC- and
DRAM-resident calibrations to extend the validated envelope is
future work; the soundness machinery is invariant under such
extensions, only the calibration constants change."""


# --- P18: Chronomaly consistency flag ---
P18_OLD = r"""\textbf{Multi-VCPU exploits.} Chronomaly-class race-condition
exploits (CVE-2025-38352, POSIX CPU timer
UAF~\cite{linuxkernel2025chronomaly}) and KVM SVM INT3 reinjection
bugs (CVE-2025-68259~\cite{linuxkernel2025int3reinject}) depend on"""

P18_NEW = r"""\textbf{Multi-VCPU exploits.} Chronomaly-class race-condition
exploits (CVE-2025-38352, POSIX CPU timer
UAF~\cite{linuxkernel2025chronomaly}; declared scope boundary,
\S\ref{sec:threat}) and KVM SVM INT3 reinjection bugs
(CVE-2025-68259~\cite{linuxkernel2025int3reinject}) depend on"""


# =====================================================================
# Patch application engine (identical to wave 1)
# =====================================================================

PATCHES = [
    ("P14   Abstract '1.0000' hedging",          P14_OLD, P14_NEW),
    ("P15a  §VIII-A AID distinction sharpening", P15a_OLD, P15a_NEW),
    ("P15b  §VII-C mechanization specificity",   P15b_OLD, P15b_NEW),
    ("P16   §II-C AC3 / causal-link defense",    P16_OLD, P16_NEW),
    ("P17b  §VI-D workload scope reframing",     P17b_OLD, P17b_NEW),
    ("P18   §VII-A Chronomaly consistency flag", P18_OLD, P18_NEW),
]


def apply_patches(text, dry_run=False):
    report = []
    for name, old, new in PATCHES:
        count = text.count(old)
        if count == 0:
            report.append((name, "FAIL", "OLD string not found"))
            continue
        if count > 1:
            report.append((name, "FAIL", f"OLD string appears {count} times (must be unique)"))
            continue
        if not dry_run:
            text = text.replace(old, new, 1)
        report.append((name, "OK", "applied (1 match)"))
    return text, report


def main():
    parser = argparse.ArgumentParser(description="Apply wave-2 EXTp NDSS revision patches.")
    parser.add_argument("--input", default="extp_revised.tex",
                        help="input .tex file (default: extp_revised.tex from wave 1)")
    parser.add_argument("--output", default="extp_revised_v2.tex",
                        help="output .tex file (default: extp_revised_v2.tex)")
    parser.add_argument("--dry-run", action="store_true", help="check applicability without writing")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        print(f"ERROR: input file not found: {in_path}", file=sys.stderr)
        print("HINT: wave 2 expects wave-1 output (extp_revised.tex) as input.", file=sys.stderr)
        return 1

    text = in_path.read_text(encoding="utf-8")
    new_text, report = apply_patches(text, dry_run=args.dry_run)

    print(f"=== Wave-2 patch report ({'DRY RUN' if args.dry_run else 'APPLIED'}) ===\n")
    for name, status, msg in report:
        marker = "✓" if status == "OK" else "✗"
        print(f"  {marker} {name:45s} [{status}] {msg}")
    print()

    failures = [r for r in report if r[1] != "OK"]
    if failures:
        print(f"FAILED: {len(failures)} patch(es) did not apply.", file=sys.stderr)
        print("HINT: ensure input is wave-1 output (extp_revised.tex), not original extp.tex.", file=sys.stderr)
        return 1

    if args.dry_run:
        print("DRY RUN complete; no file written.")
        return 0

    out_path.write_text(new_text, encoding="utf-8")
    print(f"WROTE: {out_path} ({len(text)} → {len(new_text)} bytes, +{len(new_text)-len(text)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
