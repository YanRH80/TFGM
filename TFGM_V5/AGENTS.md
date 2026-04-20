# AGENTS.md — TFGM_V5

## Project

TFG: retrospective cohort study (n=44) on IgG-ELISA seronegativization kinetics after ivermectin in strongyloidiasis (HCDGU, 2015–2025). Two outputs: (1) `Resultados.qmd` → `Resultados.pdf` (figures/tables via Python); (2) `manuscrito/main.qmd` → PDF (TFG manuscript for UAH).

## OpenCode Pipeline

**Duo:** Kimi K2.5 (ejecutor, `build`) / Kimi K2.6 (revisor, `plan`/`manuscript`).

Switch agente con **Tab**. Criterios STOP (T1–T12) → cambiar a `plan` o `manuscript`:
- T1: cambio toca ≥2 secciones simultáneamente
- T2: trade-off metodológico sin precedente
- T3: ambigüedad irreducible en datos
- T4: word count sección ±10 % de tope UAH
- T5: refactor de main.qmd, pipeline, preámbulo LaTeX
- T6: decisión bibliográfica con ≥2 candidatos equivalentes
- T7: conflicto con normativa UAH
- T8: revisión de coherencia global
- T9: validación de resultados estadísticos
- T10: switch entre rama TFG y journal/
- T11: auditoría programada (§4 prompt.md)
- T12: modelo entra en bucle o contradice iteración previa

Protocolo no-regresión (§1.8 prompt.md): cambios sobre texto validado = comentario `<!-- REV -->` in-place + diff justificado.

## Commands

Render Resultados PDF:
```bash
QUARTO_PYTHON=/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 quarto render Resultados.qmd
```

Regen single figure (standalone):
```bash
python3 code/fig_b2_km_baseline.py
python3 code/fig_b3_predictors.py
python3 code/fig_b4_lmm.py
```

Install deps: `pip install -r requirements.txt`

Resync figures to manuscrito: `bash manuscrito/figuras/make_figs.sh`

No tests, no linter.

## Architecture

**Namespace-sharing pattern (not imports).** `Resultados.qmd` runs `_setup.py` then `_data.py` in setup cell via `exec(...)`; later cells `exec()` one script from `code/`. Vars flow through cell namespace — no module imports, no pickling.

**Standalone guard.** Every `code/fig_*.py` / `code/tab_*.py` starts with:
```python
if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())
```

**Two foundation files** — no rename/restructure without updating every dependent:
- `code/_setup.py`: imports, rcParams, color palette `C`/`SAT`/`GRI`, `CONFIG` dict (SERO_NEG=1.1, SERO_NEG_ALT=0.9, SERO_DROP_SALVADOR=0.60, EOS_NEG=0.5, MICRO_MIN=7, RECIDIVA_GAP=21, ALPHA=0.05, SEED=42), helpers (`med_iqr`, `n_pct`, `rng`).
- `code/_data.py`: reads `data/BASE_EXCEL.xlsx` (5 sheets), builds `pac` (n=44), longitudinals, `ev`/`ev_alt` via `build_events()`, `cox_data`, `km_full`, `nice`.

**6 time-to-event endpoints**: SERO_ABS_X1/X2, SERO_REL_X1/X2, EOS_ABS, PARA. Primary = SERO_ABS_X1 (IgG < 1.1, first crossing). Exclusions: EXCL_SERO_IDS.

**Figure/table naming**: `fig_b2_*` = KM, `fig_b3_*`/`cox_*`/`tab_cox_*` = predictors, `fig_b4_*` = LMM, `fig_b5_*`/`tab_b5_*` = persistence/relapse. Outputs in `figures/`.

## Conventions

- Spanish throughout (comments, labels, headings).
- Thresholds from `CONFIG` / constants — never hardcode.
- Colors: use `C` dict, not raw hex.
- `archivo/` = prior versions — no edit, no delete.
- `_legacy/` = migrated Claude Code files — no edit, no delete, excluded from watcher.
- `materiales/` = bibliography, CSL, STROBE — reference only.
- `manuscrito/` = TFG manuscript assembly. Driver = `manuscrito/prompt.md`. No Python code here.
- `tools/` = validation scripts (planned).

## Data

`data/BASE_EXCEL.xlsx` = source of truth (5 sheets). `BASE_CRUDA.xlsx` = raw upstream. Cohort n=44; 36/44 valid baseline IgG; patient 18 excluded from some analyses; ELISA kit change mid-series.

## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore the codebase.**

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of Grep
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to Grep/Glob/Read **only** when the graph doesn't cover what you need.

### Key Tools

| Tool | Use when |
|------|----------|
| `detect_changes` | Reviewing code changes — gives risk-scored analysis |
| `get_review_context` | Need source snippets for review — token-efficient |
| `get_impact_radius` | Understanding blast radius of a change |
| `get_affected_flows` | Finding which execution paths are impacted |
| `query_graph` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes` | Finding functions/classes by name or keyword |
| `get_architecture_overview` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

## Watch (directories excluded from agent context)

- `_legacy/` — Claude Code migrated files
- `archivo/` — prior versions
- `manuscrito/main_files/` — Quarto media bag
- `manuscrito/main.log`, `manuscrito/main.tex` — build artifacts
