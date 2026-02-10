# Q1 Quote Sourcing Audit — Consolidated Review Artifact

## Document Information

- **Project**: Devotional Generator
- **Type**: Audit
- **Date**: 2026-02-07
- **Auditor**: AI: Claude Code (read-only analysis)
- **Reviewer**: Human: Barbara
- **Status**: PENDING HUMAN REVIEW
- **Authoritative Source Path**: `/Users/tradingwithpython/dev/claude-projects/projects/inactive-projects/devotional-generator`
- **Q1 Decision (Iteration 3)**: "Classical evangelical authors sourced from open-source websites identified in the devotional-generator project. Attribution is required and must be in Turabian format."

---

## 1. Findings — What Exists Today

### 1.1 Source Websites Identified

Six websites were selected and documented across `docs/FINAL_REPORT.md`, `docs/SEARCH_SUMMARY.md`, and `data/found_pdfs_complete.csv`:

| # | Site | URL | Role | Works Attributed | Notes |
|---|------|-----|------|------------------|-------|
| 1 | **Internet Archive** | `https://archive.org` | Primary source (96% of catalog) | 233 | URL pattern: `archive.org/details/[normalized-title-author]`; quality varies (OCR to high-quality scans) |
| 2 | **SpurgeonGems.org** | `https://www.spurgeongems.org` | Spurgeon specialty | 4 verified | Modern typeset PDFs; e.g., `spurgeongems.org/chs_matthew.pdf` |
| 3 | **Monergism.com** | `https://www.monergism.com` | Reformed/Puritan theology | 5 verified | Clean PDFs, ePub, Mobi; Pink, Hopkins, Calvin |
| 4 | **WesleyScholar.com** | `https://wesleyscholar.com` | Wesley family works | Unquantified | Searchable PDFs, modern formatting |
| 5 | **CCEL.org** | `https://www.ccel.org` | Christian Classics Ethereal Library | Unquantified | HTML + PDF; Calvin, Wesley, Edwards, Pink |
| 6 | **Grace-eBooks.com / GraceGems.org** | `https://grace-ebooks.com` / `https://gracegems.org` | Secondary | Unquantified | Clean PDFs; Pink, Spurgeon |

**How these were selected:** Through ad-hoc web searches during the January 21, 2026 research session. No formal evaluation rubric was applied. Sites were rated informally by coverage breadth and PDF formatting quality (star ratings in `FINAL_REPORT.md`). No per-site usage terms were reviewed or documented.

### 1.2 Author Selection Criteria

**Method used:** A 1,439-page bibliography PDF (77.8 MB) was exported from Logos Bible Software and parsed by `scripts/parse_bibliography.py`. The script extracted entries matching **17 author last names** via string pattern matching, producing `data/classical_authors.csv` with 565 entries.

**The 17 cataloged authors and entry counts:**

| Author | Entries | Author | Entries |
|--------|---------|--------|---------|
| Wesley (John & Charles) | 138 | Owen | 25 |
| Spurgeon (C. H.) | 92 | Luther | 17 |
| Calvin | 57 | Watson | 9 |
| Henry (Matthew) | 52 | Baxter | 6 |
| Edwards (Jonathan) | 46 | Rutherford | 6 |
| Law (William) | 37 | Whitefield | 5 |
| Pink (A. W.) | 35 | Fletcher | 3 |
| Bunyan (John) | 31 | Hopkins (Ezekiel) | 3 |
| | | Sibbes | 3 |

**Criteria for labeling these authors "acceptable":** None were formally documented. The authors appear to have been selected based on:

1. **Pre-existence in the Logos library** — the list reflects what was already owned, not a curated theological assessment
2. **Assumed public domain status** — all are pre-20th-century figures, though this was stated as an observation ("works published before 1928 are universally in public domain") rather than verified per-work
3. **Implicit theological alignment** — described collectively as "classical evangelical" in project docs, but no definition of what "classical evangelical" means was recorded
4. **No exclusion criteria** — no documented reasons for why certain historical Christian authors were omitted

