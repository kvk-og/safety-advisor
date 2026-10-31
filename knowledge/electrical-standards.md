# Electrical Safety Standards — Australia / New Zealand (Mining & Industrial)

**Purpose:** Precise, citable reference for a Telegram safety-advisor bot serving WA industrial/mining workers.
**Currency note:** Status of every standard is stated (CURRENT / SUPERSEDED / WITHDRAWN) as verified against Standards Australia, SAI Global / Intertek Inform, and regulator guidance. Where a clause number could not be verified against an authoritative source it is marked `[clause unverified]` — do not cite it as fact.
**Last verified:** 31 October 2026.

---

## 1. AS/NZS 3000:2018 — Electrical installations (the "Wiring Rules")

- **Number / year:** AS/NZS 3000:2018 — *Electrical installations (known as the Australian/New Zealand Wiring Rules)*
- **Status:** **CURRENT** (6th edition). Published 26 June 2018; supersedes AS/NZS 3000:2007.
- **Amendments in force:** Amd 1:2020, Amd 2:2021, Amd 3:2023, Rul 1:2024 (all published by Standards Australia — confirm latest amendment before citing a specific clause).
- **Committee:** EL-001 (Wiring Rules). Joint SA / SNZ standard.
- **Structure note:** Two-part document. Part 1 = essential safety/performance requirements; Part 2 (Sections 2–8) = "deemed to comply" installation practices.

### Key parts (verified clause/section numbers)

| Topic | Clause/Section | Note |
|---|---|---|
| Fundamental principles (control & isolation, electric shock) | **Section 1.5** | 1.5.2 Control and isolation; 1.5.3 Protection against electric shock |
| Additional protection by RCDs (fundamental principle) | **Clause 1.5.6** | |
| Control of the installation — isolation & switching | **Section 2.3** | 2.3.2 Common control requirements; 2.3.3 Main switches; 2.3.4 Additional isolating switches; 2.3.5 Emergency switching/stopping; 2.3.6 Mechanical-maintenance isolation |
| Isolating switches — locking in OFF | **Clause 2.3.2.2** | Isolator may only indicate OFF when contacts are physically open; must be capable of being **locked in the OFF position** |
| **RCD protection (additional protection)** | **Section 2.6** | Core RCD requirements |
| RCD selection — type (AC / A / B) | **Clause 2.6.2.2.2** | As amended by Amd 2:2021. **Type AC RCDs must not be newly installed** after the 24-month transitional period following Amd 2 (i.e. from 30 April 2023); Type A (or B) required. Type A recommended as the general type. |
| RCDs must interrupt all active conductors | **Clause 2.6.2.2.2** | As a minimum |
| RCD requirements for installations (30 mA) | **Clause 2.6.3** | 2.6.3.2.2 domestic/residential (30 mA); 2.6.3.2.5 alterations & switchboard replacement |
| Protection against fire hazard due to arcing faults (AFDDs) | **Section 2.9** | Arc Fault Detection Devices |
| Segregation of wiring systems / voltage levels | **Clause 3.9.8** | Segregation of cables of different installations & voltage levels; 3.9.8.2.1 segregation within common enclosures |
| **Earthing** | **Section 5** | Earthing arrangements, MEN system |
| Earthing conductors | Clause 5.5 | |
| Equipotential bonding | Clause 5.6 | |
| Earth fault-loop impedance / disconnection times | Clause 5.7 | |
| **Verification (inspection & testing)** | **Section 8** | Pre-commissioning verification |

**Key concepts for the bot:**
- **Earthing:** MEN (Multiple Earthed Neutral) / TN-C-S system (Section 5). Protective earthing + equipotential bonding + earth fault-loop impedance/disconnection times are the fault-protection backbone.
- **RCDs:** additional protection is 30 mA for socket-outlet/final subcircuits in most installations; Type A is the default, Type AC is banned for new installs (Amd 2:2021); Type B required where DC residual currents can occur (EV chargers, PV inverters, VSDs).
- **Isolation:** isolating switches must provide visible, lockable OFF (2.3.2.2); emergency switching and mechanical-maintenance isolation are distinct functions (2.3.5, 2.3.6).
- **Segregation:** cables of different installations/voltage levels must be segregated (3.9.8).

