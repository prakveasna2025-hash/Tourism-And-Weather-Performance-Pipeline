# Project Decisions

A record of design decisions made during this project, with rationale and
tradeoffs. Each entry is dated and immutable — if a decision changes, add a
new entry that supersedes the old one rather than editing history.

---

## D-001 — Tourism source: MEF Open Data API (MOT dataset)

**Date:** 2026-11-12
**Status:** Decided

### Decision
Use the Ministry of Economy and Finance (MEF) Open Data platform — which
hosts the Ministry of Tourism (MOT) dataset — as the tourism source:

- **Dataset ID:** `pd_6715e15d40cc5500017936e5`
- **Title:** International Tourist Arrivals to Cambodia 2018 - 2025
- **Organization:** Ministry of Tourism (MOT) — MEF is the hosting platform only
- **Endpoint:** `https://data.mef.gov.kh/api/v1/public-datasets/pd_6715e15d40cc5500017936e5/json`
- **Metadata endpoint:** `https://data.mef.gov.kh/api/v1/public-datasets/pd_6715e15d40cc5500017936e5`
- **Pagination:** `page` / `page_size` query params; `total_pages` in response
- **Auth:** none (public)
- **Coverage:** 2018-01-01 → 2025-12-31
- **Frequency:** monthly
- **Total records:** 94 rows
- **CSV fallback:** `file_url = pd_6715e15d40cc5500017936e5.csv` on the same platform

### Schema (confirmed via metadata endpoint)

| Field | Type | Format | Description |
|---|---|---|---|
| `year` | number | YYYY | Year of statistical report |
| `months` | text | — | Month name (Jan..Dec) |
| `number_of_tourists` | number | — | Number of tourists who arrived in Cambodia (persons) |

### Measure
**International tourist arrivals only.** Confirmed by metadata description:
*"Number of Tourist who arrived in Cambodia"* under a dataset titled
*"International Tourist Arrivals to Cambodia."* Domestic tourists are
**not** included.

### Rationale
- Public, stable, paginated API with self-describing metadata.
- MOT is the authoritative source; MEF is the publishing platform.
- Real ingestion work: pagination loop, raw snapshot with provenance.
- Metadata confirms units (persons) and frequency (monthly) — no inference needed.

### Alternatives considered
- **MOT regional CSV** — would give zone detail (Siem Reap Angkor, Coastal,
  Preah Sihanouk) but mixes domestic + foreign arrivals; not an international-only
  measure. Rejected for this iteration.
- **CSV download only** — no ingestion logic to build; loses provenance
  metadata that the API returns naturally.

---

## D-002 — Grain: national, monthly, international

**Date:** 2026-11-12
**Status:** Decided

### Decision
The tourism dataset's grain is **one row per (year, month)**, nationally
aggregated, measuring **international tourist arrivals**.

### Rationale
- The MEF/MOT dataset has **no location/zone column** — per-location grain
  is not available from this source.
- Metadata confirms `frequency = "monthly"` and `coverage` from 2018-01 to
  2025-12.
- National-monthly is sufficient for the first iteration of weather-correlation
  analysis.

### Consequences
- **Cannot disaggregate** below national-monthly. All downstream analysis
  must respect this grain.
- If regional breakdown is later required, a second source must be added
  (see D-001 "Alternatives considered").

---

## D-003 — Ingestion pattern: API → immutable raw snapshot

**Date:** 2026-11-12
**Status:** Decided

### Decision
Ingestion fetches from the API and writes a **dated, immutable JSON snapshot**
to `data/raw/`. Transform reads only from `data/raw/` — never directly from
the API.

### Snapshot format
```json
{
  "fetched_at": "ISO-8601 UTC",
  "source_url": "https://...",
  "dataset_id": "pd_...",
  "total_items": 94,
  "items": [ ... ]
}
```

### Rationale
- **Provenance:** snapshot is self-describing — where it came from, when,
  which dataset version. Required for reproducibility and debugging.
- **Reproducibility:** transform can be re-run without re-fetching the API.
- **Resilience:** if the source is down, transform still works.
- **Bronze-layer pattern:** mirrors the raw/immutable layer of lakehouse
  architectures.

### Alternatives considered
- **Transform reads directly from the API** — rejected: transform would fail
  whenever the API is down, and analyses wouldn't be reproducible from a
  known point in time.

---

## D-004 — Dependency management: uv (pyproject.toml + uv.lock)

**Date:** 2026-11-11
**Status:** Decided

### Decision
Use `uv` for Python dependency management. Dependencies are declared in
`pyproject.toml`; exact versions are pinned in `uv.lock`.

### Rationale
- Fast, single tool for venv + dependency resolution + lock file.
- `uv.lock` is fully deterministic (transitive deps pinned) — stronger than
  hand-maintained `requirements.txt`.
- Modern standard for new Python projects.

### Tradeoffs
- `requirements.txt` is intentionally omitted. If a downstream target requires
  it (e.g., some Docker base images, some CI systems), generate it at build
  time with `uv export --format requirements-txt`.

---

## D-005 — Repository structure: stage-separated src/

**Date:** 2026-11-10
**Status:** Decided

### Decision
`src/` is split by pipeline stage: `ingestion/`, `transform/`, `load/`.
Data is split into `data/raw/` (immutable) and `data/processed/` (derived).

### Rationale
- Each stage has a distinct failure mode and can be tested and re-run
  independently. Mirrors Airflow tasks / dbt models.
- Raw/processed split means transforms are replayable from source.

---

## Template for future decisions

```
## D-XXX — <Title>

**Date:** YYYY-MM-DD
**Status:** Proposed | Decided | Superseded by D-YYY

### Decision
What was decided.

### Rationale
Why this and not something else.

### Alternatives considered
What else was on the table, and why rejected.

### Consequences
What this decision implies downstream.
```