**Critical gap in name matching:** The script matched on last name substrings, causing false positives:
- "Charles, Robert Henry" matched to "Henry" category
- "Comfort, Philip Wesley" matched to "Wesley" category
- Works *about* classical authors (e.g., modern commentaries) were captured alongside works *by* them

### 1.3 What the Output Actually Used

The completed 28-day devotional (`personal_devotional.md`) contains 28 quotes from **22 distinct authors**. Cross-referencing against the cataloged 17 authors reveals a major disconnect:

| # | Author Quoted | In Catalog? | Era | Theological Tradition | PD Status (US) |
|---|---------------|-------------|-----|----------------------|----------------|
| 1 | George Muller | No | 1805-1898 | Evangelical (Plymouth Brethren) | Public domain |
| 2 | R. A. Torrey | No | 1856-1928 | Evangelical | Public domain |
| 3 | **Ralph Waldo Emerson** | No | 1803-1882 | **Transcendentalist / Unitarian** | Public domain |
| 4 | A. W. Tozer (x2) | No | 1897-1963 | Christian & Missionary Alliance | **Under copyright** |
| 5 | C. H. Spurgeon | Yes | 1834-1892 | Baptist / Reformed | Public domain |
| 6 | Oswald Chambers | No | 1874-1917 | Holiness movement | **2000 compilation under copyright** |
| 7 | Blaise Pascal | No | 1623-1662 | Catholic (Jansenist) | Public domain (translation may not be) |
| 8 | John Henry Newman | No | 1801-1890 | Anglican then Catholic cardinal | Public domain |
| 9 | George Fox | No | 1624-1691 | Quaker founder | Public domain (1976 edition?) |
| 10 | Brother Lawrence | No | 1614-1691 | Catholic (Carmelite) | Public domain (1977 translation?) |
| 11 | Andrew Murray | No | 1828-1917 | Dutch Reformed | Public domain |
| 12 | Jeanne Guyon | No | 1648-1717 | Catholic contemplative | Public domain (1975 translation?) |
| 13 | **Richard J. Foster** | No | 1942-present | **Quaker** | **Under copyright (1978)** |
| 14 | **John Ortberg** | No | 1957-present | **Presbyterian** | **Under copyright (1997)** |
| 15 | Samuel Chadwick | No | 1860-1932 | Methodist | Public domain |
| 16 | **Dietrich Bonhoeffer** | No | 1906-1945 | Lutheran | **Translation (1963) under copyright** |
| 17 | Hannah Whitall Smith | No | 1832-1911 | Quaker / Holiness | Public domain |
| 18 | Henry Ward Beecher | No | 1813-1887 | Congregationalist | Public domain |
| 19 | Thomas a Kempis | No | 1380-1471 | Catholic (Augustinian) | Public domain (1989 translation?) |
| 20 | S. Hall Young | No | 1847-1927 | Presbyterian | Public domain |
| 21 | **Francesco Petrarch** | No | 1304-1374 | **Renaissance humanist** | Public domain (1982 translation?) |
| 22 | **C. S. Lewis** (x3) | No | 1898-1963 | Anglican | **Under copyright** |
| 23 | **Leonard Ravenhill** | No | 1907-1994 | Holiness / Revival | **Under copyright** |
| 24 | Augustine of Hippo | No | 354-430 | Church Father | Public domain — **but quote unverified (see footnote 27)** |

**Summary:** Of 22 authors quoted, **only 1** (Spurgeon) appears in the cataloged author list. At least **8 authors** have works under copyright. At least **3** (Emerson, Petrarch, and arguably Guyon/Newman) fall outside any reasonable definition of "classical evangelical."

### 1.4 Attribution and Turabian Format

Turabian note-bibliography style is used in the footnotes section of `personal_devotional.md`. Example:

> ^5 Charles H. Spurgeon, "Hannah's Heart-Song," in *The Metropolitan Tabernacle Pulpit*, vol. 35 (London: Passmore & Alabaster, 1889), 565.

