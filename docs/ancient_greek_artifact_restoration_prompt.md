# Ancient Greek Artifact Restoration — Giant Prompt for an AI Collaborator

> **Purpose:** This markdown is a single, exhaustive instruction package for an AI collaborator. Use it to gather datasets (2D and 3D), build a historically-constrained restoration pipeline, integrate NLP-derived constraints (typology, inscriptions, provenance), run experiments (2D inpainting + 3D completion pilot), and produce deliverables for an MSc-level project (6 months). This doc contains EVERYTHING the human researcher and earlier analysis provided: feasibility, scope decision rules, prioritized datasets, concrete scripts and commands, modeling choices, validation plans, ethical constraints, outreach email templates, evaluation metrics, and a week-by-week schedule.

---

## TL;DR — brutal summary the AI must obey

- **Project goal (single sentence):** Produce historically-plausible digital restorations of a narrowly-scoped class of Ancient Greek artifacts (recommendation: Attic red-figure pottery) using multimodal ML (NLP + diffusion + 3D completion) with explicit constraints and archaeologist validation.
- **Hard constraints:** always label outputs as *speculative reconstruction*; include provenance & citation; enforce typology rules (shape proportions, motif placement); keep a human-in-the-loop vetting step.
- **Scope rule (non-negotiable):** Choose **one** artifact class. If data ≥500 curated images + some 3D scans → proceed. If not, pivot to coins or dataset-release deliverable.
- **MSc deliverable (6 months):** dataset (\~500–2k images), trained 2D inpainting model, 3D photogrammetry pilot (10–30 objects), expert blind evaluation, thesis + demo.

---

# Instruction to the AI collaborator — act like a ruthless project manager

1. **Immediately ask the human (Bill) which scope they lock** — `"pottery"` or `"coins"`. If no reply in 24 hours, default to **Attic red-figure pottery**.
2. **Prioritize data acquisition**: collect Met API images, Smithsonian 3D models (CC0), Sketchfab CC models, Wikimedia Commons images, and Beazley Archive metadata (BAPD) — respectfully scrape or contact CARC for bulk. Build local dataset ASAP.
3. **Run NLP pipeline first** to extract structured attributes from labels/texts (shape, period, motif, dimensions, condition, inscriptions). This JSON will be the canonical conditioning object per artifact.
4. **Produce synthetic training pairs** by masking real images (handles, rims, painted panels) to supervise inpainting. Generate 5–20 variants per image.
5. **Train a 2D inpainting diffusion model** (Stable Diffusion base + fine-tune LoRA/DreamBooth) with ControlNet edge conditioning. Also prepare an exemplar nearest-neighbor baseline.
6. **Run a 3D pilot** using photogrammetry on 10–30 objects or convert CC models to point clouds. Try Point-E/PoinTr for quick conditional completion experiments. Keep 3D minimal.
7. **Validation:** run blind tests with archaeologists (n≥3) on plausibility; compute LPIPS/SSIM for synthetic ground-truth tasks and Chamfer distance for 3D where possible.
8. **Produce deliverables:** cleaned dataset + metadata, training code, model weights, evaluation results, an interactive web UI for expert corrections, and a 10–15 minute demo.

Be transparent about risk: any final outputs must include a provenance block listing which textual sources and exemplar images influenced the generation.

---

# Full project context (copied & condensed from initial research + analysis)

- **Feasibility:** AI can *produce visually plausible reconstructions* (coins, vases, and certain 3D shapes), but **historical accuracy** is hard: models hallucinate. Existing studies show success in coin restoration (GANs) and in 3D point-cloud completion when class variability is controlled. Generative models must be constrained by typology and expert validation.

- **Main bottlenecks:** (1) Data scarcity (esp. 3D scans), (2) copyright/legal access to museum photos, (3) risk of hallucination and misrepresentation.

- **Path to success:** narrow scope, build/clean dataset, embed typology rules (knowledge graph), and perform robust archaeologist validation. Combine NLP (to extract constraints from texts & labels) + diffusion models + 3D completion techniques.

---

# Prioritized artifact classes — choose exactly one

1. **Attic painted pottery (red-figure / black-figure)** — recommended: lots of curated corpus (Beazley Archive), clear typology (kylix, krater, amphora), many museum images.
2. **Coins (Greek / Hellenistic)** — easiest data availability, 2D flatness simplifies the task, many examples to train on.
3. **Marble portrait busts & small sculptures** — harder; geometry varies a lot; more 3D-focused.

**Decision policy:** If you can scrape or secure ≥500 curated images of one class (and ideally 100+ 3D scans or photogrammetry of replicas), proceed. Otherwise, pivot to coins or dataset paper.

---

# Data sources & rapid access commands

> **Note:** Always respect licenses. Prefer Met & Smithsonian (open), Wikimedia (varied CC), Sketchfab (filter CC-licensed), and contact Beazley/other museums for bulk access.

### Quick API examples (run on your machine)

**Met Museum (public-domain images & metadata)**

```bash
# Search objects in Greek Dept with keyword krater
curl "https://collectionapi.metmuseum.org/public/collection/v1/search?departmentId=13&q=krater" | jq .
# Get object JSON (replace OBJECTID)
curl "https://collectionapi.metmuseum.org/public/collection/v1/objects/OBJECTID" | jq .
```

