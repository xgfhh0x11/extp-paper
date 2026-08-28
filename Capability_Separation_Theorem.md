# Capability Separation Theorem

> **Cross-reference convention.** This entry was originally drafted
> as Chapter 4 of an integrated paper; references to other paper
> sections were preserved when the entry was extracted to vault
> format. The mapping from paper-section refs to vault entries is:
> - "Section 5" / "Section 5'te" → `Strong_Observational_Equivalence.md`
>   (defines *observable*(·) function)
> - "Section 6" / "Section 6'da" → `Measurement_Interference.md`
>   (timing-domain detectability) and `Strong_Observational_Equivalence.md`
>   §4 (empirical determinism validation)
> - "Section 6.3" → `Strong_Observational_Equivalence.md` §4 (Strong SOE)
> - "Section 6.4" → `Counterfactual_Soundness_Theorem.md`
>
> Internal §X.Y references (within this entry) target this entry's
> own sections. The §5–§7 sections of this entry (Concession Footnote,
> Implications, Files) are vault-format additions; they do **not**
> correspond to the original paper structure.

# 1. Notation and Preliminaries

Bu section'da Capability Separation theorem'i ve onun destekleyici
yapısı boyunca kullanılacak formal kelime dağarcığını kuruyoruz. Üç
kavram baştan netleşmeli, çünkü ikisinin karışması theorem'in claim'ini
hem zayıflatır hem de hatalı şekilde generalize ettirir:

1. Capability'lerin **statik dağılımı** — belirli bir anda kim hangi
   yetkiye sahip
2. Capability'lerin **dinamik yaşam döngüsü** — yetkiler zaman içinde
   nasıl transition eder
3. Bu transition'lar sırasında **gözlem ile gerçeklik arasındaki
   temporal gap**

Bu üç ayrımın paper'ın claim yapısına ve sınırlarına nasıl bağlandığını
section sonunda göreceğiz.

## 1.1 The seL4 Capability Model

seL4'te kernel-managed her kaynak — memory frame'leri, IPC endpoint'leri,
scheduler context'leri, VMX yapıları — bir *capability* üzerinden
manipüle edilir. Capability iki şeyi aynı anda yapar: kaynağı isimler
ve o kaynak üzerinde belirli bir operation set'ini yetkilendirir.
Capability *unforgeable*'dır — yani kernel'in kendisi dışında hiçbir
component bir capability üretemez veya doğrulamadan başkasına aktaramaz.

Bir thread bir kaynağa erişmek istediğinde, kernel her system call'da
o thread'in capability set'ini kontrol eder. Eğer authorize eden
capability yoksa, operation yapılamadan dönülür. Bu kontrolün
correctness'i seL4'ün verified proof'una dahildir [Klein 2009].

Bu model'in iki ayrı formal aspect'i var, ve bu ayrım theorem için
kritik:

> **Static Aspect.** Let *t* be a thread with capability set *t.caps*,
> and let *r* be a resource. An operation *op* on *r* by *t* is
> permitted if and only if *t.caps* contains a capability authorizing
> *op* on *r*. This is enforced by the kernel on every invocation.

Bu kadarı zaten capability-based access control'ün standart tanımı.
Linux file descriptor'ları, POSIX timer ID'leri, hatta Windows
handle'ları benzer bir şey yapar — runtime check, authorization set,
thread-resource binding. Statik aspect tek başına seL4'ü ayırt etmez.

Asıl ayırt edici özellik dinamik tarafta:

> **Dynamic Aspect.** Capabilities can be created (derived from existing
> capabilities), copied (delegated), revoked (removed from one or more
> capability sets), and destroyed. seL4 guarantees that revocation is
> *atomic with respect to access*: once a capability is revoked, no
> subsequent operation through any reference to it succeeds. There
> exists no observable interval during which "the capability is being
> revoked" — the transition is instantaneous from the perspective of
> any concurrent thread, interrupt handler, or kernel subsystem.

Bu garantinin pratik anlamı şu: Linux'ta `close(fd)` çağrıldıktan sonra
başka bir thread aynı fd'yi yeniden kullanırsa, race window vardır —
descriptor table güncellenirken eski referans hâlâ in-flight olabilir,
veya yeni allocation eski slot'a düşebilir, vb. Capability **referansı**
ile capability'nin **işaret ettiği kaynak** aralarında zamansal bir
boşluk doğurur. seL4 bu boşluğu **yapısal olarak yok eder** — kernel'in
verified proof'u, revoke'tan sonra hiçbir code path'in eski capability
üzerinden bir operation tamamlayamayacağını matematiksel olarak gösterir.

Bu ayrımı Section 3'te derinleştireceğiz, çünkü EXTp'nin counterfactual
analiz için seL4 üzerine kurulması bir tasarım tercihi değil, framework'ün
ölçüm zemininin koşulu. Race-window-vulnerable kernel'ler (Linux, Windows)
üzerinde benzer bir framework prensipte inşa edilebilir, ancak ölçtüğü
*observable*'lar üzerinde ek noise kaynaklarının (external interrupt'lar,
scheduler preemption, SMI, kernel daemon aktivitesi) hangi run'da hangi
şiddette manifest olduğu **a priori** belirsizdir. Bu durumda counterfactual
reasoning tek başına unpredictable olan bir observable üzerinden ikinci
katman unpredictable observable üretmeyi gerektirir — formal anlamda
ölçülemez.

Bu paper kapsamında **non-seL4 platformlar out-of-scope**'tur — currently
out-of-scope; formalization under different kernel models requires separate
treatment. Yapısal karşılaştırma örnek olarak Linux'a (CVE-2025-38352
üzerinden) referans veriyor olsak da, başka kernel'lerin formal model'leri
ve bu model'lerin deterministic replay için yeterliliği bağımsız bir
literatür ve değerlendirme gerektirir.

## 1.2 Symbol Conventions

Aşağıdaki notation'u tüm formal section'lar boyunca kullanacağız.
Şu anda hepsini tek yerde topluyoruz; kullanım sırasında her birini
yeniden tanımlamayacağız.

| Symbol | Meaning |
|--------|---------|
| *E* | Bir *exploit execution* — kernel security'sini ihlal etmeye çalışan guest-level computation |
| *R* | Bir *replay execution* — *E*'nin observable trace'ini EXTp kontrolünde yeniden çalıştırma |
| *t* | Bir thread (capability set'i *t.caps* ile) |
| *t.caps* | *t* thread'inin sahip olduğu capability'ler kümesi |
| *τ* | Bir *trace* — EXTp tarafından yakalanan, sıralı VM exit event listesi |
| *τ.events[i]* | *τ* trace'indeki *i*'inci event |
| *EPT_manipulation* | Extended Page Table'ları modify etmeye yetki veren capability'ler kümesi |
| *guest_caps* | Guest thread'lerin sahip olduğu capability'lerin birleşim kümesi |
| *extp_caps* | EXTp VMM'in sahip olduğu capability'lerin kümesi |
| *observable(X)* | *X* execution'ı tarafından üretilen externally visible state (`Strong_Observational_Equivalence.md` §1.1'de formalize) |
| *gap(S, r)* | Component *S*'in resource *r*'nin state transition'ını gözlemlediği moment ile *r*'nin state'inin gerçekten değiştiği moment arasındaki temporal interval (Section 3'te formalize) |
| *caps(X)* | *X* execution'ı sırasında **erişilebilir** (held) ve **kullanılabilir** (authority) capability'ler kümesi. Theorem proof'unda (§4.2) execution-level capability bound olarak kullanılır: *caps(X)* ⊆ ⋃ {*t.caps* : *t* thread in *X*}. Held vs used ayrımı şu an theorem statement için önemsiz çünkü her ikisi de guest authority'sinin bound'u içinde |
| *replay(X)* | *X* execution'ının EXTp tarafından yeniden çalıştırılması — *R = replay(E)* |
| *K_verified* | seL4'ün L4.verified scope'unda yer alan capability operasyonları kümesi: {*create*, *copy*, *revoke*, *destroy*} |
| *K_extended* | seL4'ün VT-x extension'ı üzerinde tanımlı, verified scope'un dışındaki operasyonlar kümesi: {*MapEPT*, *Unmap*, *WriteVMCS*, *ReadVMCS*, ...} |

