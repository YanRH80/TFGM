# TFGM_V5 — Cinética de seronegativización IgG-ELISA tras ivermectina en estrongiloidiasis

Análisis de supervivencia y modelización paramétrica del tiempo hasta la
seronegativización por IgG-ELISA en una cohorte retrospectiva de 44 adultos
tratados con ivermectina (HCDGU, 2015–2025).

## Estructura del proyecto

```
TFGM_V5/
├── Resultados.qmd       ← ÚNICO documento Quarto en la raíz
├── Resultados.pdf       ← salida renderizada
├── README.md
├── requirements.txt
│
├── code/                ← scripts Python modulares (editables uno por uno)
│   ├── _setup.py              imports, paleta, helpers, constantes
│   ├── _data.py               carga BASE_EXCEL.xlsx → pac, ev, cox_data, ser_long, ...
│   ├── tab_basales.py         Tabla 1 (basales): LaTeX + markdown
│   ├── fig_b1_cohort.py       Figura 1: descripción de cohorte (4 paneles)
│   ├── fig_b2_km_baseline.py  Figura 2: Kaplan–Meier primaria + landmarks (SOLA)
│   ├── fig_b2_sensitivity.py  Figura 3: sensibilidad 7 endpoints
│   ├── stats_b2.py            texto: mediana KM, landmarks, tasa persona-año
│   ├── fig_b3_km_strat.py     Figura 4: KM estratificado 1×3
│   ├── cox_compute.py         Cox univariable sobre 15 covariables (BH–FDR)
│   ├── fig_b3_forest.py       Figura 5: forest plot (p < 0,01)
│   ├── tab_cox_uni.py         Tabla 2: Cox univariable completa
│   └── fig_b4_lmm.py          Figura 6: trayectoria LMM global + por sexo
│
├── data/                ← datos fuente
│   ├── BASE_CRUDA.xlsx
│   ├── BASE_EXCEL.xlsx
│   └── data_dictionary.csv
│
├── materiales/          ← bibliografía, checklists, referencias
│   ├── Humano.qmd             draft narrativo manual (referencia)
│   ├── OE_Literatura.md       evidencia externa / contexto
│   ├── Resultados_peer_review.md
│   ├── STROBE_checklist.csv
│   └── references.bib
│
├── figures/             ← salidas generadas (PNG + markdown)
│   ├── fig-b1-cohort.png
│   ├── fig-b2-km-baseline.png
│   ├── fig-b2-sensitivity.png
│   ├── fig-b3-km-strat.png
│   ├── fig-b3-forest.png
│   ├── fig-b4-lmm.png
│   ├── tab-basales.md
│   └── tab-cox-uni.md
│
└── archivo/             ← versiones previas no borradas
```

## Render completo

```bash
QUARTO_PYTHON=/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 \
    quarto render Resultados.qmd
```

## Regenerar una figura aislada

Cada script en `code/` es autoejecutable. Edítalo, ejecútalo y el PNG se
actualiza en `figures/` sin rerenderizar el PDF completo:

```bash
python3 code/fig_b2_km_baseline.py       # Figura 2 (KM basal)
python3 code/fig_b2_sensitivity.py       # Figura 3 (sensibilidad)
python3 code/fig_b3_km_strat.py          # Figura 4 (estratificada)
python3 code/fig_b3_forest.py            # Figura 5 (forest plot)
python3 code/fig_b4_lmm.py               # Figura 6 (LMM)
```

El bloque guard `if 'pac' not in dir(): exec(...)` al inicio de cada script
carga automáticamente `_setup.py` + `_data.py` cuando se ejecuta fuera de
Quarto.

## Patrón de modularidad

Dentro de `Resultados.qmd` cada celda Python delega en un script:

```python
```{python}
#| label: fig-b2-km-baseline
#| fig-cap: "..."
exec(open('code/fig_b2_km_baseline.py').read())
```
```

Las variables (`pac`, `ev`, `kmf`, `cox_uni`, …) fluyen al *namespace* de la
celda, así que los *scripts* se pueden encadenar sin imports ni *pickling*.

## Dependencias

Ver `requirements.txt`. Las principales son `pandas`, `numpy`, `matplotlib`,
`scipy`, `statsmodels` y `lifelines`.
