# Citation Verification Report: Paper 3

**Paper**: `paper/paper3.tex` -- "SO(14) Unification: A Machine-Verified Algebraic Scaffold with Phenomenological Predictions"
**Date**: 2026-03-14
**Protocol**: citation-verification skill (INSPIRE-HEP, Semantic Scholar, CrossRef, arXiv, OpenAlex)
**Bibliography**: Inline `\bibitem` entries (35 citations total in `\begin{thebibliography}`)

---

## Part A: Per-Citation Verification Table

| # | Cite Key | Classification | API Source | DOI | Notes |
|---|----------|---------------|------------|-----|-------|
| 1 | `einstein1925` | UNVERIFIABLE | CrossRef (partial) | 10.1002/3527608958.ch30 (reprint) | Historical. Original 1925 Sitzungsberichte has no DOI. Reprint DOI exists. Existence confirmed. |
| 2 | `kaluza1921` | UNVERIFIABLE | CrossRef (not found) | None known | Historical. Original 1921 Sitzungsberichte pre-dates DOI system. Existence confirmed by standard physics reference. |
| 3 | `klein1926` | VERIFIED | CrossRef | 10.1007/BF01397481 | Z. Phys. 37, 895 (1926). All metadata matches. |
| 4 | `weinberg1967` | VERIFIED | INSPIRE + CrossRef | 10.1103/PhysRevLett.19.1264 | PRL 19, 1264 (1967). All metadata matches. DOI_MISSING in bib. |
| 5 | `glashow1961` | VERIFIED | INSPIRE + CrossRef | 10.1016/0029-5582(61)90469-2 | Nucl. Phys. 22, 579 (1961). All metadata matches. DOI_MISSING in bib. |
| 6 | `salam1968` | VERIFIED | INSPIRE + CrossRef | 10.1142/9789812795915_0034 | Conf. Proc. C 680519, 367 (1968). Metadata matches. The DOI is for the reprint in "Selected Papers of Abdus Salam" (1994). DOI_MISSING in bib. |
| 7 | `georgi1974` | VERIFIED | INSPIRE + CrossRef | 10.1103/PhysRevLett.32.438 | PRL 32, 438 (1974). All metadata matches. DOI_MISSING in bib. |
| 8 | `fritzsch1975` | VERIFIED | INSPIRE + CrossRef | 10.1016/0003-4916(75)90211-0 | Ann. Phys. 93, 193 (1975). All metadata matches. DOI_MISSING in bib. |
| 9 | `georgi1975` | VERIFIED | INSPIRE + CrossRef | 10.1063/1.2947450 | AIP Conf. Proc. 23, 575 (1975). All metadata matches. DOI_MISSING in bib. |
| 10 | `gursey1976` | VERIFIED | INSPIRE + CrossRef | 10.1016/0370-2693(76)90417-2 | Phys. Lett. B 60, 177 (1976). All metadata matches. DOI_MISSING in bib. |
| 11 | `langacker1981` | VERIFIED | INSPIRE + CrossRef | 10.1016/0370-1573(81)90059-4 | Phys. Rep. 72, 185 (1981). All metadata matches. DOI_MISSING in bib. |
| 12 | `dimopoulos1981` | VERIFIED | INSPIRE + CrossRef | 10.1103/PhysRevD.24.1681 | Phys. Rev. D 24, 1681 (1981). All metadata matches. DOI_MISSING in bib. |
| 13 | `nesti2007` | **METADATA_MISMATCH** | INSPIRE + CrossRef | 10.1088/1751-8113/41/7/075405 | **Cite key says 2007 but paper published 2008** (JPA 41, 075405, 2008). arXiv:0706.3307 submitted 2007, but journal year is 2008. Bib entry correctly says J. Phys. A 41, 075405 (2008) so the content is correct; only the cite key is misleading. |
| 14 | `nesti2010` | VERIFIED | INSPIRE + CrossRef | 10.1103/PhysRevD.81.025010 | PRD 81, 025010 (2010). All metadata matches. |
| 15 | `krasnov2018` | VERIFIED | INSPIRE + CrossRef | 10.1088/1361-6382/aac58d | CQG 35, 143001 (2018). All metadata matches. |
| 16 | `krasnov2022` | VERIFIED | INSPIRE + CrossRef | 10.1063/5.0070058 | JMP 63, 031701 (2022). All metadata matches. |
| 17 | `ida1980` | VERIFIED | INSPIRE + CrossRef | 10.1143/PTP.64.1745 | Prog. Theor. Phys. 64, 1745 (1980). All metadata matches. DOI_MISSING in bib. |
| 18 | `ma1981` | **METADATA_MISMATCH** | INSPIRE | None found | **Journal name wrong.** Bib says "Chinese Physics C" but INSPIRE shows journal "HEPNP" (High Energy Physics and Nuclear Physics / Gao Neng Wu Li Yu He Wu Li). "Chinese Physics C" is a different journal (the English-language journal, ISSN 1674-1137). The 1981 paper was published in the Chinese-language journal. Volume 5, pages 664 confirmed. No DOI found. |
| 19 | `wilczek1982` | VERIFIED | INSPIRE + CrossRef | 10.1103/PhysRevD.25.553 | PRD 25, 553 (1982). All metadata matches. DOI_MISSING in bib. |
| 20 | `lisi2007` | VERIFIED | INSPIRE | None (unpublished preprint) | arXiv:0711.0770. Confirmed as preprint, never journal-published. Metadata matches. |
| 21 | `distler2010` | **METADATA_MISMATCH** | INSPIRE + CrossRef | 10.1007/s00220-010-1006-y | **arXiv ID is WRONG.** Bib says arXiv:0904.1447, but that is Kapustin & Saulina, "Chern-Simons-Rozansky-Witten topological field theory" (completely unrelated). The correct arXiv ID is **0905.2658**. Title, journal, volume, pages all match. |
| 22 | `kawamura2010` | VERIFIED | INSPIRE + CrossRef | 10.1103/PhysRevD.81.075011 | PRD 81, 075011 (2010). All metadata matches. |
| 23 | `wilson2024` | **METADATA_MISMATCH** (severe) | INSPIRE + CrossRef | See notes | **Multiple errors.** (a) Title: bib says "Uniqueness of an E8 model of elementary particles" but the paper at JMP 63, 081703 is actually "Octions: An E8 description of the Standard Model" by **Manogue, Dray, and Wilson** (3 authors, not Wilson solo). DOI: 10.1063/5.0095484. (b) Wilson's actual "Uniqueness of an E8 model" paper is arXiv:2407.18279 (2024), an **unpublished preprint**, not JMP 63. (c) The cite key says 2024 but the bib entry says 2022. **All three metadata fields (title, authors, journal) are wrong for the JMP reference; the title belongs to the 2024 arXiv preprint.** |
| 24 | `wilson2024b` | **METADATA_MISMATCH** (severe) | INSPIRE | None (preprint) | **Title is WRONG.** Bib says "On the problem of interacting particles in theoretical physics" with arXiv:2407.18279, but INSPIRE confirms arXiv:2407.18279 has title "Uniqueness of an E8 model of elementary particles" (the title from citation #23). The paper "On the problem of interacting particles in theoretical physics" was NOT FOUND in any database (INSPIRE, Semantic Scholar, CrossRef). It may not exist, or may have a different arXiv ID. **Possible hallucination of the title, or a swap between citations 23 and 24.** |
| 25 | `bentov2016` | VERIFIED | INSPIRE + CrossRef | 10.1103/PhysRevD.93.065036 | PRD 93, 065036 (2016). All metadata matches. |
| 26 | `maru2025` | VERIFIED | INSPIRE | None (preprint) | arXiv:2503.12455 (2025). Confirmed as recent preprint by Maru & Nago. Title matches. Not yet published. |
| 27 | `candelas1985` | VERIFIED | CrossRef | 10.1016/0550-3213(85)90602-9 | Nucl. Phys. B 258, 46 (1985). All metadata matches. DOI_MISSING in bib. |
| 28 | `li1974` | VERIFIED | INSPIRE + CrossRef | 10.1103/PhysRevD.9.1723 | PRD 9, 1723 (1974). All metadata matches. DOI_MISSING in bib. |
| 29 | `michel1971` | VERIFIED | CrossRef | 10.1016/0003-4916(71)90079-0 | Ann. Phys. 66, 758 (1971). All metadata matches. DOI_MISSING in bib. |
| 30 | `slansky1981` | VERIFIED | INSPIRE + CrossRef | 10.1016/0370-1573(81)90092-2 | Phys. Rep. 79, 1 (1981). All metadata matches. DOI_MISSING in bib. |
| 31 | `freedman1976` | VERIFIED | INSPIRE + CrossRef | 10.1103/PhysRevD.13.3214 | PRD 13, 3214 (1976). All metadata matches. DOI_MISSING in bib. |
| 32 | `green1984` | VERIFIED | INSPIRE + CrossRef | 10.1016/0370-2693(84)91565-X | Phys. Lett. B 149, 117 (1984). All metadata matches. DOI_MISSING in bib. |
| 33 | `nath2007` | VERIFIED | INSPIRE + CrossRef | 10.1016/j.physrep.2007.02.010 | Phys. Rep. 441, 191 (2007). All metadata matches. DOI_MISSING in bib. |
| 34 | `superkamiokande2020` | VERIFIED | CrossRef | 10.1103/PhysRevD.102.112011 | PRD 102, 112011 (2020). All metadata matches. |
| 35 | `hyperkamiokande2018` | VERIFIED | INSPIRE | None (preprint) | arXiv:1805.04163 (2018). Confirmed as Hyper-Kamiokande Proto-Collaboration design report. Not journal-published (preprint only). Metadata matches. |
| 36 | `pdg2024` | VERIFIED | CrossRef | 10.1103/PhysRevD.110.030001 | PRD 110, 030001 (2024). Confirmed as PDG 2024 Review. |
| 37 | `demoura2021lean4` | VERIFIED | CrossRef | 10.1007/978-3-030-79876-5_37 | CADE-28, LNCS, pp. 625-635 (2021). All metadata matches. DOI_MISSING in bib. |
| 38 | `mathlib` | VERIFIED | CrossRef | 10.1145/3372885.3373824 | CPP 2020, pp. 367-381 (2020). All metadata matches. DOI_MISSING in bib. |
| 39 | `hales2017formal` | VERIFIED | CrossRef | 10.1017/fmp.2017.1 | Forum of Mathematics, Pi 5, e2 (2017). All metadata matches. DOI_MISSING in bib. |
| 40 | `commelin2022liquid` | **METADATA_MISMATCH** | CrossRef | 10.1515/dmvm-2022-0058 (Commelin article) | **Not a standard academic paper.** The bib entry says "Lean Community (2022)" but no paper with title "Completion of the liquid tensor experiment" exists. Commelin published a summary in Mitteilungen der DMV 30(3), 166-170 (2022), DOI 10.1515/dmvm-2022-0058. Scholze published "Liquid Tensor Experiment" in Experimental Mathematics 31(2), 349-354 (2022), DOI 10.1080/10586458.2021.1926016. **The bib entry conflates the community project completion announcement with a published paper. Consider citing Scholze 2022 or Commelin 2022 with correct metadata.** |
| 41 | `arnoldy2026cicm` | UNVERIFIABLE | N/A | None | Author's own paper, submitted to CICM 2026. Cannot verify via APIs. |
| 42 | `arnoldy2026aaca` | UNVERIFIABLE | N/A | None | Author's own paper, submitted to AACA. Cannot verify via APIs. |
| 43 | `arnoldy2026prl` | UNVERIFIABLE | N/A | None | Author's own paper, in preparation. Cannot verify via APIs. Note: cite key says "prl" but this is Paper 4 (LMP target per CLAUDE.md), not PRL. |
| 44 | `uft-github` | UNVERIFIABLE | N/A | None | Author's GitHub repository. Cannot verify via APIs. Software citation. |
| 45 | `jaffe2006` | UNVERIFIABLE | CrossRef (not found) | None found | Clay Millennium Prize problem statement. Not a standard journal publication. A common citation but no standard DOI. The year "2006" may refer to the reprint in "The Millennium Prize Problems" (AMS, 2006). The original problem statement was from 2000. Existence confirmed by the Clay Mathematics Institute website. |
| 46 | `humphreys1972` | VERIFIED | CrossRef | 10.1007/978-1-4612-6398-2 | Springer textbook (1972). ISBN: 978-0-387-90053-7. DOI_MISSING in bib. |

---

## Part B: Corrected .bib Entries

### CRITICAL FIXES (must address before submission)

#### Fix 1: `distler2010` -- Wrong arXiv ID

**Current (WRONG):**
```bibtex
\bibitem{distler2010}
J.~Distler and S.~Garibaldi,
``There is no `theory of everything' inside $E_8$,''
Commun.\ Math.\ Phys.\ \textbf{298}, 419 (2010)
[arXiv:0904.1447].
```

**Corrected:**
```bibtex
\bibitem{distler2010}
J.~Distler and S.~Garibaldi,
``There is no `theory of everything' inside $E_8$,''
Commun.\ Math.\ Phys.\ \textbf{298}, 419 (2010)
[arXiv:0905.2658].
```

**Severity: HIGH.** arXiv:0904.1447 is Kapustin & Saulina on Chern-Simons-Rozansky-Witten theory -- a completely unrelated paper. A reviewer following this link would find the wrong paper.

---

#### Fix 2: `wilson2024` -- Wrong title, wrong authors, wrong journal

**Current (WRONG):**
```bibtex
\bibitem{wilson2024}
R.~A.~Wilson,
``Uniqueness of an $\mathrm{E}_8$ model of elementary particles,''
J.\ Math.\ Phys.\ \textbf{63}, 081703 (2022).
```

**Problem:** JMP 63, 081703 (2022) is actually:
- **Title**: "Octions: An E8 description of the Standard Model"
- **Authors**: C.A. Manogue, T. Dray, and R.A. Wilson (3 authors)
- **DOI**: 10.1063/5.0095484

Wilson's solo paper "Uniqueness of an E8 model of elementary particles" is only an arXiv preprint (arXiv:2407.18279, July 2024), not published in JMP.

**Two possible corrections depending on which paper is actually being cited:**

**Option A** (if citing the 2022 JMP collaborative paper):
```bibtex
\bibitem{manogue2022}
C.~A.~Manogue, T.~Dray, and R.~A.~Wilson,
``Octions: An $E_8$ description of the Standard Model,''
J.\ Math.\ Phys.\ \textbf{63}, 081703 (2022)
[arXiv:2204.05310].
```

**Option B** (if citing Wilson's 2024 solo preprint on uniqueness):
```bibtex
\bibitem{wilson2024}
R.~A.~Wilson,
``Uniqueness of an $\mathrm{E}_8$ model of elementary particles,''
arXiv:2407.18279 (2024).
```

**Severity: CRITICAL.** The current entry attributes a 3-author paper to one author, gives the wrong title, and assigns a published journal reference to an unpublished preprint. A reviewer checking JMP 63, 081703 would find a different paper by different authors with a different title.

---

#### Fix 3: `wilson2024b` -- Title does not match arXiv ID

**Current (WRONG):**
```bibtex
\bibitem{wilson2024b}
R.~A.~Wilson,
``On the problem of interacting particles in theoretical physics,''
arXiv:2407.18279 (2024).
```

**Problem:** arXiv:2407.18279 has the title "Uniqueness of an E8 model of elementary particles" (confirmed by INSPIRE). The title "On the problem of interacting particles in theoretical physics" was NOT FOUND in any academic database (INSPIRE, Semantic Scholar, CrossRef). It may be a hallucinated title, or it may exist under a different arXiv ID.

**Corrected (if the intent is to cite arXiv:2407.18279):**
```bibtex
\bibitem{wilson2024b}
R.~A.~Wilson,
``Uniqueness of an $\mathrm{E}_8$ model of elementary particles,''
arXiv:2407.18279 (2024).
```

**But this creates a duplicate with `wilson2024` (Fix 2, Option B).** The two Wilson citations need to be disentangled. Based on context in the paper:
- `wilson2024` (Sec. 5.1, future directions): cites Wilson for discrete order-3 elements, centralizer SU(9)/Z_3 -- this is content from the "Uniqueness" preprint (2407.18279)
- `wilson2024b` (Sec. 5.1, chirality): cites Wilson for argument that non-compact degrees of freedom serve as mass parameters -- this content may be in a different Wilson paper

**Recommendation:** Ian must manually identify which Wilson paper(s) contain these specific claims and provide correct references.

**Severity: CRITICAL.** One of these two citations likely has a fabricated or swapped title.

---

### MODERATE FIXES

#### Fix 4: `ma1981` -- Wrong journal name

**Current:**
```bibtex
\bibitem{ma1981}
Z.-Q.~Ma, D.-S.~Du, P.-Y.~Xue, and X.-J.~Zhou,
``Generation problem and $\mathrm{SO}(14)$ grand unified theories,''
Chinese Physics C \textbf{5}, 664 (1981).
```

**Corrected:**
```bibtex
\bibitem{ma1981}
Z.-Q.~Ma, T.-S.~Tu (D.-S.~Du), P.-Y.~Xue, and X.-J.~Zhou,
``Generation problem and $\mathrm{SO}(14)$ grand unified theories,''
High Energy Physics and Nuclear Physics (Gao Neng Wu Li Yu He Wu Li)
\textbf{5}, 664 (1981).
```

**Notes:** "Chinese Physics C" (ISSN 1674-1137) is the modern English-language journal. The 1981 paper was published in the Chinese-language journal "High Energy Physics and Nuclear Physics" (HEPNP, ISSN 0254-3052), which was later renamed. INSPIRE also lists author "Tu, Tung-sheng" rather than "Du, Dongsheng" -- these may be alternate romanizations. No DOI available.

**Severity: MODERATE.** Journal name is wrong; a reviewer familiar with Chinese physics journals would notice.

---

#### Fix 5: `commelin2022liquid` -- Not a standard publication

**Current:**
```bibtex
\bibitem{commelin2022liquid}
J.~Commelin \textit{et al.},
``Completion of the liquid tensor experiment,''
Lean Community (2022).
```

**Problem:** No paper with this exact title exists. The project completion was announced as a community event. Two related published papers exist:

**Option A** (cite Scholze's published account):
```bibtex
\bibitem{scholze2022liquid}
P.~Scholze,
``Liquid tensor experiment,''
Experimental Mathematics \textbf{31}, 349 (2022),
doi:10.1080/10586458.2021.1926016.
```

**Option B** (cite Commelin's summary article):
```bibtex
\bibitem{commelin2022liquid}
J.~Commelin,
``Liquid tensor experiment,''
Mitteilungen der DMV \textbf{30}, 166 (2022),
doi:10.1515/dmvm-2022-0058.
```

**Severity: MODERATE.** Current entry cites a non-existent publication. Either Scholze or Commelin's actual paper should be cited.

---

## Part C: Severity Summary

```
VERIFIED:             26 citations
METADATA_MISMATCH:     5 citations
  - distler2010:       arXiv ID wrong (0904.1447 -> 0905.2658)
  - wilson2024:        Title, authors, and journal ALL wrong
  - wilson2024b:       Title does not match arXiv ID (possible hallucination)
  - ma1981:            Journal name wrong (Chinese Physics C -> HEPNP)
  - commelin2022liquid: Paper does not exist in cited form
NOT_FOUND:             0 citations
HALLUCINATED:          0 citations (wilson2024b title is suspect but needs manual check)
MISATTRIBUTED:         0 citations
UNVERIFIABLE:          6 citations
  - einstein1925:      Historical, pre-dates DOI system
  - kaluza1921:        Historical, pre-dates DOI system
  - arnoldy2026cicm:   Author's own, submitted
  - arnoldy2026aaca:   Author's own, submitted
  - arnoldy2026prl:    Author's own, in preparation
  - uft-github:        Software/GitHub
  - jaffe2006:         Clay Millennium problem statement (non-standard publication)
DOI_MISSING:          19 citations (see Part D)
```

**Action items by severity:**

1. **CRITICAL (fix before submission):**
   - `distler2010`: Change arXiv ID from 0904.1447 to 0905.2658
   - `wilson2024`: Disentangle from wilson2024b. Identify correct paper and fix title/authors/journal
   - `wilson2024b`: Verify which Wilson paper contains the cited claims. "On the problem of interacting particles" not found in any database.

2. **MODERATE (fix before submission):**
   - `ma1981`: Change "Chinese Physics C" to "High Energy Physics and Nuclear Physics" (or "Gao Neng Wu Li Yu He Wu Li")
   - `commelin2022liquid`: Replace with Scholze 2022 or Commelin 2022 published reference

3. **LOW (improve quality):**
   - Add DOIs to 19 citations (see Part D)
   - `nesti2007`: Cite key implies 2007 but journal year is 2008 (cosmetic)
   - `arnoldy2026prl`: Cite key says "prl" but project docs say target is LMP (cosmetic)

---

## Part D: DOI Patch

The following citations have verified DOIs that are missing from the bibliography. Add these to improve the bibliography quality:

```
weinberg1967:       doi:10.1103/PhysRevLett.19.1264
glashow1961:        doi:10.1016/0029-5582(61)90469-2
salam1968:          doi:10.1142/9789812795915_0034
georgi1974:         doi:10.1103/PhysRevLett.32.438
fritzsch1975:       doi:10.1016/0003-4916(75)90211-0
georgi1975:         doi:10.1063/1.2947450
gursey1976:         doi:10.1016/0370-2693(76)90417-2
langacker1981:      doi:10.1016/0370-1573(81)90059-4
dimopoulos1981:     doi:10.1103/PhysRevD.24.1681
ida1980:            doi:10.1143/PTP.64.1745
wilczek1982:        doi:10.1103/PhysRevD.25.553
candelas1985:       doi:10.1016/0550-3213(85)90602-9
li1974:             doi:10.1103/PhysRevD.9.1723
michel1971:         doi:10.1016/0003-4916(71)90079-0
slansky1981:        doi:10.1016/0370-1573(81)90092-2
freedman1976:       doi:10.1103/PhysRevD.13.3214
green1984:          doi:10.1016/0370-2693(84)91565-X
nath2007:           doi:10.1016/j.physrep.2007.02.010
demoura2021lean4:   doi:10.1007/978-3-030-79876-5_37
mathlib:            doi:10.1145/3372885.3373824
hales2017formal:    doi:10.1017/fmp.2017.1
humphreys1972:      doi:10.1007/978-1-4612-6398-2
klein1926:          doi:10.1007/BF01397481
```

**Citations that already have DOIs in the bibliography (confirmed correct):**
```
nesti2007:          10.1088/1751-8113/41/7/075405 (implicit from journal ref)
nesti2010:          10.1103/PhysRevD.81.025010
krasnov2018:        10.1088/1361-6382/aac58d
krasnov2022:        10.1063/5.0070058
kawamura2010:       10.1103/PhysRevD.81.075011
bentov2016:         10.1103/PhysRevD.93.065036
distler2010:        10.1007/s00220-010-1006-y
superkamiokande2020: 10.1103/PhysRevD.102.112011
pdg2024:            10.1103/PhysRevD.110.030001
```

Note: The bibitem format in the paper does not include explicit DOI fields, but the journal references are sufficient for PRD/REVTeX style. Adding DOIs would still improve machine-readability and reviewer verification.

---

## Verification Methodology

Each citation was queried against at least one (usually two) of the following APIs:
- **INSPIRE-HEP**: `https://inspirehep.net/api/literature?q=...` (primary for HEP papers)
- **CrossRef**: `https://api.crossref.org/works/...` (primary for DOI verification)
- **Semantic Scholar**: `https://api.semanticscholar.org/graph/v1/paper/search?...` (fallback)
- **arXiv**: `http://export.arxiv.org/api/query?...` (for preprints)

All API queries were performed live on 2026-03-14. No classifications were made based on training data alone.

---

## Wilson Citation Diagnosis

The Wilson situation requires manual intervention. Here is the diagnosis:

**What exists (verified):**
1. Manogue, Dray, Wilson, "Octions: An E8 description of the Standard Model", JMP 63, 081703 (2022), DOI:10.1063/5.0095484, arXiv:2204.05310
2. Wilson (solo), "Uniqueness of an E8 model of elementary particles", arXiv:2407.18279 (2024), unpublished preprint

**What the paper cites:**
- `wilson2024`: Wilson, "Uniqueness of an E8 model", JMP 63, 081703 (2022) -- CONFLATES papers #1 and #2
- `wilson2024b`: Wilson, "On the problem of interacting particles", arXiv:2407.18279 (2024) -- Title NOT FOUND in any database; arXiv ID belongs to paper #2

**What the paper text claims these citations support:**
- `wilson2024` (used in Sec. 5.1): "Wilson identifies discrete order-3 elements of E8 whose centralizer SU(9)/Z_3 provides a fundamentally discrete three-generation symmetry" -- This claim is in the "Uniqueness" preprint (arXiv:2407.18279)
- `wilson2024b` (used in Sec. 5.1): "Wilson argues that for theories with explicitly non-zero masses, this no-go theorem does not apply---the non-compact degrees of freedom serve as mass parameters rather than ghosts" -- This claim needs manual verification for which Wilson paper contains it

**Recommended action:** Ian must:
1. Determine which Wilson paper contains the "mass parameters rather than ghosts" argument
2. Split the citations properly: one for the SU(9)/Z_3 content (arXiv:2407.18279) and one for the ghost/mass argument
3. Remove the false JMP 63 reference from the "Uniqueness" paper
4. If citing the Octions paper, add it as a separate citation with correct authorship

---

*Report generated by citation-verification protocol. All classifications based on live API queries, not training data.*