> Clause numbers above were verified against the Standards Australia full-text table of contents and Amd 2:2021 amendment text (ERAC/regulator sources). Sub-clause detail below section level (e.g. specific earthing-conductor sizing clauses within 5.5) is NOT verified here — cite at section/clause level only.

---

## 2. AS/NZS 3012:2019 — Electrical installations on construction & demolition sites

- **Number / year:** AS/NZS 3012:2019 — *Electrical installations — Construction and demolition sites*
- **Status:** **CURRENT** (5th edition). Reissued incorporating Amendment No. 1 (March 2020); reaffirmed (R2026).
- **Scope:** Design, construction and testing of electrical installations supplying construction/demolition sites, and in-service testing of portable, transportable and fixed electrical equipment on those sites. To be read with AS/NZS 3000.
- **Key requirements (verified):**
  - Construction/demolition site equipment and RCDs have their own test/tag regime (see AS/NZS 3760 notes and the **3-month retest interval** for construction sites).
  - Uses a **Class H Portable Residual Current Device (PRCD)** socket-outlet assembly with integral 30 mA RCD + MCB overcurrent protection (definition verified in 2010 preview; confirm wording in 2019 ed.).
  - RCD **push-button tests** on construction sites: portable RCDs **daily / before each use**; fixed RCDs monthly `[interval clause unverified — treat as guidance]`.
  - RCD operating-time test results on construction sites must be recorded and retained for a minimum of **5 years** (SafeWork SA guidance; note this is regulator guidance, not a 3012 clause).

> Specific 2019 clause numbers for RCD/PRCD requirements were not extracted from the full text — mark `[clause unverified]` when citing beyond the definitions/scope above.

---

## 3. AS/NZS 3017:2022 — Electrical installations, verification by inspection & testing

- **Number / year:** AS/NZS 3017:2022 — *Electrical installations — Verification by inspection and testing*
- **Status:** **CURRENT** (4th edition). Published 2 December 2022; supersedes AS/NZS 3017:2007.
- **Committee:** EL-001 (Wiring Rules).
- **Scope:** Inspection and test methods to demonstrate that low-voltage installations comply with safety requirements (shock & fire prevention), including installations on an MEN (TN-C-S) earthing system.
- **Relationship to 3000:** AS/NZS 3000 Section 8 requires installations be inspected & tested before service; AS/NZS 3017 provides the methods.
- **Content (verified TOC):** Section 1 Scope; 2 Test equipment; 3 Visual inspection; 4 Testing installations; 5 Installation test records; App A/B.
- **Tests commonly cited:** earth continuity, insulation resistance, polarity/correct circuit connections, RCD trip time, earth fault-loop impedance, prospective short-circuit current (PSC).

> Specific sub-clause numbers for individual tests are `[clause unverified]` — reference the Section-level TOC above.

---

## 4. AS/NZS 3760:2022 — In-service safety inspection & testing of electrical equipment (test & tag)

- **Number / year:** AS/NZS 3760:2022 — *In-service safety inspection and testing of electrical equipment and RCDs*
- **Status:** **CURRENT**. Full revision replacing AS/NZS 3760:2010 (title now explicitly includes RCDs).
- **Scope:** In-service inspection/testing of LV electrical equipment, cord sets, extension leads, power boards (EPODs) and RCDs. **Does not cover** medical equipment or construction/demolition sites (AS/NZS 3012 applies there).

### Retest intervals (verified against SafeWork SA guidance table — authoritative)

**Equipment (Class I & Class II, cord sets, cord extension sets, EPODs):**

| Environment | Interval |
|---|---|
| Factories, workshops, manufacturing/assembly/maintenance/fabrication | **6 months** |
| Equipment/cord subject to flexing in normal use OR hostile environment | **12 months** |
| NOT subject to flexing, NOT open to abuse, NOT hostile (e.g. fixed office) | **5 years** |
| Residential-type areas (hotels, motels, halls, hostels, accommodation) | **2 years** |
| Commercial cleaning equipment | **6 months** |
| Hire equipment | **3 months** (test & tag); inspection before hire |
| Repaired / serviced / second-hand | After repair/service or on reintroduction to service |