Notation seçimleri kasıtlı:
- *E* ve *R* ayrı semboller, çünkü counterfactual analizde her ikisi
  aynı anda referans edilecek. "Original execution" ve "replay" demek
  prose'da yeterli ama formal manipulation'da net sembol gerekir.
- *τ* event sequence'ı için tek harf — `trace` veya `events` yazmak
  formal eşitliklerde okunaksız olur.
- *gap(S, r)* fonksiyonel notation — argümanlar component ve resource,
  value temporal interval. Section 3'te bu fonksiyonun değerinin sistemin
  bir özelliği olduğunu, execution'ın değil — yani gap'in component-resource
  pair'ine bağımlılığının aslında çalıştığı sistemin yapısal özelliğine
  bağlılık olduğunu açacağız.
- *t.caps* ve *caps(X)* farklı kavramlar: birincisi belirli bir
  thread'in herhangi bir andaki capability set'idir (statik snapshot);
  ikincisi bir execution'ın **kullandığı** capability'lerin kümesidir
  (dinamik authority). Bir thread çok sayıda capability'ye sahip
  olabilir (*t.caps*), ama belirli bir execution'da bunlardan sadece
  bir alt-kümesini kullanır (*caps(X)*). Bu ayrım Section 4'teki
  theorem statement'ında, capability convergence'ın yapısal
  imkansızlığı iddiasının (¬∃ : *caps*(*E*) = *caps*(*R*)) formal
  temelini oluşturur.

## 1.3 Observation versus Reality — A Temporal Distinction

Şimdi paper'ın boyunca defalarca dönüleceğimiz bir kavramı kuruyoruz.
State değiştiren herhangi bir computation'da iki ayrı moment ayırt
edilmelidir:

> **Reality moment.** The instant at which the underlying state —
> memory contents, capability set membership, kernel data structure
> field — actually changes.
>
> **Observation moment.** The instant at which an observer (another
> thread, an interrupt handler, a hypervisor, an external verifier)
> perceives that state change.

Senkron, atomik state transition'lara sahip bir sistemde bu iki moment
**çakışır**: gap = 0. Asenkron, partially-ordered transition'larla bir
sistemde **ayrılabilir**: gap > 0.

Önemli olan şu: gap'in büyüklüğü execution'ın bir özelliği değil,
**sistemin tasarım özelliği**. Aynı kod farklı sistemlerde çalışırsa
farklı gap üretebilir. Linux'ta POSIX CPU timer cleanup yolunda gap
~24-26 ms (CVE-2025-38352 "Chronomaly"). Aynı operation seL4'te yapılsa
gap 0 olurdu — çünkü kernel'in verified proof'u atomicity'yi garanti
eder.

Bu distinction paper'ın geri kalanında üç farklı yerde tekrar
karşımıza çıkacak:

**Section 3'te**, seL4'ün capability lifecycle transition'ları için
gap = 0 garantisini Linux'un race-window-vulnerable subsystem'leriyle
karşılaştıracağız. Chronomaly somut bir örnek — POSIX CPU timer'in
firing ve deletion code path'leri arasındaki gap, attacker tarafından
24-26 ms'lik bir window'a kilitlenebiliyor. seL4'te bu yapısal olarak
imkansız.

**`Strong_Observational_Equivalence.md`'de**, *observational
equivalence* tanımlanırken. Burada gap iki execution **arasında**
olacak, tek execution **içinde** değil. Yine de altta yatan kavram
aynı: bir observer'ın iki şeyi ayırt edip edemediği.

**Subsequent property entries'te** (özellikle
`Counterfactual_Soundness_Theorem.md`), intra-execution race window
ile inter-execution observability arasındaki ilişki açıkça incelenecek
ve sınırları çizilecek. İki kavram **yapısal olarak eşdeğer değil** —
race window tek execution içinde "observer state'i tutarsız gördü"
demek; SOE iki execution arasında "observer ikisini ayırt edemiyor"
demek. Bunlar aynı şey değil. Ama her ikisi de *observational fidelity*
denilebilecek bir abstract category'nin elemanları: kendi domain'lerinde,
gözlem ile gerçeklik arasındaki uyumun ölçüsünü veriyorlar.

---

# 2. Static Capability Distribution

Section 1.1'de capability model'in iki aspect'inden bahsetmiştik —
statik ve dinamik. Bu section statik tarafı formalize ediyor: belirli
bir anda guest ve EXTp arasındaki capability dağılımı, ve bu dağılımın
neden non-trivial bir security boundary kurduğu.

## 2.1 Guest Capability Set

EXTp'nin VMM'i altında çalışan herhangi bir guest process — exploit
dahil — boot zamanında sınırlı bir capability set'iyle başlar.
Kritik gözlem: bu set EPT manipulation için gereken capability'leri
**içermez**.

