# Strong Observational Equivalence

> **Cross-reference convention.** This entry was originally drafted
> as Chapter 5 of an integrated paper; references to other paper
> sections were preserved when the entry was extracted to vault
> format. The mapping from paper-section refs to vault entries is:
> - "Section 4.1" / "Capability Separation Theorem'inde Section X" →
>   `Capability_Separation_Theorem.md`
> - "Section 6.3" → `Measurement_Interference.md`
> - "Section 6" / "Section 6.4" → empirical methodology of this entry
>   itself (within-boot N=998 in §4.1; cross-boot N=3400 in §4.2) and
>   `Counterfactual_Soundness_Theorem.md` (CST property)
>
> Internal §X.Y references (within this entry) target this entry's
> own sections. The §5–§7 sections (Concession Footnote, Implications,
> Files) are vault-format additions; they do **not** correspond to the
> original paper's chapter structure.

# 1. Notation and Preliminaries

## 1.1 The Observable Surface

Capability Separation Theorem'inde *observable*(·) fonksiyonunu formal
tanımı olmadan kullandık (`Capability_Separation_Theorem.md` §4.1
definitional dependence notu). Burada formalize ediyoruz.

> **Definition (Observable Surface).** Bir execution *X* için:
>
> *observable*(*X*) = ⟨τ(*X*), exit_reason(*X*), exit_qual(*X*), rax(*X*)⟩
>
> dört bileşenli sıralı tuple. Bileşenler:
>
> - *τ*(*X*) — VM exit event sequence (Section 1.2'deki *τ* notasyonu)
> - *exit_reason*(*X*) — her event için VMX exit reason kodu (CPUID,
>   VMCALL, EPT_VIOLATION, vb.)
> - *exit_qual*(*X*) — her event için exit qualification field
>   (event-specific semantic, örn. EPT violation için fault address)
> - *rax*(*X*) — her event sınırında guest RAX register değeri

Bu tanım **kasıtlı olarak dar**. Genişletilebilecek dimension'lar:

- **Geniş register set** — RCX, RDX, RBX, R8, R9, R10 vb. EXTp
  implementation'ında event struct bu field'ları capture eder,
  ancak observable surface'in bu paper'daki resmi tanımı RAX ile
  sınırlıdır. **Explicit scope-limitation:** RAX-dışı register
  divergence (örn. RDX'in System V ABI syscall arg'larında veya
  RBX/RCX'in exception handler state'inde manipüle edildiği
  exploit'ler) **bu surface'ta sessizdir** — score_S = 1.0000 sadece
  RAX agreement'i gösterir, RBX/RCX/RDX agreement'i kanıtlamaz.
  Bu MI'nın "silent leak scope-out"'una (timing-dışı
  microarchitectural state) yapı olarak benzer: SOE detects RAX
  divergence; non-RAX register divergence is silent on the SOE
  surface, not asserting its absence. Genişletme bir
  implementation tercihi olarak ileri çalışmaya bırakılır.
- **Memory state** — guest fiziksel memory snapshot. Pratik olarak
  ölçülmez (boyut, performans), bu paper kapsamında dışlandı.
- **Timing** — event'ler arası TSC delta. `Measurement_Interference.md`'de
  ayrı olarak ele alınır; observable surface'in parçası **değil** çünkü
  microarchitectural noise dahil eder.
- **Microarchitectural side-channels** — cache state, branch predictor
  state. Bu paper'ın kapsamı dışında.

Observable surface'in dar tanımlanması iki yarar sağlar:
**(1) measurability** — surface ölçülebilir field'lardan oluşuyor;
**(2) falsifiability** — surface üzerinde mismatch kategorik olarak
detect edilebilir (Section 3'teki four-field injection test bunu
gösterir).

### Why These Four Fields

Dahil edilen dört field convenience seçimi değil, her biri unique bir
exploit-relevant signal yakalar:

- *τ*(*X*) — guest control flow'un VMX exit sınırlarındaki **temporal
  yapısı**. Event sequence eşleşmiyorsa execution farklı code path'ler
  izliyor demektir.
- *exit_reason*(*X*) — her exit'in **hypercall taxonomy**'sini
  belirler (CPUID vs VMCALL vs EPT_VIOLATION vb.). Aynı RIP'te farklı
  exit_reason, farklı hypervisor handler'ının invoke edildiğini
  gösterir.
- *exit_qual*(*X*) — exit-specific **semantic payload**. EPT
  violation için fault address, IO instruction için port number, vb.
  Exploit'in ürettiği specific failure context buradadır.
- *rax*(*X*) — x86-64 ISA convention gereği hypercall ve syscall
  **return value / output register**'ı. Guest'in hypercall'dan ne
  aldığını veya CPUID gibi instruction'lardan ne extract ettiğini
  yakalar.

Üçünden herhangi birini dışlamak specific bir exploit-relevant
signal'i kaybeder: exit_reason'sız hypercall taxonomy belirsiz;
exit_qual'sız fault context kayıp; rax'sız return value semantic'i
kayıp. Dört field birlikte minimal sufficient surface'i oluşturur
**bu paper'ın counterfactual analysis kapsamında**.

### Trace Alignment

Section 2'deki equivalence relation'ları |τ(*X*)| = |τ(*Y*)| şartını
varsayar — eşleşme öncesi event count'larının eşit olması. Bu şart
EXTp'nin bu paper'ın deneylerinde aşağıdaki nedenlerle empirical olarak
sağlanmıştır:

- EXTp'nin deneysel guest workload'u (`guest_code`, 7 byte: CPUID +
  VMCALL) deterministic olarak iki VM exit üretir
- EXTp'nin VMM'i single-threaded execution modelinde çalışır;
  asenkron interrupt veya scheduler preemption bu deneylerde
  tetiklenmez
- Measurement instrumentation (TSC reads, log writes) VM exit
  üretmez — guest mode'da kalır

Bu tasarımsal çevrede |τ(*E*)| = |τ(*R*)| empirical olarak her
replay'de sağlanır (Section 6). Daha kompleks workload'larda (multi-
instruction guest code, asenkron event'li guest'ler) trace alignment
ek normalization gerektirebilir — bu paper'ın kapsamı dışı, ileri
çalışmaya bırakılır.

## 1.2 Symbol Conventions

`Capability_Separation_Theorem.md` §1.2'de kurulan notation
korunur (E, R, t, t.caps, τ, τ.events[i], caps(X), replay(X),
K_verified, K_extended). SOE'ye özel ek notation:

| Symbol | Meaning |
|--------|---------|
| *observable(X)* | Execution X'in observable surface'i (Section 1.1) |
| *τ.events[i].rip* | i'inci event'in instruction pointer'ı |
| *τ.events[i].exit_reason* | i'inci event'in VMX exit reason'u |
| *τ.events[i].exit_qual* | i'inci event'in exit qualification field'ı |
| *τ.events[i].rax* | i'inci event sınırındaki guest RAX değeri |
| *X ≈_W Y* | X ve Y arasında **weak observational equivalence** (Section 2.1) |
| *X ≈_S Y* | X ve Y arasında **strong observational equivalence** (Section 2.2) |
| *score_W(E, R)* | Empirical weak equivalence ratio: matched events / total events, where an event is **matched** iff its (rip, exit_reason) pair equals the corresponding event's |
| *score_S(E, R)* | Empirical strong equivalence ratio: matched events / total events, where an event is **matched** iff all four observable fields (rip, exit_reason, exit_qual, rax) equal the corresponding event's |

Notation seçimleri:
- *≈_W* ve *≈_S* binary equivalence relation'lar — categorical: ya
  hold ya etmez. Her event eşleşmek zorunda.
- *score_W* ve *score_S* numerical ratios [0, 1] — graduated
  measurement: kısmi eşleşmeyi quantify eder. Empirical observation
  için kullanılır, formal property için değil.
- Equivalence (≈) ile score arasındaki distinction kritik: Section 2
  formal tanımları verir, Section 3-4 empirical measurement'ı sağlar.
  Bunların aynı şey olmaması paper'ın methodological omurgasının
  parçası.

## 1.3 What "Observational Equivalence" Means in this Paper

"Observational equivalence" terimi process algebra ve concurrency
literatüründe yerleşik bir kavram (bkz. Milner, CCS bisimulation;
Hoare, CSP). Genel formu şu: iki sistem davranışı, bir external
observer'ın ayırt edemediği ölçüde eşdeğerdir.

Bu paper'da kullandığımız "observational equivalence" bu literatür
geleneğine **structural olarak** akrabadır ama **semantik olarak
daralır**. Üç fark:

1. **Observer fixed.** Klasik bisimulation'da observer "any context"
   altında ayırt edilemezlik aranır. Burada observer EXTp'nin replay
   harness'ı — sabit, observable surface'i Section 1.1'de tanımlı.

2. **Surface bounded.** Klasik observational equivalence sonsuz
   trace'leri ve infinite branching'i kapsar. Buradaki tanım finite
   trace'ler üzerinde, bounded register subset üzerinde çalışır.

3. **Two-level hierarchy.** Klasik formalismler tek bir equivalence
   relation tanımlar. Burada kasıtlı olarak iki seviye veriyoruz
   (weak ≈_W, strong ≈_S) çünkü EXTp'nin operasyonel context'i bu
   ayrımı **zorunlu kılar**: divergence detection ve full state
   verification farklı methodolojik amaçlara hizmet eder.

Bu farkları flag'liyoruz çünkü reviewer "klasik observational
equivalence'tan ne kadar uzaktasınız?" diye soracak. Cevap: structural
olarak akraba, semantic olarak bu paper'ın spesifik measurement
context'ine adapte edilmiş.

**Capability scope uniformity.** SOE bir measurement-level property'dir;
tanımı capability authority'nin verified scope'unda (K_verified) veya
extended scope'unda (K_extended) çalışması arasında ayrım yapmaz.
Observable surface (Section 1.1) capability invocation'ının sonuçlarını
yakalar, invocation'ın hangi verification scope'unda olduğunu değil.
Empirical observation (Section 4) her iki set'ten operasyon invoke
eden execution'ları kapsar — yani score_S = 1.0000 bulgusu Capability
Separation'ın hibrit zemininin SOE measurement'ında uniform geçerli
olduğunu gösterir.

Section 1.3'ün asıl iddiası şu: observational equivalence burada bir
**measurement framework** olarak kullanılır, klasik anlamda bir
**behavioral semantic equivalence** olarak değil. Bu fark Section 2'de
formal tanımlarda kendini gösterir — equivalence relation'lar event
sequence üzerinde **point-wise** karşılaştırma yapar, bisimulation
gibi co-inductive relation kurmaz.

---

# 2. The Two-Level Equivalence Definition

Section 1'de observable surface'i ve "observational equivalence"
teriminin bu paper'daki kapsamını kurduk. Şimdi iki formal equivalence
relation tanımlıyoruz. İkisi de point-wise comparison yapar, ancak
**farklı surface subset'leri** üzerinde çalışır.

## 2.1 Weak Observational Equivalence

> **Definition (Weak Observational Equivalence).** İki execution *X*
> ve *Y* için:
>
> *X* ≈_W *Y*  iff  |τ(*X*)| = |τ(*Y*)|  ∧
>                   ∀i ∈ [0, |τ(*X*)|) :
>                       τ(*X*).events[i].rip = τ(*Y*).events[i].rip ∧
>                       τ(*X*).events[i].exit_reason = τ(*Y*).events[i].exit_reason
>
> Yani: aynı sayıda event, ve her event için (rip, exit_reason) çifti
> eşit.

WOE observable surface'in **iki bileşenini** kullanır: event sequence
yapısı ve her event'in exit type'ı. Bu seviye iki şeyi yakalar:

1. **Control-flow equivalence.** Aynı RIP'lerde aynı exit type'lar
   üretiliyorsa, guest control-flow path'i aynı yerden geçiyor demektir.
2. **Sequence preservation.** Event sayısı ve sırası eşleşiyorsa,
   execution'ın temporal yapısı korunmuş demektir.

WOE **kategorik** bir relation: ya tüm event'ler eşleşir (≈_W TRUE),
ya da en az bir event'te ayrışma vardır (≈_W FALSE). Section 3'te
empirical measurement'a (score_W) geçildiğinde graduated form
kazanılır, ancak relation ile score arasında information loss yoktur:
≈_W TRUE iff score_W = 1.0 — yani relation, score'un boundary case'i.
Score graduation kısmi divergence'ı quantify eder, kategorik bilgiyi
yok etmez.

WOE'nin **yetersiz** olduğu yer: register state. İki execution aynı
RIP'de aynı exit_reason üretebilir, ama farklı RAX değerleriyle.
Örneğin CPUID exit'inde EAX'a yüklenen leaf değeri farklıysa, control
flow aynı görünür ama semantic state farklıdır. Bu boşluğu kapatmak
için Strong Observational Equivalence gerekir.

## 2.2 Strong Observational Equivalence

> **Definition (Strong Observational Equivalence).** İki execution
> *X* ve *Y* için:
>
> *X* ≈_S *Y*  iff  *X* ≈_W *Y*  ∧
>                   ∀i ∈ [0, |τ(*X*)|) :
>                       τ(*X*).events[i].exit_qual = τ(*Y*).events[i].exit_qual ∧
>                       τ(*X*).events[i].rax = τ(*Y*).events[i].rax
>
> Yani: WOE'ye ek olarak, her event için (exit_qual, rax) çifti de
> eşit.

SOE observable surface'in **dört bileşenini de** kullanır — Section
1.1'in tam tanımına eşdeğer:

> *X* ≈_S *Y*  ⟺  *observable*(*X*) = *observable*(*Y*)

Bu eşdeğerlik tanımsal: SOE, observable surface üzerinde tam eşitliğin
relation formundaki ifadesidir. SOE WOE'den **daha güçlü** bir
property:

> **Hierarchy.** ∀ X, Y: (X ≈_S Y) ⟹ (X ≈_W Y)
>
> *Proof.* By Definition 2.2, SOE conjuncts include all WOE conjuncts
> plus exit_qual and rax equality; therefore SOE TRUE forces WOE TRUE.
> ∎

Tersi geçerli değil: WOE sağlanır ama SOE sağlanmazsa, control-flow
ve event sequence aynıdır ama event-level semantic state (qual, rax)
ayrışır.

## 2.3 The Hierarchy: Why Two Levels?

Tek bir equivalence yerine iki seviye tanımlamamızın iki nedeni var:

**Methodological:** Replay framework'ü iki ayrı soruya cevap verir:
- "Replay execution exploit'in ürettiği aynı code path'i izledi mi?"
  → WOE
- "Replay execution exploit'in ürettiği aynı semantic state'e ulaştı
  mı?" → SOE

İki soru farklı kullanım context'lerine hizmet eder. Forensic analysis
WOE yeterli olabilir (hangi code path tetiklendi); counterfactual
verification SOE gerektirir (state'in tam olarak yeniden üretilmesi).

**Empirical:** WOE ve SOE farklı failure mode'larına karşı duyarlıdır.
WOE control-flow divergence'ı yakalar; SOE semantic divergence'ı.
İkisinin **ayrı ayrı raporlanması** measurement methodology'sinin
ayrıştırılabilirlik gücünü artırır — Section 3'teki four-field
injection test bu ayrımı empirically gösterir.

İki seviyeyi tek bir relation'a indirgemek (sadece SOE kullanmak)
mümkün ama information loss üretir: SOE FALSE bir sonuçta divergence'ın
control-flow düzeyinde mi yoksa state düzeyinde mi olduğu kaybolur.
WOE/SOE distinction bu bilgiyi korur.

---

# 3. Empirical Validation Methodology

Section 2'de WOE ve SOE'yi formal relation'lar olarak tanımladık. Bu
tanımlar **kategorik** — ya hold ya etmez. Pratikte EXTp birden fazla
replay run'ında **graduated measurement** üretir: matches/total
oranları (score_W ve score_S). Bu section şu üç soruyu ele alır:

1. Numerical score'lar (≈) relation'larıyla nasıl ilişkilenir?
2. Score'lar gerçekten formal property'yi ölçüyor mu, yoksa tautological
   output mu üretiyor?
3. Empirical methodology bu soruyu nasıl ayırt eder?

## 3.1 The Tautology Problem

Replay framework'ü her run sonunda iki score raporlar: score_W ve
score_S, her ikisi de [0, 1] aralığında. EXTp'nin Section 6'da
göstereceği tipik sonuç: score_W = score_S = 1.0000 (N=998 replay).

Bu sonuç iki farklı durumdan gelebilir:

> **Genuine determinism.** Sistem gerçekten her run'da aynı observable
> surface'i üretiyor; comparator specification'ına faithful (her
> claimed field'ı runtime'da gerçekten karşılaştırıyor); score
> formula matematiksel olarak doğru hesaplıyor. Score = 1.0
> informative, SOE'nin empirical manifestation'ı.
>
> **Tautological output.** Comparator broken (no-op return MATCH);
> veya score formula hardcoded; veya event capture eksik. Score = 1.0
> uninformative, sadece "kod 1.0 raporlamak için yazılmış" demek.

İki durum **score değerine bakarak ayırt edilemez**. Score = 1.0
gözlemi her iki hipotezle de tutarlı.

Bu paper'ın methodological iddiası: "EXTp deterministic replay üretiyor"
demek için score'a bakmak yetmez; **comparator'ın specification'ına
faithful olduğunu da göstermek gerekir**. İki yol var:

- **Code review.** Manuel inceleme syntactic correctness'i kurabilir
  ve basit comparator semantik'leri için (birkaç yüz satır field
  comparison gibi) reliable'dır. Ancak code review **runtime-falsifiable
  evidence** üretmez — reader'ın reviewer'a güvenmesini gerektiren bir
  argument üretir.
- **Negative test.** Broken-by-construction input ver, beklenen fail'i
  observe et. Comparator runtime'da gerçekten field-by-field
  karşılaştırma yapıyorsa, mutate edilen field'da divergence raporlar.
  Yapmıyorsa, mutation rağmen MATCH raporlar — bu broken comparator'ın
  imzasıdır. Negative test'in evidence'ı **mechanically reproducible**;
  bu paper bu sebeple negative test'i tercih eder.

EXTp negative test methodology'sini kullanır — comparator'ın
specification'ına faithful olduğunu (her iddia ettiği field'ı runtime'da
gerçekten karşılaştırdığını) falsification yoluyla göstermek için.
Aşağıdaki section bu test'in formal yapısını verir.

## 3.2 Four-Field Injection Test

Test design observable surface'in dört bileşenini hedef alır: rip,
exit_reason, exit_qual, rax. Her bileşen için ayrı bir mutation run'ı
yapılır — toplam dört run, her biri o bileşeni mutate eder, diğer üçü
bozulmadan kalır.

| Test | Mutated field | Beklenen ≈_W | Beklenen ≈_S |
|------|---------------|---------------|---------------|
| A | rip | FALSE | FALSE |
| B | exit_reason | FALSE | FALSE |
| C | exit_qual | TRUE | FALSE |
| D | rax | TRUE | FALSE |

Test A ve B WOE'yi falsify eder — rip veya exit_reason mutate edilirse
WOE'nin tanımı gereği FALSE döner, SOE de zincirleme FALSE.

Test C ve D **kritik**: WOE TRUE kalır (rip ve exit_reason değişmedi),
ama SOE FALSE olmalı (exit_qual veya rax mutate edildi). Bu iki test
SOE'nin WOE'den **strict olarak güçlü** olduğunu empirical olarak
gösterir — yani SOE WOE'den ek bilgi taşıyor, sadece daha sıkı bir
isim değil.

> **Falsifiability claim.** Eğer Test C veya Test D run'unda SOE
> FALSE rapor edilmiyorsa, comparator strong path'in extra field'ları
> kontrol etmiyor demektir. Bu durumda SOE iddiası tautological hale
> gelir.

Test'in pratik uygulanması: mutation point trace_buf üzerinde, capture
sonrası ve compare öncesi yapılır. Baseline_buf'a dokunulmaz. Bu
isolation kritik — mutation persistent corruption üretmemeli, sadece
o run'a etki etmeli. Mutation per-run isolated:

```
Run N (control):  trace üretildi, mutation YOK    → score 1.0/1.0
Run N+1 (test):   trace üretildi, mutate, compare  → score değişir
Run N+2 (after):  yeni trace, mutation YOK         → score 1.0/1.0
```

Run N+2'nin 1.0/1.0 raporlaması isolation'ın kanıtı — mutation leak
etmedi.

## 3.3 Falsifiability Discipline

Negative test methodology'si daha geniş bir epistemik prensibin
uygulamasıdır: positive observation (score = 1.0) tek başına
informative değildir; ancak **falsifiability test'i geçtiyse**
informative hale gelir.

Bu prensibin operational karşılığı şu: her measurement framework için
"beklenen failure mode'u nedir, framework bunu detect edebiliyor mu?"
sorusu **before** asıl ölçüm yapılır. Eğer framework failure mode'u
detect edemiyorsa, framework'ün success raporu da güvensizdir —
çünkü framework'ün kendisi falsify edilememiş olur.

Four-field injection test bu disciplin'in EXTp-spesifik manifestation'ı:

- Beklenen failure mode'lar: dört observable field'da mutation
- Framework'ün detect kapasitesi: her field için ayrı test
- Test geçti ise: framework specification'ına faithful, score = 1.0
  informative
- Test geçmedi ise: framework non-degenerate değil, hangi score
  raporlanırsa raporlansın güvensiz

Bu paper Section 4'te SOE property statement'ını verirken, property'nin
empirical desteği bu test'in geçmesine dayanır — score = 1.0
gözlenmesine değil. İki şey ayrı kanıt yükü taşır.

---

# 4. The Strong Observational Equivalence Property

Section 2'de WOE ve SOE'yi formal relation'lar olarak tanımladık,
Section 3'te empirical methodology'yi (negative test discipline)
kurduk. Şimdi bu paper'ın SOE üzerine yaptığı **formal claim**'i
ifade ediyoruz.

## 4.1 Property Statement

> **Property (Strong Observational Equivalence under EXTp).** Let *E*
> be a guest execution under EXTp's VMM, and let *R* = *replay(E)* be
> the corresponding replay execution under EXTp's authority. Then:
>
> *E* ≈_S *R*    holds, conditional on:
>
> **Premise 1** (Capability Separation Theorem, Section 4.1):
> ¬∃ (*E*, *R*) : *observable*(*E*) = *observable*(*R*) ∧
> *caps*(*E*) = *caps*(*R*). Yani observable equivalence sağlandığında
> capability convergence yapısal olarak imkansız — observable
> eşleşmesi gözlendiğinde replay'in farklı authority üzerinden
> çalıştığı garantili.
>
> **Premise 2** (Comparator Validity, Section 3 of this entry): The
> SOE detector has been falsified through four-field injection
> (tests A-D, Section 3.2), establishing that the comparator is
> faithful to its specification — every claimed field is actually
> compared at runtime.
>
> **Empirical Claim**: Across N=998 replay runs, score_S(E, R) =
> 1.0000 (exact: every event in every run matched on all four
> observable fields; not a rounded value). With 0 observed
> failures in N=998 trials, the Clopper-Pearson 95% upper bound
> on the per-run failure rate is **0.37%**; the "1.0000"
> framing is therefore *high-confidence empirical*, not
> categorical. The N=34 × 100 = 3400 cross-boot extension
> (Section 4.2) yields a tighter bound: 95% upper bound on
> per-run failure rate = **0.11%** under 0/3400 observed failures.
> By Premise 2, this score is informative **with respect to the
> four-field observable surface defined in Section 1.1**;
> informativeness with respect to broader behavioral equivalence
> (memory state, RBX/RCX/RDX register divergence beyond the RAX
> surface, timing, microarchitectural side-channels) is out of
> scope for this property. By Section 2.2 hierarchy, *E* ≈_S *R*
> holds for all measured runs within this scope.

Property koşullu yapıdadır — Capability Separation Theorem'inin
methodology'si (verified core + empirical extension) ile aynı hibrit
zemini kullanır. Hibrit'in iki ayağı vardır:

- **Formal antecedent**: Capability Separation theorem'inden gelen
  yapısal koşul
- **Empirical antecedent**: Comparator validity (Section 3)

İki ayak da gereklidir, ne tek başına yeterlidir. Capability Separation
theorem'i SOE'nin trivially achievable olmadığını söyler (capability
divergence garantisi üzerinden farklı authority path'lerinin aynı
observable surface'i üretebilmesi non-trivial); empirical claim ise
bu surface'in **gerçekten** üretildiğini gösterir.

## 4.2 EXTp's Achievement of SOE

SOE'nin empirically sağlandığı **üç primary finding**'e dayanır
(Section 6'da raporlanır):

1. **Replay determinism (Section 6.1)**: N=998 replay run, score_S =
   1.0000 — observable surface'de tek bir field'da bile divergence yok.
2. **Negative test passing (Section 6.2)**: Four-field injection
   testleri A-D beklenen sonuçları üretir — comparator
   specification'ına faithful.
3. **Cross-boot stability (Section 6.4)**: N=34 cold-boot
   rastgeleştirme altında, 3400 replay'in (34 boot × 100 run)
   hepsinde score_S = 1.0000 — categorical 4-tuple determinism
   boot-to-boot persistent. (Timing-domain cross-boot dispersion
   stats — cycle-level mean spread, within-boot range — are
   timing observables outside the SOE surface and are reported
   in the MI entry's reproducibility section, not here.)

Üç primary finding birlikte SOE'nin **measurement methodology +
actual replay implementation + cross-boot reproducibility**
kombinasyonunda sağlandığını gösterir. Hiçbiri tek başına yeterli
değildir:

- Score determinism comparator validity olmadan tautological
- Comparator validity actual deterministic execution olmadan boş
- Single-boot determinism cross-boot reproducibility olmadan
  test setup artefaktına dair şüphe bırakır

Üç bulgu birlikte SOE'nin **measurement framework + execution
substrate + boot environment** üç ekseninde de sağlandığını gösterir.

## 4.3 Operational Meaning

SOE EXTp için iki concrete kazanç sağlar:

**Counterfactual ground**: SOE = TRUE durumunda, "exploit'in başardığı
state replay tarafından yeniden üretildi mi?" sorusunun cevabı
event-by-event, field-by-field doğrulanabilir — Section 1.1'de
tanımlanan dört-field observable surface kapsamında. Capability
Separation theorem'i, observable yeniden üretim gerçekleştiğinde
bunun zorunlu olarak farklı authority üzerinden olduğunu garanti eder
(conditional yapı: theorem unconditional bir authority ayrımı
söylemiyor); SOE bu yeniden üretimin **gerçekten gerçekleştiğini**
ölçer. İki property birlikte counterfactual analysis'in formal ve
empirical iki ayağını tamamlar.

**Failure mode separation**: SOE FALSE bir sonuçta WOE/SOE distinction
sayesinde divergence'ın control-flow seviyesinde (≈_W FALSE) mi yoksa
semantic state seviyesinde (≈_W TRUE ∧ ≈_S FALSE) mi olduğu ayırt
edilir. Bu bilgi exploit characterization için diagnostic değer taşır
— Section 6.4 ve Counterfactual Soundness Theorem (CST) property (ayrı vault entry)
bu ayrımı operasyonel olarak kullanır.

Bu temel üzerine Measurement Interference (timing-level effects, ayrı
property — observable surface'in dışındaki dimension'ları ele alır)
ve Counterfactual Soundness Theorem (CST) (branch reasoning üzerinde SOE, ayrı
property) inşa edilecek — her ikisi de SOE'yi assumption olarak
kullanır.

---

# 5. Concession Footnote

## 5.1 RAX-only register surface

SOE's observable surface includes RAX as the sole register; RBX,
RCX, RDX, R8-R15 are captured by EXTp's event struct but excluded
from the formal surface (§1.1). The justification is measurability
+ falsifiability + minimal-sufficient-for-this-paper. **The
limitation:** exploits manipulating non-RAX registers (System V
ABI syscall arguments via RDI/RSI/RDX, exception handler state via
RBX/RCX) produce divergence undetectable by score_S = 1.0000. This
is a *silent surface*, structurally parallel to MI's silent
microarchitectural leak (§5.2 in MI). Extension to the full
general-purpose register set is straightforward (data already
captured); the empirical campaign would re-validate score_S under
the broader surface and is logged as future work.

## 5.2 Trace-alignment assumption fragility

SOE's score formulas (§1.2) assume $|τ(E)| = |τ(R)|$ — event-count
equality. The deterministic guest workload of this paper (`guest_code`
= CPUID + VMCALL, 7 bytes, 2 VM exits) satisfies this empirically.
Paper-scale CVE replay would involve longer, more complex guest
traces where event count divergence is plausible. SOE's current
formulation does **not** define behavior for unequal-length traces;
they are flagged as **structural failures**, not soft divergences.
Extension to alignment-tolerant scoring (e.g., longest common
subsequence over event tuples) is future work.

## 5.3 Four-field injection test empirical results

§3.2 defines the four-field injection test; this entry asserts the
test passes (§4.2 line 451-455). The actual run logs, trace
outputs, and per-test scores belong in a separate empirical-
antecedent vault entry (`SOE_Falsification_Test.md`, forthcoming)
to keep this entry property-focused. Pending that entry, paper
text citing "comparator validity established by negative test"
should reference the forthcoming antecedent entry; this SOE entry
provides the methodological framing only.

## 5.4 N=998 vs N=34 × 100 sample organization

The empirical claims invoke two N values: N=998 (within-boot
replay determinism) and N=34 × 100 = 3400 (cross-boot stability
across 34 boots × 100 runs/boot). These are **distinct
experiments** measuring different aspects:

- N=998: within-boot reproducibility under fixed hardware state
- N=3400 cross-boot: persistence of reproducibility under
  cold-boot rerandomization of microarch state

Both yield score_S = 1.0000 (with Clopper-Pearson upper bounds
on failure rate of 0.37% and 0.11% respectively). Paper text
citing "score_S = 1.0000" must declare which experiment the score
refers to; conflating the two over-states the empirical foundation.

---

# 6. Implications

## 6.1 For replay verdict interpretation

**Frozen.**

- Every replay verdict asserting SOE must report the score with
  its Clopper-Pearson upper bound (per §4.1 disclosure discipline).
  Score-only citations are forbidden.
- Score = 1.0000 alone is not sufficient evidence; the comparator
  validity test (§3.2) must have been passed for the (instrument,
  workload) tuple of the verdict.
- WOE / SOE distinction (Section 2.3) is preserved in verdict
  output: a SOE-FALSE verdict must indicate whether WOE-FALSE
  (control-flow divergence) or WOE-TRUE ∧ SOE-FALSE (semantic
  state divergence) holds.

**Evolving.**

- Trace alignment normalization for paper-scale workloads (§5.2
  scope) — implementation strategy not locked.

## 6.2 For paper framing

**Frozen — citation conventions.**

- "Observational equivalence" in paper text must be qualified
  ("weak" or "strong" or both) per §2.3 hierarchy.
- "Score_S = 1.0000" citations must include sample size and
  Clopper-Pearson CI: e.g., "score_S = 1.0000 (N=998 within-boot,
  95% CI upper bound 0.37%)" or "score_S = 1.0000 (N=3400
  cross-boot, 95% CI upper bound 0.11%)".
- The RAX-only surface scope-limitation (§5.1) must be explicit
  at first paper-text reference to "observational equivalence".

**Frozen — forbidden framings.**

- ❌ "EXTp's replay achieves behavioral equivalence" — SOE
  scope is the 4-field observable surface, not behavioral
  equivalence in the process-algebra sense (§1.3 distinction).
- ❌ "Score_S = 1.0000 proves deterministic replay" — the
  Clopper-Pearson CI bounds the failure rate, not establishes
  zero. Use "high-confidence empirical determinism, 95% CI on
  per-run failure rate ≤ 0.37%" or equivalent.
- ❌ "SOE covers all register state" — RAX-only scope, others
  silent (§5.1).

## 6.3 For Counterfactual Soundness Theorem

**Frozen — interface contract.**

CST consumes the following from SOE:
- The four-field observable surface (§1.1) — basis for A2's SOE
  clause in CST §3.2
- The deterministic agreement guarantee under fresh-boot
  single-config (score_S = 1.0000 in non-intervention case) —
  basis for A4 in CST §3.2
- The two-level hierarchy (WOE/SOE, §2.3) — useful for
  per-event diagnostic in CST's compositional claims (§3.3.1)

**Evolving — surface expansion path.**

If future work expands SOE's surface (RBX/RCX/RDX inclusion,
§5.1), CST's A2 scope-out narrows accordingly. CST envelope
versioning (CST §3.4.5) tracks this evolution.

---

# 7. Files

**Adjacent property entries (cross-referenced):**

- `Capability_Separation_Theorem.md` — defines the capability
  authority discipline under which SOE's empirical observation
  meaningfully isolates intervention causation
- `Measurement_Interference.md` — timing-domain complement of
  SOE (different observable surface, different noise model)
- `Counterfactual_Soundness_Theorem.md` — consumes SOE's
  4-tuple surface and determinism as A2/A4 assumptions

**Empirical antecedents (forthcoming as separate entries):**

- `Cross_Boot_Stability_N34.md` — cross-boot N=34 × 100 = 3400
  experiment data
- `SOE_Falsification_Test.md` — four-field injection test run
  logs and per-test verdicts (per §5.3)

**Forward references:**

- Paper text citation discipline per §6.2
- Surface-expansion future work per §5.1
- Alignment-tolerant scoring future work per §5.2
