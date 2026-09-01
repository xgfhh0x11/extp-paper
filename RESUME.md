# RESUME — EXTp CST Isabelle Mekanizasyonu (checkpoint)

**Son güncelleme:** 2026-09-01 · **Durum:** çalışır, temiz; §8 eklendi (115 fact).
Bu dosya, PC restart sonrası **tam olarak kaldığımız yerden** devam etmek için.

---

## 30 saniyelik özet

EXTp paper'ının Counterfactual Soundness Theorem'inin (CST) **koşullu çekirdeğini**
Isabelle/HOL'de mekanize ettik. **115 fact ispatlı, `sorry` YOK**, Isabelle2025-1'de
temiz derleniyor. Paper (`extp.tex`) NDSS 2027 **≤13pp gövde şartını karşılıyor**
(Overleaf'te doğrulandı: gövde s.13'te bitiyor, Ethics s.14).

- Mekanizasyon: `isabelle/CST_Model.thy` (~1756 satır) + `isabelle/ROOT`
- Detaylı log: `Isabelle_Mechanization_CST.md` (vault notu)
- Paper: `SUBMISSION_READY_NDSS2027/extp.tex` (yedek: `extp.tex.bak-pre-C`)
- Overleaf paketi: `EXTp_Overleaf_upload.zip`

---

## Build komutu (ÖNEMLİ — Windows tuzağı)

Git Bash'ten Isabelle çalışmaz (`uname`→MINGW, "Failed to determine hardware…").
**Kendi bundled Cygwin login shell'i şart:**

```powershell
& "C:\Users\tylersec\Desktop\Isabelle2025-1\contrib\cygwin\bin\bash.exe" -l -c `
  "cd /cygdrive/c/Users/tylersec/Desktop/extp-paper/isabelle && `
   /cygdrive/c/Users/tylersec/Desktop/Isabelle2025-1/bin/isabelle build -D ."