The format is correctly applied across 27 of 28 footnotes, with structured elements: author, title, editor/translator (where applicable), publication location, publisher, year, and page number.

**Exception — footnote ^27:**
> "Augustine of Hippo, attributed, though not directly verified in extant works. The sentiment reflects Augustinian theology regarding hope and transformation."

This is an explicitly **unverified attribution** in published output.

### 1.5 Verification Infrastructure vs. Actual Use

| Asset Built | Purpose | Used in Output? |
|-------------|---------|-----------------|
| `data/classical_authors.csv` (565 entries) | Bibliography catalog from Logos | No — output quotes 21 authors not in it |
| `data/found_pdfs_complete.csv` (242 works) | Free PDF URLs for 17 classical authors | No — no evidence quotes were checked against PDFs |
| `quotes.csv` (351 entries) | Batch search results across 5 themes | No — 0 high-confidence results; search found theme *mentions*, not usable quotes |
| `scripts/batch_quote_search.py` | Parallel theme search | Ran once; produced low-quality results not used for output |
| `scripts/quote_search.py` | Single-theme search | Test only |

**The verification pipeline was built but never connected to the content generation step.** The 28 quotes in the devotional appear to have been selected by the AI from its training knowledge, not extracted from verified local/online sources.

---

## 2. Risks and Gaps

### HIGH Severity

| ID | Risk | Evidence | Impact |
|----|------|----------|--------|
| **RISK-1** | **Copyright infringement in publish-ready output** | 8+ of 28 quotes from copyrighted authors (Tozer, Lewis x3, Foster, Ortberg, Bonhoeffer, Ravenhill, Chambers). Several cite specific editions published after 1928. | DMCA takedown, KDP account suspension, legal liability. Blocks publish-ready path entirely. |
| **RISK-2** | **Unverified / potentially fabricated quotes** | Footnote ^27 explicitly admits the Augustine quote is unverified. No other quotes were confirmed against source documents. Project rule (`claude.md`): "No generated quotes — extract from local/online resources." | Credibility destruction if a fabricated quote is published. Violates the project's own integrity rules. |
| **RISK-3** | **Verification infrastructure is disconnected from output** | 242 PDFs cataloged, batch search tooling built, but none of it gates or informs the actual quote selection. The AI generated quotes from memory, bypassing the entire verification system. | The entire quote sourcing process documented in Q1 is theater — it exists on paper but did not govern the output. |

### MEDIUM Severity

| ID | Risk | Evidence | Impact |
|----|------|----------|--------|
| **RISK-4** | **Theological curation drift** | Emerson (Unitarian), Petrarch (Renaissance humanist), Guyon (Catholic mystic), Newman (Catholic cardinal) included despite "classical evangelical" specification. | Misaligns with stated audience/positioning. Could confuse or alienate evangelical readers. |
| **RISK-5** | **No formal author inclusion/exclusion criteria** | The 17-author list was derived from Logos library contents, not a theological or legal assessment. No definition of "classical evangelical" recorded. | Any future AI session will repeat the same drift — no gating criteria exist to enforce the Q1 decision. |
| **RISK-6** | **Specific-edition copyright risk for public domain authors** | Several quotes cite modern translations/editions (Pascal trans. Trotter 1958; Brother Lawrence trans. Delaney 1977; Guyon trans. 1975; a Kempis trans. Creasy 1989). Original text may be PD, but the cited translation may not be. | Even "public domain" authors become copyright risks when modern translations are quoted verbatim. |

### LOW Severity

| ID | Risk | Evidence | Impact |
|----|------|----------|--------|
| **RISK-7** | **"Open-source websites" is imprecise terminology** | Q1 decision uses "open-source" (a software licensing term) to mean "freely accessible." No per-site usage terms were documented. | Could lead to incorrect assumptions about commercial republication rights. |
| **RISK-8** | **False positives in author catalog** | Name-matching on last name captures works about/referencing the classical authors, not just works by them. | Inflates catalog counts; low practical impact since catalog was not used for output. |

