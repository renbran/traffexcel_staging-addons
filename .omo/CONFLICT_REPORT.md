# Combined Projects Dashboard — Excel vs Odoo Staging Conflict Report
**Generated:** 2026-07-10  
**Source:** `/opt/merged-addons/.omo/Combined_Projects_Dashboard.xlsx`  
**Target:** Odoo staging (`staging.sgctech.ai` — `traffexcel_staging`)

---

## 1. Executive Summary

The Excel dashboard was built from **unzipped source documents** (contracts, invoices, bills, payment certificates). Odoo staging contains **database records** from the production import. These are fundamentally different data sources — the Excel counts **files on disk**, while Odoo counts **posted journal entries**.

### Critical Conflicts Requiring Human Decision

| # | Conflict Type | Severity | Action Needed |
|---|---|---|---|
| C-1 | Invoice amount mismatch (all projects) | 🔴 CRITICAL | Human must confirm which source is correct |
| C-2 | Bill amount mismatch (5 of 7 projects) | 🔴 CRITICAL | Human must confirm which source is correct |
| C-3 | Document count vs Odoo record count | 🟡 HIGH | Clarify: file count ≠ Odoo invoices |
| C-4 | Payment data missing in Odoo | 🔴 CRITICAL | 505 JE + 810 payments have no project link |
| C-5 | Client name mismatch (Project 2015, 4006, 2047) | 🟡 HIGH | Human must confirm correct client |
| C-6 | Project 2047 — no data in either source | 🟢 LOW | Confirm if project is active |

---

## 2. Project-Level Comparison

### Project 2006 — NCTC Souq Al Haraj

| Metric | Excel (Source Docs) | Odoo (Database) | Conflict? |
|---|---|---|---|
| Project Name | NCTC Souq Al Haraj | NCTC Souq Al Haraj | ✅ Match |
| Client | NCTC | NCTC | ✅ Match |
| Contract Value | Not verified | AED 7,878,906.00 | ⚠️ Excel says N/A |
| **Total Invoiced** | **AED 1,014,968.69** | **AED 7,878,906.47** | 🔴 **+676% difference** |
| **Total Bills** | **AED 417,741.12** | **AED 243,848.37** | 🔴 **-42% difference** |
| Invoice Doc Count | 40 files | 21 invoices | ⚠️ See C-3 |
| Bill Doc Count | 103 files | 9 bills | ⚠️ See C-3 |
| Payment In Docs | 12 files | 0 payments linked | 🔴 See C-4 |
| Payment Out Docs | 11 files | 0 payments linked | 🔴 See C-4 |
| Total Documents | 172 files | — | N/A |

**Decision needed (C-1, C-2):**  
- Excel total invoiced: AED 1,014,968.69 (from PDF files)  
- Odoo total invoiced: AED 7,878,906.47 (from posted invoices)  
- **Which number is correct for reporting?**

---

### Project 2015 — R1111-A Installation Jn47

| Metric | Excel | Odoo | Conflict? |
|---|---|---|---|
| Project Name | R1111-**A** Installation Jn47 | R1111_**A** Installation Jn47 | ⚠️ Hyphen vs Underscore |
| Client | **NCTC / Kapsch** | **NCTC** only | 🔴 **Client mismatch** |
| Contract Value | Not verified | AED 1,779,885.00 | ⚠️ |
| **Total Invoiced** | **AED 1,384,620.35** | **AED 6,042,327.81** | 🔴 **+336% difference** |
| **Total Bills** | **AED 270,366.92** | **AED 244,222.73** | 🟡 **-10% difference** |
| Invoice Doc Count | 43 files | 19 invoices | ⚠️ |
| Bill Doc Count | 32 files | 9 bills | ⚠️ |
| Payment In Docs | 16 files | 0 payments linked | 🔴 |
| Payment Out Docs | 28 files | 0 payments linked | 🔴 |

**Decisions needed (C-1, C-5):**  
- Is the client NCTC only, or NCTC/Kapsch?  
- Which invoiced amount is correct?

---

### Project 2033 — AMC Sharjah UTMC

| Metric | Excel | Odoo | Conflict? |
|---|---|---|---|
| Project Name | AMC Sharjah UTMC | AMC Sharjah UTMC | ✅ Match |
| Client | Transport Telematics (Kapsch) / SRTA | KAPSCH | ⚠️ Excel has more detail |
| Contract Value | Not verified | AED 1,916,398.00 | ⚠️ |
| **Total Invoiced** | **AED 820,124.00** | **AED 3,074,474.01** | 🔴 **+275% difference** |
| Total Bills | Not fully quantified | AED 0.00 | 🟡 |
| Invoice Doc Count | 39 files | 24 invoices | ⚠️ |
| Bill Doc Count | 1 file | 0 bills | ⚠️ |
| Payment In/Out | 0 each | 0 each | ✅ |

