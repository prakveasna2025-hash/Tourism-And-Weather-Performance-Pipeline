# Development Notes

Living decision log and scratchpad.

## Goal
End-to-end pipeline: ingest tourism + weather data -> transform -> load into
a queryable destination for performance analysis.

## Stack
- Python, managed with uv (pyproject.toml + uv.lock)
- Data processing / storage: TBD Day 2

## Decisions

| Date       | Decision                          | Rationale                                            |
|------------|-----------------------------------|------------------------------------------------------|
| 2026-11-11 | Separate raw/ and processed/      | Raw immutable; re-run transforms without re-fetching |
| 2026-11-11 | Split src/ by pipeline stage      | Each stage testable/re-runnable independently        |
| 2026-11-11 | Use uv instead of pip+venv        | Faster, lock file, single tool                       |
| 2026-11-11 | Skip requirements.txt             | pyproject.toml + uv.lock is the modern equivalent    |

## TODO
- [ ] Confirm weather API + tourism source
- [ ] Build ingestion module
- [ ] Build transform module
- [ ] Build load module
- [ ] Add unit tests
- [ ] Add CI (GitHub Actions)

## Commands
uv sync              # install from lock
uv add <pkg>         # add dependency
uv run <cmd>         # run inside project env
git status
git log --oneline --graph --all
