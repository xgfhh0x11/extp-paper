# EXTp Paper — Overleaf Setup

NDSS 2027 Fall Cycle submission. Anonymous for double-blind review.

## Quick Start (Overleaf)

1. Open https://www.overleaf.com — sign in.
2. **New Project → Upload Project** → drop this entire `.zip` file.
3. Overleaf will auto-detect `extp.tex` as the main document.
4. Click **Recompile** (top of right pane). It should compile cleanly
   with **pdfLaTeX** (the default) and produce an 11-page PDF.
5. If the bibliography appears as `[?]` after first compile, click
   the menu icon (top-left of right pane), set **Compiler: pdfLaTeX**
   if not already, then recompile twice more so bibtex resolves.

## Files in this project

| File | Purpose |
|---|---|
| `extp.tex` | Main paper source. |
| `refs.bib` | BibTeX bibliography (20 verified citations). |
| `fig/paper_section6_silent_histogram.pdf` | Figure 2: silent-hook timing distribution. |
| `fig/paper_section6_signature_comparison.pdf` | Figure 3: naïve vs silent hook scatter. |

## Class file: currently IEEEtran, swap to ndss.cls before submission

The active class line in `extp.tex` (around line 23):
```latex
\documentclass[conference]{IEEEtran}
% \documentclass[conference]{ndss}
```

**IEEEtran** is used for early drafting because it ships with TeX Live
and works out of the box on Overleaf. Page geometry is close to NDSS
but not identical.

**For final submission**, swap to the official NDSS class:

1. Download the NDSS 2026 template from
   https://www.ndss-symposium.org/ndss2026/submissions/templates/
2. Upload `ndss.cls` (and any required auxiliary files from the
   template zip) to this Overleaf project.
3. In `extp.tex`, swap the comment markers on the two
   `\documentclass` lines so `ndss` is active and `IEEEtran` is
   commented out.
4. Recompile.

## Sections status (as of this build)

| Section | Status |
|---|---|
| §1 Introduction | complete |
| §2 Background | complete |
| §3 Threat Model | complete |
| §4 Framework (Fig. 1 placeholder; TikZ port pending) | complete |
| §5 Formal Properties (CapSep / SOE / MI / CST) | complete |
| §6.1 Setup | complete |
| §6.2 Demonstration | complete (real Day 8 data) |
| §6.3 Measurement Characterization | complete |
| §6.4 Limitations | complete |
| §7 Discussion | placeholder |
| §8 Related Work | complete |
| §9 Conclusion | partial |
| Abstract | placeholder (write last) |
| Appendices A–D | placeholder |

## Compile expectations

- **Pages**: 11 (will grow to ~13 once §7, §9, Abstract, Appendices fill in)
- **Errors**: 0
- **Overfull hbox**: 0
- **Undefined references**: 0
- **Build sequence**: `pdflatex` → `bibtex` → `pdflatex` → `pdflatex`
  (Overleaf does this automatically on "Recompile")
