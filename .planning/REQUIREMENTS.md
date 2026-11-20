# Requirements: SigmaLens for Tech4Bharat 2026

- **Project Identity:**
  - **Competition:** Tech4Bharat 2026 | Global Accelerator Vision Summit (JanAI Mass Entrepreneurship Challenge)
  - **Organizers:** Karnataka Arya Vysya Mahasabha (KAVM) in partnership with JanAI & RV College of Engineering
  - **Theme & Problem:** Theme 4: Manufacturing & Industry — Problem Statement 4.2: Defect Inspection
  - **Classification:** Applied AI System (Commodity Hardware Vision • Measured Performance)
  - **Field Origin:** Rural MSME Problem Inventory by Madan Padaki & JanAI Problem Set
  - **Solution:** SigmaLens — Edge-based Few-Shot Machine Vision & Auditable Quality Assurance Platform
  - **Team:** Team Strawhead — Abhijeet Dubey (CTO / Founder), Shiva Pandey (COO) & Keval Shinde (AI/ML & Edge Deployment Lead)

---

## 1. Problem Definition & Ecosystem Context
- **The Core Problem:** Manual visual inspection misses 10–15% of defects due to human eye fatigue within 30 minutes of continuous line work. High-end automated optical inspection (AOI) systems (Keyence, Cognex) cost upwards of ₹20,00,000 ($25,000) per line and require specialized vision engineers, locking small manufacturers out of Tier-1 supply chains.
- **Affected Population:** Micro, small, and medium enterprises (MSMEs) producing precision components, packaging materials, and textiles. Inspection is currently performed ad-hoc by whoever happens to be free on the line.
- **Economic Toll:** Rejected consignments, punitive debit notes/chargebacks (5–12% invoice haircuts), return freight costs, and disqualification from enterprise buyer vendor pools.
- **Stakeholders:**
  1. Line Workers & Supervisors (operating in tight spaces with varying shift skills)
  2. Buyer Quality Teams (demanding verifiable statistical proof of quality)
  3. Tier-1 Suppliers / Integrators (sourcing sub-assemblies from MSMEs)
  4. Testing & Certification Labs (providing periodic third-party audits)

---

## 2. Technical Hurdles ("What Makes It Hard")
1. **Defect Scarcity:** Small factories have no defect image banks. Collecting and labeling thousands of defect samples stops production and is economically infeasible.
2. **Uncontrolled Environments:** Factory lighting varies between 150 lux (cloudy/dawn) and 900+ lux (afternoon glare), with cramped physical footprints and vibration.
3. **Non-Expert Operators:** Shop-floor workers cannot tune neural hyperparameters, draw bounding boxes, or curate AI datasets.

---

## 3. Mandatory Boundaries
1. **Actual Inspection Reflection:** Every record in the system must map directly to an individual unit physically evaluated under the camera at line speed. No fabricated or interpolated batch records.
2. **Owner/Supervisor Sign-Off:** Every batch quality certificate and shift audit report must feature explicit owner/supervisor verification and digital sign-off before consignment dispatch.

---

## 4. Key Functional Requirements
- **FR-1 Few-Shot Baseline Learning:** Learn statistical tolerances from 20–30 golden good units in under 2 seconds. Zero defect images required.
- **FR-2 Real-Time Edge Inference:** <50ms per frame execution on standard webcams/smartphones directly inside the client browser.
- **FR-3 Adaptive Environmental Normalization:** Real-time CIELAB luminance equalization and spatial deskewing (±30°).
- **FR-4 Explainable Diagnostics:** Turbo colormap anomaly heatmaps with bounding-box quadrant localization.
- **FR-5 Auditable Compliance Reporting:** Auto-generated ISO 9001:2015 Conformance Certificates computing Yield Rate and $C_{pk}$ Process Capability Index with owner sign-off blocks.
- **FR-6 Shift Audit Logging:** Tamper-evident CSV and JSON export with unit timestamps, anomaly scores, and Pass/Fail statuses.