**RCDs:**

| RCD type | Push-button test (by user) | Operating-time + push-button test |
|---|---|---|
| Portable | Daily / before each use (hostile row 1); 3 months (rows 2–3) | 12 months (rows 1–2); 2 years (row 3) |
| Fixed | 6 months | 12 months (rows 1–2); 2 years (row 3) |

- **Construction & demolition sites (under AS/NZS 3012):** **3-month** equipment retest interval.
- **Mining / industrial sites:** mining and heavy-industrial environments are typically treated as a hostile/high-risk environment; WA industry practice commonly applies a **3-month** interval. Treat the 3-month mining figure as industry guidance, not a 3760 clause `[clause unverified]`.
- **Competent person:** 2022 edition tightened the definition — knowledge "should be maintained" (not merely "updated") with an understanding of electrical risk.
- **Records:** durable, non-reusable, non-metallic tag required; record must include tester, test date, result, next retest date.

> Retest-interval tables above are well-corroborated by multiple regulator/industry sources, but the authoritative source is AS/NZS 3760:2022 Table 4 (itself). Where the bot cites an interval, phrase as "per AS/NZS 3760:2022" rather than a specific clause number unless verified.

---

## 5. AS/NZS 4836:2023 — Safe working on or near LV (and ELV) electrical installations & equipment

- **Number / year:** AS/NZS 4836:2023 — *Safe working on or near low-voltage and extra-low voltage electrical installations and equipment*
- **Status:** **CURRENT** (3rd edition). Published 3 March 2023; supersedes AS/NZS 4836:2011.
- **Note on title:** 2023 edition adds **extra-low voltage (ELV)** to the title (the 2011 edition was LV only). Verify the exact title when quoting.
- **Scope:** Principles, guidelines and procedures for safe work by electrical AND non-electrical workers on or near LV and ELV installations/equipment (a.c. and d.c.). Manages hazards of **arc blast, arc flash, electric shock and electrocution** (verified — Standards Australia product summary).

### Key concepts (verified)

- **The safe work hierarchy — de-energise / isolate / lock out first:** Work is carried out de-energised (isolated and locked out) unless it is not reasonably practicable to do so; energised work is the exception, requiring a risk assessment and Safe Work Method Statement (SWMS).
- **"Electrically safe work condition":** established by isolating, locking/tagging, proving de-energised, and (where relevant) earthing. The exact clause number for the step-by-step isolation sequence is `[clause unverified]`.
- **Proving dead:** test instrument against a known source → test the isolated conductors → re-test instrument against known source ("prove-test-prove").
- **500 mm work zone:** within 500 mm of exposed LV/ELV live parts is classified as "work on" (definition verified via standard text; clause 1.4.16/1.4.18 definitions, Figure 2.2).
- **Bonding conductors when isolating at remote locations / induced-voltage risk:** **Clause 3.1.6** (verified via WorkSafe QLD "Guide for isolation and lockout procedures").
- **Safety observer** — Clause 4.2 (verified via text).
- **Definitions of voltage bands:** ELV = not exceeding 50 V a.c. / 120 V ripple-free d.c.; LV = exceeding ELV up to 1000 V a.c. / 1500 V d.c. (verified, clause 1.4.41).

### Arc-flash / arc-blast
- AS/NZS 4836:2023 is the primary AU/NZ standard that names **arc flash and arc blast** as hazards to be managed (alongside shock/electrocution), through hierarchy-of-controls, PPE selection (arc-rated clothing) and working-distance/work-zone concepts. Specific arc-flash incident-energy calculation is not prescribed in 4836 (that is normally via IEEE 1584 / NFPA 70E); 4836 provides the safe-working framework. Mark specific arc-flash clause numbers `[clause unverified]`.

---

## 6. Mining-specific electrical standards