---

## 3. Ranked Recommendations

### Tier 1 — MUST (blocks publish-ready output if unresolved)

**R1. Create a human-verified Author Whitelist**

Produce a controlled artifact (`author-whitelist.csv` or equivalent) with:
- Author full name, birth year, death year
- Theological tradition (e.g., Reformed Baptist, Wesleyan Methodist, Anglican)
- Classification: `classical-evangelical | evangelical-adjacent | excluded`
- Public domain status (US): `yes (pre-1929)` | `no` | `conditional (original PD, check translation)`
- Approved for publish-ready: `yes | no | human-review-required`
- Rationale for inclusion/exclusion

This artifact must be **human-approved** (Barbara). AI cannot make copyright or theological alignment determinations for publication purposes.

**R2. Restrict publish-ready quotes to verified public domain works**

For any output with `output_mode: publish-ready`:
- Block all quotes from authors whose works are under copyright unless fair use analysis or written permission is documented (human-only legal concern)
- Block all quotes citing post-1928 translations/editions unless the specific edition is confirmed public domain
- Personal-use output may use broader sourcing but must still track copyright status

**R3. Require source-level verification before export**

Every quote in publish-ready output must have:
- `source_document`: specific PDF/URL where the quote text was confirmed
- `source_page`: page number or section reference
- `text_match`: confirmed exact or acknowledged modernization
- `verification_status`: one of `unverified | source_identified | text_confirmed | human_approved`

Export must be blocked for any quote with status below `text_confirmed`. The existing `found_pdfs_complete.csv` catalog is the starting point, but must be extended to cover all whitelisted authors.

### Tier 2 — SHOULD (significantly improves quality and auditability)

**R4. Define "classical evangelical" formally**

Document the inclusion criteria as a product-intent decision (human-required):
- **Era:** e.g., authors active before 1950 (aligns roughly with public domain and "classical" framing)
- **Tradition:** e.g., Protestant evangelical, Reformed, Wesleyan, Holiness, Puritan
- **Exclusions:** e.g., Unitarian, Transcendentalist, Catholic (unless broadly claimed by Protestants like Augustine)
- **Edge cases:** how to handle figures like Augustine, Luther, Pascal, Bonhoeffer who are widely quoted in evangelical contexts but belong to other traditions

**R5. Build a pre-verified Quote Catalog**

Replace the current "search-at-generation-time" approach with a curated database:
- Fields: `quote_id`, `quote_text`, `author`, `source_work`, `edition`, `page`, `public_domain_status`, `theme_tags[]`, `verification_status`, `turabian_note`
- Target size: 300+ verified quotes (covers 180 days with margin for rotation)
- Source: extract from the 242 cataloged PDFs, verify text against originals
- This catalog becomes the **exclusive source** for publish-ready quote selection

**R6. Document per-site usage terms**

For each of the 6 identified source websites, record:
- Terms of service URL and access date
- Whether content is explicitly public domain, Creative Commons, or other license
- Any restrictions on commercial use or republication
- Any attribution requirements beyond standard Turabian citation

### Tier 3 — NICE (improves maintainability and data model)

**R7. Add structured Turabian fields to the data model**

Phase 001 schema should include:

```
quote:
  text: string
  author: string
  source_title: string
  publication_info: string   # publisher, location
  year: integer
  page: string               # page, section, or URL
  public_domain: boolean
  verification_status: enum  # unverified | source_identified | text_confirmed | human_approved
  turabian_note: string      # computed/formatted
```

**R8. Connect verification tooling to the generation pipeline**

Refactor so that:
- Quote selection draws from the verified Quote Catalog (R5), not AI memory
- The batch search tooling (`batch_quote_search.py`) is repurposed to index the catalog by theme
- A validation step checks every quote against the catalog before PDF export

---

## 4. Proposed Document Updates (Not Applied)

### PRD (`docs/projects/devotional-generator/prd.md`)

