# EXTp — NDSS 2027 Fall · TEMİZ SUBMISSION PAKETİ

*Bu klasör = EXTp paper'ının **temiz, kendine-yeten** submission kaynak-paketi.
`extp-fixes-v2` boru-hattından (patch / original / wave ara-dosyaları) **izole** —
burada yalnız submission için gereken dosyalar var, fazlası yok.*

Oluşturuldu: 2026-08-05 · İçerik = `extp_revised_v2.tex`'in son (edit'li) hâli + assets.

---

## Manifest (paketteki her şey)

| Dosya | Ne | Boyut |
|---|---|---|
| `extp.tex` | Ana paper kaynağı (final; IEEEtran, B1-düzeltmeli) | ~126 KB |
| `refs.bib` | BibTeX bibliyografyası (36 atıf) | ~9 KB |
| `fig/paper_section6_silent_histogram.pdf` | Figure 2 | 29 KB |
| `fig/paper_section6_signature_comparison.pdf` | Figure 3 | 32 KB |
| `fig/paper_section6_fuzz_causal_map.pdf` | Figure (fuzz causal map) | 32 KB |
| `extp_v2_PREVIEW_pre-B1.pdf` | Görsel önizleme (aş. nota bak) | 518 KB |

Not: Figure 1 (architecture) TikZ ile tex-içinde çiziliyor → harici dosya gerektirmez.

---

## Kendine-yeterlik denetimi (2026-08-05, doğrulandı)

`extp.tex` üzerinde otomatik kontrol — hepsi ✅:

- **Aktif sınıf:** `\documentclass[conference]{IEEEtran}` ✓ (NDSS 2027 = IEEEtran; ayrı `ndss.cls` YOK).
- **`\includegraphics` (3):** hepsi `fig/paper_section6_*.pdf` → **üçü de pakette mevcut** ✓.
- **`\bibliography{refs}`** → `refs.bib` pakette ✓.
- **Harici `\input`/`\include`:** YOK — tek-dosya ✓.
- **`forthcoming` kalıntısı:** 0 (B1 uygulandı) ✓.
- **`\author`:** `Anonymous Authors` — double-blind ✓.

→ **tex'in referans verdiği HER ŞEY pakette.** Dışarıdan yalnız `IEEEtran.cls` gerekir — o standart
(Overleaf'te ve her TeX Live'da hazır), bundle'a koymaya gerek yok.

---

## Submission-hazırlık durumu

**Bitti (doğrulandı):** A1 (class doğru + ana-gövde ≤13 sayfa) · A4 (anonimlik temiz) · A5 (AI-disclosure uygun) ·
B1 (forthcoming→future) · C1 (karar: N=34 ile submit). Detay: `../SUBMISSION_CHECKLIST.md`.

**Kalan (Overleaf turu + senlik):**
1. **Final compile** → PDF üret (aş.).
2. **B3** — final proofread.
3. ⚠️ **VERIFY** — fall HotCRP açılış-tarihi + submission URL.

---

## Nasıl derlenir (final PDF)

1. Overleaf → **New Project → Upload Project** → bu klasörü (`extp.tex` + `refs.bib` + `fig/`) zip'leyip yükle.
2. Overleaf `extp.tex`'i ana dosya olarak algılar; derleyici **pdfLaTeX**.
3. **Recompile** (bibtex çözülmesi için 2. kez recompile: `pdflatex → bibtex → pdflatex → pdflatex`).
4. Format otomatik: US-letter, iki-sütun, Times 10pt (IEEEtran conference default = NDSS gereksinimi).

**Beklenti:** 0 error, 0 undefined-ref, ~19 sayfa toplam (ana-gövde ≤13, geri kalan Ethics + refs + appendix).

---

## `extp_v2_PREVIEW_pre-B1.pdf` hakkında (önemli not)

Bu önizleme PDF'i, **B1 kelime-düzeltmelerinden ÖNCE** derlenmişti ("forthcoming" → "future/planned",
3 yer). Görsel olarak temsili ve sayfa-yerleşimi aynı (3-kelimelik fark, layout'u değiştirmez) — ama
**SUBMISSION PDF'i değil.** Final PDF'i yukarıdaki adımla `extp.tex`'ten üret.

---

**Deadline:** NDSS 2027 Fall — **19 Ağustos 2026, 23:59 AoE (UTC-12).** Erken submit (~17-18 Ağu).
