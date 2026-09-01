---
title: "CST Isabelle Mekanizasyonu — Koşullu Çekirdek"
tags:
  - extp
  - isabelle
  - formal-methods
  - cst
  - sel4
status: kosullu-cekirdek-bcdfghi-e-13pp-ok
isabelle-version: Isabelle2025-1
session: EXTp_CST
build-status: "0 error / 0 warning / 0 sorry"
proven-facts: 115
created: 2026-08-27
updated: 2026-09-01
---

# CST Isabelle Mekanizasyonu — Koşullu Çekirdek

> [!success] Durum
> `extp.tex`'in **"semi-formal sketch"** dediği CST'nin **koşullu çekirdeği**
> artık makine-kontrollü bir Isabelle/HOL teoremi.
> **115 fact ispatlı, `sorry` YOK**, Isabelle2025-1'de temiz derleniyor (§8 eklendi 2026-09-01).
> seL4 harness'ına ve lifting açığına **hiç dokunulmadı**.

> [!tip] Yeni analitik sonuç (2026-08-28, adım (b))
> Tanık ayrımı **kozmetik olmadı**: AC2(a)'nın iki tanığının *mantıksal bağımsızlığı*
> karşı-örneklerle ispatlandı, her tanığa **kendi hata zarfı** bağlandı, ve
> **hangisinin daha sıkı olduğunun tek bir eşitsizlikle** (`ε_SOE ≤ α`) karakterize
> edildiği gösterildi. Paper'ın iki kalibrasyon rejimi bu eşitsizliğin **zıt
> taraflarında** çıkıyor. Bu, `extp.tex`'in prose'unda türetilmemiş yeni içerik → §7.8.

İlgili notlar: [[Counterfactual_Soundness_Theorem_v1 (1)|CST v1.0 (tam doküman)]] ·
[[extp_formal_properties|Formal Properties P1–P8]] ·
[[Capability_Separation_Theorem|CapSep]] ·
[[Strong_Observational_Equivalence (2)|SOE]] ·
[[Measurement_Interference_v1 (1)|MI]] ·
[[SUBMISSION_CHECKLIST]]

---

## 1. Stratejik karar: neden lifting'le başlamadık

Başlangıç sorusu şuydu: *"seL4'ün soyut API trace'leri ile VT-x'in somut mikromimari
register durumları arasındaki lifting açığını kapatmak."*

İnceleme sonucu: **`extp.tex` §`sec:discussion-isabelle` iki ayrı açık sayıyor**, ve
sezgisel olarak "asıl mesele" görünen birincisi, formal deliverable'ın kritik yolunda **değil**.

| # | Açık | Nedir | Kapanır mı |
|---|---|---|---|
| 1 | **Abstraction-layer / lifting gap** | seL4 Isabelle makine modeli kernel-API seviyesinde soyut event trace'leri üzerinde; EXTp yüzeyi VT-x mikromimari durumu (VMCS, EPT, register file) üzerinde | Kısmen — yalnızca `K_verified` için; **çok-yıllık** |
| 2 | **Empirical-to-structural lifting** | A4/A3 ampirik olasılık sınırları (Clopper-Pearson, N=34); HOL'de olasılık monad'ı yok | **Hayır** — ölçümdür, ispatlanamaz |

> [!warning] Kritik bulgu
> `K_extended` (`ReadVMCS` / `WriteVMCS` / `MapEPT` / `Unmap`) zaten **L4.verified kapsamı
> dışında**. Lifting bitse bile A1 bu operasyonlar için **ampirik kalır** — A4 ile aynı duvar.
> Detaylı CST dokümanı §5.4 bunu dürüstçe söylüyor: *"intervention machinery seL4'ün verified
> kernel scope'unun ÜSTÜNDEKİ VMM katmanında çalışır… çok-yıllık bir efor."*
> Ana metnin ("infrastructure already in place") bundan daha iyimser olduğu bir **çerçeve
> gerilimi** var → bkz. §9.

### Faz planı

| Faz | İş | seL4 gerekir mi | Maliyet | Durum |
|---|---|---|---|---|
| **0** | Trace/event/observable datatype, `D`, 4-adım check, envelope `E` | Hayır | Günler | ✅ **Tamam** |
| **1** | A1–A4 locale assumption'ları; `⟸` yönü | Hayır | Günler | ✅ **Tamam** |
| **2** | `⟹` yönü = **koşullu teorem**; 3 bounding lemma + AC2(b) + Prop 1 | Hayır | Haftalar | ✅ **Tamam** |
| **3** | Lifting: `sel4_abstract_state → observable`; A1'i **yalnızca** `K_verified` için discharge | **Evet** | Çok-yıllık | ⏸️ Bilinçli stub (§7) |
| **4** | Ampirik antecedent'leri mekanize et | — | İmkânsız | ❌ Yapılamaz |

**Tek cümlelik gerekçe:** koşullu teorem A1–A4'ü *hipotez* aldığı için lifting'den
**yapısal olarak bağımsız**; Faz 3 yalnızca tek bir assumption'ı, operasyonların bir
alt-kümesi için düşürür.

---

## 2. Ortam ve build

- **Isabelle2025-1** — `C:\Users\tylersec\Desktop\Isabelle2025-1`
- Session: `EXTp_CST` (HOL tabanlı), `imports Complex_Main`
- Dosyalar: `isabelle/CST_Model.thy`, `isabelle/ROOT`

> [!bug] Windows tuzağı — Git Bash çalışmaz
> Git Bash / MSYS içinden çağrılınca launcher `uname`'i `MINGW64_NT-…` görür ve
> **`Failed to determine hardware and operating system type!`** verir.
> Isabelle **kendi bundled Cygwin'inin login shell'i** ile çağrılmalı (`uname` → `CYGWIN_NT-…`).

```powershell
& "C:\Users\tylersec\Desktop\Isabelle2025-1\contrib\cygwin\bin\bash.exe" -l -c `
  "cd /cygdrive/c/Users/tylersec/Desktop/extp-paper/isabelle && `
   /cygdrive/c/Users/tylersec/Desktop/Isabelle2025-1/bin/isabelle build -D ."
```

Temiz rebuild için `-c` (clean) ekle. Son çıktı:

```
Cleaned EXTp_CST
Running EXTp_CST ...
EXTp_CST: theory EXTp_CST.CST_Model
Finished EXTp_CST (0:00:02 elapsed time)
```

**`ROOT`:**

```isabelle
session "EXTp_CST" = "HOL" +
  description \<open>
    EXTp Counterfactual Soundness Theorem -- Isabelle/HOL mekanizasyonu.
  \<close>
  options [document = false]
  theories
    CST_Model
```

---

## 3. Model katmanı (Faz 0)

### 3.1 Gözlemlenebilir yüzey + trace

SOE'nin 4-tuple yüzeyi (`extp.tex` §`sec:soe`) + per-event timing `Δᵢ`.

```isabelle
record observable =
  rip         :: nat
  exit_reason :: nat
  exit_qual   :: nat
  rax         :: nat

record event =
  obs    :: observable
  timing :: nat

type_synonym trace = "event list"

definition aligned :: "trace \<Rightarrow> trace \<Rightarrow> bool" where
  "aligned To Tc \<longleftrightarrow> length To = length Tc"
```

> [!note] Tasarım notu
> `nat` kullanıldı; ileride 64-bit `word`'e çevrilebilir. Model **total** — kısmi fonksiyon yok,
> her tanım her girdide tanımlı, dolayısıyla `by eval` ile çalıştırılabilir.

### 3.2 Divergence detection `D` — iki clause

[[extp_formal_properties|P2 (SOE)]] + [[extp_formal_properties|P3 (MI)]] birleşimi;
App A'daki `D` tanımı birebir.

```isabelle
definition soe_clause :: "trace \<Rightarrow> trace \<Rightarrow> nat \<Rightarrow> bool" where
  "soe_clause To Tc i \<longleftrightarrow> obs (To ! i) \<noteq> obs (Tc ! i)"

definition timing_clause :: "nat \<Rightarrow> trace \<Rightarrow> trace \<Rightarrow> nat \<Rightarrow> bool" where
  "timing_clause Dstar To Tc i \<longleftrightarrow>
     \<bar>int (timing (Tc ! i)) - int (timing (To ! i))\<bar> > int Dstar"

definition D :: "nat \<Rightarrow> trace \<Rightarrow> trace \<Rightarrow> nat \<Rightarrow> bool" where
  "D Dstar To Tc i \<longleftrightarrow> soe_clause To Tc i \<or> timing_clause Dstar To Tc i"

definition diverges :: "nat \<Rightarrow> trace \<Rightarrow> trace \<Rightarrow> bool" where
  "diverges Dstar To Tc \<longleftrightarrow> (\<exists>i < length Tc. D Dstar To Tc i)"
```

**Neden `int`?** `timing :: nat` üzerinde çıkarma *truncating* olur (`3 - 5 = 0` — sessiz
hata). `int`'e cast + `abs` ile mutlak fark **her iki yönde** doğru hesaplanır.
Bu, modelin sessizce yanlış cevap vermesini engelleyen somut bir karar.

### 3.3 Intervention + validity envelope `E`

CST doküman §2.2 (intervention surface) ve §3.4 (envelope).

```isabelle
datatype scope  = PerEvent | PerWindow | Global
datatype iclass = NopCount | RegWrite | InputValue | CachePreload

record intervention =
  var      :: nat      \<comment> \<open>hedef degisken X'in ID'si\<close>
  newval   :: nat      \<comment> \<open>x'\<close>
  at_event :: nat      \<comment> \<open>e_i indeksi\<close>
  icls     :: iclass

record envelope =
  instr    :: nat      \<comment> \<open>timing enstruman ID'si (S1 / S2)\<close>
  wl_class :: nat
  gw_type  :: nat
  scp      :: scope
  s_in     :: "nat set"
  s_out    :: "nat set"