**Smithsonian 3D**

- Browse [https://3d.si.edu](https://3d.si.edu) and download CC0 models directly via website. Use polite scraping only if API access is unavailable.

**Sketchfab (CC models)**

- Use the Sketchfab API to search for CC-licensed models with query `Greek pottery` or `krater` and filter by license.

**Wikimedia Commons**

- Use the MediaWiki API to query images by category (e.g., `Category:Attic_vases`).

**Beazley Archive (BAPD)**

- Beazley is authoritative for Attic pottery; bulk scraping may be disallowed — email CARC / Beazley for permission to use images & metadata in research.

**Perseus / Scaife / PHI inscriptions**

- Use the Perseus/Scaife APIs for ancient text retrieval (Pausanias, Pliny, etc.). Use PHI for epigraphic corpora (check license).

---

# NLP: the non-optional backbone (exact tasks to implement)

Implement the following pipeline in code. Every artifact receives a canonical JSON record after NLP processing.

### 1) Metadata extraction & normalization

- Scrape museum captions (Met JSON fields like `objectName`, `title`, `objectDate`, `medium`, `dimensions`).
- Normalise shape names: map synonyms to canonical tokens (e.g., `kylix`, `kylikes`, `cup` → `kylix`). Use a CSV ontology.

**Output JSON example:**

```json
{
  "id": "met_12345",
  "shape": "krater",
  "period": "5thC_BCE",
  "technique": "red-figure",
  "motifs": ["warrior", "chariot"],
  "dimensions": {"height_cm": 45, "diameter_cm": 60},
  "image_urls": ["..."]
}
```

### 2) Attribute extraction (NER & classifiers)

- Fine-tune a small transformer (XLM-R / mBERT or equivalent) on **modern language** museum captions to extract `motif`, `condition`, `inscription_text`, `provenance`.
- For **ancient-Greek** textual sources, use CLTK + AGDT/PROIEL treebanks for tokenization/lemmatization before any downstream NER.

### 3) Inscriptions pipeline (if present)

- If object has inscriptions, transcribe text (OCR manual), encode via EpiDoc standards, and add to JSON.

### 4) Knowledge graph / typology rules

- Build a small KG mapping `shape → typical_dimensions, handle_types, motif_zones, century_ranges`. Compute corpus stats (median rim\:body ratio, typical handle curvature) and store as constraints.

### 5) Retrieval-Augmented Generation (RAG)

- Index corpora (Perseus texts, Beazley notes, museum captions) with SentenceTransformers → FAISS.
- On each artifact, retrieve top-k relevant paragraphs and feed them to an LLM (local or API) that outputs a structured constraint JSON (e.g., `"handle_type":"single_loop"`).

### 6) Provenance & explainability

- For every generated reconstruction, attach the top-k retrieved sources that influenced the generation and provide a confidence score.

---

# Data curation & synthetic pair generation (how to make supervised pairs fast)

- **Image normalization:** center object, align vertical axis, scale to approximate real size using metadata.
- **Mask generation:** create morphological masks for handles, rims, and painted panels. Randomize mask shapes and sizes to simulate real damage.
- **Paired dataset:** original image + masked image + mask → use for inpainting supervision (diffusion or supervised CNNs).
- **3D photogrammetry:** for local casts/replicas, capture 40–80 photos per object with consistent lighting; process with COLMAP / Meshroom to produce meshes.

---

# Modeling plan — keep it pragmatic (2 tracks)

## Track A — 2D inpainting pipeline (primary, fast, likely MSc target)

- **Model:** Fine-tune Stable Diffusion (inpainting) using LoRA/DreamBooth techniques.
- **Conditioning:** ControlNet with edge/structure maps; tokens from NLP JSON (e.g., `<krater_redfigure_5thC>`). Use classifier-free guidance.
- **Losses & constraints:** diffusion loss, perceptual LPIPS loss, edge-preserve loss. After generation, run a typology check (geometry heuristic) and a motif-token classifier to reject anachronistic motifs.
- **Baseline:** LaMa or DeepFillv2 (simpler) and a nearest-neighbor exemplar retrieval method.

**Training spec (example):**

- Image size: 512×512. Steps: 10k–30k (depending on data size). Batch size tuned to GPU memory.

## Track B — 3D completion pilot (show feasibility, not perfection)

- **Data:** 10–30 photogrammetry-derived meshes or CC models.
- **Models to try:** Point-E (fast prototyping), PoinTr (point-cloud completion), or a conditional diffusion on meshes if time and compute allow.
- **Evaluation:** Chamfer distance against held-out complete meshes, and qualitative archaeologist review.

---

# Human-in-the-loop & UI

- Build a minimal web app (Flask/Streamlit or simple React) showing: original damaged photo, AI reconstruction(s) with confidence, provenance links, and buttons: `Accept`, `Edit`, `Reject`. Allow archaeologist to load top-k exemplar images and copy motifs from an exemplar.

---

# Validation & evaluation (required to pass review)

**Quantitative metrics (where possible):**

- 2D: LPIPS, SSIM, PSNR vs synthetic ground truth.
- 3D: Chamfer distance, IoU.
- Classifier: motif-token accuracy, typology constraint satisfaction rate.

**Qualitative (human) tests:**

- **Blind A/B test**: Present archaeologists with (A) fragm
