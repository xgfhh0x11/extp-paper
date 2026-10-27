# EXTp — A Soundness Theorem for Counterfactual Exploit Replay on Formally Verified Microkernels

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23403670.svg)](https://doi.org/10.5281/zenodo.23403670)

Utku Erol, Independent Researcher — utkuerol71@gmail.com

This repository holds the paper source and preprint for **EXTp**, together with the
supporting formal development, measurement protocols, and figures. The work states
and (partially) mechanizes a *Counterfactual Soundness Theorem* (CST) for exploit
replay on top of a formally verified microkernel (seL4).

## Published preprint

- **Preprint PDF:** [`SUBMISSION_READY_NDSS2028/extp.pdf`](SUBMISSION_READY_NDSS2028/extp.pdf)
- **Zenodo DOI (all versions):** [10.5281/zenodo.22849590](https://doi.org/10.5281/zenodo.22849590) (CC BY 4.0); resolves to the latest version. Current: version 3, 2026-10-22, [10.5281/zenodo.23575086](https://doi.org/10.5281/zenodo.23575086).
- **Self-contained artifact:** https://github.com/xgfhh0x11/extp-artifact
  (Isabelle/HOL mechanization, measurement summaries, seL4/EXTp VMM boot images, figures)

## Versions

| Version | Date | DOI | What changed |
|---|---|---|---|
| 3 | 2026-10-22 | [10.5281/zenodo.23575086](https://doi.org/10.5281/zenodo.23575086) | seL4's verified `X64` configuration excludes VT-x hypervisor mode and x86-64 has no integrity/confidentiality proofs, so the L4.verified results are now stated as an assumption about a neighbouring configuration (Sections II, III, V, VII and the Erratum appendix). Artifact bundle unchanged. |
| 2 | 2026-10-15 | [10.5281/zenodo.23403670](https://doi.org/10.5281/zenodo.23403670) | False-positive rates re-measured with the lemma's own pair-difference clause; family-wise threshold (see the artifact's `CHANGELOG.md`). |
| 1 | 2026-09-19 | [10.5281/zenodo.22849591](https://doi.org/10.5281/zenodo.22849591) | First preprint. |

`SUBMISSION_READY_NDSS2028/` holds the version-3 source and PDF.

## Contents

| Path | What it is |
|---|---|
| `SUBMISSION_READY_NDSS2028/extp.tex` | Paper source (LaTeX). |
| `SUBMISSION_READY_NDSS2028/extp.pdf` | Compiled preprint. |
| `SUBMISSION_READY_NDSS2028/refs.bib`, `fig/` | Bibliography and figures. |
| `isabelle/CST_Model.thy` | Isabelle/HOL development: 115 facts, `sorry`-free, session `EXTp_CST` (Isabelle2025-1 + HOL-Library). |
| `isabelle/ROOT`, `isabelle/build_log.txt` | Session definition and last build output. |
| `paper_section6_artifacts/` | Evaluation-section figures and the demonstration table. |
| `extp-vmm-cross-boot/`, `extp-vmm-demo/` | seL4/EXTp VMM boot images and protocols for the bare-metal runs. |
| `Counterfactual_Soundness_Theorem_v1.md`, `Measurement_Interference_v1.md`, `extp_formal_properties.md` | Design notes behind the formal model. |

## Reproducing the Isabelle check

```
isabelle build -d isabelle -v EXTp_CST
```

Expected: `Finished EXTp_CST`.

## License

The paper is distributed under **CC BY 4.0** (see the Zenodo record above).