```
Temiz rebuild için `-c` ekle. Beklenen: `Finished EXTp_CST` (~10-15s).
ROOT'a `sessions HOL-Library` eklendi (Word için) — Isabelle2025-1'de mevcut.

**pdflatex YEREL'DE YOK** → LaTeX derlemesi Overleaf'te yapılır. Statik ön-uçuş
scripti: `scratchpad/check.py` (ref/cite/graphics/env dengesi), `scratchpad/wc.py`
(gövde kelime sayısı, ~1000 kelime/sayfa).

---

## Tamamlanan adımlar (hepsi makine-kontrollü)

| Adım | Ne yapıldı | Anahtar fact |
|---|---|---|
| **Faz 0-2** | Model + koşullu CST teoremi (⟹ yönü), A1-A4 hipotez | `cst_conditional` |
| **(a)** | do-operatör severance (True placeholder → gerçek state-update) | `apply_iv_severs`, `effective_holds` |
| **(b)** | AC2(a) iki tanığa ayrıldı + bağımsızlık + tanık-başına zarf | `structural_bound_tighter_iff` (kriter: ε_SOE≤α) |
| **(c)** | Paper'a "machine-checked conditional core" işlendi (6 nokta) | — |
| **(d)** | `lem:silent` + A2 aktif (soundness vs scope-completeness ekseni) | `cst_scope_complete` |
| **(f)** | Paralel sweep tanık-duyarlı ensemble zarfı (karışık kesin daha sıkı) | `sweep_three_level_bound` |
| **(h)** | Gerçek 33-claim sweep verisine bağlama (zarf=1 claim=1.35%) | `dead_sweep_envelope_vs_naive_swept` |
| **(i)** | Silent-leak = kanıtlanmış scope sınırı (in-scope sessiz sızıntı imkânsız) | `silent_leak_only_out_of_scope` |
| **(g)** | seL4 lifting **arayüzü** — yükümlülük İZOLE, AÇIK KAPATILMADI | `A1_unconditional_for_verified` |
| **(e)** | Observable → 64/32-bit word (timing nat kaldı) | — |
| **§8 F2** (2026-09-01) | Composition **W/K_fwk formunda** (paper item ii birebir): `hold`, `pert_bounded`, locale `cst_composition`; katı form δ→0'da geri | `composition_W_holds`, `composition_strict_recovered`, `cst_conditional_W` |
| **§8 F5** (2026-09-01) | Prop 1 **trace-zincirli**: `Ts!(k+1)` = k. adımın T_cf'i = k+1. adımın baseline'ı | `chain_ok_iff_steps`, `chain_extend`, `chain_conditional`, `chain_envelope_bound` |

**2026-09-01 turu ayrıca:** statement-fidelity denetimi (paper ↔ .thy) yapıldı; `tab:mechanized`'da
üç bounding lemma → "assumed (A-content)", lem:silent tek yön, composition + Prop 1 satırları yeni
fact'lere bağlandı; App. A "fourth"→"third admissibility step" ×2 düzeltildi; **`tab:mechanized`
satır sonları tek `\` idi (LaTeX bozuk!) → `\\` yapıldı.** Overleaf'te yeniden derle ve tabloyu gözle kontrol et.

---

## ⚠️ Dürüstlük sınırları (KAPATILMADI — iddia etme)

1. **(g) lifting açığı AÇIK.** `verified_no_fwk_touch` assumption'ı ispatlanmadı —
   onu L4.verified'in gerçek atomicity teoreminden türetmek **çok-yıllık**, kapsamda
   değil. Yapılan: yükümlülüğü tek isimli assumption'a indirgemek + altından çıkanları
   (K_verified δ=0) ispatlamak. Bu **arayüz**, kapatma değil.
2. **Ampirik antecedent'ler** (score_S=1.0000, Clopper-Pearson, α_realized) Isabelle'de
   ASLA ispatlanmaz — ölçüm. Soyut reel parametre olarak dışarıdan girer; yalnızca
   union-bound aritmetiği ispatlanır.
3. **timing wraparound** (TSC 64-bit) kapsam dışı — timing `nat` olarak modellendi.

---

## Sıradaki adımlar (öncelik sırası)

Mekanizasyonda **anlamlı iş büyük ölçüde bitti.** Kalan seçenekler:
- **g-tam:** `verified_no_fwk_touch`'ı gerçek seL4 ispatından türet → ❌ çok-yıllık, kapsamda değil.
- **Konsolidasyon:** olduğumuz yerde durup paper'ı cilalamak (önerilen).
- ✅ §Related formal-methods karşılaştırması (substrate vs analysis-method, b9794b8)
- ✅ Appendix `tab:mechanized` — 19 bileşen → Isabelle fact → assumed/proved/model (5280b30)
- ✅ `fig:demo-sweep` caption → `dead_sweep_envelope_vs_naive_swept` (cced441)
- **Overleaf 2026-08-30: gövde s.13'te bitiyor, taşma yok. Pay ~sıfır — gövdeye kelime
  EKLEME; yeni içerik yalnızca appendix'e.**
- Kalan: `SUBMISSION_CHECKLIST.md` üzerinden son gözden geçirme.

---

## Kritik dosya konumları

```
extp-paper/
├── RESUME.md                          ← BU DOSYA
├── Isabelle_Mechanization_CST.md      ← tam log (115 fact envanteri, tüm kod)
├── isabelle/
│   ├── CST_Model.thy                  ← ~1756 satır, tüm mekanizasyon
│   ├── ROOT                           ← session EXTp_CST (+ sessions HOL-Library)
│   └── build_log.txt                  ← son build çıktısı
├── SUBMISSION_READY_NDSS2027/
│   ├── extp.tex                       ← paper (≤13pp gövde OK)
│   ├── extp.tex.bak-pre-C             ← C-turu öncesi yedek
│   ├── refs.bib, fig/*.pdf
├── EXTp_Overleaf_upload.zip           ← Overleaf'e hazır (extp.tex+refs.bib+fig)
└── memory/ (…/.claude/…/memory/)      ← extp-isabelle-phase-plan.md, -build-cygwin.md
```

## Sayfa limiti notu (NDSS 2027)
- Gövde (Intro→Conclusion) **≤13pp** — Ethics + refs + appendix HARİÇ. ✅ Karşılanıyor.
- Mekanizasyon içeriği tamamen **App A**'da (limit dışı) → gövdeye dokunmadan büyütülebilir.
- Deadline 19 Ağu 2026 geçti → **diğer cycle** için hazırlanıyor (13-limit geçerli).
- Redundans kesildi (Pearl/HP tekrar paragrafı, A1-modulo) + float `[t]→[tb]`.

---

**Devam etmek için:** yukarıdaki build komutunu çalıştır, `Finished EXTp_CST` görürsen
her şey yerinde. Sonra `Isabelle_Mechanization_CST.md`'yi aç — tam durum orada.