**Note:** Only 4 invoices (AED 2,055,523.58) show as "paid" in Odoo; 20 are "not_paid" (AED 1,018,950.43).

**Decision needed (C-1):**  
- Which invoiced amount is correct?

---

### Project 2034 — R_1903 Tunnels SRTA

| Metric | Excel | Odoo | Conflict? |
|---|---|---|---|
| Project Name | R_1903 Tunnels SRTA | R_1903 Tunnels SRTA | ✅ Match |
| Client | Kapsch | KAPSCH | ✅ Match (case only) |
| Contract Value | Not verified | AED 41,096,568.63 | ⚠️ |
| **Total Invoiced** | **AED 4,121,775.00** | **AED 37,704,543.63** | 🔴 **+815% difference** |
| **Total Bills** | **AED 4,364,990.53** | **AED 0.00** | 🔴 **All bills missing** |
| Total Paid | AED 1,468,101.64 | AED 0.00 | 🔴 |
| Total Receipts | AED 2,210,000.00 | AED 0.00 | 🔴 |
| Invoice Doc Count | 10 files | 6 invoices | ⚠️ |
| Bill Doc Count | 0 files | 0 bills | ✅ |

**Decisions needed (C-1, C-2, C-4):**  
- Massive invoice amount discrepancy (AED 4.1M vs AED 37.7M)  
- AED 4.36M in bills in Excel but zero in Odoo  
- AED 2.21M in receipts in Excel but zero in Odoo  
- **This project has the largest financial discrepancy**

---

### Project 4004 — RAK Tolling AMC

| Metric | Excel | Odoo | Conflict? |
|---|---|---|---|
| Project Name | RAK Tolling AMC | RAK Tolling AMC | ✅ Match |
| Client | KAPSCH | KAPSCH | ✅ Match |
| Contract Value | AED 3,240,000 | AED 1,678,740.00 | 🔴 **Contract value mismatch** |
| **Total Invoiced** | **AED 1,417,000.00** | **AED 825,720.00** | 🔴 **-42% difference** |
| **Total Bills** | **AED 184,730.00** | **AED 0.00** | 🔴 **All bills missing** |
| Total Paid | AED 102,830.00 | AED 0.00 | 🔴 |
| Invoice Doc Count | 66 files | 14 invoices | ⚠️ |
| Bill Doc Count | 11 files | 0 bills | 🔴 |

**Decisions needed (C-1, C-2):**  
- Contract value differs (AED 3.24M vs AED 1.68M)  
- Which invoiced amount is correct?

---

### Project 4006 — Damage Gantry Rectification

| Metric | Excel | Odoo | Conflict? |
|---|---|---|---|
| Project Name | Damage Gantry Rectification | Damage Gantry Rectification | ✅ Match |
| Client | **Transport Telematic Systems (TTS) / RAK PSD** | **KAPSCH** | 🔴 **Client mismatch** |
| Contract Value | Not verified | AED 1,260,000.00 | ⚠️ |
| Total Invoiced | AED 630,000.00 | AED 630,000.00 | ✅ **Match!** |
| **Total Bills** | **AED 91,350.00** | **AED 800,000.00** | 🔴 **+776% difference** |
| Invoice Doc Count | 2 files | 1 invoice | ⚠️ |
| Bill Doc Count | 1 file | 1 bill | ✅ |

**Decisions needed (C-2, C-5):**  
- Is the client TTS/RAK PSD or KAPSCH?  
- Which bill amount is correct?

---

### Project 2047 — R_1732_NCTC_JN51&52

| Metric | Excel | Odoo | Conflict? |
|---|---|---|---|
| Project Name | R_1732_NCTC_JN51**&**52 | R_1732_NCTC_JN51**and**52 | ⚠️ & vs and |
| Client | **Unknown** | **NCTC** | 🔴 **Client mismatch** |
| Status | No data - empty source folder | pending | ⚠️ |
| All financials | N/A | AED 0.00 | ✅ Both empty |

**Decision needed (C-6):**  
- Confirm client name (Unknown vs NCTC)  
- Is this project active or should it be removed?

---

## 3. Portfolio-Level Summary

