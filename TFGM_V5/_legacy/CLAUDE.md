# CLAUDE.md

Guidance for Claude Code (claude.ai/code) in this repo.

## Project

TFG: retrospective cohort study (n=44) on IgG-ELISA seronegativization kinetics after ivermectin in strongyloidiasis (HCDGU, 2015–2025). Output = single Quarto PDF (`Resultados.qmd` → `Resultados.pdf`), driven by modular Python scripts in `code/`.

## Commands

Render full PDF (need Python 3.14 at path below; adjust if different):

```bash
QUARTO_PYTHON=/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 \
    quarto render Resultados.qmd
```

Regen single figure without re-rendering PDF — each script standalone:

```bash
python3 code/fig_b2_km_baseline.py
python3 code/fig_b3_predictors.py
python3 code/fig_b4_lmm.py
# etc. for any code/fig_*.py or code/tab_*.py
```

Install deps: `pip install -r requirements.txt` (pandas, numpy, matplotlib, scipy, statsmodels, lifelines, miceforest, openpyxl).

No tests, no linter.

## Architecture

**Namespace-sharing pattern (not imports).** `Resultados.qmd` runs `_setup.py` then `_data.py` in setup cell via `exec(...)`; later cells `exec()` one script from `code/`. Vars flow through cell namespace — no module imports, no pickling. Each analysis script reads globals like `pac`, `ev`, `cox_data`, `ser_long` and writes new ones (e.g. `kmf`, `cox_uni`) for downstream cells.

**Standalone guard.** Every `code/fig_*.py` / `code/tab_*.py` starts with:

```python
if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())
```

Same file works inside Quarto and as `python3 code/xxx.py`. Preserve guard when editing/adding scripts.

**Two foundation files** — no rename/restructure without updating every dependent script:

- `code/_setup.py`: imports, matplotlib rcParams, color palette `C` / `SAT` / `GRI`, `CONFIG` dict (thresholds: `SERO_NEG=1.1`, `SERO_NEG_ALT=0.9`, `SERO_DROP_SALVADOR=0.60`, `EOS_NEG=0.5`, `MICRO_MIN=7`, `RECIDIVA_GAP=21`, `ALPHA=0.05`, `SEED=42`), formatting helpers (`med_iqr`, `n_pct`, `rng`). No data loading.
- `code/_data.py`: reads `data/BASE_EXCEL.xlsx` (5 sheets: `bas`, `ser`, `eos`, `mic`, `seg`), T0 = first consult with `DOSIS_IVM` non-null, builds cohort `pac` (n=44), longitudinals (`ser_long`, `eos_long`, `ser_post`, `eos_post`, `mic_post`), event datasets via `build_events(...)` → `ev` (primary, thresh 1.1) and `ev_alt` (thresh 0.9), Cox/KM dataset `cox_data` / `km_full`, label dict `nice`.

**6 time-to-event endpoints** built by `build_events()` in `_data.py`: `SERO_ABS_X1`, `SERO_ABS_X2`, `SERO_REL_X1`, `SERO_REL_X2`, `EOS_ABS`, `PARA`. `ev` = primary (thresh 1.1); `ev_alt` = same 6 at thresh 0.9 for sensitivity. Primary endpoint = `SERO_ABS_X1` (IgG < 1.1, first crossing). Exclusions `EXCL_SERO_IDS` = patients with qualitative NEG baseline serology (dropped from KM/Cox).

**Figure/table naming mirrors sections.** `fig_b2_*` = Kaplan–Meier, `fig_b3_*` / `cox_*` / `tab_cox_*` = predictors, `fig_b4_*` = LMM, `fig_b5_*` / `tab_b5_*` = persistence/relapse. Outputs land in `figures/` (PNG) or `figures/*.md` (tables via `#| output: asis`).

## Conventions

- Spanish throughout (comments, labels, headings). Match existing language when editing.
- Thresholds from `CONFIG` / module constants (`SERO_NEG`, `EOS_NEG`, `MICRO_MIN`, `ALPHA`) — never hardcode.
- Colors: use `C` dict (`C['red']`, `C['blue']`, …), not raw hex.
- `archivo/` = prior versions — no edit, no delete.
- `materiales/` = bibliography (`references.bib`), CSL (`vancouver.csl`), STROBE checklist, narrative drafts — reference only, not executed.
- `manuscrito/` = final TFG manuscript assembly (Google Docs target). Driver = `manuscrito/prompt.md` (iterative spec of requirements, UAH rules, corrections). `protocolo.qmd` + portada PDF here. All new manuscript work goes in this dir.

## Data

`data/BASE_EXCEL.xlsx` = source of truth (5 sheets). `BASE_CRUDA.xlsx` = raw upstream; `data_dictionary.csv` documents fields. Cohort fixed at n=44; 36/44 have valid baseline IgG, patient 18 excluded from some analyses, ELISA kit change mid-series — account for these when adding analyses.