| Section | Current Text | Proposed Change |
|---------|-------------|-----------------|
| Q1 row (line 295) | "Classical evangelical authors from identified open-source websites; Turabian attribution required" | "Classical evangelical authors from a **human-approved author whitelist**, sourced from **websites hosting public domain works**. Quotes restricted to **verified public domain editions** for publish-ready output. Turabian attribution required. All quotes require **source-level verification** before export." |
| Assumption #1 (line 315) | "Quotes: Classical evangelical authors from identified open-source websites; Turabian attribution required" | Add: "Governed by author whitelist (human-verified); publish-ready output restricted to copyright-cleared, source-verified quotes only." |
| FR-1.2 (line 193) | "All 5 elements present for each day" | Add new FR-1.4: "Quote Verification Gate — No publish-ready export permitted unless all quotes have `verification_status = human_approved` and `public_domain = true`." |
| Decisions table | No entry for author criteria | Add D006: "Quote sourcing governed by human-approved author whitelist with public domain verification. AI may not select quotes from memory or uncataloged sources." |
| Constraints | No quote-sourcing constraint | Add: "Quotes must be selected exclusively from the verified Quote Catalog. AI-generated or AI-recalled quotes are prohibited." |

### Iteration 3 Artifact (`docs/system/outputs/2026-02-07__02__planner__open-questions-q1-q13-final.md`)

| Section | Proposed Change |
|---------|-----------------|
| Q1 Risks (line 44-47) | Add: "The personal-use output (Jan 2026) demonstrated that without an enforced whitelist, the AI selects authors outside the intended scope — including copyrighted, non-evangelical, and unverified sources. The Q1 decision requires operationalization through an author whitelist and quote catalog, not just a policy statement." |
| Q1 Affected Artifacts (line 49-55) | Add: "New artifact required: `author-whitelist.csv` (human-verified). New artifact required: `quote-catalog.csv` (pre-verified quotes with Turabian metadata). Phase 004 validation must enforce whitelist and catalog compliance." |
| Cross-Cutting Risks table (line 503-510) | Add row: "Unverified quotes in output \| Q1 \| Fabricated or misattributed quotes undermine credibility \| Quote Catalog with mandatory source verification; export gate on verification_status" |
| Cross-Cutting Risks table | Add row: "Copyright violation from post-1928 authors \| Q1 \| Legal liability, KDP account risk \| Author whitelist with PD status; publish-ready restricted to PD-confirmed quotes" |

### New Artifacts Needed (not yet created)

| Artifact | Purpose | Owner |
|----------|---------|-------|
| `author-whitelist.csv` | Curated, human-approved list of acceptable quote authors with PD status and theological classification | Human: Barbara (approve); AI: Claude Code (draft) |
| `quote-catalog.csv` | Pre-verified quotes with full Turabian metadata, source document references, and verification status | AI: Claude Code (build); Human: Barbara (approve) |
| `site-usage-terms.md` | Per-site documentation of licensing/usage terms for the 6 identified source websites | Human: Barbara (verify legal); AI: Claude Code (draft) |

---

## What to Keep

- **Turabian citation format** — well-chosen, executed correctly in the output
- **Archive.org as primary source** — comprehensive, reliable, genuinely public domain
- **The source website priority list** (Archive.org > author-specific sites > CCEL > fallback)
- **The found_pdfs_complete.csv catalog** — solid foundation, needs connection to the output pipeline
- **The batch search tooling** (scripts, grep-based approach) — efficient, just needs to be integrated

## What Must Remain Human-Verified

- Author whitelist: theological alignment classification
- Copyright/public domain determination for each author's works
- Per-site usage terms for commercial republication
- Any quote by a post-1928 author (copyright risk)
- The Augustine footnote ^27 and any similar unverified attributions
- Final approval of all quotes before publish-ready export

---

## End of Artifact

This audit was performed as read-only analysis. No project files were modified. All proposed changes are documented above for human review and approval before application.
