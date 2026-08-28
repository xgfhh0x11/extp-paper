---
title: "CST Isabelle Mekanizasyonu — Matematiksel Sunum"
tags:
  - extp
  - isabelle
  - formal-methods
  - cst
  - math
status: kosullu-cekirdek-bcdfghi-e-13pp-ok
isabelle-version: Isabelle2025-1
session: EXTp_CST
build-status: "0 error / 0 warning / 0 sorry"
proven-facts: 94
created: 2026-08-29
updated: 2026-08-29
---

# CST Isabelle Mekanizasyonu — Matematiksel Sunum

> [!info] Bu not ne
> [[Isabelle_Mechanization_CST]] notunun **kod-siz, matematiksel** kardeşi. Her tanım ve
> teorem `CST_Model.thy`'den LaTeX'e çevrildi; Isabelle fact adı her ifadenin yanında
> `code` olarak verilir. Kaynak: `isabelle/CST_Model.thy` (1334 satır, 94 fact, `sorry` yok).

İlgili notlar: [[Isabelle_Mechanization_CST|Isabelle log (kodlu)]] ·
[[Counterfactual_Soundness_Theorem_v1 (1)|CST v1.0]] ·
[[extp_formal_properties|P1–P8]] ·
[[Capability_Separation_Theorem|CapSep]] ·
[[Strong_Observational_Equivalence (2)|SOE]] ·
[[Measurement_Interference_v1 (1)|MI]]

---

## 0. Notasyon