definition cst_v1_covered :: "envelope \<Rightarrow> intervention \<Rightarrow> bool" where
  "cst_v1_covered E \<iota> \<longleftrightarrow>
     scp E = PerEvent \<and>
     icls \<iota> \<in> {NopCount, RegWrite, InputValue, CachePreload} \<and>
     s_in E \<inter> s_out E = {}"
```

`PerWindow` / `Global` **datatype'ta var ama `cst_v1_covered` onları reddediyor** —
CST v1.0'ın "yalnızca per-event scope" kısıtı (CST doc §2.2) modele **kodlanmış** durumda,
prose'da kalmıyor.

---

## 4. do-operatörünün anlambilimi (Pearl severance)

> [!important] Bu bölüm (a) adımında eklendi
> Önceki iskelette `effectiveness ≡ True` bir **placeholder**'dı. Artık gerçek bir
> state-güncelleme semantiği var ve App A item (i) boş olmaktan çıktı.

Guest durumu bir *valuation*; `do(X=x')` fonksiyonel güncelleme.

```isabelle
type_synonym valuation = "nat \<Rightarrow> nat"

definition apply_iv :: "intervention \<Rightarrow> valuation \<Rightarrow> valuation" where
  "apply_iv \<iota> \<sigma> = \<sigma>(var \<iota> := newval \<iota>)"

definition effective :: "intervention \<Rightarrow> bool" where
  "effective \<iota> \<longleftrightarrow> (\<forall>\<sigma>. apply_iv \<iota> \<sigma> (var \<iota>) = newval \<iota>)"
```

Pearl'ün *"X'e giden tüm nedensel bağlantıları keser"* ifadesi **üç ayrı lemmaya** ayrıldı:

```isabelle
\<comment> \<open>(1) Effectiveness: do() X'i basariyla x'e set eder\<close>
lemma apply_iv_severs: "apply_iv \<iota> \<sigma> (var \<iota>) = newval \<iota>"
  by (simp add: apply_iv_def)

\<comment> \<open>(2) Locality: X disindaki degiskenlere DOKUNULMAZ\<close>
lemma apply_iv_local: "y \<noteq> var \<iota> \<Longrightarrow> apply_iv \<iota> \<sigma> y = \<sigma> y"
  by (simp add: apply_iv_def)

\<comment> \<open>(3) Severance: sonuc X'in ONCEKI degerinden BAGIMSIZ\<close>
lemma apply_iv_indep_pre: "apply_iv \<iota> \<sigma> (var \<iota>) = apply_iv \<iota> \<sigma>' (var \<iota>)"
  by (simp add: apply_iv_def)

lemma effective_holds: "effective \<iota>"
  by (simp add: effective_def apply_iv_severs)
```

| Lemma | Pearl karşılığı | Neden önemli |
|---|---|---|
| `apply_iv_severs` | effectiveness | `do()` gerçekten `x'` yazar |
| `apply_iv_local` | modularity'nin yapısal çekirdeği | çerçeve değişkenleri korunur → composition ile bağ |
| `apply_iv_indep_pre` | **asıl severance** | `σ` ve `σ'` farklı ön-durumlar olsa da sonuç aynı ⇒ X'e giden oklar kesik |

Somut `by eval` örnekleri:

```isabelle
lemma sanity_effective_forces:
  "apply_iv \<lparr> var = 7, newval = 42, at_event = 0, icls = RegWrite \<rparr> (\<lambda>_. 0) 7 = 42"
  by eval

lemma sanity_effective_local:
  "apply_iv \<lparr> var = 7, newval = 42, at_event = 0, icls = RegWrite \<rparr> (\<lambda>_. 5) 3 = 5"
  by eval
```

---

## 5. Dört-adımlı admissibility check + Teorem 1'in `⟸` yönü

`extp.tex` §`sec:intervention` adım (1)–(4) birebir:

```isabelle
definition admissible ::
    "nat \<Rightarrow> envelope \<Rightarrow> intervention \<Rightarrow> bool \<Rightarrow> trace \<Rightarrow> trace \<Rightarrow> bool" where
  "admissible Dstar E \<iota> assum_ok To Tc \<longleftrightarrow>
     cst_v1_covered E \<iota>      \<comment> \<open>adim 1: envelope CST v1.0 kapsaminda\<close>
   \<and> assum_ok                   \<comment> \<open>adim 2: A1-A4 referanslari mevcut/guncel\<close>
   \<and> diverges Dstar To Tc      \<comment> \<open>adim 3: D = true gozlemlendi\<close>
   \<and> var \<iota> \<in> s_in E"           \<comment> \<open>adim 4: X valide mudahale yuzeyinde\<close>

definition emits :: "..." where
  "emits Dstar E \<iota> assum_ok To Tc \<longleftrightarrow> admissible Dstar E \<iota> assum_ok To Tc"

lemma left_direction:
  "emits Dstar E \<iota> assum_ok To Tc \<longleftrightarrow> admissible Dstar E \<iota> assum_ok To Tc"
  by (simp add: emits_def)
```

> [!info] Neden bu yön trivial *olmalı*
> App A açıkça diyor: *"This direction is established by **code-level inspection** of the
> admissibility implementation, not by deductive proof."* Yani `⟸` yönü **inşaat gereği**
> doğrudur; modelde de öyle görünmesi **doğru** modellemenin işareti, zayıflık değil.

---

## 6. Sanity check'ler — `by eval` ile *ispatlanmış* gerçekler

`value` (sadece hesaplar, çıktıyı gözle okursun) yerine **lemma + `by eval`** kullanıldı:
böylece modelin doğru hesapladığı **build'in bir parçası**, yani regresyon koruması var.

```isabelle
definition ev :: "nat \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> event" where
  "ev r er eq a t =
     \<lparr> obs = \<lparr> rip = r, exit_reason = er, exit_qual = eq, rax = a \<rparr>, timing = t \<rparr>"

definition ex_orig :: trace where
  "ex_orig = [ ev 10 1 0 5 1000, ev 14 2 0 5 1050 ]"

lemma sanity_no_divergence:   "\<not> diverges 500 ex_orig ex_orig" by eval
lemma sanity_soe_clause:      "diverges 500 ex_orig [ ev 10 1 0 5 1000, ev 14 2 0 9 1050 ]" by eval
lemma sanity_timing_clause:   "diverges 500 ex_orig [ ev 10 1 0 5 3000, ev 14 2 0 5 1050 ]" by eval
lemma sanity_below_threshold: "\<not> diverges 500 ex_orig [ ev 10 1 0 5 1400, ev 14 2 0 5 1050 ]" by eval
```

| Senaryo | `Δ*` | Beklenen | Test eder |
|---|---|---|---|
| Aynı iz, mudahale yok | 500 | `False` | A4 tabanı (determinizm) |
| `rax` 5→9 @event 1 | 500 | `True` | **SOE clause** |
| timing +2000 cycle @event 0 | 500 | `True` | **timing clause** |
| timing +400 cycle @event 0 | 500 | `False` | **eşik altı** — `Δ*` gerçekten bağlıyor |

Son satır kritik: `Δ*`'ın *sadece* aşıldığında ateşlediğini gösterir — MI'ın konservatif
eşik yapısının modelde doğru olduğunu doğrular.

---

## 7. Faz 2 — Koşullu CST teoremi

### 7.1 Locale: A1–A4 hipotez, olasılıklar dışarıdan

> [!abstract] Mekanizasyonun kalbi
> A1–A4 **soyut predicate**; `δ_A1`, `ε_SOE`, `α` **soyut reel parametre**.
> `p_soe` / `p_tim` / `p_conf` = App A'nın üç bounding argümanındaki **ölçülen (bilinmeyen)
> katkı miktarları**; assumption'lar bunları sınırlar.
> **Isabelle bu sayıları üretmez** — Clopper-Pearson / MI kalibrasyonundan girer.

```isabelle
locale cst_assumptions =
  fixes Dstar    :: nat
    and delta_A1 :: real        \<comment> \<open>CapSep ampirik zarfi (A1)\<close>
    and eps_SOE  :: real        \<comment> \<open>SOE Clopper-Pearson ust siniri (A4)\<close>
    and alpha    :: real        \<comment> \<open>MI realized FPR (A3)\<close>
    and A1 A2 A3 A4 :: "envelope \<Rightarrow> intervention \<Rightarrow> bool"
    and p_soe  :: "envelope \<Rightarrow> intervention \<Rightarrow> real"
    and p_tim  :: "envelope \<Rightarrow> intervention \<Rightarrow> real"
    and p_conf :: "envelope \<Rightarrow> intervention \<Rightarrow> real"
    and eff_vars :: "envelope \<Rightarrow> nat set"
  assumes prob_nonneg: "0 \<le> delta_A1" "0 \<le> eps_SOE" "0 \<le> alpha"
      and prob_le_one:  "delta_A1 \<le> 1" "eps_SOE \<le> 1" "alpha \<le> 1"
      and A4_bounds_soe:  "\<And>E \<iota>. A4 E \<iota> \<Longrightarrow> 0 \<le> p_soe E \<iota> \<and> p_soe E \<iota> \<le> eps_SOE"
      and A3_bounds_tim:  "\<And>E \<iota>. A3 E \<iota> \<Longrightarrow> 0 \<le> p_tim E \<iota> \<and> p_tim E \<iota> \<le> alpha"
      and A1_bounds_conf: "\<And>E \<iota>. A1 E \<iota> \<Longrightarrow> 0 \<le> p_conf E \<iota> \<and> p_conf E \<iota> \<le> delta_A1 + alpha"
      and eff_subset:     "\<And>E. eff_vars E \<subseteq> s_in E"
```

*(Not: gerçek dosyada `A1 A2 A3 A4` ayrı ayrı `and` ile yazılı; burada okunurluk için birleştirildi.)*

Kalıntı epistemik zarf — App A'nın *"reported per-claim"* dediği büyüklük:

```isabelle
definition residual :: real where
  "residual = eps_SOE + delta_A1 + alpha"

lemma residual_nonneg: "0 \<le> residual"  using prob_nonneg by (simp add: residual_def)
lemma residual_le_three: "residual \<le> 3" using prob_le_one by (simp add: residual_def)
```

### 7.2 Üç bounding lemma (App A)

App A'daki **elimination → bounding** yeniden adlandırmasına sadık: *coincidence elimine
edilmez, sınırlanır.*

```isabelle
\<comment> \<open>App A lem:coincidence-soe\<close>
lemma coincidence_soe_bound:
  assumes "A4 E \<iota>" shows "p_soe E \<iota> \<le> eps_SOE"
  using A4_bounds_soe[OF assms] by simp

\<comment> \<open>App A lem:coincidence-timing\<close>
lemma coincidence_timing_bound:
  assumes "A3 E \<iota>" shows "p_tim E \<iota> \<le> alpha"
  using A3_bounds_tim[OF assms] by simp

\<comment> \<open>App A lem:confounder (bounding modulo A1)\<close>
lemma confounder_bound:
  assumes "A1 E \<iota>" shows "p_conf E \<iota> \<le> delta_A1 + alpha"
  using A1_bounds_conf[OF assms] by simp
```

| Lemma | App A karşılığı | Kaynak property |
|---|---|---|
| `coincidence_soe_bound` | `lem:coincidence-soe` | [[Strong_Observational_Equivalence (2)\|SOE]] → A4 |
| `coincidence_timing_bound` | `lem:coincidence-timing` | [[Measurement_Interference_v1 (1)\|MI]] → A3 |
| `confounder_bound` | `lem:confounder` | [[Capability_Separation_Theorem\|CapSep]] → A1 |

### 7.3 HP witness inşası — AC2(b), App A item (iv)

Paper'ın **en yeni ve en özgün** parçası; burada birebir mekanize edildi.
App A: *"W = S_in \ observable(·)ᵢ"*.

```isabelle
definition witness_W :: "envelope \<Rightarrow> nat set" where
  "witness_W E = s_in E - eff_vars E"

definition mask_prob :: "envelope \<Rightarrow> intervention \<Rightarrow> real" where
  "mask_prob E \<iota> = p_soe E \<iota> + p_conf E \<iota>"

lemma witness_W_subset: "witness_W E \<subseteq> s_in E"
  by (simp add: witness_W_def)

\<comment> \<open>W2 union bound: mask olasiligi <= residual\<close>
lemma w2_residual_bound:
  assumes "A1 E \<iota>" "A4 E \<iota>"
  shows "mask_prob E \<iota> \<le> residual"
  using coincidence_soe_bound[OF assms(2)] confounder_bound[OF assms(1)]
  unfolding mask_prob_def residual_def by linarith

lemma mask_prob_nonneg:
  assumes "A1 E \<iota>" "A4 E \<iota>"
  shows "0 \<le> mask_prob E \<iota>"
  using A4_bounds_soe[OF assms(2)] A1_bounds_conf[OF assms(1)]
  unfolding mask_prob_def by linarith
```

> [!tip] `w2_residual_bound` = App A'nın union bound'unun tam mekanizasyonu
> App A: *"the probability that D arises from a W-violation rather than from do(x') is
> bounded above by **ε_SOE + δ_A1 + α_realized**."*
> Burada `p_soe + p_conf ≤ ε_SOE + (δ_A1 + α) = residual`, `by linarith` ile ispatlı.
> **W1** (fixity enforceability) A4 ile, **W2** (fixity-does-not-mask) bu lemma ile discharge edilir.

### 7.4 Pearl/HP korespondans predicate'leri — artık somut

```isabelle
\<comment> \<open>delta_A1-relaxed composition\<close>
definition composition_relaxed :: "envelope \<Rightarrow> intervention \<Rightarrow> bool" where
  "composition_relaxed E \<iota> \<longleftrightarrow> p_conf E \<iota> \<le> delta_A1 + alpha"

\<comment> \<open>HP AC1: etki D, Tcf'de olay i'de mevcut\<close>
definition ac1 :: "trace \<Rightarrow> trace \<Rightarrow> nat \<Rightarrow> bool" where
  "ac1 To Tc i \<longleftrightarrow> D Dstar To Tc i"

\<comment> \<open>HP AC2(a): counterfactual sensitivity\<close>
definition ac2a :: "trace \<Rightarrow> trace \<Rightarrow> nat \<Rightarrow> bool" where
  "ac2a To Tc i \<longleftrightarrow> D Dstar To Tc i"

\<comment> \<open>HP AC2(b): W1 (A4) + W subset S_in + W2 (mask <= residual)\<close>
definition ac2b :: "envelope \<Rightarrow> intervention \<Rightarrow> bool" where
  "ac2b E \<iota> \<longleftrightarrow> A4 E \<iota> \<and> witness_W E \<subseteq> s_in E \<and> mask_prob E \<iota> \<le> residual"

lemma composition_relaxed_holds:
  assumes "A1 E \<iota>" shows "composition_relaxed E \<iota>"
  unfolding composition_relaxed_def using confounder_bound[OF assms] by simp

lemma ac2b_holds:
  assumes "A1 E \<iota>" "A4 E \<iota>" shows "ac2b E \<iota>"
  unfolding ac2b_def
  using assms(2) witness_W_subset w2_residual_bound[OF assms(1) assms(2)] by simp
```

> [!note] `ac1 = ac2a = D` neden aynı?
> **Kasıtlı.** App A: *"The fourth admissibility step (D = true) is therefore **exactly the
> operational test of AC2(a)**"* ve AC1 için *"D occurs in Tcf at event i by the fourth
> admissibility step."* Yani paper'da da ikisi aynı operasyonel teste indirgeniyor.
> Modeldeki bu özdeşlik **paper'a sadakat**, tembellik değil. (Ayrıştırma = sıradaki (b) adımı.)

### 7.5 Ana teorem — Teorem 1'in `⟹` yönü

```isabelle
theorem cst_conditional:
  assumes A1h: "A1 E \<iota>" and A2h: "A2 E \<iota>" and A3h: "A3 E \<iota>" and A4h: "A4 E \<iota>"
      and align: "aligned To Tc"
      and adm: "admissible Dstar E \<iota> assum_ok To Tc"
  shows "effective \<iota>
       \<and> composition_relaxed E \<iota>
       \<and> (\<exists>i w. i < length Tc \<and> i < length To
            \<and> D Dstar To Tc i
            \<and> ac1 To Tc i
            \<and> ac2a To Tc i
            \<and> ac2a_wit w To Tc i
            \<and> ac2b E \<iota>
            \<and> wit_bound w E \<iota> \<le> max (eps_SOE + delta_A1 + alpha)
                                     (delta_A1 + 2 * alpha))"
proof -
  from adm have "diverges Dstar To Tc" by (simp add: admissible_def)
  then obtain i where i: "i < length Tc" "D Dstar To Tc i"
    by (auto simp: diverges_def)
  from align i(1) have iTo: "i < length To" by (rule aligned_index_safe)
  from i(2) obtain w where w: "witnesses w Dstar To Tc i"
    using D_iff_witness by blast
  have wb: "wit_bound w E \<iota> \<le> max (eps_SOE + delta_A1 + alpha) (delta_A1 + 2 * alpha)"
  proof (cases w)
    case StructuralW then show ?thesis using wit_bound_structural[OF A1h A4h] by simp
  next
    case TimingW     then show ?thesis using wit_bound_timing[OF A1h A3h] by simp
  qed
  have "effective \<iota>" by (rule effective_holds)
  moreover have "composition_relaxed E \<iota>" using composition_relaxed_holds[OF A1h] .
  moreover have "ac1 To Tc i" using i(2) by (simp add: ac1_def)
  moreover have "ac2a To Tc i" using i(2) by (simp add: ac2a_def)
  moreover have "ac2a_wit w To Tc i" using w by (simp add: ac2a_wit_def)
  moreover have "ac2b E \<iota>" using ac2b_holds[OF A1h A4h] .
  ultimately show ?thesis using i iTo wb by blast
qed
```

> [!success] Teorem artık daha güçlü
> Önceki hali sadece *"bir i vardır ki D"* diyordu. Şimdi ek olarak:
> **(1)** `i < length To` — `aligned` gerçekten kullanılıyor, indeks güvenli;
> **(2)** somut bir **tanık `w`** dışarı veriliyor — hangi clause'un ateşlediği bilinir;
> **(3)** o tanığın **kendi zarfı** sınırlanıyor, blanket union bound değil.

```isabelle

corollary cst_residual_reported:
  assumes "A1 E \<iota>" "A4 E \<iota>"
  shows "0 \<le> mask_prob E \<iota> \<and> mask_prob E \<iota> \<le> residual"
  using mask_prob_nonneg[OF assms] w2_residual_bound[OF assms] by simp
```

**Okunuşu:** A1–A4 sağlanır ve dört-adımlı check geçerse ⟹ (i) effectiveness,
(ii) `δ_A1`-relaxed composition, (iii) AC1, (iv) AC2(a)+AC2(b) — hepsi bir arada,
`residual` zarfı per-claim raporlanarak.

### 7.55 AC2(a) tanıklarının ayrışması ve **bağımsızlığı** *(adım b)*

App A: *"The structural-clause version and timing-clause version **each independently**
witness AC2(a)."* Bu ifade modele taşındı — ve "independently" **ispatlandı**.

```isabelle
datatype ac2a_witness = StructuralW | TimingW

definition witnesses :: "ac2a_witness \<Rightarrow> nat \<Rightarrow> trace \<Rightarrow> trace \<Rightarrow> nat \<Rightarrow> bool" where
  "witnesses w Dstar To Tc i \<longleftrightarrow>
     (case w of StructuralW \<Rightarrow> soe_clause To Tc i
              | TimingW     \<Rightarrow> timing_clause Dstar To Tc i)"

\<comment> \<open>D, tanik varliginin TAM karsiligi\<close>
lemma D_iff_witness: "D Dstar To Tc i \<longleftrightarrow> (\<exists>w. witnesses w Dstar To Tc i)"

\<comment> \<open>her tanik TEK BASINA yeterli\<close>
lemma structural_witness_suffices: "soe_clause To Tc i \<Longrightarrow> D Dstar To Tc i"
lemma timing_witness_suffices: "timing_clause Dstar To Tc i \<Longrightarrow> D Dstar To Tc i"
```

**Bağımsızlık = hiçbiri diğerini gerektirmez.** İki somut karşı-örnekle ispatlandı:

```isabelle
definition ex_soe_only :: trace where    \<comment> \<open>rax @1 farkli, timing AYNI\<close>
  "ex_soe_only = [ ev 10 1 0 5 1000, ev 14 2 0 9 1050 ]"

definition ex_tim_only :: trace where    \<comment> \<open>timing @0 farkli, 4-tuple AYNI\<close>
  "ex_tim_only = [ ev 10 1 0 5 3000, ev 14 2 0 5 1050 ]"

lemma witness_indep_structural:
  "witnesses StructuralW 500 ex_orig ex_soe_only 1
   \<and> \<not> witnesses TimingW 500 ex_orig ex_soe_only 1"  by eval

lemma witness_indep_timing:
  "witnesses TimingW 500 ex_orig ex_tim_only 0
   \<and> \<not> witnesses StructuralW 500 ex_orig ex_tim_only 0" by eval

lemma witnesses_logically_independent:
  "(\<exists>To Tc i Dstar. witnesses StructuralW Dstar To Tc i \<and> \<not> witnesses TimingW Dstar To Tc i)
 \<and> (\<exists>To Tc i Dstar. witnesses TimingW Dstar To Tc i \<and> \<not> witnesses StructuralW Dstar To Tc i)"
  using witness_indep_structural witness_indep_timing by blast
```

> [!important] Neden bu önemli
> `D`'nin OR yapısı **gerçekten iki ayrı kanıt** — tek kanıtın iki yazılışı değil.
> Bu, aşağıdaki zarf-refinement'ın ön koşulu: ayrı tanıklar ⇒ ayrı hata kütlesi.

**`aligned` artık iş yapıyor** (önceden kullanılmayan hipotezdi):

```isabelle
lemma aligned_index_safe: "aligned To Tc \<Longrightarrow> i < length Tc \<Longrightarrow> i < length To"

\<comment> \<open>A4'un operasyonel ifadesi: mudahale yoksa 4-tuple noktasal esit\<close>
lemma no_divergence_obs_eq:
  assumes "aligned To Tc" and "\<not> diverges Dstar To Tc"
  shows "\<forall>i < length Tc. obs (To ! i) = obs (Tc ! i) \<and> i < length To"
```

---

### 7.8 ⭐ Tanık-başına hata zarfı — **yeni analitik sonuç**

> [!abstract] Çıkış noktası
> Paper'ın **OR-clause asimetrisi** (CST doc §2.1): SOE clause **deterministik**
> (A4 altında FPR sıfır), timing clause **olasılıksal** (FPR ≤ α).
> Buradan `extp.tex`'in prose'unda **açıkça türetilmemiş** bir sonuç çıkar:
> *bir claim'in epistemik ağırlığı, hangi tanığın ateşlediğine göre değişir.*

Blanket `residual` yerine tanık-başına zarf:

```isabelle
definition wit_bound :: "ac2a_witness \<Rightarrow> envelope \<Rightarrow> intervention \<Rightarrow> real" where
  "wit_bound w E \<iota> =
     (case w of StructuralW \<Rightarrow> p_soe E \<iota> + p_conf E \<iota>
              | TimingW     \<Rightarrow> p_tim E \<iota> + p_conf E \<iota>)"

lemma wit_bound_structural:
  assumes "A1 E \<iota>" "A4 E \<iota>"
  shows "wit_bound StructuralW E \<iota> \<le> eps_SOE + delta_A1 + alpha"

lemma wit_bound_timing:
  assumes "A1 E \<iota>" "A3 E \<iota>"
  shows "wit_bound TimingW E \<iota> \<le> delta_A1 + 2 * alpha"
```

**Ana sonuç** — karşılaştırma sadeleşince *tek bir eşitsizliğe* iner:

```isabelle
lemma structural_bound_tighter_iff:
  "(eps_SOE + delta_A1 + alpha \<le> delta_A1 + 2 * alpha) \<longleftrightarrow> eps_SOE \<le> alpha"
  by simp
```

> [!success] Yorum
> Yapısal tanık daha sıkı zarf verir **ancak ve ancak** `ε_SOE ≤ α_realized`.
> Bu kriter framework tarafından bir kez ve herkes için belirlenmiş **değil** —
> **kalibrasyon rejimi** belirler. Ve paper'ın iki rejimi eşitsizliğin **zıt
> taraflarında** duruyor.

#### Paper'ın gerçek sayılarıyla instantiation

İki `interpretation`, `extp.tex`'in ilan ettiği değerlerle:

```isabelle
interpretation cst_withinboot:
  cst_assumptions 9077 "37/10000" "37/10000" "61/10000" ... by unfold_locales auto

interpretation cst_crossboot:
  cst_assumptions 9077 "1040/10000" "1040/10000" "61/10000" ... by unfold_locales auto
```

| Rejim | `ε_SOE` | `δ_A1` | `α` | Kriter `ε_SOE ≤ α` | Yapısal zarf | Zamanlama zarfı | **Daha sıkı** |
|---|---|---|---|---|---|---|---|
| **Within-boot** (N=998) | 0.37% | 0.37% | 0.61% | ✅ sağlanır | **1.35%** | 1.59% | **yapısal** |
| **Cross-boot** (N=34) | 10.4% | 10.4% | 0.61% | ❌ ihlal | 21.41% | **11.62%** | **zamanlama** |

```isabelle
lemma withinboot_criterion:        "(37/10000 :: real) \<le> 61/10000" by simp
lemma withinboot_structural_tighter:
  "(37/10000 :: real) + 37/10000 + 61/10000 \<le> 37/10000 + 2 * (61/10000)" by simp

lemma crossboot_criterion:         "\<not> ((1040/10000 :: real) \<le> 61/10000)" by simp
lemma crossboot_timing_tighter:
  "(1040/10000 :: real) + 2 * (61/10000) \<le> 1040/10000 + 1040/10000 + 61/10000" by simp
```

> [!quote] Paper'a işlenen sonuç (App A, *Witness-refined epistemic envelopes*)
> *"…the structural witness gives the tighter envelope **iff** ε_SOE ≤ α_realized.
> This criterion is not decided once and for all by the framework — it is decided by
> the calibration regime, and the two regimes reported in §V-A fall on **opposite
> sides** of it. …the question 'which clause carries more evidential weight?' has **no
> regime-independent answer**."*

**Pratik sonuç:** downstream tüketici (mitigation verification, counterfactual fuzzing)
blanket union bound yerine **ateşleyen tanığın zarfını** raporlamalı — within-boot'ta
bu **daha sıkı**, cross-boot'ta ise **daha dürüst** bir sınır verir.

---

### 7.9 ⭐ `lem:silent` ve A2'nin gerçek rolü *(adım d)*

> [!danger] Kaçınılması gereken tuzak
> App A açıkça uyarıyor: lemmanın içeriği *"A2 kendi kapsamını ima eder"* **değil**
> (bu **definitional** olurdu). İçerik, **bağımsız belirtilmiş** iki bileşenin
> tutarlılığı: A2 *neyin gözlemlenebilir olduğunu*, emission policy *hangi gözlem
> altında claim yayınlandığını* söyler.

**Modeldeki bağımsızlık yapısaldır:**

| Bileşen | Nerede tanımlı | Diğerine referans? |
|---|---|---|
| `emits` / `admissible` | **top-level** definition | A2'ye referans **yok** |
| `A2` + `effect_at` | **locale parametresi** | emission'a referans **yok** |

Kilit hamle: **`effect_at` — yer altındaki nedensel etki — `D`'den ayrı bir parametre.**
A2'nin operasyonel içeriği bir locale assumption'ı olarak yazıldı:

```isabelle
and A2_manifests:
  "\<And>E \<iota> To Tc i. A2 E \<iota> \<Longrightarrow> var \<iota> \<in> s_in E
                  \<Longrightarrow> effect_at E \<iota> To Tc i \<Longrightarrow> D Dstar To Tc i"
```

`var ι ∈ s_in E` **guard'ı şart** — A2, `S_out` hakkında hiçbir şey söylemez.

#### İki yön

```isabelle
\<comment> \<open>(i) SOUNDNESS: gozlemlenebilir divergence OLMADAN claim yok (A2 GEREKMEZ)\<close>
lemma emits_implies_divergence:
  "emits Dstar E \<iota> assum_ok To Tc \<Longrightarrow> diverges Dstar To Tc"
  by (simp add: emits_def admissible_def)

\<comment> \<open>(ii) SCOPE-COMPLETENESS: S_in icindeki etki RAPORSUZ kalmaz (A2 GEREKLI)\<close>
lemma silent_no_missed_effect:
  assumes "A2 E \<iota>" and "var \<iota> \<in> s_in E"
      and "effect_at E \<iota> To Tc i" and "i < length Tc"
  shows "diverges Dstar To Tc"
```

#### A2'nin gerçek rolü — "ölü hipotez" değil, **farklı yönde** çalışıyor

```isabelle
theorem cst_scope_complete:
  assumes "A2 E \<iota>" "cst_v1_covered E \<iota>" "var \<iota> \<in> s_in E"
          "assum_ok" "effect_at E \<iota> To Tc i" "i < length Tc"
  shows "emits Dstar E \<iota> assum_ok To Tc \<and> (\<exists>j < length Tc. D Dstar To Tc j)"

\<comment> \<open>kontrapozitif: sessizlik S_in uzerinde BILGILENDIRICIDIR\<close>
corollary silence_informative_over_s_in:
  assumes "A2 E \<iota>" "var \<iota> \<in> s_in E" "\<not> diverges Dstar To Tc" "i < length Tc"
  shows "\<not> effect_at E \<iota> To Tc i"
```

> [!success] Çözülen bulmaca
> A2'nin `cst_conditional`'ın hipotez listesinde görünüp ispatta çağrılmaması
> bir **eksiklik değilmiş** — CST'nin iki ayrı yeterlilik yönü var:
>
> | Yön | Teorem | Kullanır |
> |---|---|---|
> | **Soundness** — yayınlanan claim'ler sağlam | `cst_conditional` | A1, A3, A4 |
> | **Scope-completeness** — S_in'deki etkiler kaçırılmaz | `cst_scope_complete` | **A2** |
>
> A2, emission sınırının **öteki tarafında** çalışıyor.

#### A2 tautoloji **değil** — yanlışlanabilirliğin somut kanıtı

Reviewer itirazı *"A2, D'nin tanımını tekrar etmiyor mu?"* — cevap `by eval` ile:

```isabelle
definition ex_silent :: trace where   \<comment> \<open>timing @0 +400: GERCEK fark, D'ye yansimaz\<close>
  "ex_silent = [ ev 10 1 0 5 1400, ev 14 2 0 5 1050 ]"

lemma silent_effect_exists:
  "timing (ex_silent ! 0) \<noteq> timing (ex_orig ! 0)
   \<and> \<not> diverges 500 ex_orig ex_silent"  by eval

lemma silent_effect_invisible_on_both_clauses:
  "\<not> soe_clause ex_orig ex_silent 0 \<and> \<not> timing_clause 500 ex_orig ex_silent 0"
  by eval
```

**Gerçek bir 400-cycle farkı var, ama `Δ*`=500 eşiğinin altında ⇒ D ateşlenmiyor.**
Böyle bir fark `S_in` içinde nedensel etki olsaydı **A2 ihlal edilirdi** ⇒ A2 dünyaya
dair bir şey söylüyor ve yanlış çıkabilir. Bu, MI'ın sub-`Δ*` silent-leak sınıfının
varsayım tarafından görünüşü.

---

### 7.95 ⭐ Paralel sweep: tanık-duyarlı ensemble zarfı *(adım f)*

> [!warning] Eksen ayrımı — karıştırma
> `accum_delta` (§7.6, Prop 1) **sıralı** kompozisyonun `δ_A1` union-bound birikimi.
> Bu bölüm **paralel** sweep için — App A *"sequential vs parallel ensembles"*: sweep =
> **33 bağımsız atomik claim**, `δ_A1` per-claim sınırlı, `i` üzerinde birikim **yok**,
> kapsam O(n). Bunlar **farklı eksenler**.

(b) gösterdi ki her claim'in zarfı **ateşleyen tanığa** bağlı. Bir sweep'te farklı
claim'ler farklı tanıklarla ateşlenebilir ⇒ ensemble-toplam zarf **tanık-duyarlı** olmalı
ve naïve `n · blanket`'ten **daha sıkı**.

```isabelle
definition wit_ub :: "ac2a_witness \<Rightarrow> real" where
  "wit_ub w = (case w of StructuralW \<Rightarrow> eps_SOE + delta_A1 + alpha
                       | TimingW     \<Rightarrow> delta_A1 + 2 * alpha)"

definition blanket :: real where
  "blanket = max (eps_SOE + delta_A1 + alpha) (delta_A1 + 2 * alpha)"

definition sweep_ub :: "ac2a_witness list \<Rightarrow> real" where
  "sweep_ub ws = sum_list (map wit_ub ws)"
```

**Kapalı form** (`k` yapısal, `n−k` zamanlama tanığı):

```isabelle
lemma sweep_ub_closed_form:
  "sweep_ub ws = of_nat (countS ws) * (eps_SOE + delta_A1 + alpha)
               + of_nat (countT ws) * (delta_A1 + 2 * alpha)"

lemma sweep_ub_tighter:            \<comment> \<open>ANA SONUC: naif blanket'ten daha siki\<close>
  "sweep_ub ws \<le> of_nat (length ws) * blanket"
```

**Üç kademeli sınır** — ölçülen ≤ tanık-sayımlı ≤ naïve:

```isabelle
theorem sweep_three_level_bound:
  assumes "A1 E \<iota>" "A3 E \<iota>" "A4 E \<iota>"
  shows "sweep_actual E \<iota> ws \<le> sweep_ub ws
       \<and> sweep_ub ws \<le> of_nat (length ws) * blanket"
```

> [!success] Kesin daha sıkı — sayısal kanıt (within-boot)
> Biri yapısal biri zamanlama tanığıyla ateşlenen 2-claim'lik sweep:
>
> | | Değer | Lemma |
> |---|---|---|
> | Tanık-duyarlı `sweep_ub [S,T]` | **2.94%** | `withinboot_sweep_value` |
> | Naïve `n · blanket` | 3.18% | `withinboot_blanket_value` |
> | **Kesin daha sıkı** (`<`) | ✓ | `withinboot_sweep_strictly_tighter` |
> | Homojen `[T,T]` → eşitlik | 3.18% = 3.18% | `withinboot_homogeneous_equality` |
>
> Sıkılık kazancı **tam olarak tanık karışımından** geliyor: homojen sweep'te eşitlik,
> karışık sweep'te kesin küçüklük. Fark, karışık-tanık claim sayısıyla **doğrusal büyür** —
> S1/T1 sweep'inin uçtan uca kapsam haritasında (paper Fig. sweep) doğrudan işe yarar.

---

### 7.96 ⭐ Gerçek sweep verisine bağlama *(adım h)*

> [!abstract] Teori ↔ artefakt köprüsü
> `sweep_ub` artık soyut değil — paper'ın **gerçek §sec:eval-demo-sweep sonucuna**
> bağlandı. Ve bu, (f) ile (d)'yi birleştiren en güçlü sonuç.

**Gerçek veri** (`extp.tex` sec:eval-demo-sweep): 33 input taranıyor, **divergence 1/33** —
yalnızca `0xDEAD` ateşliyor (SOE clause, RIP 0x10016). Diğer 32'si default-path, SOE-silent
⇒ `D=false` ⇒ **admissible claim yok**. Tüm divergence SOE-clause; **timing tanığı hiç yok**.

```isabelle
\<comment> \<open>input basina sonuc: Some w (admissible, tanikli) | None (sessiz)\<close>
definition emitted_of :: "ac2a_witness option list \<Rightarrow> ac2a_witness list" where
  "emitted_of xs = map the (filter (\<lambda>x. x \<noteq> None) xs)"

definition dead_sweep :: "ac2a_witness option list" where
  "dead_sweep = Some StructuralW # replicate 32 None"

lemma dead_sweep_total:         "length dead_sweep = 33"
lemma dead_sweep_emitted:       "emitted_of dead_sweep = [StructuralW]"
lemma dead_sweep_emitted_count: "length (emitted_of dead_sweep) = 1"
```

**Ensemble zarfı, gerçek kalibrasyonla:**

```isabelle
lemma dead_sweep_envelope_withinboot:
  "cst_withinboot.sweep_ub (emitted_of dead_sweep) = 135/10000"   \<comment> \<open>1.35%\<close>
lemma dead_sweep_envelope_crossboot:
  "cst_crossboot.sweep_ub (emitted_of dead_sweep) = 2141/10000"   \<comment> \<open>21.41%\<close>
```

> [!success] Asıl sonuç: scope-honesty × ensemble
> 33-input'luk sweep'in zarfı, **taranan input sayısıyla değil, admissible claim
> sayısıyla (1)** ölçekleniyor. Naïve "her taranan input bir yük taşır" görüşü
> `33 × blanket = 52.47%` verirdi; gerçek zarf **1.35%** — **~39 kat daha sıkı**,
> çünkü 32 sessiz input **bedava** (`dead_sweep_envelope_vs_naive_swept`).

```isabelle
\<comment> \<open>silent input'lar zarfa hic girmez -- (d) scope-honesty'nin ensemble sonucu\<close>
lemma silent_inputs_free:
  "sweep_ub (emitted_of (None # xs)) = sweep_ub (emitted_of xs)"

lemma dead_sweep_envelope_vs_naive_swept:
  "cst_withinboot.sweep_ub (emitted_of dead_sweep)
     < of_nat (length dead_sweep) * cst_withinboot.blanket"   \<comment> \<open>1.35% << 52.47%\<close>
```

Bu, mekanizasyonun **deneysel artefakta doğrudan bağlandığı** nokta: teorinin ürettiği
sayı (1.35%) paper'ın Fig. sweep verisinden çıkıyor ve makine-kontrollü.

> [!bug] Isabelle tuzağı — kayıt için
> `cst_crossboot` param'ı `1040/10000`, Isabelle bunu `13/125`'e **sadeleştiriyor**;
> bu, `simp`'in interpreted `sweep_ub` sabitini singleton lemmayla eşlemesini bozuyor
> (raw `cst_assumptions.sweep_ub` formuna açılıyor). Çözüm: `simp` yerine **`subst`**
> ile kontrollü rewrite (`apply (subst dead_sweep_emitted, subst …singleton_struct, simp)`).

---

### 7.97 ⭐ Silent-leak sınıfı = kanıtlanmış scope sınırı *(adım i)*

> [!abstract] Prose → teorem
> Paper'ın MI sub-Δ* silent-leak sınıfı ("explicitly deferred to a future CMD
> property class") artık **kanıtlanmış bir scope sınırı**: A2 altında S_in içinde
> sessiz sızıntı **imkânsız**, dolayısıyla **her** sessiz sızıntı zorunlu olarak
> S_out'ta. Scope sınırı ilan edilmiyor — assumption yapısı tarafından **zorlanıyor**.

```isabelle
definition silent_leak :: "trace \<Rightarrow> trace \<Rightarrow> nat \<Rightarrow> bool" where
  "silent_leak To Tc i \<longleftrightarrow> \<not> soe_clause To Tc i \<and> \<not> timing_clause Dstar To Tc i"

\<comment> \<open>(i.1) A2, S_in-ICI sessiz sizintiyi YASAKLAR\<close>
lemma A2_forbids_inscope_silent_leak:
  assumes "A2 E \<iota>" "var \<iota> \<in> s_in E" "effect_at E \<iota> To Tc i" "silent_leak To Tc i"
  shows False

\<comment> \<open>(i.2) ASIL SONUC: her sessiz sizinti ZORUNLU olarak S_out'ta\<close>
theorem silent_leak_only_out_of_scope:
  assumes "A2 E \<iota>" "effect_at E \<iota> To Tc i" "silent_leak To Tc i"
  shows "var \<iota> \<notin> s_in E"

\<comment> \<open>(i.3) kontrapozitif: S_in-ici etki GOZLEMLENEBILIR olmak zorunda\<close>
corollary inscope_effect_is_observable:
  assumes "A2 E \<iota>" "var \<iota> \<in> s_in E" "effect_at E \<iota> To Tc i"
  shows "soe_clause To Tc i \<or> timing_clause Dstar To Tc i"
```

**Somut bağlantı** (gerçek Δ*=9077, within-boot): `ex_silent`'teki +400-cycle fark
sub-eşik ⇒ her iki clause sessiz ⇒ `silent_leak`; dolayısıyla `silent_leak_only_out_of_scope`
ile ancak S_out'ta yaşayabilir.

```isabelle
lemma ex_silent_is_silent_leak_withinboot:
  "cst_withinboot.silent_leak ex_orig ex_silent 0"   \<comment> \<open>400 < 9077 ⇒ sessiz\<close>
```

> [!success] Stratejik çıkar
> Bu, CST'nin *scope-honesty* çekirdeğini prose'dan teoreme çeviriyor. Reviewer'a:
> "CMD'ye erteleme keyfî değil — A2'nin altında sessiz sızıntının S_out'ta olması
> **zorunlu**." Paper'a **yalnızca App A**'ya işlendi (limit dışı; gövde ≤13pp korundu).

---

### 7.6 Proposition 1 — sıralı kompozisyon

```isabelle
\<comment> \<open>Zincir admissible <=> tum atomik adimlar admissible\<close>
lemma chain_iff_all_atomic:
  "list_all (\<lambda>b. b) steps \<longleftrightarrow> (\<forall>k < length steps. steps ! k)"
  by (simp add: list_all_length)

primrec accum_delta :: "nat \<Rightarrow> real" where
  "accum_delta 0 = 0"
| "accum_delta (Suc n) = accum_delta n + delta_A1"

lemma accum_delta_eq: "accum_delta n = of_nat n * delta_A1"
  by (induct n) (simp_all add: algebra_simps)

lemma accum_delta_mono: "accum_delta n \<le> accum_delta (Suc n)"
  using prob_nonneg(1) by simp

lemma accum_delta_linear_bound: "accum_delta n \<le> of_nat n * delta_A1"
  by (simp add: accum_delta_eq)
```

App A: *"δ_A1 accumulates by union bound; tighter bounds under independence are not asserted."*
→ `accum_delta_eq` tam olarak `n · δ_A1` verir: **O(n), bozunma yok**, commutativity **iddia edilmiyor**.

> [!success] 2026-09-01 — §8.3 bu soyutlamayı **gerçek zincirle** değiştirdi
> `chain_iff_all_atomic` (boolean listesi) yerine `chain_ok E ιs ok Ts`: `Ts!0 = T_orig`,
> `Ts!(k+1)` = k. adımın T_cf'i **ve** k+1. adımın baseline'ı. `chain_ok_iff_steps` Prop 1'in
> ifadesi, `chain_extend` App A'nın tümevarım adımı ("T_cf^(n) as the original trace"),
> `chain_conditional` her adıma Teorem 1. Bkz. §8.006.

### 7.65 Composition aksiyomu — W/K_fwk formunda (§8.1–8.2, 2026-09-01)

Statement-fidelity denetimi: paper item (ii) *"for all W ∈ K_fwk, the outcome under do(x') equals the
outcome under do(x') while holding W = w_orig, up to a perturbation bounded by Δ* on each W with
probability ≥ 1 − δ_A1"* — mekanizasyon bunu yalnızca `composition_relaxed ↔ p_conf ≤ δ+α`
(confounder bound) olarak **modellemişti**. Şimdi birebir:

```isabelle
definition hold :: "nat set ⇒ valuation ⇒ valuation ⇒ valuation" where
  "hold W σo σ = (λv. if v ∈ W then σo v else σ v)"

lemma composition_strict_structural:      (* Pearl strict form *)
  assumes "var ι ∉ W" and "∀w∈W. σc w = σo w"
  shows "hold W σo (apply_iv ι σc) = apply_iv ι σc"

locale cst_composition = cst_assumptions +
  fixes fwk_vars :: "nat set" and p_pert :: "envelope ⇒ intervention ⇒ nat ⇒ real"
  assumes A1_pert_per_var: "A1 E ι ⟹ w ∈ fwk_vars ⟹ 0 ≤ p_pert E ι w ∧ p_pert E ι w ≤ delta_A1"
      and A1_target_outside_fwk: "A1 E ι ⟹ var ι ∉ fwk_vars"      (* CapSep: K_int ∩ K_fwk = ∅ *)

theorem composition_W_holds: "A1 E ι ⟹ composition_W E ι"
theorem composition_strict_recovered: "A1 E ι ⟹ delta_A1 = 0 ⟹ w ∈ fwk_vars ⟹ p_pert E ι w = 0"
theorem cst_conditional_W: ... shows "composition_W E ι ∧ effective ι ∧ composition_relaxed E ι ∧ (∃i w. ...)"
```

Antecedent disiplini korundu: `p_pert` soyut reel (ölçüm), yalnızca yapısal kısım + aritmetik ispatlı.
`var ι ∉ K_fwk` ön-koşulu tam olarak CapSep'in yapısal iddiasıdır — katı formun **neden** disjointness
gerektirdiği makinede görünür oluyor (aksi halde `hold` müdahaleyi geri alır).

### 7.7 Locale tutarlılığı — "vacuously true" değil

```isabelle
interpretation cst_trivial:
  cst_assumptions
    500                              \<comment> \<open>Dstar\<close>
    "1/10" "1/10" "1/20"             \<comment> \<open>delta_A1, eps_SOE, alpha\<close>
    "\<lambda>E \<iota>. True" "\<lambda>E \<iota>. True"         \<comment> \<open>A1, A2\<close>
    "\<lambda>E \<iota>. True" "\<lambda>E \<iota>. True"         \<comment> \<open>A3, A4\<close>
    "\<lambda>E \<iota>. 0" "\<lambda>E \<iota>. 0" "\<lambda>E \<iota>. 0"     \<comment> \<open>p_soe, p_tim, p_conf\<close>
    "\<lambda>E. {}"                         \<comment> \<open>eff_vars\<close>
  by unfold_locales auto
```

> [!important] Bu neden şart
> Locale assumption'ları çelişkili olsaydı, içindeki **her teorem boş yere doğru** olurdu
> (*ex falso*). `interpretation` somut bir model verip assumption'ları gerçekten sağlayarak
> bunu dışlar. Mekanizasyonun **anlamlı** olduğunun kanıtı.

---

## 8. İspatlanan fact envanteri (115 fact, `sorry` yok)

### 8.006 §8 (2026-09-01) ile eklenen 21 fact — F2/F5 köşeleri

| Fact | Ne kurar |
|---|---|
| `hold_in`, `hold_out` | `hold W σ_orig σ`: W'yi T_orig değerlerine sabitleme operatörü |
| `composition_strict_structural` | Pearl **katı** composition: W dogal değerindeyse `hold W (do x') = do x'` — ön-koşul `var ι ∉ W` (CapSep) |
| `hold_preserves_effectiveness` | W tutulurken `do(x')` geri alınmaz |
| `composition_relaxed_structural` | Gevşek form, yapısal kısım: W dışında özdeş, W içinde ≤ Δ* (pert_bounded altında) |
| `composition_W_holds` | **App A item (ii) birebir**: A1 ⟹ `composition_W` (locale `cst_composition`) |
| `composition_W_keeps_effect` | Effectiveness composition altında korunur |
| `composition_strict_recovered` | δ_A1 = 0 ⟹ her W için p_pert = 0 (katı form geri kazanımı) |
| `composition_W_union_bound` | Sonlu K_fwk: Σ p_pert ≤ |K_fwk|·δ_A1 |
| `cst_conditional_W` | Koşullu CST + `composition_W` birlikte |
| `comp_demo_nonvacuous`, `comp_demo_A1_falsifiable` | `cst_composition` tutarlı ve vacuous değil (K_fwk={0}, A1 = "hedef≠0") |
| `chain_ok_iff_steps` | **Prop 1'in gerçek ifadesi**: zincir admissible ⟺ her adım *kendi baseline'ıyla* admissible |
| `chain_extend` | App A tümevarım adımı: zinciri uzatmak = `last Ts`'i baseline alan atomik adım |
| `chain_conditional` | Zincirin her adımı için Teorem 1 sonucu (`Ts!k`, `Ts!(k+1)` üzerinde) |
| `chain_delta_step` | A1^(n+1) = A1^(n) + δ_A1 |
| `chain_envelope_bound` | Zincir tanık zarfı ≤ `sweep_ub` ≤ n·blanket (bağımsızlık varsayılmaz) |
| `chain_demo_step1/2`, `chain_demo`, `chain_demo_baseline_shift` | Somut 2-adım zincir; ikinci adım T_orig'e değil T1'e karşı ölçülür |


### 8.0 Adım (b) ile eklenen 19 fact

| Fact | Ne kurar |
|---|---|
| `witnesses_struct`, `witnesses_timing` | tanık ↔ clause eşlemesi (simp kuralları) |
| `D_iff_witness` | `D` = tanık varlığının tam karşılığı |
| `structural_witness_suffices` | yapısal tanık tek başına yeterli |
| `timing_witness_suffices` | zamanlama tanığı tek başına yeterli |
| `aligned_index_safe` | indeks güvenliği — `aligned` iş yapar |
| `no_divergence_obs_eq` | A4'ün operasyonel ifadesi |
| `witness_indep_structural` | **karşı-örnek:** yapısal ateşler, zamanlama ateşlemez |
| `witness_indep_timing` | **karşı-örnek:** zamanlama ateşler, yapısal ateşlemez |
| `witnesses_logically_independent` | **iki tanık mantıksal olarak bağımsız** |
| `ac2a_iff_wit` | AC2(a) ⟺ bir tanık var |
| `wit_bound_structural` | yapısal zarf ≤ `ε_SOE + δ_A1 + α` |
| `wit_bound_timing` | zamanlama zarfı ≤ `δ_A1 + 2α` |
| `wit_bound_structural_is_residual` | yapısal zarf = App A'nın `residual`'i |
| **`structural_bound_tighter_iff`** | ⭐ **tam kriter:** sıkılık ⟺ `ε_SOE ≤ α` |
| `withinboot_criterion` | within-boot'ta kriter **sağlanır** |
| `withinboot_structural_tighter` | 1.35% ≤ 1.59% |
| `crossboot_criterion` | cross-boot'ta kriter **ihlal** |
| `crossboot_timing_tighter` | 11.62% ≤ 21.41% (**ters döner**) |

### 8.05 Adım (d) ile eklenen 8 fact

| Fact | Ne kurar |
|---|---|
| `emits_implies_divergence` | soundness yönü: divergence'sız claim yok |
| `silent_no_missed_effect` | **A2 aktif:** S_in içi etki ⟹ divergence |
| `silent_emission_complete` | S_in içi etki ⟹ claim mutlaka yayınlanır |
| `scope_honest_silence` | divergence yoksa claim yok |
| **`cst_scope_complete`** | ⭐ kapsam-tamlığı teoremi (soundness'ın eşi) |
| `silence_informative_over_s_in` | kontrapozitif: sessizlik S_in'de bilgilendirici |
| **`silent_effect_exists`** | ⭐ **A2 tautoloji değil** — gerçek fark, D sessiz |
| `silent_effect_invisible_on_both_clauses` | her iki clause da sessiz |

### 8.02 Adım (f) ile eklenen 14 fact

| Fact | Ne kurar |
|---|---|
| `wit_ub` / `blanket` / `sweep_ub` | tanık-üst-sınır, naïve blanket, ensemble zarfı (def) |
| `wit_ub_le_blanket`, `wit_ub_nonneg` | tanık zarfı ≤ blanket, ≥ 0 |
| `sum_list_const_real` | yardımcı: sabit toplamı |
| `countS` / `countT`, `length_countS_countT` | tanık sayımı, `n = k + (n−k)` |
| `sweep_ub_closed_form` | kapalı form: `k·(ε+δ+α)+(n−k)·(δ+2α)` |
| **`sweep_ub_tighter`** | ⭐ tanık-duyarlı ≤ naïve `n·blanket` |
| `sweep_ub_nonneg`, `sweep_actual_le_ub` | ≥ 0; ölçülen ≤ tanık-sayımlı |
| **`sweep_three_level_bound`** | ⭐ ölçülen ≤ tanık-sayımlı ≤ naïve |
| **`withinboot_sweep_strictly_tighter`** | ⭐ karışık sweep **kesin** daha sıkı (2.94 < 3.18) |
| `withinboot_sweep_value`, `withinboot_blanket_value` | 294/10000, 318/10000 |
| `withinboot_homogeneous_equality` | homojen sweep → eşitlik |

### 8.01 Adım (h) ile eklenen 14 fact

| Fact | Ne kurar |
|---|---|
| `emitted_of` + `_Nil`/`_None`/`_Some` | sessiz (None) düşürülür, tanık listesi (def+simp) |
| `sweep_ub_singleton_struct`/`_timing` | tekil claim zarfı |
| `ensemble_envelope_bound` | zarf ≤ admissible-claim-sayısı × blanket |
| `silent_inputs_free` | **sessiz input zarfa girmez** (d×f) |
| `dead_sweep` + `_total`/`_emitted`/`_emitted_count` | gerçek veri: 33 input, 1 admissible, `[StructuralW]` |
| **`dead_sweep_envelope_withinboot`** | ⭐ = 1.35% (gerçek sayı) |
| `dead_sweep_envelope_crossboot` | = 21.41% |
| `dead_sweep_naive_swept_value` | naïve = 52.47% |
| **`dead_sweep_envelope_vs_naive_swept`** | ⭐ 1.35% ≪ 52.47% (~39×) |

### 8.005 Adım (i) ile eklenen 5 fact

| Fact | Ne kurar |
|---|---|
| `silent_leak` + `silent_leak_iff_not_D` | sessiz sızıntı = ¬D (def) |
| `A2_forbids_inscope_silent_leak` | A2, S_in-içi sessiz sızıntıyı yasaklar |
| **`silent_leak_only_out_of_scope`** | ⭐ her sessiz sızıntı zorunlu S_out'ta |
| `inscope_effect_is_observable` | kontrapozitif: S_in-içi etki gözlemlenebilir |
| `ex_silent_is_silent_leak_withinboot` | somut: 400<9077 ⇒ sessiz |

### 8.1 Faz 0–2 çekirdek fact'leri

| # | Fact | Bölüm | İspat | App A / paper karşılığı |
|---|---|---|---|---|
| 1 | `apply_iv_severs` | §3.1 | `simp` | item (i) effectiveness |
| 2 | `apply_iv_local` | §3.1 | `simp` | modularity yapısal çekirdeği |
| 3 | `apply_iv_indep_pre` | §3.1 | `simp` | Pearl severance |
| 4 | `effective_holds` | §3.1 | `simp` | item (i) |
| 5 | `sanity_effective_forces` | §3.1 | `eval` | somut do() örneği |
| 6 | `sanity_effective_local` | §3.1 | `eval` | locality örneği |
| 7 | `left_direction` | §4 | `simp` | **Teorem 1 `⟸` yönü** |
| 8 | `sanity_no_divergence` | §5 | `eval` | A4 tabanı |
| 9 | `sanity_soe_clause` | §5 | `eval` | SOE clause |
| 10 | `sanity_timing_clause` | §5 | `eval` | timing clause |
| 11 | `sanity_below_threshold` | §5 | `eval` | `Δ*` eşik davranışı |
| 12 | `residual_nonneg` | §6 | `simp` | zarf ≥ 0 |
| 13 | `residual_le_three` | §6 | `simp` | zarf sınırlı |
| 14 | `coincidence_soe_bound` | §6.1 | `simp` | `lem:coincidence-soe` |
| 15 | `coincidence_timing_bound` | §6.1 | `simp` | `lem:coincidence-timing` |
| 16 | `confounder_bound` | §6.1 | `simp` | `lem:confounder` |
| 17 | `witness_W_subset` | §6.2 | `simp` | W ⊆ S_in |
| 18 | `w2_residual_bound` | §6.2 | `linarith` | **AC2(b) W2 union bound** |
| 19 | `mask_prob_nonneg` | §6.2 | `linarith` | zarf alt sınırı |
| 20 | `composition_relaxed_holds` | §6.3 | `simp` | item (ii) δ-relaxed composition |
| 21 | `ac2b_holds` | §6.3 | `simp` | item (iv) AC2(b) |
| 22 | **`cst_conditional`** | §6.4 | `proof–qed` | **Teorem 1 `⟹` yönü** |
| 23 | `cst_residual_reported` | §6.4 | `simp` | "reported per-claim" |
| 24 | `chain_iff_all_atomic` | §6.5 | `simp` | **Proposition 1** |
| 25 | `accum_delta_eq` | §6.5 | `induct` | union-bound birikimi |
| 26 | `accum_delta_mono` | §6.5 | `simp` | monotonluk |
| 27 | `accum_delta_linear_bound` | §6.5 | `simp` | O(n) ölçekleme |

**+1** `interpretation cst_trivial` — locale tutarlılık yükümlülüğü (`unfold_locales auto`).

---

## 8.9 Adım (g) ve (e) — dürüst kısmi + gerçekçilik

### (g) seL4 lifting arayüzü — **açık KAPATILMADI, izole edildi**

> [!danger] Bu, lifting'i kapatmaz
> Gerçek kapatma = `verified_no_fwk_touch` assumption'ını L4.verified'in gerçek
> atomicity teoreminden **türetmek** + `lift`/`sel4_astate`'i gerçek seL4 makine
> modeline bağlamak. Çok-yıllık, K_verified'le sınırlı. Bu dosyada **YOK**.

Yapılan: yükümlülüğü **tek, isimli bir assumption'a** indirgeyen tipli arayüz.

```isabelle
typedecl sel4_astate
consts lift :: "sel4_astate \<Rightarrow> observable"
datatype kop = Create | Copy | Revoke | Destroy      \<comment> \<open>K_verified\<close>
             | MapEPT | Unmap | ReadVMCS | WriteVMCS  \<comment> \<open>K_extended\<close>

locale sel4_lifting =
  fixes op_authority :: "kop \<Rightarrow> nat set" and fwk_vars :: "nat set"
  assumes verified_no_fwk_touch:      \<comment> \<open>^ L4.verified'in SAGLADIGI; ISPATLANMAZ\<close>
    "\<And>op. op \<in> k_verified \<Longrightarrow> op_authority op \<inter> fwk_vars = {}"
begin
  theorem A1_unconditional_for_verified:   \<comment> \<open>assumption VERILDIGINDE delta=0\<close>
    assumes "op \<in> k_verified" shows "op_authority op \<inter> fwk_vars = {}"
end
```

| Fact | Ne kurar |
|---|---|
| `k_partition_disjoint`/`_complete` | K_verified ⊎ K_extended = UNIV |
| **`A1_unconditional_for_verified`** | ⭐ assumption altında K_verified δ=0 |
| `verified_no_confounder` | K_verified op'u K_fwk'e dokunmaz |
| `extended_can_touch_fwk` | K_extended framework'e **dokunabilir** (ampirik kalır) |
| `verified_cannot_touch_fwk` | somut: Create dokunmaz |

**Değer:** paper'ın "chartered via seL4's infrastructure" ifadesi artık **tek
yükümlülüğü isimlendirilmiş tipli arayüz** — ama açık kapatılmadı, *sınırlandı*.
Kosullu CST teoremi (Faz 2) bunun hiçbirine ihtiyaç duymaz.

### (e) Observable yüzeyi = gerçek register genişlikleri

`nat` → **`64 word`** (rip/exit_qual/rax) + **`32 word`** (exit_reason, gerçek VMCS
genişliği). Dürüstlük kararı: yüzey yalnızca **eşitlikle** karşılaştırılır
(`soe_clause`), o yüzden word'e çevirmek **taşma riski taşımaz**. `timing` **`nat`
kaldı** — TSC aritmetiği + wraparound bilinçli olarak kapsam dışı (fresh-boot
disiplini kısa izler + oturum-içi reset sağlar). Tüm `by eval` sanity'ler word
altında geçiyor. `HOL-Library.Word` import edildi (ROOT'a `sessions HOL-Library`).

---

## 9. Ne ispatlanmadı — dürüstlük bölümü

> [!danger] Bunları iddia ETME
> Aşağıdakiler mekanizasyonun **kapsamı dışında** ve öyle kalacak.

1. **Ampirik antecedent'ler ispatlanmadı.** `score_S = 1.0000`, Clopper-Pearson ≤%0.37 / ≤%10.4,
   `α_realized` %0.61–2.78 — bunlar **ölçüm**. Isabelle sadece `[0,1]` aralığı ve union-bound
   aritmetiğini ispatlar. Bu bir eksik değil, **CST'nin koşullu teorem oluşunun doğal sonucu**
   (`extp.tex`: *"Isabelle establishes the conditional soundness theorem; calibration data
   supplies the antecedents"*).
2. **Lifting yapılmadı** (Faz 3, §7 stub). Dolayısıyla A1, `K_verified` için bile
   L4.verified'den **discharge edilmiş değil** — locale hipotezi olarak duruyor.
3. ~~`ac1` ve `ac2a` aynı~~ → **(b) ile çözüldü.** AC2(a) artık tanık-indeksli
   (`ac2a_wit`), iki tanık ayrıştırıldı ve bağımsızlıkları ispatlandı.
   `ac1` hâlâ `D`'ye indirgeniyor — bu **doğru**, App A AC1'i dördüncü admissibility
   adımına bağlıyor.
4. ~~A2 teoremde kullanılmıyor~~ → **(d) ile çözüldü.** A2 artık `cst_scope_complete`
   teoreminde aktif; `cst_conditional`'da görünmemesi doğruymuş — A2 soundness'a değil,
   **kapsam-tamlığına** katkı verir (emission sınırının öteki tarafı). Ayrıca
   `effect_at` ayrı parametre yapılarak tautoloji tuzağından kaçınıldı ve A2'nin
   yanlışlanabilirliği `by eval` ile gösterildi.
5. ~~`aligned` kullanılmıyor~~ → **(b) ile çözüldü.** `aligned_index_safe` ve
   `no_divergence_obs_eq` ile devreye girdi; `cst_conditional` artık `i < length To`
   sonucunu da veriyor.
6. **Multi-VCPU race'ler, silent mikromimari kanallar** — App A'daki gibi kapsam dışı.
7. **`p_soe`/`p_tim`/`p_conf` gerçek değerleri modelde 0.** Interpretation'larda
   katkılar 0 alındı (assumption'lar `0 ≤ p ≤ bound` istiyor). Zarf **üst sınırları**
   ispatlı; gerçek katkı miktarları kalibrasyondan gelir. Yani tablo `1.35%` vs `1.59%`
   **worst-case** zarflardır, ölçülen değerler değil.

### Paper'da düzeltilmesi önerilen çerçeve gerilimi

`extp.tex` §`sec:discussion-isabelle` *"infrastructure is already in place"* diyor;
CST doc §5.4 ise *"VMM katmanı seL4'ün verified scope'unun üstünde… çok-yıllık efor"* diyor.
seL4'ü bilen bir NDSS reviewer'ı `K_extended`'ın verified olmadığını hemen görür.
**Öneri:** ana metni §5.4'ün dürüstlüğüne yaklaştır — hem savunulabilirlik hem beklenti yönetimi için.

---

## 10. Sıradaki adımlar

| Öncelik | İş | Durum |
|---|---|---|
| ~~(b)~~ | `ac2a`'yı iki tanığa ayır + bağımsızlık + tanık-başına zarf | ✅ **Tamam** (2026-08-28) |
| ~~(c)~~ | `extp.tex`'e "machine-checked conditional theorem" ibaresi | ✅ **Tamam** (6 nokta) |
| ~~(d)~~ | `lem:silent` + A2'nin aktifleştirilmesi | ✅ **Tamam** (2026-08-28) |
| ~~(f)~~ | Paralel sweep'te tanık-duyarlı ensemble zarfı | ✅ **Tamam** (2026-08-28) |
| ~~(h)~~ | `sweep_ub`'ı gerçek 33-claim verisine bağla | ✅ **Tamam** (2026-08-28) |
| ~~(i)~~ | Silent-leak = kanıtlanmış scope sınırı (A2) | ✅ **Tamam** (2026-08-28) |
| ~~(g)~~ | seL4 lifting **arayüzü** (açık izole, kapatılmadı) | ✅ **Kısmi** (2026-08-28) — bkz §8.9 |
| ~~(e)~~ | Observable → 64/32-bit `word` (timing nat kaldı) | ✅ **Tamam** (2026-08-28) |
| ~~(F2)~~ | Composition W/K_fwk formunda (paper item ii birebir) | ✅ **Tamam** (2026-09-01, §8.1–8.2) |
| ~~(F5)~~ | Prop 1 trace-zincirli (T_cf^(k) baseline) | ✅ **Tamam** (2026-09-01, §8.3) |
| (g-tam) | `verified_no_fwk_touch`'ı L4.verified'den türet | ❌ Çok-yıllık; kapsamda değil |

> [!check] Sayfa limiti doğrulandı (2026-08-28)
> Overleaf derlemesi: **gövde (Intro→Conclusion) sayfa 13'e sığıyor**, Ethics 14'te
> başlıyor ⇒ NDSS 2027 ≤13pp şartı **karşılandı**. Redundans kesimi (Pearl/HP tekrar
> paragrafı, A1-modulo tekrarı) + float `[t]→[tb]` yetti; orijinal içerikten kesim
> gerekmedi. Tüm mekanizasyon içeriği App A'da (limit dışı). hyperref uyarısı
> (`$\Kextended$` başlığı) `\texorpdfstring` ile düzeltildi.

> [!success] A1–A4'ün tamamı artık aktif
> Mekanizasyonda **ölü hipotez kalmadı**: A1 → confounder bound + composition,
> A3 → timing coincidence + tanık zarfı, A4 → SOE coincidence + AC2(b) W1,
> A2 → kapsam-tamlığı. Dördü de en az bir ispatta gerçekten çağrılıyor.

> [!question] Sıradaki aday: **(e)** veya konsolidasyon
> Analitik iddia artık oldukça güçlü (82 fact, dört antecedent aktif, teori deneysel
> artefakta bağlı). Kalan işler **artımsal**: **(e)** `nat`→`word` gerçekçiliği artırır
> ama iddiayı değiştirmez; **(i)** silent-leak'i A2 ihlali olarak formalize eder.
> Alternatif: yeni fact eklemek yerine **Overleaf'te derleyip sayfa limitini doğrulamak**
> ve mevcut mekanizasyonu konsolide etmek (bkz. §9 sayfa-limiti uyarısı).

---

## Ek: dosya konumları

```
extp-paper/
├── isabelle/
│   ├── CST_Model.thy      ← 1756 satır, tüm mekanizasyon
│   ├── ROOT               ← session EXTp_CST
│   └── build_log.txt      ← son build çıktısı
└── Isabelle_Mechanization_CST.md   ← bu not
```