> **Major 2025 change:** The AS/NZS 3007 and AS/NZS 4871 series have been **amalgamated and superseded** by a new consolidated standard, **AS/NZS 5368:2025**. A bot advising WA mine workers must reference 5368:2025 as current, and flag 3007/4871 as superseded.

### 6a. AS/NZS 5368:2025 — Electrical equipment in mines and quarries (NEW, consolidated)

- **Number / year:** AS/NZS 5368:2025 — *Electrical equipment in mines and quarries*
- **Status:** **CURRENT**. Published 27 June 2025. Committee EL-023.
- **Supersedes:** AS/NZS 3007:2013 **and** all parts of AS/NZS 4871 (1–6), amalgamating them into one document (verified — Standards Australia preface).
- **Scope:** Design, installation, operation and maintenance of electrical plant/equipment at mining & quarrying operations, including fixed plant, transportable/mobile plant, hazardous areas, HV transmission, and static-electricity control.
- **Structure (verified from preview):**
  - Section 1 — General requirements
  - Section 2 — Fixed equipment and installations (overhead lines, substations, distribution cables, conveyors, winding systems, etc.)
  - Section 3 — Transportable and mobile plant (mobile substations, reeling/trailing cables, mobile machines, DCBs/Jumbo boxes, etc.)
  - Hazardous-area electrical equipment included.
- Note: does **not** provide guidance on hand-held/portable equipment.

### 6b. AS/NZS 3007:2013 — Electrical equipment in mines and quarries (SUPERSEDED)

- **Status:** **SUPERSEDED** (superseded date 27 June 2025, by AS/NZS 5368:2025).
- **Title:** *Electrical equipment in mines and quarries — Surface installations and associated processing plant.*
- Covered design/installation/operation of electrical plant at surface mining & quarrying operations, surface of underground mines, and processing plants. Now folded into 5368.

### 6c. AS/NZS 4871 series — Electrical equipment for mines and quarries (SUPERSEDED)

- **Status:** **SUPERSEDED** in full by AS/NZS 5368:2025.
- **Parts (verified):**
  - Part 1 (AS/NZS 4871.1:2012) — General requirements
  - Part 2 (AS/NZS 4871.2:2010) — Distribution, control and auxiliary equipment
  - Part 3 (AS/NZS 4871.3:2010) — Substations
  - Part 4 (AS/NZS 4871.4:2010) — Mains-powered electrical mobile machines
  - Part 5 (AS/NZS 4871.5:2010) — Battery-powered electrical mobile machines
  - Part 6 (AS/NZS 4871.6:2013) — Diesel-powered machinery and ancillary equipment

### 6d. AS/NZS 2290 series — Electrical equipment for coal mines (mostly SUPERSEDED / restructured)

- **AS/NZS 2290.1:2014** — *Introduction, inspection and maintenance, Part 1: For hazardous areas.*
  - **Status:** **SUPERSEDED** by **AS 2290.1:2021** (note: the replacement is now an **Australian-only** "AS" standard, not joint AS/NZS).
- **AS 2290.1:2021** — *Electrical equipment for coal mines — Introduction, inspection and maintenance, Part 1: Hazardous areas.* **CURRENT.**
  - Covers inspection/maintenance of explosion-protected (Ex) electrical equipment and cables in underground coal-mine hazardous areas. Referenced by QLD/NSW coal-mine recognised standards for routine testing of Ex plant.
- **AS/NZS 2290.2-1989** — *Maintenance and overhaul, Part 2: Overhaul of electrical equipment for hazardous areas.* **SUPERSEDED** (now covered within AS 2290.1:2021).
- **AS/NZS 2290.3:2018** — *Introduction, inspection and maintenance, Part 3: Gas detecting and monitoring equipment.* **CURRENT** (reissued incorporating Amd 1: October 2019). Sets inspection/calibration requirements for gas detection & monitoring equipment in coal mines.

> **Summary for the bot:** For coal-mine hazardous-area Ex equipment, cite **AS 2290.1:2021** (current). For gas monitoring equipment, cite **AS/NZS 2290.3:2018** (current). The older AS/NZS 2290.1:2014 and 2290.2-1989 are superseded/withdrawn.