> **Definition (Guest Capability Set).** *guest_caps* ⊆ {capabilities
> available to any thread executing in guest mode under EXTp's VMM}.
> Concretely, *guest_caps* contains capabilities for guest-internal
> resources (guest memory frames as seen through guest virtual addressing,
> guest scheduler contexts, guest IPC endpoints) but excludes any
> capability authorizing direct manipulation of the EPT hierarchy or
> VMCS state.

Operasyonel olarak guest aşağıdaki invocation'ları yapamaz:

```c
seL4_X86_Page_MapEPT      // ❌ guest'in cap'i yok
seL4_X86_Page_Unmap       // ❌ guest'in cap'i yok (EPT frame'leri için)
seL4_X86_EPTPML4_Map      // ❌ guest'in cap'i yok
seL4_X86_VCPU_WriteVMCS   // ❌ guest'in cap'i yok
seL4_X86_VCPU_ReadVMCS    // ❌ guest'in cap'i yok
```

Guest'in EPT hierarchy üzerinde herhangi bir write girişimi iki
katmandan birinde durdurulur:

1. **Eğer guest VMX root mode'a geçmeye çalışırsa**: Bu zaten guest
   mode'dan tamamen çıkmayı gerektirir, ki seL4 bunu sadece VMCS'in
   uygun şekilde set up edilmiş bir transition path üzerinden izin
   verir — guest'in ulaşamadığı bir mekanizma.

2. **Eğer guest fiziksel adres üzerinden EPT entry'ye yazmaya
   çalışırsa**: EPT enforcement bunu permission violation olarak
   yakalar ve EPT violation exit üretir. Execution kontrolü EXTp'ye
   geçer.

İki yol da guest'in **yetkili olmadığını söyler** — ama farklı
seviyelerde. İlki capability check (seL4 kernel), ikincisi memory
permission check (Intel VMX hardware). EXTp'nin counterfactual
analizi her iki seviyeyi de kapsayan exit event'leri yakalar.

## 2.2 EXTp Capability Set

EXTp, seL4'ün boot-time'da verdiği untyped memory'den türetilmiş bir
root task'tır. Boot sequence'ında şu capability'leri elde eder:

> **Definition (EXTp Capability Set).** *extp_caps* contains:
>
> - *seL4_X86_Page_MapEPT* — EPT frame mapping
> - *seL4_X86_Page_Unmap* — EPT frame unmapping (COW operations)
> - *seL4_X86_EPTPML4Object* — EPT hierarchy creation and management
> - *seL4_X86_VCPUObject* — VCPU lifecycle (create, configure, destroy)
> - *seL4_X86_VCPU_WriteVMCS* — guest state programming
> - *seL4_X86_VCPU_ReadVMCS* — guest state inspection
> - *seL4_X86_VCPU_SetTCB* — VCPU-thread binding
>
> Plus standard root task capabilities (untyped memory, IPC endpoints,
> notification objects).

Bu capability'ler seL4 tarafından EXTp'ye **kasıtlı olarak** verilir —
EXTp'nin bir VMM olarak işlevini yerine getirebilmesi için zorunludur.
Verilmesinin gerekçesi seL4'ün design philosophy'siyle uyumludur:
sistemin minimum trust boundary'sini koruyarak gerekli authority'yi
gerekli component'e delege etmek.

## 2.3 The Disjoint Property

İki set'in temel ilişkisi şudur:

> **Property (Capability Disjointness).**
> *guest_caps* ∩ *EPT_manipulation* = ∅
>
> Yani guest'in EPT'yi manipüle etmesini sağlayacak hiçbir capability,
> guest'in capability set'inde bulunmaz.

Bu property formal olarak seL4'ün capability derivation rules'u
tarafından enforce edilir — EXTp boot sequence'ında EPT manipulation
capability'lerini guest'in erişebileceği capability space'e **dahil
etmez**. Guest'in bu capability'leri sonradan elde etmesinin tek yolu
delegation olur, ki EXTp bunu programlamamıştır.

> **Lemma (No Lateral Acquisition).** Eğer *t* bir guest thread'iyse
> ve *t.caps* ∩ *EPT_manipulation* = ∅ ise, *t* kendi başına
> *EPT_manipulation*'dan herhangi bir capability **edinemez**.
>
> *Proof sketch.* seL4'te capability acquisition için iki yol vardır:
> (1) explicit delegation by a capability holder, (2) derivation from
> an untyped memory capability. Guest, EPT-related untyped memory
> capability'sine sahip değildir; ve EXTp guest'e böyle bir delegation
> yapmaz. Capability'ler unforgeable olduğundan, üçüncü bir yol yoktur.
>
> *Assumptions (EXTp Configuration Correctness).* Bu lemma şu iki
> property'yi varsayar:
> (1) EXTp'nin boot configuration'ı *EPT_manipulation* capability'lerini
>     guest'in initial capability space'ine dahil etmez
> (2) EXTp'nin runtime path'leri böyle capability'leri guest'e delegate
>     etmez
> Bu iki property seL4 kernel garantisinin değil, EXTp implementation'ının
> özellikleridir, ve §6'da (Methodology) empirik olarak validate edilir.
> Capability unforgeability seL4 kernel tarafından verified, ama (1) ve
> (2) numaralı assumption'lar EXTp'nin kendi correctness obligation'ıdır.

Bu lemma triviyal görünür ama önemli: paper'ın sonraki section'larında
"guest exploit kendisini privilege escalate edemez" gibi claim'ler
yapacağız — bu claim'lerin altında yatan formal garanti tam burada.

---

# 3. Dynamic Capability Lifecycle

## 3.1 Static Picture Sufficiency — A Limitation

Section 2'de kurduğumuz statik capability dağılımı, theorem için
**zorunlu ama yeterli olmayan** bir koşuldur. Bu sınırı şimdi açıyoruz,
çünkü Section 3'ün geri kalanı tam bu boşluğu doldurmak üzere kurulu.

Linux file descriptor sistemi de statik bir disjointness gösterir:
kernel descriptor'ları user space'ten ayrı bir name space'tedir, user
process'ler kernel'in internal table'larına doğrudan erişemez. Bu
yapısal olarak benzer bir picture'dır — *guest_caps* ile
*EPT_manipulation*'ın disjoint olması gibi. Yine de Linux file
descriptor sistemi race window'lara karşı savunmasızdır:
*close-after-use* race'leri, *fork-after-close* race'leri,
*dup2*-related race'ler, hatta `epoll_ctl` ile yarış senaryoları.

Buradaki paradoks aslında paradoks değil. Statik resmin yetersizliği
**capability acquisition'da** değil, **capability lifecycle'ında**.
Yani: "guest şu anda EPT capability'sine sahip mi?" sorusu Section 2'nin
cevapladığı soru. Ama "guest'in observable bir state üzerinde EPT
capability sahibi olmadığı an ile bir başka observable state üzerinde
gerçekten EPT'ye dokunamadığı an arasında geçen sürede başka bir
component'in hatalı bir state'i yakalayıp kullanması mümkün mü?"
sorusu — bu Section 3'ün cevaplaması gereken soru.

Bu iki soru arasındaki fark, Section 1.3'te kurduğumuz **observation
moment ile reality moment** ayrımının pratik karşılığı. Statik resim
"kim neye sahip" sorusunu cevaplar; dinamik resim "bu sahiplik bilgisi
zaman içinde tutarlı kalıyor mu" sorusunu cevaplar.

EXTp'nin counterfactual analiz claim'i ikinci soruya verilen cevaba
bağlıdır. Section 3'ün geri kalanı bu cevabın seL4 ile race-window-
vulnerable kernel'lerde nasıl şekillendiğini sırayla ele alacak.

## 3.2 Capability Revocation Atomicity

Section 1.1'de seL4'ün dynamic aspect'inden bahsetmiştik —
revocation'ın *atomic with respect to access* olduğu garantisi. Bu
section o garantiyi formal hâle getiriyor: ne demek "atomic", hangi
operation'lar bu atomicity'nin kapsamında, ve neden bu garanti
counterfactual analiz için kritik.

Önce kavramı izole edelim. Capability lifecycle'ında dört temel
operation var:

> **Operations.** Let *c* be a capability and *t* a thread.
>
> - *create(c)* — capability'yi mevcut bir untyped memory veya parent
>   capability'den türet
> - *copy(c, t)* — capability'nin bir kopyasını *t*'nin capability
>   set'ine ekle (delegation)
> - *revoke(c)* — *c*'nin türevlerini ve kopyalarını sistemden kaldır
> - *destroy(c)* — capability'yi tamamen yok et (genelde revoke'un
>   ardından)

Bu operation'ların hepsi seL4 kernel tarafından **atomically**
gerçekleştirilir — yani her biri ya başarıyla tamamlanır ve sonucu
diğer thread'lere ve interrupt handler'lara hemen görünür, ya da hiç
gerçekleşmemiş gibi davranır. Half-completed bir state yoktur.

Burada "atomically" kelimesinin **iki farklı anlamı** birbirinden
ayırt edilmeli, çünkü reviewer'ın ilk takılacağı yer burası:

> **Internal atomicity.** seL4 kernel'in kendi içinde, capability
> table operasyonu lock-protected veya wait-free şekilde yapılır.
> Operation tamamlandığında kernel state tutarlıdır.
>
> **External atomicity (atomic with respect to access).** Operation
> tamamlandıktan **sonraki** ilk anda, başka herhangi bir thread,
> interrupt handler, veya kernel subsystem o capability'yi kullanmaya
> kalkarsa, **operation'ın yeni state'iyle** karşılaşır. Eski state
> üzerinden hiçbir operation tamamlanamaz.
>
> Notational equivalence: external_atomic(*op*) ≡ ∀ *S*, *r* observing
> *op*: gap(*S*, *r*) = 0. Yani external atomicity, operation'ın
> gözlemlenebilir tüm component-resource ilişkileri üzerinde
> observation-reality gap'inin sıfır olması ile **tanımsal olarak
> eşdeğerdir**.

İlk anlam çoğu kernel'de zaten vardır (Linux dahil — file descriptor
table operasyonları lock'larla korunmuştur). EXTp için **kritik olan
ikinci anlam**. seL4'ün verified proof'u bu anlamı garanti eder; Linux
ise — ki bunu Section 3.5'te detaylandıracağız — internal atomicity'ye
sahip ama external atomicity'ye sahip değildir.

External atomicity garantisinin formal ifadesi şu:

> **Property (Revocation External Atomicity).** *revoke(c)* operation'ı
> tamamlandıktan sonraki herhangi bir *t* (operation thread'inden
> farklı), *t.caps* ∩ {*c* veya *c*'nin türevleri} = ∅ olmasıyla
> **eşzamanlı olarak** tutarsız bir state gözlemleyemez. Yani:
>
> ¬∃ moment *m* such that:
>   - *revoke(c)* başlamış ama tamamlanmamış,
>   - bir başka *t'* thread'i *c* üzerinden bir operation tamamlıyor,
>   - bu operation kernel state'inde gözlemlenebilir bir effect
>     üretiyor.

Bu property'nin önemli bir corollary'si var: revocation **happens-before**
herhangi bir subsequent observation'dan. Yani temporal sıralama formal
olarak total bir order kurabilir — gözlemci hiçbir zaman "revoke ortada"
durumu göremez.

> **Corollary (No Stale Reference State).** seL4'te bir capability
> revoke edildikten sonra, sistem'in herhangi bir component'i o
> capability'nin "kısmen revoke edilmiş" hâlini observe edemez. Stale
> reference durumu yapısal olarak bulunmaz.

Bu corollary tam olarak Linux'ta olmayan şey. Linux'ta `close(fd)`
çağrıldıktan sonra başka bir thread aynı fd'yi yeniden allocate edebilir,
ve bu allocation tamamlanmadan önce **eski reference üzerinden** in-flight
bir operation hâlâ progress yapıyor olabilir. Bu boşluk race window'un
kendisidir — Section 3.3'te bu pencerenin neden ve nasıl açıldığını
inceleyeceğiz.

External atomicity'nin EXTp için pratik anlamı şudur: counterfactual
analizde "bu operation revoke'tan önce mi sonra mı yapıldı?" sorusunun
**her zaman** kesin bir cevabı vardır. Linux'ta bu soru bazen anlamsız
olur (operation revoke ile çakıştı, hangisi önce belirsiz); seL4'te
anlamsız olamaz.

## 3.3 Race Window as Observation-Reality Gap

Section 1.3'te observation moment ile reality moment arasındaki temporal
distinction'ı kurmuştuk. Section 3.2'de external atomicity garantisi
olan ve olmayan sistemler arasındaki niteliksel farkı ortaya koyduk.
Şimdi bu iki kavramı birleştiriyoruz: external atomicity'nin yokluğu,
observation moment ile reality moment arasında ölçülebilir bir gap
açar — ve bu gap'in somut adı **race window**'dur.

Önce kavramı resmi olarak tanımlayalım:

> **Definition (Race Window).** Let *S* be a system component (e.g., a
> kernel subsystem, a user thread, an interrupt handler) and let *r*
> be a resource undergoing a state transition initiated by another
> component. The *race window* of *S* with respect to *r*'s transition
> is the temporal interval [*t_obs*, *t_real*] where:
>
> - *t_obs* is the moment at which *S* observed *r*'s state (and based
>   subsequent computation on this observation),
> - *t_real* is the moment at which *r*'s state actually changed.
>
> If *t_obs* < *t_real*, then *S* operates on stale information during
> the interval. If *t_obs* > *t_real*, then *S* may observe a
> not-yet-committed state. In both cases, the gap creates a
> *manipulation surface*: an attacker who can predict or manipulate
> the timing of operations can place malicious actions within this
> interval.

İki nokta dikkat çekici:

**Birincisi**, race window sadece bir "bug" değil, sistemin yapısal
özelliği. Aynı kod farklı ortamlarda çalıştığında race window'un
büyüklüğü değişebilir, ama varlığı kod'a değil **mekanizmaya** bağlı.
Lock kullanımı race window'u **küçültebilir**, ama tamamen kapatabilmek
için lock'un kapsamı state transition'ın tüm gözlemlenebilir
etkileriyle örtüşmek zorundadır. Pratikte bu örtüşme nadiren elde
edilir — özellikle async path'lerin (interrupt handler'ları, IPC
endpoint callback'leri, signal delivery) söz konusu olduğu durumlarda.

**İkincisi**, race window'un "küçüklüğü" exploit edilebilirliğini
**kaldırmaz**, sadece **erteler**. 24-26 ms'lik bir window, attacker'ın
scheduler üzerinde yeterli baskı uygulayabildiği durumlarda
deterministic olarak hedeflenebilir. Window 100 mikrosaniyeye düşürülse
bile, doğru koşullar altında — örneğin kernel preemption disabled
olmayan path'lerde, hyperthreading paylaşımı altında — yine de
hedeflenebilir. Sadece **window'un yapısal olarak sıfır olması**, race
window-tabanlı exploitation'ın kategorik olarak imkansız hâle
getirilmesini sağlar.

Bu iki noktayı birleştiren formal observation:

> **Property (Race Window as Observation-Reality Gap).** Bir state
> transition'ı gerçekleştiren herhangi bir operation *op* için, eğer
> *op* external atomicity garantisi sağlamıyorsa, ∃ *S*, *r* öyle ki
> race window > 0. Yani:
>
> ¬external_atomic(*op*) → ∃ *S*, *r*: gap(*S*, *r*) > 0
>
> Burada gap(*S*, *r*) = |*t_real* − *t_obs*|, Section 1.3'te
> tanımlanan temporal interval'in operasyonel adı.

Bu property Section 3.4'ün asıl iddiasını kuracak: external atomicity
garantisi sağlanan operation'lar için, Section 3.2'de kurulan tanımsal
eşdeğerlik gereği gap = 0; yani race window kategorik olarak imkansız.

EXTp'nin counterfactual analiz claim'i için bu kavram köprü işlevi
görür. Counterfactual reasoning, "olmayan bir senaryo gerçekleşseydi
ne olurdu?" sorusunu sorar. Bu soruya formal olarak cevap verebilmek
için, gerçekleşen senaryonun **gözlemlenebilir state'i** ile
gerçekleşmeyenin **hipotetik state'i** arasında karşılaştırma yapılır.
Eğer gözlemlenebilir state'in kendisi belirsizse — yani race window
açıksa, hangi state'i gözlemlediğimiz tam olarak belli değilse —
counterfactual karşılaştırma metafora indirgenir.

Şu örneği düşünelim: bir attacker exploit'ini Linux kernel üzerinde
çalıştırıyor, exploit POSIX CPU timer race window'u sömürüyor. EXTp
bu senaryoyu replay etmek istiyor. Replay sırasında "race window
açıldı mı?" sorusu, Linux'un kendisinde 24-26 ms'lik bir interval'de
belirsiz olduğu için, replay'in reproducibility'si en iyi durumda
**istatistiksel** olur — her replay'de race window'un açılma anı,
süresi, ve diğer thread'lerin bu interval'deki davranışı stochastic
olarak değişir. Bu durumda counterfactual question'ın cevabı bir
**dağılım** olur, kesin bir state değil.

seL4'te aynı senaryo formal olarak farklı: race window kategorik
olarak yok olduğu için, counterfactual reasoning **deterministic**
zemin üzerinde yapılır. EXTp'nin Section 6'da göstereceği gibi, replay
score 1.0000 = bu zeminin yapısal sonucu, mühendislik başarısı değil.

## 3.4 seL4's Structural Guarantee: gap → 0 in K_verified, Empirically in K_extended

Section 3.2 ve 3.3'te kurduğumuz kavramları şimdi seL4 üzerinde
operasyonel olarak birleştiriyoruz. Burada kritik bir ayrım yapıyoruz:
seL4'ün capability operasyonları **iki ayrı küme**ye ayrılır, ve
bunların external atomicity garantileri **niteliksel olarak farklı
zeminlerde** durur.

> **Definitions (Capability Operation Sets).**
>
> - **K_verified** = {*create*, *copy*, *revoke*, *destroy*} —
>   seL4'ün cap-table operasyonları. Bu küme L4.verified projesinin
>   formal scope'undadır.
>
> - **K_extended** = {*MapEPT*, *Unmap*, *WriteVMCS*, *ReadVMCS*,
>   *EPTPML4_Map*, ...} — seL4'ün x86-64 VT-x extension'ı üzerinde
>   tanımlı operasyonlar. Bu küme L4.verified projesinin **formal
>   scope'unun dışındadır**; verification status ileride formalize
>   edilebilir, ancak bu paper yazıldığı sırada VT-x path'leri
>   verified değildir.

Bu iki küme için garantinin yapısı farklıdır:

> **Property (External Atomicity, Hybrid Form).**
>
> ∀ *op* ∈ K_verified : external_atomic(*op*) = TRUE   *(formally proven)*
>
> ∀ *op* ∈ K_extended : external_atomic(*op*) = TRUE   *(methodological assumption, empirically tested)*

Section 3.2'de kurulan tanımsal eşdeğerlik (external_atomic(*op*) ≡
∀ *S*, *r* : gap(*S*, *r*) = 0) her iki kümeye uygulandığında,
gap = 0 garantisi K_verified üzerinde kategorik, K_extended üzerinde
methodological-empirical zeminde durur. Bu hibrit yapı paper'ın
contribution model'inin özünü oluşturur — Section 4.1'de Premise 2
olarak formalize edilir.