| Sembol | Isabelle | Anlam |
|---|---|---|
| $T_o, T_c$ | `To`, `Tc` | orijinal ve counterfactual trace |
| $e_i = (o_i, \tau_i)$ | `To ! i` | $i$. olay: gözlemlenebilir 4-tuple + timing |
| $\Delta^{*}$ | `Dstar` | MI timing eşiği |
| $\iota = (X, x', i, c)$ | `intervention` | hedef değişken, yeni değer, olay indeksi, sınıf |
| $\mathcal{E}$ | `envelope` | validity envelope: $(\text{instr}, \text{wl}, \text{gw}, \text{scp}, S_{in}, S_{out})$ |
| $\delta_{A1}, \varepsilon_{SOE}, \alpha$ | `delta_A1`, `eps_SOE`, `alpha` | CapSep zarfı, SOE Clopper–Pearson üst sınırı, MI realized FPR |
| $p_{soe}, p_{tim}, p_{conf}$ | `p_soe`, `p_tim`, `p_conf` | ölçülen (bilinmeyen) hata katkıları |

---

## 1. Model katmanı (Faz 0)

### 1.1 Gözlemlenebilir yüzey ve trace

SOE 4-tuple yüzeyi (adım (e) sonrası gerçek register genişlikleriyle):

$$
\mathrm{Obs} = \{\,(\mathrm{rip},\ \mathrm{exit\_reason},\ \mathrm{exit\_qual},\ \mathrm{rax})\,\}
\subseteq \mathbb{W}_{64}\times\mathbb{W}_{32}\times\mathbb{W}_{64}\times\mathbb{W}_{64}
$$

$$
\mathrm{Event} = \mathrm{Obs}\times\mathbb{N},\qquad
\mathrm{Trace} = \mathrm{Event}^{*},\qquad
\mathrm{aligned}(T_o,T_c) \iff |T_o| = |T_c|
$$

Timing $\tau_i\in\mathbb{N}$ kaldı — TSC wraparound bilinçli olarak kapsam dışı.

### 1.2 Divergence detection $D$ — iki clause

`soe_clause`:
$$
\mathrm{soe}(T_o,T_c,i) \iff o^{o}_i \neq o^{c}_i
$$

`timing_clause` (fark $\mathbb{Z}$'de alınır):
$$
\mathrm{tim}_{\Delta^{*}}(T_o,T_c,i) \iff \bigl|\,\tau^{c}_i - \tau^{o}_i\,\bigr| > \Delta^{*}
$$

`D` ve `diverges`:
$$
D_{\Delta^{*}}(T_o,T_c,i) \iff \mathrm{soe}(T_o,T_c,i)\ \lor\ \mathrm{tim}_{\Delta^{*}}(T_o,T_c,i)
$$

$$
\mathrm{diverges}_{\Delta^{*}}(T_o,T_c) \iff \exists\, i<|T_c|.\; D_{\Delta^{*}}(T_o,T_c,i)
$$

> [!note] Neden $\mathbb{Z}$?
> $\mathbb{N}$ üzerinde çıkarma truncating'dir ($3-5=0$). Mutlak fark $\mathbb{Z}$'ye cast
> edilerek **her iki yönde** doğru hesaplanır.

### 1.3 Intervention ve validity envelope

$$
\mathrm{scope} = \{\mathrm{PerEvent},\ \mathrm{PerWindow},\ \mathrm{Global}\},\qquad
\mathrm{iclass} = \{\mathrm{NopCount},\ \mathrm{RegWrite},\ \mathrm{InputValue},\ \mathrm{CachePreload}\}
$$

CST v1.0 kapsam predikatı (`cst_v1_covered`):

$$
\mathrm{covered}(\mathcal{E},\iota) \iff
\mathrm{scp}(\mathcal{E}) = \mathrm{PerEvent}
\ \land\ \mathrm{icls}(\iota)\in\mathrm{iclass}
\ \land\ S_{in}(\mathcal{E})\cap S_{out}(\mathcal{E}) = \varnothing
$$

`PerWindow` / `Global` tipte var ama `covered` tarafından **reddedilir** — v1.0'ın "yalnızca
per-event" kısıtı modele kodlanmıştır.

---

## 2. do-operatörünün anlambilimi (Pearl severance) — adım (a)

Guest durumu bir valuation $\sigma:\mathbb{N}\to\mathbb{N}$; $do(X=x')$ fonksiyonel güncelleme:

$$
\mathrm{apply}_\iota(\sigma) = \sigma[\,X \mapsto x'\,],\qquad
\mathrm{effective}(\iota) \iff \forall\sigma.\ \mathrm{apply}_\iota(\sigma)(X) = x'
$$

Pearl'ün "X'e giden tüm nedensel bağlantıları keser" ifadesi üç lemmaya ayrıldı:

| # | İfade | Pearl karşılığı | Fact |
|---|---|---|---|
| 1 | $\mathrm{apply}_\iota(\sigma)(X) = x'$ | effectiveness | `apply_iv_severs` |
| 2 | $y\neq X \implies \mathrm{apply}_\iota(\sigma)(y) = \sigma(y)$ | modularity çekirdeği | `apply_iv_local` |
| 3 | $\forall\sigma,\sigma'.\ \mathrm{apply}_\iota(\sigma)(X) = \mathrm{apply}_\iota(\sigma')(X)$ | **severance** | `apply_iv_indep_pre` |

$$
\vdash\ \forall\iota.\ \mathrm{effective}(\iota)\qquad\text{(effective\_holds)}
$$

(3) asıl severance: sonuç $X$'in **önceki** değerinden bağımsız $\Rightarrow$ $X$'e giden oklar kesik.

---

## 3. Dört-adımlı admissibility ve Teorem 1'in $\Leftarrow$ yönü

$$
\mathrm{adm}_{\Delta^{*}}(\mathcal{E},\iota,\mathsf{ok},T_o,T_c) \iff
\underbrace{\mathrm{covered}(\mathcal{E},\iota)}_{\text{adım 1}}
\ \land\ \underbrace{\mathsf{ok}}_{\text{adım 2: A1–A4 güncel}}
\ \land\ \underbrace{\mathrm{diverges}_{\Delta^{*}}(T_o,T_c)}_{\text{adım 3}}
\ \land\ \underbrace{X\in S_{in}(\mathcal{E})}_{\text{adım 4}}
$$

$$
\mathrm{emits} := \mathrm{adm},\qquad
\vdash\ \mathrm{emits} \iff \mathrm{adm}\qquad\text{(left\_direction)}
$$

> [!info] Bu yön trivial *olmalı*
> App A: bu yön deductive ispatla değil, **code-level inspection** ile kurulur. Modelde
> inşaat gereği doğru görünmesi doğru modellemenin işaretidir.

---

## 4. Sanity check'ler — `by eval` ile ispatlı

$T_{orig} = [\,e(10,1,0,5;\,1000),\ e(14,2,0,5;\,1050)\,]$, $\Delta^{*}=500$:

| Senaryo | Sonuç | Fact |
|---|---|---|
| $T_c = T_{orig}$ | $\neg\,\mathrm{diverges}$ | `sanity_no_divergence` |
| $\mathrm{rax}:5\to9$ @1 | $\mathrm{diverges}$ (SOE) | `sanity_soe_clause` |
| $\tau_0: 1000\to3000$ | $\mathrm{diverges}$ (timing, $2000>500$) | `sanity_timing_clause` |
| $\tau_0: 1000\to1400$ | $\neg\,\mathrm{diverges}$ ($400\le500$) | `sanity_below_threshold` |

Son satır $\Delta^{*}$'ın **gerçekten bağladığını** gösterir.

---

## 5. Faz 2 — Koşullu CST teoremi

### 5.1 Locale: A1–A4 hipotez, olasılıklar dışarıdan

Sabitler $\Delta^{*}\in\mathbb{N}$; $\delta_{A1},\varepsilon_{SOE},\alpha\in\mathbb{R}$;
predikatlar $A_1,\dots,A_4:\ \mathcal{E}\times\iota\to\mathbb{B}$;
katkılar $p_{soe},p_{tim},p_{conf}:\ \mathcal{E}\times\iota\to\mathbb{R}$;
$\mathrm{eff}:\mathcal{E}\to\mathcal{P}(\mathbb{N})$. Varsayımlar:

$$
\begin{aligned}
&0\le\delta_{A1},\ \varepsilon_{SOE},\ \alpha\le 1 \\
&A_4(\mathcal{E},\iota)\implies 0\le p_{soe}(\mathcal{E},\iota)\le\varepsilon_{SOE} \\
&A_3(\mathcal{E},\iota)\implies 0\le p_{tim}(\mathcal{E},\iota)\le\alpha \\
&A_1(\mathcal{E},\iota)\implies 0\le p_{conf}(\mathcal{E},\iota)\le\delta_{A1}+\alpha \\
&\mathrm{eff}(\mathcal{E})\subseteq S_{in}(\mathcal{E}) \\
&A_2(\mathcal{E},\iota)\land X\in S_{in}(\mathcal{E})\land \mathrm{effect}(\mathcal{E},\iota,T_o,T_c,i)\implies D_{\Delta^{*}}(T_o,T_c,i)
\end{aligned}
$$

(sırasıyla `prob_nonneg`/`prob_le_one`, `A4_bounds_soe`, `A3_bounds_tim`, `A1_bounds_conf`, `eff_subset`, `A2_manifests`)

> [!abstract] Isabelle bu sayıları üretmez
> $\delta_{A1},\varepsilon_{SOE},\alpha$ Clopper–Pearson / MI kalibrasyonundan girer;
> yalnızca $[0,1]$ aralığı ve union-bound aritmetiği ispatlanır.

Kalıntı epistemik zarf (`residual_nonneg`, `residual_le_three`):

$$
\mathrm{residual} := \varepsilon_{SOE}+\delta_{A1}+\alpha,\qquad
0\le\mathrm{residual}\le 3
$$

### 5.2 Üç bounding lemma (App A) — *coincidence elimine edilmez, sınırlanır*

$$
\begin{aligned}
A_4(\mathcal{E},\iota) &\implies p_{soe}(\mathcal{E},\iota)\le\varepsilon_{SOE} \\
A_3(\mathcal{E},\iota) &\implies p_{tim}(\mathcal{E},\iota)\le\alpha \\
A_1(\mathcal{E},\iota) &\implies p_{conf}(\mathcal{E},\iota)\le\delta_{A1}+\alpha
\end{aligned}
$$

| Lemma | App A | Kaynak property |
|---|---|---|
| `coincidence_soe_bound` | `lem:coincidence-soe` | [[Strong_Observational_Equivalence (2)\|SOE]] → $A_4$ |
| `coincidence_timing_bound` | `lem:coincidence-timing` | [[Measurement_Interference_v1 (1)\|MI]] → $A_3$ |
| `confounder_bound` | `lem:confounder` | [[Capability_Separation_Theorem\|CapSep]] → $A_1$ |

### 5.3 HP witness inşası — AC2(b), App A item (iv)

$$
W(\mathcal{E}) := S_{in}(\mathcal{E})\setminus\mathrm{eff}(\mathcal{E}),\qquad
\mathrm{mask}(\mathcal{E},\iota) := p_{soe}(\mathcal{E},\iota)+p_{conf}(\mathcal{E},\iota)
$$

$$
\vdash\ W(\mathcal{E})\subseteq S_{in}(\mathcal{E})\qquad\text{(witness\_W\_subset)}
$$

**W2 union bound** (`w2_residual_bound`) ve alt sınır (`mask_prob_nonneg`):

$$
A_1(\mathcal{E},\iota)\land A_4(\mathcal{E},\iota)\implies
0\ \le\ \mathrm{mask}(\mathcal{E},\iota)\ \le\ \varepsilon_{SOE}+\delta_{A1}+\alpha = \mathrm{residual}
$$

> [!tip] App A'nın union bound'unun tam mekanizasyonu
> "$D$'nin $do(x')$ yerine bir $W$-ihlalinden doğma olasılığı $\varepsilon_{SOE}+\delta_{A1}+\alpha_{realized}$ ile sınırlıdır."
> W1 (fixity enforceability) $A_4$ ile, W2 (fixity-does-not-mask) bu lemma ile discharge edilir.

### 5.4 Pearl/HP korespondans predikatları

$$
\begin{aligned}
\mathrm{comp}_\delta(\mathcal{E},\iota) &\iff p_{conf}(\mathcal{E},\iota)\le\delta_{A1}+\alpha \\
\mathrm{AC1}(T_o,T_c,i) &\iff D_{\Delta^{*}}(T_o,T_c,i) \\
\mathrm{AC2a}(T_o,T_c,i) &\iff D_{\Delta^{*}}(T_o,T_c,i) \\
\mathrm{AC2a}_w(T_o,T_c,i) &\iff \mathrm{witnesses}(w,\Delta^{*},T_o,T_c,i) \\
\mathrm{AC2b}(\mathcal{E},\iota) &\iff A_4(\mathcal{E},\iota)\land W(\mathcal{E})\subseteq S_{in}(\mathcal{E})\land\mathrm{mask}(\mathcal{E},\iota)\le\mathrm{residual}
\end{aligned}
$$

(`composition_relaxed`, `ac1`, `ac2a`, `ac2a_wit`, `ac2b`)

$$
A_1\implies\mathrm{comp}_\delta,\qquad
A_1\land A_4\implies\mathrm{AC2b},\qquad
\mathrm{AC2a}\iff\exists w.\,\mathrm{AC2a}_w
$$

(`composition_relaxed_holds`, `ac2b_holds`, `ac2a_iff_wit`)

> [!note] $\mathrm{AC1}=\mathrm{AC2a}=D$ neden aynı?
> Kasıtlı: App A dördüncü admissibility adımını "tam olarak AC2(a)'nın operasyonel testi"
> sayar ve AC1'i de aynı adıma bağlar. Ayrışma tanık düzeyinde yapılır (§6).

### 5.5 Ana teorem — Teorem 1'in $\Rightarrow$ yönü (`cst_conditional`)

> [!abstract] Teorem (koşullu CST)
> $A_1(\mathcal{E},\iota)\land A_2(\mathcal{E},\iota)\land A_3(\mathcal{E},\iota)\land A_4(\mathcal{E},\iota)$,
> $\mathrm{aligned}(T_o,T_c)$ ve $\mathrm{adm}_{\Delta^{*}}(\mathcal{E},\iota,\mathsf{ok},T_o,T_c)$ olsun. O zaman
> $$
> \begin{aligned}
> &\mathrm{effective}(\iota)\ \land\ \mathrm{comp}_\delta(\mathcal{E},\iota)\ \land\
> \exists\, i\,\exists\, w.\ \Bigl[\, i<|T_c|\ \land\ i<|T_o|\ \land\ D_{\Delta^{*}}(T_o,T_c,i) \\
> &\qquad \land\ \mathrm{AC1}(T_o,T_c,i)\ \land\ \mathrm{AC2a}(T_o,T_c,i)\ \land\ \mathrm{AC2a}_w(T_o,T_c,i)\ \land\ \mathrm{AC2b}(\mathcal{E},\iota) \\
> &\qquad \land\ \mathrm{wb}(w,\mathcal{E},\iota)\ \le\ \max\bigl(\varepsilon_{SOE}+\delta_{A1}+\alpha,\ \ \delta_{A1}+2\alpha\bigr)\,\Bigr]
> \end{aligned}
> $$

**İspat taslağı.** Adım 3'ten $\exists i<|T_c|.\,D$; `aligned_index_safe` ile $i<|T_o|$;
`D_iff_witness` ile bir tanık $w$; $w$ üzerinde case: yapısal ise `wit_bound_structural`
($A_1,A_4$), zamanlama ise `wit_bound_timing` ($A_1,A_3$). Kalanlar `effective_holds`,
`composition_relaxed_holds`, `ac2b_holds`. $\square$

Sonuç (`cst_residual_reported`):
$$
A_1\land A_4\implies 0\le\mathrm{mask}(\mathcal{E},\iota)\le\mathrm{residual}
$$

> [!success] Teorem güçlendi
> (1) $i<|T_o|$ — `aligned` gerçekten kullanılıyor; (2) somut **tanık $w$** dışarı veriliyor;
> (3) o tanığın **kendi zarfı** sınırlanıyor, blanket union bound değil.

---

## 6. AC2(a) tanıklarının ayrışması ve bağımsızlığı — adım (b)

$$
\mathcal{W} = \{\mathsf{S},\ \mathsf{T}\}\quad(\text{StructuralW, TimingW}),\qquad
\mathrm{witnesses}(w,\Delta^{*},T_o,T_c,i) \iff
\begin{cases}
\mathrm{soe}(T_o,T_c,i) & w=\mathsf{S}\\
\mathrm{tim}_{\Delta^{*}}(T_o,T_c,i) & w=\mathsf{T}
\end{cases}
$$

`D_iff_witness`:
$$
D_{\Delta^{*}}(T_o,T_c,i)\iff\exists w\in\mathcal{W}.\ \mathrm{witnesses}(w,\Delta^{*},T_o,T_c,i)
$$

`structural_witness_suffices`, `timing_witness_suffices`:
$$
\mathrm{soe}\implies D,\qquad \mathrm{tim}_{\Delta^{*}}\implies D
$$

**Mantıksal bağımsızlık** (`witnesses_logically_independent`) — iki somut karşı-örnekle:

$$
\begin{aligned}
&\exists T_o,T_c,i,\Delta^{*}.\ \mathrm{witnesses}(\mathsf{S},\ldots)\land\neg\,\mathrm{witnesses}(\mathsf{T},\ldots) \\
\land\ &\exists T_o,T_c,i,\Delta^{*}.\ \mathrm{witnesses}(\mathsf{T},\ldots)\land\neg\,\mathrm{witnesses}(\mathsf{S},\ldots)
\end{aligned}
$$

| Tanık | Karşı-örnek | Fact |
|---|---|---|
| yalnız $\mathsf{S}$ | $\mathrm{rax}:5\to9$ @1, timing aynı | `witness_indep_structural` |
| yalnız $\mathsf{T}$ | $\tau_0:1000\to3000$, 4-tuple aynı | `witness_indep_timing` |

`aligned` artık iş yapıyor (`aligned_index_safe`, `no_divergence_obs_eq` = $A_4$'ün operasyonel ifadesi):

$$
\mathrm{aligned}(T_o,T_c)\land i<|T_c|\implies i<|T_o|
$$

$$
\mathrm{aligned}(T_o,T_c)\land\neg\,\mathrm{diverges}_{\Delta^{*}}(T_o,T_c)\implies
\forall i<|T_c|.\ o^{o}_i=o^{c}_i\ \land\ i<|T_o|
$$

---

## 7. ⭐ Tanık-başına hata zarfı — yeni analitik sonuç

Blanket $\mathrm{residual}$ yerine tanık-başına zarf (`wit_bound`, kısaca $\mathrm{wb}$):

$$
\mathrm{wb}(w,\mathcal{E},\iota) =
\begin{cases}
p_{soe}(\mathcal{E},\iota)+p_{conf}(\mathcal{E},\iota) & w=\mathsf{S}\\
p_{tim}(\mathcal{E},\iota)+p_{conf}(\mathcal{E},\iota) & w=\mathsf{T}
\end{cases}
$$

`wit_bound_structural`, `wit_bound_timing`:
$$
\begin{aligned}
A_1\land A_4 &\implies \mathrm{wb}(\mathsf{S},\mathcal{E},\iota)\le\varepsilon_{SOE}+\delta_{A1}+\alpha \\
A_1\land A_3 &\implies \mathrm{wb}(\mathsf{T},\mathcal{E},\iota)\le\delta_{A1}+2\alpha
\end{aligned}
$$

**Ana sonuç** (`structural_bound_tighter_iff`) — karşılaştırma tek eşitsizliğe iner:

$$
\boxed{\ \varepsilon_{SOE}+\delta_{A1}+\alpha\ \le\ \delta_{A1}+2\alpha\quad\iff\quad\varepsilon_{SOE}\le\alpha\ }
$$

> [!success] Yorum
> Yapısal tanık daha sıkı zarf verir **ancak ve ancak** $\varepsilon_{SOE}\le\alpha_{realized}$.
> Kriter framework'ün değil, **kalibrasyon rejiminin** kararıdır — ve paper'ın iki rejimi
> eşitsizliğin zıt taraflarında.

### Paper'ın gerçek sayılarıyla instantiation

| Rejim | $\varepsilon_{SOE}$ | $\delta_{A1}$ | $\alpha$ | $\varepsilon_{SOE}\le\alpha$ | Yapısal zarf | Zamanlama zarfı | Daha sıkı |
|---|---|---|---|---|---|---|---|
| Within-boot ($N=998$) | $0.37\%$ | $0.37\%$ | $0.61\%$ | ✅ | $\mathbf{1.35\%}$ | $1.59\%$ | yapısal |
| Cross-boot ($N=34$) | $10.4\%$ | $10.4\%$ | $0.61\%$ | ❌ | $21.41\%$ | $\mathbf{11.62\%}$ | zamanlama |

`withinboot_criterion`, `withinboot_structural_tighter`:
$$
\tfrac{37}{10000}\le\tfrac{61}{10000},\qquad
\tfrac{37+37+61}{10000}\le\tfrac{37+2\cdot61}{10000}
$$

`crossboot_criterion`, `crossboot_timing_tighter`:
$$
\neg\Bigl(\tfrac{1040}{10000}\le\tfrac{61}{10000}\Bigr),\qquad
\tfrac{1040+2\cdot61}{10000}\le\tfrac{1040+1040+61}{10000}
$$

---

## 8. ⭐ `lem:silent` ve $A_2$'nin gerçek rolü — adım (d)

Kilit hamle: yer altındaki nedensel etki $\mathrm{effect}(\mathcal{E},\iota,T_o,T_c,i)$,
$D$'den **ayrı** bir locale parametresi. $A_2$'nin içeriği (`A2_manifests`):

$$
A_2(\mathcal{E},\iota)\ \land\ X\in S_{in}(\mathcal{E})\ \land\ \mathrm{effect}(\mathcal{E},\iota,T_o,T_c,i)
\ \implies\ D_{\Delta^{*}}(T_o,T_c,i)
$$

$X\in S_{in}$ guard'ı şart — $A_2$, $S_{out}$ hakkında hiçbir şey söylemez.

### İki yön

(i) Soundness — $A_2$ gerekmez (`emits_implies_divergence`):
$$
\mathrm{emits}\implies\mathrm{diverges}_{\Delta^{*}}(T_o,T_c)
$$

(ii) Scope-completeness — $A_2$ gerekli (`silent_no_missed_effect`):
$$
A_2\land X\in S_{in}\land\mathrm{effect}(\cdot,i)\land i<|T_c|\implies\mathrm{diverges}_{\Delta^{*}}(T_o,T_c)
$$

> [!abstract] Teorem (kapsam-tamlığı, `cst_scope_complete`)
> $A_2(\mathcal{E},\iota)$, $\mathrm{covered}(\mathcal{E},\iota)$, $X\in S_{in}(\mathcal{E})$, $\mathsf{ok}$,
> $\mathrm{effect}(\mathcal{E},\iota,T_o,T_c,i)$, $i<|T_c|$ olsun. O zaman
> $$
> \mathrm{emits}_{\Delta^{*}}(\mathcal{E},\iota,\mathsf{ok},T_o,T_c)\ \land\ \exists j<|T_c|.\ D_{\Delta^{*}}(T_o,T_c,j)
> $$

Kontrapozitif (`silence_informative_over_s_in`):

$$
A_2\land X\in S_{in}\land\neg\,\mathrm{diverges}_{\Delta^{*}}(T_o,T_c)\land i<|T_c|\implies\neg\,\mathrm{effect}(\mathcal{E},\iota,T_o,T_c,i)
$$

| Yön | Teorem | Kullanır |
|---|---|---|
| Soundness — yayınlanan claim sağlam | `cst_conditional` | $A_1,A_3,A_4$ |
| Scope-completeness — $S_{in}$'deki etki kaçmaz | `cst_scope_complete` | $A_2$ |

### $A_2$ tautoloji değil

$T_{silent}=[\,e(10,1,0,5;\,1400),\ e(14,2,0,5;\,1050)\,]$, $\Delta^{*}=500$:

`silent_effect_exists`:
$$
\tau^{silent}_0\neq\tau^{orig}_0\ \land\ \neg\,\mathrm{diverges}_{500}(T_{orig},T_{silent})
$$

`silent_effect_invisible_on_both_clauses`:
$$
\neg\,\mathrm{soe}(T_{orig},T_{silent},0)\ \land\ \neg\,\mathrm{tim}_{500}(T_{orig},T_{silent},0)
$$

Gerçek 400-cycle fark var, $D$ sessiz. Böyle bir fark $S_{in}$ içinde nedensel etki olsaydı
$A_2$ ihlal edilirdi $\Rightarrow$ $A_2$ dünya hakkında bir şey söylüyor, yanlışlanabilir.

---

## 9. ⭐ Paralel sweep: tanık-duyarlı ensemble zarfı — adım (f)

> [!warning] Eksen ayrımı
> §12'deki $\mathrm{accum}$ **sıralı** kompozisyon ($\delta_{A1}$ birikimi). Bu bölüm **paralel**
> sweep: $n$ bağımsız atomik claim, $\delta_{A1}$ per-claim, birikim yok.

$$
\mathrm{ub}(w) =
\begin{cases}
\varepsilon_{SOE}+\delta_{A1}+\alpha & w=\mathsf{S}\\
\delta_{A1}+2\alpha & w=\mathsf{T}
\end{cases},\qquad
\mathrm{blanket}=\max(\varepsilon_{SOE}+\delta_{A1}+\alpha,\ \delta_{A1}+2\alpha)
$$

$$
\mathrm{sweep\_ub}(w_1,\dots,w_n)=\sum_{j=1}^{n}\mathrm{ub}(w_j)
$$

`wit_ub_nonneg`, `wit_ub_le_blanket`:
$$
0\le\mathrm{ub}(w)\le\mathrm{blanket}
$$

**Kapalı form** (`sweep_ub_closed_form`), $k=\#\mathsf{S}$, $n-k=\#\mathsf{T}$:

$$
\mathrm{sweep\_ub}(\vec w)=k\,(\varepsilon_{SOE}+\delta_{A1}+\alpha)+(n-k)\,(\delta_{A1}+2\alpha)
$$

**Ana sonuç** (`sweep_ub_tighter`):

$$
\mathrm{sweep\_ub}(\vec w)\ \le\ n\cdot\mathrm{blanket}
$$

Ölçülen ensemble hatası $\mathrm{sweep\_actual}(\mathcal{E},\iota,\vec w)=\sum_j\mathrm{wb}(w_j,\mathcal{E},\iota)$ ile **üç kademeli sınır** (`sweep_three_level_bound`):

$$
A_1\land A_3\land A_4\implies
\mathrm{sweep\_actual}(\mathcal{E},\iota,\vec w)\ \le\ \mathrm{sweep\_ub}(\vec w)\ \le\ n\cdot\mathrm{blanket}
$$

> [!success] Kesin daha sıkı — within-boot, 2 claim $[\mathsf{S},\mathsf{T}]$
> $$
> \mathrm{sweep\_ub}[\mathsf{S},\mathsf{T}]=\tfrac{294}{10000}=2.94\%\ <\ 2\cdot\mathrm{blanket}=\tfrac{318}{10000}=3.18\%
> $$
> (`withinboot_sweep_strictly_tighter`); homojen $[\mathsf{T},\mathsf{T}]$ için **eşitlik**
> (`withinboot_homogeneous_equality`). Kazanç tam olarak tanık karışımından gelir.

---

## 10. ⭐ Gerçek sweep verisine bağlama — adım (h)

Gerçek veri (`sec:eval-demo-sweep`): 33 input, divergence $1/33$ — yalnızca `0xDEAD` (SOE, RIP `0x10016`).

$$
\mathrm{emitted}(xs)=[\,w\mid \mathrm{Some}\,w\in xs\,],\qquad
\mathrm{dead\_sweep}=\mathrm{Some}\,\mathsf{S}\ \#\ \mathrm{None}^{32}
$$

$$
|\mathrm{dead\_sweep}|=33,\qquad \mathrm{emitted}(\mathrm{dead\_sweep})=[\mathsf{S}],\qquad |\mathrm{emitted}(\cdot)|=1
$$

Ensemble zarfı gerçek kalibrasyonla (`dead_sweep_envelope_withinboot`, `_crossboot`):

$$
\mathrm{sweep\_ub}^{wb}(\mathrm{emitted}(\mathrm{dead\_sweep}))=\tfrac{135}{10000}=1.35\%,\qquad
\mathrm{sweep\_ub}^{cb}(\cdot)=\tfrac{2141}{10000}=21.41\%
$$

Sessiz input'lar zarfa girmez (`silent_inputs_free`):

$$
\mathrm{sweep\_ub}(\mathrm{emitted}(\mathrm{None}\#xs))=\mathrm{sweep\_ub}(\mathrm{emitted}(xs))
$$

Ensemble sınırı (`ensemble_envelope_bound`) ve naïve karşılaştırma (`dead_sweep_envelope_vs_naive_swept`):

$$
\mathrm{sweep\_ub}(\mathrm{emitted}(xs))\le|\mathrm{emitted}(xs)|\cdot\mathrm{blanket},\qquad
\underbrace{1.35\%}_{\text{gerçek}}\ <\ \underbrace{33\cdot\mathrm{blanket}^{wb}=52.47\%}_{\text{naïve}}
$$

> [!success] Scope-honesty × ensemble
> Zarf **taranan input sayısıyla değil, admissible claim sayısıyla** ölçeklenir:
> 32 sessiz input **bedava**, $\sim39\times$ daha sıkı.

---

## 11. ⭐ Silent-leak sınıfı = kanıtlanmış scope sınırı — adım (i)

$$
\mathrm{silent\_leak}(T_o,T_c,i)\iff\neg\,\mathrm{soe}(T_o,T_c,i)\land\neg\,\mathrm{tim}_{\Delta^{*}}(T_o,T_c,i)
\quad\Bigl(\iff\neg D_{\Delta^{*}}(T_o,T_c,i)\Bigr)
$$

(i.1) `A2_forbids_inscope_silent_leak`:
$$
A_2\land X\in S_{in}\land\mathrm{effect}(\cdot,i)\land\mathrm{silent\_leak}(T_o,T_c,i)\implies\bot
$$

> [!abstract] Teorem (`silent_leak_only_out_of_scope`)
> $$
> A_2(\mathcal{E},\iota)\ \land\ \mathrm{effect}(\mathcal{E},\iota,T_o,T_c,i)\ \land\ \mathrm{silent\_leak}(T_o,T_c,i)
> \ \implies\ X\notin S_{in}(\mathcal{E})
> $$

Kontrapozitif (`inscope_effect_is_observable`):

$$
A_2\land X\in S_{in}\land\mathrm{effect}(\cdot,i)\implies\mathrm{soe}(T_o,T_c,i)\lor\mathrm{tim}_{\Delta^{*}}(T_o,T_c,i)
$$

Somut (gerçek $\Delta^{*}=9077$): $400<9077\Rightarrow\mathrm{silent\_leak}^{wb}(T_{orig},T_{silent},0)$
(`ex_silent_is_silent_leak_withinboot`).

> [!success] Stratejik çıkar
> CMD'ye erteleme keyfî değil — $A_2$ altında sessiz sızıntının $S_{out}$'ta olması **zorunlu**.

---

## 12. Proposition 1 — sıralı kompozisyon

`chain_iff_all_atomic`:
$$
\mathrm{all}(\mathit{steps})\iff\forall k<|\mathit{steps}|.\ \mathit{steps}_k
$$

$$
\mathrm{accum}(0)=0,\qquad\mathrm{accum}(n+1)=\mathrm{accum}(n)+\delta_{A1}
$$

`accum_delta_eq`, `accum_delta_mono`, `accum_delta_linear_bound`:
$$
\mathrm{accum}(n)=n\,\delta_{A1},\qquad
\mathrm{accum}(n)\le\mathrm{accum}(n+1),\qquad
\mathrm{accum}(n)\le n\,\delta_{A1}
$$

App A: union bound ile $O(n)$ birikim; bağımsızlık altında daha sıkı sınır **iddia edilmiyor**.

---

## 13. Locale tutarlılığı — "vacuously true" değil

Üç `interpretation` locale'in **tutarlı** olduğunu (assumption'ların çelişmediğini) gösterir:

| Interpretation | $\Delta^{*}$ | $\delta_{A1}$ | $\varepsilon_{SOE}$ | $\alpha$ | $A_i$ | $p_\ast$ |
|---|---|---|---|---|---|---|
| `cst_trivial` | 500 | $1/10$ | $1/10$ | $1/20$ | $\top$ | $0$ |
| `cst_withinboot` | 9077 | $37/10000$ | $37/10000$ | $61/10000$ | $\top$ | $0$ |
| `cst_crossboot` | 9077 | $1040/10000$ | $1040/10000$ | $61/10000$ | $\top$ | $0$ |

> [!important] Neden şart
> Çelişkili assumption $\Rightarrow$ her teorem *ex falso* doğru olurdu. Somut model bunu dışlar.
> Not: $p_\ast=0$ alındığı için tablodaki zarflar **worst-case üst sınırlar**, ölçülen değerler değil.

---

## 14. seL4 lifting arayüzü — adım (g), açık KAPATILMADI

$$
\mathrm{kop}=\underbrace{\{\mathrm{Create},\mathrm{Copy},\mathrm{Revoke},\mathrm{Destroy}\}}_{K_{verified}}
\ \uplus\ \underbrace{\{\mathrm{MapEPT},\mathrm{Unmap},\mathrm{ReadVMCS},\mathrm{WriteVMCS}\}}_{K_{extended}}
$$

`k_partition_disjoint`, `k_partition_complete`:
$$
K_{verified}\cap K_{extended}=\varnothing,\qquad K_{verified}\cup K_{extended}=\mathrm{kop}
$$

Locale `sel4_lifting`: $\mathrm{auth}:\mathrm{kop}\to\mathcal{P}(\mathbb{N})$, $F\subseteq\mathbb{N}$ (framework değişkenleri), **tek assumption** (`verified_no_fwk_touch` — L4.verified'in sağladığı; **ispatlanmaz**):

$$
\forall op\in K_{verified}.\ \mathrm{auth}(op)\cap F=\varnothing
$$

`A1_unconditional_for_verified` (assumption altında $\delta=0$):
$$
op\in K_{verified}\implies\mathrm{auth}(op)\cap F=\varnothing
$$

`extended_can_touch_fwk` (ampirik kalır):
$$
\exists\,\mathrm{auth}.\ \exists op\in K_{extended}.\ \mathrm{auth}(op)\cap F\neq\varnothing
$$

> [!danger] Bu lifting'i kapatmaz
> Yükümlülük tek isimli assumption'a indirgendi ve altından çıkanlar ispatlandı. Assumption'ı
> L4.verified'in gerçek atomicity teoreminden türetmek **çok-yıllık**, kapsam dışı.
> Koşullu CST (§5) bunun hiçbirine ihtiyaç duymaz.

---

## 15. Ne ispatlanmadı — dürüstlük

1. **Ampirik antecedent'ler** ($\mathrm{score}_S=1.0000$, Clopper–Pearson $\le0.37\%$ / $\le10.4\%$, $\alpha_{realized}\in[0.61\%,\,2.78\%]$) ölçümdür; Isabelle yalnızca $[0,1]$ ve union-bound aritmetiğini ispatlar.
2. **Lifting yapılmadı**; $A_1$, $K_{verified}$ için bile L4.verified'den discharge edilmiş değil.
3. **Multi-VCPU race'ler, sessiz mikromimari kanallar** kapsam dışı.
4. $p_{soe},p_{tim},p_{conf}$ interpretation'larda $0$ — zarflar üst sınır, ölçüm değil.
5. **Timing wraparound** (TSC 64-bit) kapsam dışı; $\tau\in\mathbb{N}$.

---

## 16. Fact envanteri (94, `sorry` yok) — özet

| Grup | Sayı | Öne çıkan |
|---|---|---|
| Faz 0–2 çekirdek | 27 (+1 interp.) | `cst_conditional`, `w2_residual_bound`, `left_direction` |
| (b) tanık ayrımı | 19 | `structural_bound_tighter_iff`, `witnesses_logically_independent` |
| (d) $A_2$ / scope | 8 | `cst_scope_complete`, `silent_effect_exists` |
| (f) paralel sweep | 14 | `sweep_three_level_bound`, `withinboot_sweep_strictly_tighter` |
| (h) gerçek veri | 14 | `dead_sweep_envelope_withinboot`, `dead_sweep_envelope_vs_naive_swept` |
| (i) silent-leak | 5 | `silent_leak_only_out_of_scope` |
| (g) lifting arayüzü | 7 | `A1_unconditional_for_verified` |

Tam envanter ve Isabelle kaynak kodu: [[Isabelle_Mechanization_CST]] §8.
