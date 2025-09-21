# Dataset Analysis for Ancient Greek Artifact Restoration

This document provides a comprehensive analysis of potential datasets for the master's thesis project. Each entry is evaluated based on its suitability for training machine learning models for 2D inpainting and 3D shape completion, considering factors like data volume, quality, licensing, and accessibility.

---

## Tier 1: Primary Authoritative Databases & APIs

These are the most important sources. They combine world-class, academically-vetted collections with powerful, programmatic access (API/SPARQL) and clear, permissive licensing. Our data collection strategy should be built around these.

### 1. The Metropolitan Museum of Art Collection API
- **Link:** [https://metmuseum.github.io/](https://metmuseum.github.io/)
- **Rating:** ★★★★★ (For collection, license, and API quality)
- **Pros:** World-class collection, CC0 (Public Domain) license, excellent keyless REST API.
- **Cons:** None. This is the gold standard.
- **Verdict:** Primary source #1. We will start data collection here.

### 2. British Museum Collection (SPARQL)
- **Link:** [http://collection.britishmuseum.org/sparql](http://collection.britishmuseum.org/sparql)
- **Rating:** ★★★★★ (For data quality and query power)
- **Pros:** One of the world's most important collections, powerful SPARQL endpoint, academic data model (CIDOC CRM).
- **Cons:** Requires learning SPARQL, which has a steeper learning curve than a REST API.
- **Verdict:** Primary source #2. The query power is invaluable for a thesis.

### 3. Beazley Archive Pottery Database (BAPD)
- **Link:** [https://www.carc.ox.ac.uk/databases/bapd/](https://www.carc.ox.ac.uk/databases/bapd/)
- **Rating:** ★★★★★ (For academic focus and scope)
- **Pros:** The world's largest and most authoritative collection of Greek figure-decorated pottery. Extremely detailed metadata.
- **Cons:** No public API or bulk download. Requires web scraping.
- **Verdict:** Primary source #3 for metadata. We must scrape a subset of this for the invaluable, structured metadata which is not available anywhere else.

### 4. Corpus Vasorum Antiquorum (CVA)
- **Link:** [https://www.carc.ox.ac.uk/databases/cva/](https://www.carc.ox.ac.uk/databases/cva/)
- **Rating:** ★★★★☆ (For quality and structure)
- **Pros:** Foundational international resource, fully accessible online, high quality.
- **Cons:** Organized by "fascicules" (booklets), requires parsing to build a dataset.
- **Verdict:** Excellent supplemental source to the BAPD.

---

## Tier 2: High-Quality Museum APIs & Collections

These are essential sources with great collections and permissive licenses, but may have slightly less scope or more access friction than Tier 1.

### 5. Rijksmuseum API
- **Link:** [https://data.rijksmuseum.nl/object-metadata/api/](https://data.rijksmuseum.nl/object-metadata/api/)
- **Rating:** ★★★★☆ (For API quality and license)
- **Pros:** Excellent REST API, CC0 license, no key required for search.
- **Cons:** Smaller collection of Greek antiquities compared to the Met/British Museum.
- **Verdict:** A fantastic, easy-to-use source for high-quality images.

### 6. Harvard Art Museums API
- **Link:** [https://github.com/harvardartmuseums/api-docs](https://github.com/harvardartmuseums/api-docs)
- **Rating:** ★★★★☆ (For academic quality and API)
- **Pros:** High-quality, research-focused collection. Well-documented REST API.
- **Cons:** Requires an API key.
- **Verdict:** Essential academic source. High-priority target.

### 7. Getty Museum Open Content Program
- **Link:** [https://www.getty.edu/projects/open-content-program/](https://www.getty.edu/projects/open-content-program/)
- **Rating:** ★★★★☆ (For collection quality)
- **Pros:** World-class collection of antiquities at the Getty Villa. Clear open content policy.
- **Cons:** No public API for bulk download. Requires searching the online collection and downloading manually or via scraper.
- **Verdict:** A top-tier collection that is harder to access in bulk. We will target this for specific, high-quality examples.

---

## Tier 3: Major Aggregators

These platforms provide access to millions of objects from many institutions. They are powerful but require careful filtering.

### 8. Europeana API
- **Link:** [https://pro.europeana.eu/page/apis](https://pro.europeana.eu/page/apis)
- **Rating:** ★★★★☆ (For sheer volume)
- **Pros:** Massive aggregator of European collections. Single API to search thousands of institutions.
- **Cons:** Image licenses vary. Requires careful filtering of API results to only include permissively licensed works.
- **Verdict:** A potential firehose of data. A high-risk, high-reward option that must be explored with a focus on rights filtering.

### 9. Digital Public Library of America (DPLA)
- **Link:** [https://dp.la/](https://dp.la/)
- **Rating:** ★★★☆☆ (For US collections)
- **Pros:** The US equivalent of Europeana, aggregating collections from across the United States. Has a public API.
- **Cons:** Like Europeana, rights vary by object and require careful filtering.
- **Verdict:** A good source for accessing smaller US collections that we wouldn't target individually.

### 10. Wikimedia Commons
- **Link:** [https://commons.wikimedia.org/wiki/Category:Ancient_Greek_pottery](https://commons.wikimedia.org/wiki/Category:Ancient_Greek_pottery)
- **Rating:** ★★★☆☆ (For license and volume)
- **Pros:** Massive volume, clear CC/Public Domain licenses, has an API.
- **Cons:** Inconsistent metadata and image quality.
- **Verdict:** Excellent for quickly building a large, diverse, but potentially noisy dataset.

### 11. Flickr Commons
- **Link:** [https://www.flickr.com/commons](https://www.flickr.com/commons)
- **Rating:** ★★★☆☆ (For hidden gems)
- **Pros:** A huge number of public domain images contributed by cultural institutions worldwide.
- **Cons:** Search can be difficult. Not focused on academic metadata.
- **Verdict:** Worth exploring for unique images not found elsewhere.

---

## Tier 4: 3D Model Collections

Essential for the 3D completion pilot study.

### 12. Sketchfab
- **Link:** [https://sketchfab.com/search?q=greek+pottery&type=models](https://sketchfab.com/search?q=greek+pottery&type=models)
- **Rating:** ★★★★★ (For volume and accessibility)
- **Pros:** Vast, searchable platform with many downloadable CC-licensed models. Has an API.
- **Cons:** Quality and accuracy vary wildly. Requires careful vetting.
- **Verdict:** The single best place to start for 3D models.

### 13. Smithsonian Institution 3D Digitization
- **Link:** [https://3d.si.edu/](https://3d.si.edu/)
- **Rating:** ★★★★☆ (For quality and license)
- **Pros:** Extremely high-quality, research-grade scans. CC0 license.
- **Cons:** Limited collection of Greek pottery specifically.
- **Verdict:** Primary source for any high-quality 3D models we can find.

### 14. Ancient Greek Pottery Experimental 3D Dataset (CETI)
- **Link:** [http://www.ceti.gr/earthlab/pottery_dataset.html](http://www.ceti.gr/earthlab/pottery_dataset.html)
- **Rating:** ★★★★☆ (For research focus)
- **Pros:** A dataset created *specifically* for 3D retrieval research.
- **Cons:** Available "by request only".
- **Verdict:** High-priority target. A successful request could yield a perfect ground-truth dataset for our 3D pilot. I can draft an email for this.

---

## Conclusion and Recommendation

The investigation reveals that while there is no single, pre-packaged "download-and-go" dataset for this thesis, there is an immense wealth of high-quality, open-access data available through institutional APIs and collections. The challenge is not a lack of data, but the engineering effort required to collect, aggregate, and standardize it.

**This is an ideal scenario for a master's thesis, as the dataset creation is itself a significant research contribution.**

### Recommended Data Acquisition Strategy:

1.  **Focus on Pottery:** The data availability for Ancient Greek Pottery is exceptional. We will proceed with this as our artifact class, as recommended in the original project prompt.

2.  **Build a Core 2D Dataset via APIs (The "Big Three"):**
    *   **Start with the Met API:** Use a script to query and download all CC0 images of Greek pottery. This will be our foundational dataset.
    *   **Expand with the British Museum SPARQL Endpoint:** Write queries to get all relevant pottery images and their rich metadata. This will be technically challenging and a key part of the project.
    *   **Supplement with the Rijksmuseum & Harvard APIs:** Use these excellent, easy-to-use APIs to add more high-quality images.

3.  **Enrich with Metadata from BAPD:**
    *   Develop a targeted web scraper for the Beazley Archive. For each object in our image dataset, we will attempt to find its corresponding entry in the BAPD and extract the authoritative metadata. This fusion of high-res images (from museums) and high-quality metadata (from BAPD) will create a world-class dataset.

4.  **Bootstrap the 3D Pilot with Sketchfab:**
    *   Simultaneously, download 50-100 CC-licensed, well-modeled Greek pottery examples from Sketchfab. This is more than enough to begin prototyping our 3D completion models.

5.  **Perform Outreach for the CETI 3D Dataset:**
    *   I will draft a professional email to the contact person for the "Ancient Greek Pottery Experimental 3D Dataset". Acquiring this would be a major boost for the 3D portion of the thesis.

This strategy provides a clear, multi-pronged approach to building a unique, high-quality, and comprehensive dataset that will be the bedrock of the thesis. It balances quick wins (Met API) with significant but rewarding technical challenges (British Museum SPARQL, BAPD scraping).