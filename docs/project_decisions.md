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


---

## D-006 — Weather source: Open-Meteo Historical Archive (ERA5)

**Date:** 2026-11-13
**Status:** Decided

### Decision
Use the Open-Meteo **Historical Weather API** (archive endpoint, ERA5 reanalysis) for
weather data:

- **Endpoint:** `https://archive-api.open-meteo.com/v1/archive`
- **Cities:** Phnom Penh, Siem Reap, Sihanoukville
- **Granularity:** daily
- **Variables:** `temperature_2m_mean` (°C), `precipitation_sum` (mm),
  `relative_humidity_2m_mean` (%), `wind_speed_10m_max` (km/h)
- **Timezone:** `Asia/Phnom_Penh` (required for correct daily boundaries)
- **Coverage used:** 2019-01-01 → 2023-12-31 (1826 days per city)
- **Auth:** none (public, free tier)
- **Files:** `data/raw/weather_{city}_2019-01-01_2023-12-31.json`

### Schema (as returned)

| Field | Type | Unit |
|---|---|---|
| `time` | ISO-8601 date | — |
| `temperature_2m_mean` | number | °C |
| `precipitation_sum` | number | mm |
| `relative_humidity_2m_mean` | number | % |
| `wind_speed_10m_max` | number | km/h |

### Notes
- **Grid snapping:** request coordinates snap to the nearest ~2 km ERA5 grid
  cell. The exact returned lat/lon is captured in every snapshot as
  `latitude_returned` / `longitude_returned` for provenance.
- **Units are self-documenting** — every response includes a `daily_units`
  object, stored in the snapshot. No inference needed.
- **`relative_humidity_2m_mean`** is available as a daily aggregate directly
  (no hourly aggregation required).

### Rationale
- Public, keyless, stable, with daily aggregations and self-documenting units.
- ERA5 is the standard reanalysis dataset — defensible in an interview.
- `timezone=Asia/Phnom_Penh` guarantees daily boundaries match local days.

### Alternatives considered
- **Open-Meteo forecast API** — rejected: not historical.
- **ERA5-Land (9 km)** — possible but not needed; ERA5 (11 km) is fine for
  national-level monthly analysis.
- **Hourly → daily aggregation** for humidity — not needed; the API supports
  `relative_humidity_2m_mean` directly.

---

## D-007 — Exchange-rate source + analysis window (2019–2023)

**Date:** 2026-11-13
**Status:** Decided

### Decision
Use the **NBC Khmer Riel–USD exchange rate** dataset published on the MEF Open
Data platform as a CSV:

- **Source:** MEF Open Data, "Khmer Riel-USD Exchange Rate Data 2003-2023"
- **File:** `data/raw/exchange_rate_khr_usd_2003_2023.csv`
- **Coverage:** 2003-04-01 → 2023-12-31
- **Auth:** none

### Analysis window: 2019–2023

The three sources have the following coverage:

| Source | Coverage |
|---|---|
| MOT tourism (MEF API) | 2018-01 → 2025-12 |
| Open-Meteo weather | 1940 → now |
| NBC exchange rate (this CSV) | **2003-04 → 2023-12** ← limiter |

The **common intersection is 2019-01 → 2023-12**. The initial plan targeted
2019–2024, but the exchange-rate archive does not publish 2024.

### Consequences
- **All downstream analysis is scoped to 2019-01 → 2023-12** (60 monthly rows).
- 2024 tourism + weather data can still be ingested for reference, but any
  joined/correlated analysis must exclude 2024 (missing exchange rate).
- Window includes: 1 pre-COVID baseline year (2019), 3 COVID-affected years
  (2020–2022), 1 recovery year (2023). That is a useful period for studying
  weather–tourism–currency relationships under structural break.

### Rationale
- Using the existing CSV avoids introducing a mid-series methodology break
  from stitching two sources (NBC direct + third-party).
- A clean 5-year window is defensible; a 6-year window with a known gap is not.
- NBC is the authoritative primary source for KHR/USD.

### Alternatives considered
- **NBC SDMX download** — untested; would require manual download from
  nbc.gov.kh. Deferred; can revisit if 2024 is required.
- **AllRatesToday (paid tier)** — covers 2016→now, but historical access is
  paid. Overkill for a portfolio project.
- **Stitch CSV + a 2024 source** — rejected: introduces a methodology break
  and the two sources may define "midpoint" differently.

---

## D-008 — Exchange CSV quality issues (deferred to transform)

**Date:** 2026-11-13
**Status:** Decided

### Decision
The raw exchange-rate CSV is preserved **as-is** in `data/raw/`. All cleaning is
deferred to the transform stage. Raw data is immutable (see D-003).

### Known issues (to be cleaned in transform)

| Issue | Evidence | Transform fix |
|---|---|---|
| UTF-8 BOM on header | First byte of file is `\ufeff` before `date` | Read with `encoding='utf-8-sig'` |
| Date format = M/D/YYYY | `4/1/2003` = April 1, not Jan 4 | Parse with `format='%m/%d/%Y'` |
| Missing April 2008 | Jump from 2008-03-30 to 2008-05-01 | Resample monthly; 2008-04 = NaN. **Outside analysis window** (2019–2023), no impact |
| Occasional `purchase > sale` | e.g. 2006-12-02: purchase=4173, sale=4082 | Flag or swap. Outside analysis window |
| Midpoint ≠ (purchase+sale)/2 | e.g. 2009-08-13: (4152+4167)/2=4159.5 but midpoint=4181 | Recompute midpoint in transform |
| Awkward column name | `spread_market_day_x-1_over_oer_day_x_midpoint` | Rename to `spread_pct` |

### Why deferred
- Raw data should reflect what the source published — no silent edits.
- A reviewer inspecting `data/raw/` sees exactly what came from NBC.
- Transform is the single place where cleaning decisions are made, testable,
  and reproducible.
- Cleanup here would make re-running transforms from raw impossible.

### Consequences
- Ingestion code must not "fix" the CSV — it saves bytes.
- Transform must explicitly handle each issue above.
- Any analysis on pre-2019 data must also apply these rules.