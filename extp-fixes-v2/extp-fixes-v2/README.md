# EXTp NDSS Revision Pack — Wave 2

Wave 2: empirical-data-bağımsız 6 ek patch. Wave 1'in üstüne çalışır.

---

## Önkoşul

Önce **wave 1** uygulanmış olmalı. Wave 2'nin input'u wave 1'in
output'u (`extp_revised.tex`).

Hatırlatma sıralaması:
```
extp.tex  →  [wave 1: apply_fixes.py]  →  extp_revised.tex
                                              ↓
                                      [wave 2: apply_fixes_v2.py]
                                              ↓
                                       extp_revised_v2.tex
```

---

## Hızlı Başlangıç

```bash
# Wave 2'yi wave 1 output'una uygula
python3 apply_fixes_v2.py --input extp_revised.tex --output extp_revised_v2.tex

# veya dry-run önce
python3 apply_fixes_v2.py --dry-run
```

Sonuç: `extp_revised_v2.tex`, 125513 bytes (wave 1'den +3334 bytes ≈ 1 sayfa eklenti).

**Veya** doğrudan `output/extp_revised_v2.tex`'i Overleaf'e yükleyebilirsin — zaten compile-tested final dosya.

---

## Wave 2 Patch Envanteri

| # | ID | Section | İş |
|---|----|---------|-----|
| 1 | P14  | abstract | "1.0000" → "1.0000 observed; CP bound ≤10.4%" (overclaim'i kapatır) |
| 2 | P15a | §VIII-A | AID ayrımı: "mechanized" değil, "verified substrate + enumerated antecedents" |
| 3 | P15b | §VII-C  | Mechanization difficulty: iki-katmanlı somut açıklama (abstraction gap + probability lift) |
| 4 | P16  | §II-C   | AC3 / causal-link legitimacy defense (mitigation + fuzzing use cases) |
| 5 | P17b | §VI-D   | Workload-class scope reframing (limitation → calibration scope) |
| 6 | P18  | §VII-A  | Chronomaly cross-reference consistency flag (3 yerde tutarlı) |

---

## Klasör Yapısı

```
extp-fixes-v2/
├── README.md                            ← Bu dosya
├── apply_fixes_v2.py                    ← Wave 2 patch uygulayıcısı
├── originals/
│   └── extp_revised_wave1.tex           ← Wave 1 output (input için referans)
├── patches/                             ← 6 wave-2 patch dosyası
│   ├── P14_abstract_hedging.patch
│   ├── P15a_aid_distinction.patch
│   ├── P15b_mechanization_specificity.patch
│   ├── P16_ac3_causal_link_defense.patch
│   ├── P17b_workload_scope_reframing.patch
│   └── P18_chronomaly_consistency.patch
└── output/
    ├── extp_revised_v2.tex              ← Wave 1 + Wave 2 entegre final .tex
    └── extp_revised_v2.pdf              ← Compile edilmiş, 19 sayfa
```

---

## Compile Doğrulaması

Wave 2 + wave 1 birleşik test edildi:

- **19 sayfa** final PDF (orijinal 11 → wave 1 18 → wave 2 19)
- **0 undefined reference**
- **0 LaTeX error**
- **1 minor overfull hbox** (0.84pt, wave 1'den miras, kozmetik)
- Lemma renumbering wave 1'den korundu: Lemma 1/2/3/4

---

## Senin İçin Açık Kalan (Wave 3 — empirical data lazım)

Üç madde N=200 ve LLC-pchase empirical data'sı geldiğinde güncellenecek:

1. **§V-B SOE bound güncelleme**: N=34 → N=200 yapıldığında CP bound
   ≤10.4% → ≤1.5% civarına düşer. P14'teki "10.4%" rakamı, ve §V-B'deki
   tüm cross-boot referansları update edilir.

2. **§VI-D "N=34 cross-boot sample" limitations entry**: tamamen
   kaldırılır veya N=200'le yeniden çerçevelenir.

3. **§V-C + §VI-C + Table V**: LLC-pchase satırı eklenir, §V-C'ye
   calibration paragrafı, ve P17b'deki "future work" cümlesi
   "validated across {L1, L2, LLC}" haline gelir.

Bu üç işlem için empirical data geldiğinde **Wave 3** paketini
hazırlarım. Wave 3 wave 2 output'una çalışacak şekilde olacak.

---

## Reviewer Risk Matrisi (wave 2 sonrası)

### Reviewer 1 (FM / seL4 ekosistemi)
✅ Wave 1: M2 (contradiction → bounding), M3 (AC2(b) derivation), M4+M6 (Pearl deviation modes)
✅ Wave 2: P15a (verified substrate + enumerated antecedents), P15b (mechanization specificity)
🟢 **Risk: Düşük.** Threat-elimination structure + AC2(b) construction + Isabelle pathway specificity bu reviewer'ı tatmin eder.

### Reviewer 2 (Hypervisor security)
✅ Wave 1: M10 (synthetic guest justification)
✅ Wave 2: P18 (Chronomaly consistency), P17b (workload scope honest)
🟠 **Risk: Orta.** Real CVE end-to-end demo eksikliği hâlâ açık (Tier 4, wave 3+). Synthetic justification active framing yardım ediyor ama soundness-only paper olduğu için kabul gerekiyor.

### Reviewer 3 (Pearl / causal inference)
✅ Wave 1: M3, M4, M6, M8, M9
✅ Wave 2: P14 (overclaim hedging), P16 (AC3 defense), P15a (conditioning structure novelty)
🟢 **Risk: Düşük.** Bu reviewer için asıl tehlike "monolithic Pearl deviation" eleştirisiydi; Table III restructure + P15a + P16 üçlü bunu kapatır.

---

## Sonraki Adımlar

1. **Wave 2'yi uygula**: `python3 apply_fixes_v2.py`
2. **Overleaf'te compile et**, recompile temiz olduğunu doğrula
3. **Diff'i gözden geçir**:
   ```bash
   diff originals/extp_revised_wave1.tex output/extp_revised_v2.tex | less
   ```
4. **Wave 3 için bekle**: N=200 + LLC empirical data geldiğinde
   son güncelleme yapılır
5. **Submit**: arXiv (Eylül-Ekim 2026) → NDSS Fall Cycle
   (deadline 19 Ağustos 2026)

---

## Wave 1 + Wave 2 Birleşik Özet

Toplam 21 patch uygulanmış halde:
- Wave 1: 15 patch (struct fix'ler — Lemma rewrite, AC2(b) derivation, Pearl deviation modes, framing fix'leri)
- Wave 2: 6 patch (overclaim hedging, theorem-vs-sketch defense, AC3 defense, scope reframing)

Toplam paper uzaması: 11 sayfa → 19 sayfa (+8, çoğu Appendix D AC2(b)
derivation ve §VII-C mechanization detayı).

NDSS 13 sayfa main body + unlimited appendix kuralı altında bu rahat
sığar (main body wave 1+2 ile yaklaşık 12.5 sayfa, kalan appendix'te).
