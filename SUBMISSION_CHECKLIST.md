# EXTp → NDSS 2027 Fall — Submission Checklist & Plan

*Üretildi: 2026-08-03 · Kaynak: `extp_revised_v2.tex` denetimi + NDSS 2027 CFP (ndss-symposium.org/ndss2027).*

## Deadline
- **19 Ağustos 2026, 23:59 AoE (UTC-12)** — tek deadline, ayrı abstract-registration **YOK** (CFP'den teyitli).
- Bugün 3 Ağustos → **16 gün.**
- AoE cömert (dünyanın son saat dilimi) ama **erken submit et (17–18 Ağu)**, son güne bırakma (HotCRP yükü + sürprizler).
- ⚠️ **VERIFY:** fall HotCRP submission-site ne zaman açılıyor + URL. (Bir kaynak "fall CFP 15 Ağu açılır" dedi — doğruysa submission penceresi 15–19 Ağu, yani tüm prep **14 Ağu'ya kadar** bitmeli. Summer sitesi `ndss27-summer.hotcrp.com`; fall ayrı olacak.)

## Genel hüküm
Paper **taslak olarak TAM.** Eksik bölüm / içerik-boşluğu **yok**: Intro→Conclusion + Ethics + 4 Appendix (Full Proofs dahil) + AI-disclosure — hepsi dolu, anonim, 36 atıf, 3 figür, v2 = 19 sayfa (Wave 1+2, 0 error). Kalan iş = **format + cila + 1 karar**, yeni-yazım DEĞİL. Eski overleaf README'nin "placeholder" tablosu Wave 1/2 sonrası **eskimiş.**

---

## A. BLOKERLAR (submit'ten önce ŞART — risk sırasına göre)

- [x] **A1 — SINIF ZATEN DOĞRU (ndss.cls swap GEREKMİYOR) + SAYFA-LİMİTİNİ TEYİT ET.**
      ✅ **BULGU (2026-08-03):** NDSS 2027 resmi template'i (`bare_conf_NDSS2027.tex`) `\documentclass[conference]{IEEEtran}`
      kullanıyor — NDSS'in ayrı `ndss.cls`'i **YOK**, NDSS = IEEEtran. Paper zaten IEEEtran'daydı → **doğru sınıfta.** (Overleaf-README'nin
      "ndss.cls'e geç" tavsiyesi yanlış varsayımdı; benim swap'im geri alındı, IEEEtran aktif.) → **class-swap + ndss.cls indirme İPTAL.**
      ➡️ Kalan tek iş: mevcut `extp_revised_v2.pdf` **zaten gerçek NDSS geometrisi** → **ana-gövde (Intro→Conclusion) ≤ 13 sayfa mı**
      TEYİT ET (Ethics + refs + appendix HARİÇ). Senin kendi README-tahminin ~12.5 sayfa → sığar ama sınırda. **PDF'i aç, Conclusion'ın
      bittiği + "References"ın başladığı sayfayı söyle** (yerelde pdftoppm/pdftotext yok, render edemiyorum). >13 çıkarsa: §Discussion
      (Isabelle-pathway / downstream-fuzz alt-bölümleri) veya §Related'dan ~0.5–1pp kıs. Not: preamble IEEEtran geometri/font'unu ezmesin.
- [ ] **A2 — Figür + bib taşınıyor mu.** 3 pdf (`fig/paper_section6_silent_histogram.pdf`, `_signature_comparison.pdf`,
      `_fuzz_causal_map.pdf`) + `refs.bib` submission projesinde olmalı; bibtex çözülüyor → **0 undefined-ref.**
- [ ] **A3 — 0 LaTeX error** ndss.cls altında; overfull hbox kabul-edilebilir (v2'de 1 minor 0.84pt vardı).
- [ ] **A4 — Anonimlik son-geçiş (double-blind).** `\author{Anonymous Authors}` ✓. Build-Provenance appendix seL4-commit'i
      "double-blind-redacted" ✓, donanım (Alder Lake / Z690 / FT232RL) jenerik ✓. Yine de tüm dosyada kurum/isim/
      kullanıcı-adı/path/URL YOK diye son bir tarama yap.
- [ ] **A5 — AI-disclosure (ZORUNLU).** NDSS 2027: generative-AI kullanımı submission'da bildirilmeli. `app:ai-disclosure` ✓ VAR —
      içeriğinin politika-diline uyduğunu teyit et (minimal spelling/grammar ise bildirim gerekmez; daha fazlası ise gerekli).
- [ ] **A6 — Format.** US-letter, iki-sütun, Times 10pt+ / 11pt+ leading, PDF-only (IEEEtran[conference] default bunları verir; A1'de doğrula).

## B. CİLA (yapılmalı, düşük risk)

- [x] **B1 — "forthcoming CMD" → nötr çerçeve — UYGULANDI (2026-08-05).** 3 yer: satır 374 ("A future … would address this"),
      950 ("a future CMD property class"), 1468 ("A planned … would extend"). Kelime-nötr, sayfa-etkisiz. (A4 sonrası: sızıntı değildi,
      salt stil-mütevazılaştırma.)
- [ ] **B2 — Ethics** sayfa-limitinden hariç → **dursun** (bedava, present ✓; NDSS'te opsiyonel ama zararsız-artı).
- [ ] **B3 — CST proof-sketch (App D) proofread** + "semi-formal sketch" çerçevesi §5 (sec:cst) ile tutarlı mı (Conclusion "semi-formal
      sketch" diyor → §5 ile çelişmesin).
- [ ] **B4 — Abstract** iyi (~200 kelime, N=34/CP-bound hedge'li ✓); opsiyonel sıkılaştırma, şart değil.

## C. STRATEJİK KARAR (senin)

- [x] **C1 — KARAR (2026-08-04): N=34 ile SUBMIT; N=200 EN-SON / opsiyonel** (araştırmacı: "çok sıkıntı, en son iş"). Blocker değil; accept olursa camera-ready'de.
      N=34 → SOE CP-bound ≤10.4% (Limitations'ta **dürüstçe flag'li**, "expanding N is straightforward, cost = machine time").
      N=200 → bound ~%1.5. **Blocker DEĞİL** (soundness-paper, within-boot N=998 ≤0.37% zaten tight).
      **Öneri: N=34 ile submit et.** Donanım (Alder Lake box) boştaysa hazır N=100/N=200 artefaktını ~30 dk koştur ve rakamı güncelle;
      accept olursa camera-ready'de kesin N=200. Ay-beklemeye değmez.
- [ ] **C2 — (ara-yol)** hazır **N=100** artefaktı hızlı koşulabiliyorsa, submission'a orta-yol olarak onu koy.

---

## D. PLAN (16 gün · 3 → 19 Ağustos)

| Gün | İş |
|---|---|
| **1–2 (şimdi)** | **A1** (cls-swap + compile + sayfa-ölçümü) — BUGÜN, tek geç-bite-eden. A2, A3. |
| **3–5** | A1'in çıkardığını düzelt (>13pp ise §Discussion/§Related trim); **A4** anonimlik; **B1** forthcoming. |
| **6–9 (ops.)** | **C1** N=200 koşulacaksa burada; bound + Fig/Table güncelle. Değilse atla. |
| **10–13** | **B3/B4** cila; tam proofread; ref-check; final compile (ndss.cls). |
| **14–16 (tampon)** | Final PDF; HotCRP dry-run; **~17–18 Ağu submit** (19'a bırakma). |
| **paralel/erken** | ⚠️ fall HotCRP açılış-tarihi + URL teyit (yukarıdaki VERIFY). |

---

**Tek cümle:** paper bitmiş; iş = ndss.cls'e geçir + sayfa-limitini doğrula + hafif cila + N=200-kararını ver + erken submit.
Tek gerçek risk sayfa-limiti (A1) → onu bugün ölç, gerisi rahat.