> **Corollary (No Race Window, Hybrid).** Capability operation'ları
> için race window:
>
> - K_verified üzerinde **kategorik olarak sıfır** (formal proof'tan)
> - K_extended üzerinde **empirically gözlenen sıfır** (Section 6'daki
>   replay determinism testleri)
>
> Linux'taki `posix_cpu_timer_del()` patch'i (Section 3.5'te
> detaylandırılacak) race window'u küçültür ama sıfırlamaz — patch
> sonrası bile teorik olarak çok dar bir window açıktır. seL4'te ise,
> hem K_verified hem K_extended için, garantinin yapısı **niteliksel
> olarak farklıdır**: window'un büyüklüğü tartışılmaz çünkü window'un
> kendisi yoktur (sırasıyla formal ve empirical zeminde).

### 3.4.1 Verified Scope: K_verified

K_verified üzerindeki external atomicity garantisi seL4'ün L4.verified
projesinin Isabelle/HOL proof infrastructure'ında ispatlanır.
Garantinin temelini oluşturan property'ler:

> **Verified Properties (L4.verified scope).**
>
> - **Functional correctness:** Kernel'in spec'i ile implementation'ı
>   arasındaki refinement ilişkisi [Klein 2009; Klein et al. 2014,
>   "Comprehensive Formal Verification of an OS Microkernel"].
>   **x86-64'te C-source seviyesinde mevcuttur** (status verify
>   edilmesi gereken claim — Trustworthy Systems'ın versioned
>   proof status'üne göre paper-publication anında re-confirm
>   edilir).
> - **Integrity:** Capability'siz hiçbir thread başka bir thread'in
>   state'ini değiştiremez [Sewell 2013]. **ARMv7 ve RISCV64'te
>   ispatlanmıştır; x86-64'te integrity proof bu paper yazıldığı
>   sırada mevcut değildir.**
> - **Confidentiality:** Information flow capability boundaries'i
>   tarafından kontrol edilir [Murray 2013]. **ARMv7 üzerinde
>   ispatlanmıştır; x86-64'te mevcut değildir.**
>
> Bu paper'ın seL4 platformu x86-64 olduğundan, formal zemin yalnızca
> functional correctness'ten gelir. Integrity ve confidentiality
> proof'larının x86-64'teki yokluğu ek bir scope sınırıdır;
> capability lifecycle operasyonlarının atomicity'si functional
> correctness'in altında olduğu için K_verified üzerinde external
> atomicity hâlâ formal zemine sahiptir, ancak daha güçlü
> security property'leri (integrity, confidentiality) bu paper
> tarafından x86-64'te assume edilmez.

### 3.4.2 Extended Scope: K_extended

K_extended seL4'ün x86-64 VT-x extension'ı üzerinde tanımlanan ve
EXTp tarafından doğrudan kullanılan operasyon kümesidir. Bu küme
L4.verified verified scope'un dışındadır: VT-x path'leri (MapEPT,
WriteVMCS, ReadVMCS vb.) için ne functional correctness, ne integrity,
ne de confidentiality proof'ları mevcuttur.

Bu durumda K_extended üzerinde external atomicity'nin kabul edilmesi
**formal değil, methodological** bir adımdır. Kabul'ün gerekçesi şu üç
maddeye dayanır:

1. **Architectural extension thesis.** seL4'ün capability disciplin'i
   kernel design philosophy'sinin bir parçasıdır ve verified-scope
   operasyonları ile extended-scope operasyonları arasında **architectural
   sürekliliği** vardır. Aynı capability invariants'ı (unforgeability,
   derivation rules, revocation atomicity) VT-x extension path'lerinde
   de tasarım gereği uygulanır.
2. **Empirical test.** Bu varsayımın çalıştığı Section 6'da empirically
   test edilir — replay determinism_score = 1.0000 (N=998), bu paper'ın
   verdiği en güçlü ampirik kanıttır.
3. **Methodological pozisyon.** K_extended'in unverified olması paper
   için bir limitation değil, **verified-kernel zemin üstünde kurulu
   non-verified extension'ların deterministic davranışını ölçmenin
   yapısal zemini**dir. Eğer empirical determinism gözleniyorsa, bu
   verified-zeminin matematiksel garantilerinin VT-x extension katmanına
   dolaylı manifestation'ı olarak okunabilir.

K_extended atomicity'sinin destekleyici evidence'ı **consistent ama
unique olmayan** evidence olduğu için (alternative açıklamalar:
hardware-level determinism, single-threaded VMM execution model,
measurement scope kararları) Section 6 bu alternative'leri sistemli
olarak ele alır.

## 3.5 Chronomaly as Concrete Manifestation

Section 3.2-3.4'te kurduğumuz formal yapı — external atomicity, race
window, gap = 0 — abstract düzeyde tamamlandı. Bu section kavramların
gerçek bir sistemde nasıl manifest olabildiğini somutlaştırmak için
CVE-2025-38352 (kod adıyla "Chronomaly") vakasını inceler. Vurgu
önemli: bu inceleme Linux'un mimari bir eleştirisi değil, race window
abstract tanımının ölçülebilir bir interval olarak görünür hâline
köprü kurma çabası. Aynı egzersiz başka race-window-vulnerable
subsystem'ler için de yapılabilir.

> **Length note.** §3.5 (~100 lines) is the longest single
> subsection of this entry; for paper-text adaptation, the
> illustrative depth here may be condensed to a single paragraph
> with a forward-reference to a separate demonstration entry
> (`CST_Demonstration_Chronomaly.md`, forthcoming under CST §6.3
> demonstration case requirements). The vault scope retains the
> full discussion as historical context for the race-window
> formalization.

### 3.5.1 Vakanın Yapısal Özeti

CVE-2025-38352 Linux POSIX CPU timers subsystem'inde bir use-after-free
race condition'ıdır. İki kernel code path'i — `handle_posix_cpu_timers()`
ve `posix_cpu_timer_del()` — aynı `k_itimer` objesine farklı
bağlamlardan dokunur. İlki interrupt context'inde firing timer'ları
toplar; ikincisi process context'inde timer silme operasyonunu yapar.
Race window'un yapısı üç adımda özetlenebilir:

1. `handle_posix_cpu_timers()` firing timer'ları lokal liste'ye toplar
   ve `unlock_task_sighand()` ile lock'u bırakır
2. Lock bırakıldıktan sonra IRQ handler `signalfd_notify()` döngüsüne
   girer; bu interval'de başka bir CPU `waitpid()` → `posix_cpu_timer_del()`
   → `kfree(timer)` zincirini tamamlar ve cross-cache realloc ile slot'a
   `pipe_buffer` yerleşir
3. `signalfd_notify()` döngüsü bittiğinde `handle_posix_cpu_timers()`
   firing listesini yinelemeye başlar; ama o slot'ta artık `pipe_buffer`
   var → use-after-free

Bu sıralama Section 3.3'te formalize ettiğimiz race window
definition'ının operasyonel karşılığıdır:

- *t_obs* = Adım 1'de firing timer'ın listeye eklendiği an
- *t_real* = Adım 2'de `kfree(timer)` tamamlandığı an
- gap(*S*, *r*) = *t_real* − *t_obs*, signalfd_notify döngüsü içinde
  bir noktada tamamlanır
- **Window of opportunity** ≈ 24-26 ms — gap'in attacker tarafından
  sömürülebileceği temporal kapı, signalfd_notify döngü süresine
  kilitlenir. Bu **gap'in kendisi değil**, gap'in exploit edilebileceği
  pratik aralıktır

Çoğu pratik exploit literatüründe bu ayrım yapılmaz, ama formal
section'da consistent olmak için race window (formal gap) ile
window of opportunity (exploit pratiği) ayrı tutulur.

*S* = `handle_posix_cpu_timers()`, *r* = ilgili `k_itimer` objesi
olmak üzere gap > 0 koşulunun ölçülebilir bir manifestation'ıdır.

### 3.5.2 Window'un Deterministic Olarak Hedeflenebilmesi

Race window'un sadece var olması exploit için yeterli değil —
attacker'ın window'u deterministic olarak isabet ettirebilmesi gerekir.
Chronomaly'de bu iki mekanizma ile sağlanır:

**Scheduler pressure.** 11K+ thread oluşturarak ve 50K epoll waiter
beslemeyerek `signalfd_notify()` döngüsünün süresi 24-26 ms aralığında
**deterministic olarak** kilitlenir. Window'un başlangıcı timer firing
event'i ile, bitişi `signalfd_notify()` tamamlanması ile sabittir.

**Cross-cache realloc.** `kfree(timer)` sonrası boşalan slot'un
`pipe_buffer` tarafından doldurulması rastgele değil — her iki object
de `kmalloc-192` slab'ından gelir, attacker pipe write'larını timing
açısından `kfree` ile koordine eder.

Bu iki mekanizma bir araya geldiğinde race window operasyonel olarak
**deterministic** hâle gelir — kategorik olarak değil, ama pratik
olarak. Section 3.4'teki ayrımın somut gösterimi: Linux'taki window
küçültülebilir ama yapısal olarak kapatılamaz, dolayısıyla patch
düzeyinde küçültme exploit'in **maliyetini artırır**, kategorik olarak
imkansız hâle **getirmez**.

### 3.5.3 EXTp Counterfactual Analiz Bağlamında

Chronomaly vakası EXTp için iki şeyi somutlaştırır:

**Birincisi**, race-window-vulnerable bir kernel'de counterfactual
replay'in zemininin neden statistical olduğu. Eğer EXTp Linux üzerinde
Chronomaly'yi replay etmeye çalışsaydı, race window'un her replay'de
aynı süre açılması, cross-cache realloc'un her replay'de aynı timing'de
tamamlanması, IRQ handler'ın firing listesini hangi anda yinelemeye
başlayacağı — hiçbiri garantili değil. "Exploit başarılı oldu mu?"
sorusu replay'ler arasında **dağılım** olarak cevaplanır, kesin bir
state değil. Counterfactual karşılaştırma için baseline'ın kendisi
belirsiz.

**İkincisi**, seL4 üzerinde aynı kavramsal exploit'in (cross-context
shared object lifecycle race) **simülasyonunun bile** yapay enjeksiyon
gerektirdiği. seL4'te race window kategorik olarak yok olduğu için,
Chronomaly-benzeri bir senaryo replay'de **doğal olarak** ortaya
çıkamaz — attacker'ın hipotetik exploit yolunu modellemek için EXTp'nin
deliberate olarak zaman penceresi enjekte etmesi gerekir. Bu
enjeksiyonun kendisi ayrı bir formal model gerektirir (Section 6'da
ele alınacak Measurement Interference ile bağlantılı).

Bu iki nokta, Section 3'ün başında kurduğumuz iddiayı somutlaştırır:
EXTp'nin counterfactual analiz claim'inin formal zemini, üzerine
kurulduğu kernel'in race window garantisine bağlı.

---

# 4. The Capability Separation Theorem

Section 2 ve 3'te capability dağılımının statik ve dinamik aspect'lerini
formal olarak inşa ettik. Bu section iki yapıyı tek bir theorem altında
birleştiriyor ve theorem'in EXTp üzerinde ne sağladığını netleştiriyor.

Theorem yeni bir kavram üretmiyor — Section 2.3'ün disjoint property'si
ile Section 3.4'ün external atomicity garantisini (K_verified üzerinde
formal, K_extended üzerinde empirical olmak üzere hibrit zeminde)
bir araya getiriyor. Yeniliği "verified-core ve empirical-extension
garantilerinin birleşiminin EXTp'nin counterfactual claim'i için
yeterli formal zemini kurması" iddiasında.

## 4.1 Theorem Statement

> **Theorem (Capability Separation).** Let *E* be an exploit execution
> attempting to manipulate the EPT hierarchy under EXTp's VMM, and let
> *R* = *replay(E)* be the corresponding replay execution under EXTp's
> own capability authority. Then:
>
> **Premise 1** (Static Disjointness, Section 2.3):
>   *guest_caps* ∩ *EPT_manipulation* = ∅
>
> **Premise 2** (Dynamic External Atomicity, Section 3.4):
>   ∀ *op* ∈ K_verified : external_atomic(*op*) = TRUE   (formally proven)
>   ∀ *op* ∈ K_extended : external_atomic(*op*) = TRUE   (assumed)
>
> burada:
> - **K_verified** = {*create*, *copy*, *revoke*, *destroy*} — seL4'ün
>   cap-table operasyonları, L4.verified projesinin x86-64 üzerindeki
>   functional correctness proof'uyla **C-source seviyesinde verified**
>   [Klein 2009]. Section 3.4.1'de açıklandığı üzere, integrity ve
>   confidentiality proof'ları x86-64 için bu paper yazıldığı sırada
>   mevcut değildir; theorem'in formal zemini yalnızca functional
>   correctness'e dayanır.
> - **K_extended** = {*MapEPT*, *Unmap*, *WriteVMCS*, *ReadVMCS*, vb.}
>   — seL4'ün x86-64 VT-x extension operasyonları. Bu operasyonlar
>   **L4.verified verified scope'unun dışındadır**; external atomicity
>   garantisi burada formal proof'a değil, seL4 kernel design'ının
>   capability disciplin'inin VT-x path'lerine extend edildiği
>   varsayımına dayanır.
>
> Bu ayrım sadece bir scope çizimi değil, paper'ın methodological
> pozisyonudur: Theorem'in formal omurgası K_verified üzerinde durur;
> K_extended'in atomicity'si Section 6'da empirical olarak test edilir.
> Bu test sonuçları (replay determinism_score = 1.0000, N=998), varsayımın
> çalıştığına dair **consistent ama unique olmayan** ampirik kanıt
> sağlar — alternative açıklamaları (hardware-level determinism,
> single-threaded VMM execution model, measurement scope kararları)
> Section 6'da sistemli olarak ele alınır. Bu mütevazılık göz ardı
> edilmemekle birlikte, sonuçlar **verified-zeminin matematiksel
> garantilerinin VT-x extension katmanına dolaylı manifestation'ı
> olarak okunabilir**: K_extended'in unverified olması paper için bir
> limitation değil, verified-kernel zemin üstünde kurulu non-verified
> extension'ların deterministic davranışını ölçmenin yapısal zeminidir.
>
> **Conclusion**:
>   ¬∃ (*E*, *R*) : *observable*(*E*) = *observable*(*R*) ∧
>                    *caps*(*E*) = *caps*(*R*)
>
> Equivalently (implication form, easier to parse):
>   *observable*(*E*) = *observable*(*R*)  ⟹  *caps*(*E*) ≠ *caps*(*R*)
>
> Yani: bir exploit execution ile replay execution'ın observable
> state'leri eşleştiğinde, kullandıkları capability authority'ler
> mutlaka ayrışmıştır. Capability convergence yapısal olarak imkansızdır.
>
> **Scope clarification on conclusion strength.** The negation
> form above states that the conjunction (observable equivalence
> AND capability equality) is impossible. The proof in §4.2
> actually establishes a stronger sub-claim: *caps*(*E*) =
> *caps*(*R*) alone is impossible (regardless of observable
> equivalence), because *E* as a guest execution cannot use
> EPT-manipulation capabilities (§2.3) while *R* as a replay
> execution must use them. We state the theorem in the weaker
> conjunction-negation form because that is the form
> operationally consumed by SOE and CST: SOE establishes
> observable equivalence empirically, and the theorem under
> that condition guarantees capability divergence. The stronger
> unconditional form is a corollary of the proof.

> **Definitional dependence on SOE entry.** Theorem statement'ı
> *observable*(·) fonksiyonunu kullanır, ki tam tanımı
> `Strong_Observational_Equivalence.md` §1.1'de formalize
> edilir (four-field tuple: rip, exit_reason, exit_qual, rax;
> register surface RAX-only with §5.1 scope-limitation).
> Theorem'in formal viability'si *observable*'ın SOE entry'sinde
> definite ve bounded olarak tanımlanmasına bağlıdır; şu an için
> "aynı RIP/exit_reason/exit_qual + RAX" düzeyinde sezgisel
> tanım yeterlidir.

Theorem'in iki bileşenini ayrı ayrı vurgulamak gerek:

**`observable(E) = observable(R)`** — bu eşitlik theorem'in **varsayım
zemini**, kanıtlanan kısmı değil. Bu paper'da empirically gösterilir
(Section 6, determinism_score = 1.0000). Theorem'in formal claim'i
şudur: bu eşitlik **gözlemlendiğinde**, capability'ler **zorunlu olarak**
ayrışmıştır.