---

## 7. Cross-cutting topics (as they appear in these standards)

### Isolation / Lock-out Tag-out (LOTO)
- **AS/NZS 3000:2018** Cl 2.3.2.2 — isolating switches must be lockable in OFF (installation-level isolation).
- **AS/NZS 4836:2023** — the primary safe-working standard: de-energise → isolate → lock/tag → prove dead → (earth where required) → re-verify. Safety observer (Cl 4.2); bonding of isolated conductors at remote locations (Cl 3.1.6).
- Regulator guidance (WorkSafe QLD, WorkSafe WA/DMIRS) operationalises the isolation steps; the bot should present the "de-energise, isolate, lock, tag, prove dead" hierarchy as the default and treat energised work as exceptional.

### RCD requirements (recap)
- **AS/NZS 3000:2018** Section 2.6 — additional protection; 30 mA; **Type A default, Type AC banned for new installs** (Amd 2:2021, effective 30 Apr 2023); Type B for DC-residual-risk circuits.
- **AS/NZS 3760:2022** — in-service RCD testing intervals (see §4 table).
- **AS/NZS 3012:2019** — construction-site PRCD 30 mA + daily/monthly push-button testing; 3-month equipment retest.

### Arc flash / arc blast
- **AS/NZS 4836:2023** — names arc flash/arc blast as hazards to manage via hierarchy of controls and PPE (arc-rated).
- **AS/NZS 3000:2018** Section 2.9 — Arc Fault Detection Devices (AFDDs) for fire protection from arcing faults (distinct from personnel arc-flash PPE).

---

## 8. Citation index

| Standard | Year | Status | Key cited clauses/sections |
|---|---|---|---|
| AS/NZS 3000 | 2018 | CURRENT (Amd 3:2023) | §1.5, 1.5.6, §2.3 (2.3.2.2), §2.6 (2.6.2.2.2, 2.6.3), §2.9, Cl 3.9.8, §5 (5.5–5.7), §8 |
| AS/NZS 3012 | 2019 | CURRENT (R2026) | scope + PRCD/RCD definitions; specific clauses `[unverified]` |
| AS/NZS 3017 | 2022 | CURRENT | §1–5 (TOC); individual tests `[unverified]` |
| AS/NZS 3760 | 2022 | CURRENT | retest interval tables (Table 4) |
| AS/NZS 4836 | 2023 | CURRENT | Cl 1.4.41 (voltage bands), Cl 3.1.6, Cl 4.2, 500 mm work zone; isolation sequence `[unverified]` |
| AS/NZS 5368 | 2025 | CURRENT | §1–3 (consolidated mines/quarries) |
| AS/NZS 3007 | 2013 | SUPERSEDED (by 5368:2025) | — |
| AS/NZS 4871.1–.6 | 2010–2013 | SUPERSEDED (by 5368:2025) | — |
| AS 2290.1 | 2021 | CURRENT | hazardous-area Ex inspection/maintenance |
| AS/NZS 2290.1 | 2014 | SUPERSEDED (by AS 2290.1:2021) | — |
| AS/NZS 2290.2 | 1989 | SUPERSEDED | — |
| AS/NZS 2290.3 | 2018 | CURRENT (Amd 1:2019) | gas detection/monitoring |

### Sources (authoritative)
- Standards Australia Store / product pages & previews (store.standards.org.au)
- Intertek Inform / SAI Global (infostore.saiglobal.com)
- Standards Australia full-text AS/NZS 3000:2018 (TOC & Amd 2:2021 text)
- ERAC Advisory Note (RCD Clause 2.6.3.2.5)
- SafeWork SA — Inspection & testing of electrical equipment (AS/NZS 3760:2022 intervals)
- WorkSafe QLD — Guide for isolation and lockout procedures (references AS/NZS 4836 Cl 3.1.6)
- Resources Safety & Health Queensland / NSW Resources (coal-mine recognised standards referencing AS 2290.1:2021)
- Standards New Zealand (standards.govt.nz)