| Metric | Excel Total | Odoo Total | Difference |
|---|---|---|---|
| **Total Invoiced** | **AED 9,388,488.04** | **AED 56,155,972.92** | **+498% (AED 46.7M gap)** |
| **Total Bills/POs** | **AED 5,329,178.57** | **AED 1,368,071.10** | **-74% (AED 3.96M gap)** |
| Total Paid | AED 1,974,467.29 | AED 0 (not tracked per project) | 🔴 |
| Total Receipts | AED 3,426,260.20 | AED 0 (not tracked per project) | 🔴 |

---

## 4. Document Count Comparison

| Project | Excel Invoices | Odoo Invoices | Excel Bills | Odoo Bills |
|---|---|---|---|---|
| 2006 | 40 | 21 | 103 | 9 |
| 2015 | 43 | 19 | 32 | 9 |
| 2033 | 39 | 24 | 1 | 0 |
| 2034 | 10 | 6 | 0 | 0 |
| 4004 | 66 | 14 | 11 | 0 |
| 4006 | 2 | 1 | 1 | 1 |
| 2047 | 0 | 0 | 0 | 0 |
| **Total** | **200** | **85** | **148** | **19** |

**Note:** Excel counts files (including sub-folders, payment certificates, supporting docs). Odoo counts posted `account_move` records. The Excel count is expected to be higher as it includes supporting documents, not just the actual invoices/bills.

---

## 5. Unlinked Records in Odoo

### 60 Customer Invoices — No Project Link
- **60 invoices** (AED ~2.4M) exist in Odoo but have `project_id = NULL`
- Partners: mostly partner_id 59 and 155
- These are likely **old invoices** from before project tracking was implemented

### 358 Vendor Bills — No Project Link  
- **358 bills** exist but have `project_id = NULL`
- Total: AED 7,505,978.68
- These cover ALL vendor bills, not just the 7 projects

### 505 Journal Entries — No Project Link
- **505 journal entries** (all posted) have `project_id = NULL`
- These are the accounting journal entries generated by invoices/bills

### 810 Payments — No Project Link
- **810 payment records** exist but `pdc_project_id = NULL`
- 189 inbound paid (AED 34.6M), 279 outbound paid (AED 5.1M)
- Payments exist but are NOT linked to projects

---

## 6. Decisions Required

### 🔴 CRITICAL (Must resolve before dashboard can be accurate)

**C-1: Invoice Amount Source of Truth**
- Excel extracted amounts from PDF files
- Odoo has amounts from posted invoices
- **Question:** Which source should be used for the dashboard?
- **Impact:** Affects all project financials

**C-2: Bill Amount Source of Truth**
- Excel has bill amounts from source documents
- Odoo has most bills unlinked to projects
- **Question:** Should bills be linked to projects in Odoo?
- **Impact:** Affects cost tracking per project

**C-4: Payment & Receipt Tracking**
- Excel has payment/receipt amounts per project
- Odoo has 810 payments with no project link
- **Question:** Should `account_payment.pdc_project_id` be populated?
- **Impact:** Affects outstanding balance calculations

### 🟡 HIGH (Important for data accuracy)

**C-3: Document Count Reconciliation**
- Excel counts files, Odoo counts invoices
- **Question:** Should the dashboard show file counts or Odoo invoice counts?
- **Recommendation:** Use Odoo counts (actual accounting records)

**C-5: Client Name Corrections**
| Project | Excel Client | Odoo Client | Correct? |
|---|---|---|---|
| 2015 | NCTC / Kapsch | NCTC | ? |
| 2033 | Transport Telematics (Kapsch) / SRTA | KAPSCH | ? |
| 4006 | Transport Telematic Systems (TTS) / RAK PSD | KAPSCH | ? |
| 2047 | Unknown | NCTC | ? |

### 🟢 LOW

**C-6: Project 2047 Status**
- No data in either source
- Client listed as "Unknown" in Excel, "NCTC" in Odoo
- **Question:** Is this project active? Should it be in the dashboard?

---

## 7. Recommendations

1. **For Invoice Amounts:** Use Odoo amounts (posted invoices) as source of truth, since these are the actual accounting records
2. **For Bills:** Link vendor bills to projects in Odoo using `project_id` field
3. **For Payments:** Populate `pdc_project_id` on `account_payment` records
4. **For Client Names:** Use Odoo partner names (consistent with accounting system)
5. **For Document Counts:** The Excel file count includes supporting documents; Odoo count is the actual invoice/bill count
6. **For Project 2047:** Confirm status before including in dashboard

---

*This report was generated by comparing the Excel dashboard against the Odoo staging database. All amounts are in AED unless otherwise noted.*