**`caps(E) ≠ caps(R)`** — bu eşitsizlik theorem'in **kanıtladığı**
kısım. Aynı observable state iki farklı capability set tarafından
**üretilmiş ise**, *E*'nin yolu fault üretir (capability yokluğu
kernel tarafından yakalanır); *R*'nin yolu başarılı VMM
operasyonudur. Bu ayrımın kendisi counterfactual analiz için zemin
oluşturur — eğer gözlemlenebilir state aynı ise capability path'leri
mutlaka farklıdır, dolayısıyla "bu effect'i hangi authority üretti?"
sorusu **ayrıştırılabilir** bir soru hâline gelir.

### Ne Kanıtlanıyor, Ne Kanıtlanmıyor

Theorem'in scope'u dar tutuluyor — kapsamı dışında kalanlar paper'ın
diğer section'larının konusu:

- Theorem **kanıtlıyor**: observable state eşleştiğinde capability
  authority'lerin yapısal olarak ayrılmak zorunda olduğunu (capability
  convergence imkansızlığı).
- Theorem **kanıtlamıyor**: observable equivalence'ın **achievable**
  olduğunu (mühendislik konusu, Section 6 — Methodology),
  counterfactual branch'lerin doğru modellendiğini (Section 6.4 konusu
  — Counterfactual Soundness Theorem (CST)), ya da timing-level eşdeğerliğin de
  sağlandığını (Section 6.2 konusu — Strong SOE).

Theorem **yapısal koşulu** kuruyor — observable equivalence sağlandığı
durumda capability divergence kategorik olarak garanti. Mühendislik
validation'ı (achievability) ve diğer formal property'ler bu koşul
üzerine ekleniyor.

**Forward references for non-self-contained constructs:**
- *observable*(·): `Strong_Observational_Equivalence.md` §1.1
- score determinism empirical claim: `Strong_Observational_Equivalence.md`
  §4 + `Cross_Boot_Stability_N34.md` (forthcoming)
- timing-domain detectability $\Delta^*$: `Measurement_Interference.md` §3.1
- counterfactual reasoning soundness: `Counterfactual_Soundness_Theorem.md`
- demonstration case (Chronomaly-style): `CST_Demonstration_Chronomaly.md`
  (forthcoming, per CST §6.3 requirements)

## 4.2 Proof Sketch

Bu section theorem'in **operasyonel argument**'ını verir — full
Isabelle/HOL proof değil; bu seviye bir refinement L4.verified projesinin
scope'u. Burada amaç Section 2-3'ün formal tools'larının theorem'in
**no-other-path** conclusion'ına nasıl yol açtığını dört adımda göstermek.

Proof reductio ad absurdum yapısında: caps(*E*) = caps(*R*) varsayalım,
çelişki türetelim.

