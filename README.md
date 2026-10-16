# EXTp — A Soundness Theorem for Counterfactual Exploit Replay on Formally Verified Microkernels

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23403670.svg)](https://doi.org/10.5281/zenodo.23403670)

Utku Erol, Independent Researcher — utkuerol71@gmail.com

This repository holds the paper source and preprint for **EXTp**, together with the
supporting formal development, measurement protocols, and figures. The work states
and (partially) mechanizes a *Counterfactual Soundness Theorem* (CST) for exploit
replay on top of a formally verified microkernel (seL4).

## Published preprint

- **Preprint PDF:** [`SUBMISSION_READY_NDSS2028/extp.pdf`](SUBMISSION_READY_NDSS2028/extp.pdf)
- **Zenodo DOI:** [10.5281/zenodo.22849591](https://doi.org/10.5281/zenodo.22849591) (CC BY 4.0)
- **Self-contained artifact:** https://github.com/heavyisthecrown0x11/extp-artifact
  (Isabelle/HOL mechanization, measurement summaries, seL4/EXTp VMM boot images, figures)

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