**Step 1 (Static Disjointness, Section 2.3'ten).** Premise 1 gereği
*guest_caps* ∩ *EPT_manipulation* = ∅. *E* bir guest execution
olduğundan, *E*'de yer alan thread'lerin capability set'leri için
*t.caps* ⊆ *guest_caps* (Section 1.2 notation: thread-level snapshot).
Execution-level capability set tanım gereği *E*'de yer alan thread'lerin
kullandığı capability'lerin birleşimidir: *caps*(*E*) ⊆ ⋃ *t.caps*,
dolayısıyla *caps*(*E*) ⊆ *guest_caps*. Buradan: *caps*(*E*) ∩
*EPT_manipulation* = ∅. Ek olarak No Lateral Acquisition Lemma'sı
(Section 2.3) bu disjointness'in execution boyunca korunduğunu
garanti eder — capability'ler unforgeable, EXTp delegation yapmaz, ve
guest'in EPT untyped'ı yok. **Sonuç:** Guest execution *E* hiçbir EPT
manipulation operasyonu **gerçekleştiremez**; girişimleri kernel-level
fault üretir.

**Step 2 (Dynamic External Atomicity, Section 3.4'ten).** seL4'te
∀ *op* ∈ K_verified için external_atomic(*op*) = TRUE (formally proven,
Premise 2 — x86-64 functional correctness [Klein 2009]). K_extended
için aynı property varsayılır (verified scope dışı, ama EXTp'nin VT-x
path'lerine verified-kernel disciplin'inin extend edildiği
methodological pozisyonu). Section 3.2'deki tanımsal eşdeğerlik gereği
her iki durumda da ∀ *S*, *r* : gap(*S*, *r*) = 0 — yani bir component
bu operasyonları **invoke ederse**, race window olmadan, deterministic
biçimde gerçekleşir. **Sonuç:** EXTp authority'si altında gerçekleşen
bir EPT manipulation, observation-reality gap'i sıfır olarak bir
state transition üretir; *replay(E)* deterministic. K_extended için
bu deterministik davranış Section 6'da empirical olarak ölçülür ve
varsayımı destekler.

**Step 3 (Reductio).** Şimdi theorem'in inkarını varsayalım: ∃ (*E*, *R*)
öyle ki *observable*(*E*) = *observable*(*R*) **ve** *caps*(*E*) =
*caps*(*R*). Step 1'den *caps*(*E*) ⊆ *guest_caps*; varsayım gereği
*caps*(*R*) = *caps*(*E*) ⊆ *guest_caps*. Premise 1'den *guest_caps* ∩
*EPT_manipulation* = ∅, dolayısıyla *caps*(*R*) ∩ *EPT_manipulation* = ∅.
Ama *R* = *replay*(*E*) tanımı gereği EXTp authority altında çalışan
ve EPT operasyonları gerçekleştiren bir execution'dır — *caps*(*R*),
en az bir *EPT_manipulation* elementi içermek zorundadır. Çelişki:
*caps*(*R*) hem *EPT_manipulation* ile disjoint, hem değil. Dolayısıyla
varsayım yanlış: *caps*(*E*) = *caps*(*R*) imkansız.

**Step 4 (Closure).** Step 3'ün gösterdiği imkansızlık üç ayrı
garantinin birleşiminden gelir — birincisi formal, ikincisi formal,
üçüncüsü empirical. **No Lateral Acquisition** (Step 1) guest
authority'sinin EPT'ye ulaşamayacağını L4.verified capability
disciplin'i üstünden garanti eder (functional correctness, x86-64).
**No Race Window in K_verified** (Step 2'nin formal zemini)
capability lifecycle'da deterministic davranışı [Klein 2009] ile
sağlar. **No Race Window in K_extended** (Step 2'nin empirical zemini)
VT-x extension üzerinde deterministic davranışı Section 6'da
empirically gösterir. Theorem'in DNA'sı **verified core ile empirical
extension'ın hibrit birleşimi** üzerine kuruludur — paper'ın
methodological contribution'ı budur. Capability convergence yapısal
olarak imkansızdır. ∎

Bu argument'ın resmi olmayan tarafı şu noktalarda:

- *observable* fonksiyonunun tam tanımı henüz formalize edilmedi
  (Section 5'in konusu); proof'un viability'si Section 5'in tanımının
  uygun olmasına bağlıdır
- "EXTp authority altında EPT manipulation deterministically aynı
  effect'i üretir" iddiası Premise 2 + No Lateral Acquisition
  assumption'larına dayanır; EXTp'nin VMM kodunun **kendi correctness'i**
  Section 6 (Methodology) ile validate edilir — formal değil, empirical
- Theorem capability boundary'sinde biter; microarchitectural
  side-channel'lar (Section 6.3'ün konusu) bu argument'ın dışında

## 4.3 EXTp Üzerinde Operasyonel Anlamı

Capability Separation Theorem'in EXTp için pratik kazancı şudur:
counterfactual analizde "exploit'in başardığı state'i replay'in
yetkili authority altında yeniden üretebiliyoruz" iddiasının yapısal
zemini netleştirilmiş olur. Theorem **observable equivalence'ı predict
etmez** — bu Section 6'da empirically gösterilen bir bulgudur
(determinism_score = 1.0000). Theorem koşullu yapıdadır: observable
equivalence empirically sağlandığında (Section 6), capability
divergence yapısal olarak garanti edilir. Bu iki katman — empirical
antecedent ve **hibrit consequent** (K_verified üzerinde formal,
K_extended üzerinde empirical olarak temellenen capability divergence)
— birlikte EXTp'nin counterfactual kapasitesini destekler. Theorem
ayrıca counterfactual sorgulamayı temellendirir: "*caps*(*E*) ≠
*caps*(*R*)" yapısal zorunluluğu, "bu effect hangi authority altında
üretildi?" sorusunun formal olarak **anlamlı** olduğunu garanti eder.
Bu temel üzerine `Strong_Observational_Equivalence.md` *observable*
fonksiyonunu formalize eder, `Measurement_Interference.md`
timing-domain detectability bound'unu kurar, ve
`Counterfactual_Soundness_Theorem.md` weak/strong SOE distinction'ı +
MI Δ* + bu theorem'i birleştirip causal attribution sufficiency'yi
ifade eder.

---

# 5. Concession Footnote

## 5.1 Authority disjointness vs side-effect freedom (Q4 gap)

Theorem'in formal omurgası **authority disjointness** üzerine kurulu
(§2.3 disjoint property, §3.4.1 K_verified external atomicity). Bu
authority capability'lerin **doğrudan** modifikasyon yolunu kapatır.
Ama "intervention machinery'nin *execution*'ı sırasında bounded
side-effects" (CPU cycles, scheduler time, cache lines, branch
predictor pollution) Capability Separation tarafından **bounded
değil, sadece authority-disjoint** edilir. CST entry'sinin A1
assumption'ı bu gap'i explicit ele alır (CST §3.2 A1 modulo, CST
§4.1.3 detail) ve Q4 future experiment ile validation hedeflenir
(CST §5.1).

Bu paper'da Capability Separation theorem'i **authority bound**
düzeyinde durur; side-effect bound CST tarafından inherited ve
empirically validate edilecek bir downstream concern'dir. Bu
asymmetry yapısal: capability disciplin'i authority'yi kapsar,
execution overhead'i kapsamaz.

## 5.2 x86-64 verified scope sınırı

§3.4.1'de detaylandırıldığı üzere, seL4'ün x86-64 platformunda
**functional correctness** proof'u mevcuttur, ama **integrity** ve
**confidentiality** proof'ları (ARMv7/RISCV64'te mevcut) x86-64
için bu paper yazıldığı sırada mevcut değildir. Theorem'in formal
omurgası functional correctness'ten gelir; daha güçlü security
property'leri assume edilmez.

Paper-text adaptation'da seL4 verification status'ünü
publication-time'da re-verify et: Trustworthy Systems'ın versioned
proof status'ü çevrimiçi tracked, ve x86-64 integrity proof timeline'ı
2024 sonrası planlanmış. Citation güncelleme gerek olabilir.

## 5.3 N=998 / N=34 empirical foundation CI

§4'te alıntılanan "replay determinism_score = 1.0000, N=998" ve
"score_S = 1.0000 across N=34 cross-boot trials" (Cross_Boot_Stability_N34
referans) sayıları **Clopper-Pearson 95% upper bound** ile cite
edilmelidir:
- N=998 → upper bound on failure rate = **0.37%**
- N=34 → upper bound on failure rate = **10.4%**
- N=3400 (cross-boot × 100 per boot, SOE §4.2) → upper bound = **0.11%**

"Deterministic" framing'i **high-confidence empirical**, kategorik
değil. Bu disclosure paper-text citation discipline'ının parçası
(§6.2).

## 5.4 K_extended methodological position

§3.4.2 + §4.1 K_extended (VT-x extension operations) için external
atomicity'nin **formal proof değil, methodological assumption + empirical
test** olduğunu açıkça flag'liyor. Replay determinism_score = 1.0000
bu varsayımı **consistent ama unique olmayan** evidence ile destekler
— alternative açıklamalar (hardware-level determinism, single-threaded
VMM execution, measurement scope kararları) §6'da sistemli olarak ele
alınır. Bu mütevazılık paper'ın methodological contribution'ının bir
parçası, weakness değil.

---

# 6. Implications

## 6.1 For replay verdict interpretation

**Frozen.**

- Every replay verdict invoking Capability Separation must declare
  whether the cited operation falls within K_verified or K_extended.
  Operations in K_verified inherit L4.verified formal status;
  operations in K_extended carry the methodological-empirical
  position (§3.4.2).
- The theorem's contrapositive form ("observable equivalence ⟹
  capability divergence") is the consumer-facing claim. The stronger
  unconditional form (capability divergence holds regardless of
  observable equivalence) is a proof corollary, useful for
  internal reasoning but not the primary claim.

**Evolving.**

- Side-effect bound validation status (Q4, CST §5.1) — once Q4
  resolves, this entry's §5.1 disclosure may be updated to reflect
  the post-Q4 state (strict, narrow, or falsified).

## 6.2 For paper framing

**Frozen — citation conventions.**

- Theorem citations must include the K_verified / K_extended
  distinction at first mention.
- "score_S = 1.0000" or "N=998 determinism" citations must include
  Clopper-Pearson upper bound (§5.3).
- "*observable*(·)" function references must point to SOE entry
  §1.1, not to a paper section number (the vault-entry-relative
  convention).

**Frozen — forbidden framings.**

- ❌ "Capability Separation proves race-window-free seL4" — the
  theorem holds for K_verified categorically and K_extended
  empirically (different evidence statuses).
- ❌ "EXTp's framework guarantees side-effect-free intervention" —
  Q4 gap pending (§5.1).
- ❌ "Capability Separation extends to multi-VCPU traces" —
  A4 (in CST) fails under concurrent execution; this theorem
  operates under single-threaded VMM assumption inherited from
  same scope.

## 6.3 For Counterfactual Soundness Theorem

**Frozen — interface contract.**

CST consumes the following from Capability Separation:
- *Authority disjointness* (§2.3) — basis for A1 modularity in
  CST §3.2 (modulo Q4 side-effect gap)
- *K_verified external atomicity* (§3.4.1) — formal foundation
  for CST's no-race-window guarantee on verified scope
- *K_extended methodological extension* (§3.4.2) — empirical
  basis for CST's framework-level reasoning on VT-x operations

**Evolving — Q4 resolution path.**

If Q4 (CST §5.1) validates strict side-effect freedom, this
entry's §5.1 disclosure tightens to "strict A1 confirmed";
Capability Separation's authority bound becomes operationally
equivalent to strict side-effect freedom on framework
observables. If Q4 narrows or falsifies, CST envelope updates
correspondingly (CST §3.4.5).

---

# 7. Files

**Adjacent property entries (cross-referenced):**

- `Strong_Observational_Equivalence.md` — *observable*(·) function
  formalization (§1.1) used in §4.1 theorem statement; four-field
  surface (rip, exit_reason, exit_qual, rax) with RAX-only register
  scope-limitation
- `Measurement_Interference.md` — timing-domain detectability
  $\Delta^*$ used in CST's A3 confounder boundedness; complement
  to SOE's discrete observable surface
- `Counterfactual_Soundness_Theorem.md` — composes Capability
  Separation (A1), SOE (A2 4-tuple clause), MI (A2 timing clause
  + A3 confounder bound), and SOE+CrossBoot (A4 determinism) into
  causal attribution sufficiency

**Empirical antecedents (forthcoming):**

- `Cross_Boot_Stability_N34.md` — cross-boot N=34 × 100 trial
  replay reproducibility (used by SOE §4.2 and inherited by
  Capability Separation §4 empirical citations)
- `CST_Demonstration_Chronomaly.md` — Chronomaly-style race-window
  illustration, possibly elaborating the §3.5 case study in
  CST demonstration framing

**Build/verification references:**

- seL4 L4.verified proofs (Klein 2009, Klein et al. 2014;
  Trustworthy Systems versioned proof status for x86-64) — verify
  publication-time citation
- `KernelX86DangerousMSR=ON` build flag — research builds only;
  capability concession (cross-reference MI §5.1)

**Forward references:**

- Q4 modularity side-effect validation experiment (per §5.1 +
  CST §5.1) — forthcoming
- Paper text citation discipline per §6.2 — forthcoming
