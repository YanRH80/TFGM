# ============================================================
# code/fig_b3_predictors.py
# ------------------------------------------------------------
# Figura 5: Predictores basales de seronegativización (compuesta)
#
# Layout re-diseñado: tres curvas KM estratificadas stackeadas
# en la columna izquierda + tres ejes forest independientes,
# uno por fila de GridSpec, en la columna derecha. Esta
# arquitectura garantiza que cada fila del forest quede
# verticalmente alineada **exactamente** con su panel KM
# homólogo, sin drift por asimetría del ylim.
#
#   ┌──────────────────┬───────────────────────────┐
#   │ A. KM IgG basal  │ D. Forest fila A          │
#   ├──────────────────┼───────────────────────────┤
#   │ B. KM Sexo       │    Forest fila B          │
#   ├──────────────────┼───────────────────────────┤
#   │ C. KM Eos. dx    │    Forest fila C          │
#   └──────────────────┴───────────────────────────┘
#
# Franjas grises alternas por semestre en cada panel KM →
# homogéneo con fig-b2-km-baseline. Eje superior en meses
# sobre el último panel KM (C) para no colisionar con el
# título de A.
#
# Lee:    cox_uni, km_full, nice, igg_med, EOS_NEG, C (namespace)
# Output: figures/fig-b3-predictors.png
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

if 'cox_uni' not in dir():
    exec(open('code/cox_compute.py').read())

# ------------------------------------------------------------
# Subconjunto significativo (p crudo < 0,05) para el forest plot.
#
# Filtramos la variante continua (IGG_BASAL), cuyo efecto ya está
# capturado por la forma dicotomizada SER_MEDIANA, para mantener
# una correspondencia **1:1** entre cada fila del forest y un
# panel KM categórico a la izquierda (evita duplicación y
# cluttering visual).
# ------------------------------------------------------------
cox_sig = cox_uni[cox_uni['p'] < 0.05].copy()
cox_sig = cox_sig[cox_sig['Variable'] != 'IGG_BASAL']
cox_sig = cox_sig.sort_values('HR').reset_index(drop=True)

# ------------------------------------------------------------
# Layout GridSpec (2 columnas):
#   - Izquierda: 3 filas de KM estratificados
#   - Derecha:   forest plot ocupando las 3 filas
# ------------------------------------------------------------
fig = plt.figure(figsize=(16, 10))
gs  = fig.add_gridspec(3, 2,
                       width_ratios=[1.0, 1.25],
                       hspace=0.55, wspace=0.12)

# ============================================================
# A-C. KM estratificado (columna izquierda)
# ------------------------------------------------------------
# Construimos strat_vars dinámicamente en el mismo orden (HR
# ascendente) que las filas de cox_sig, para que el panel A del
# KM coincida con la fila 1 del forest, B con la fila 2, etc.
# ============================================================
_km_strat_map = {
    'SER_MEDIANA': ('SER_MEDIANA',
                    f'IgG-ELISA basal ≥ mediana ({igg_med:.1f})',
                    {0: f'< {igg_med:.1f}', 1: f'≥ {igg_med:.1f}'}),
    'SEXO_V':      ('SEXO',
                    'Sexo',
                    {'M': 'Mujer', 'V': 'Varón'}),
    'EOS_ALTA':    ('EOS_ALTA',
                    f'Eosinofilia al diagnóstico ≥ {EOS_NEG} ×10³/µL',
                    {0: f'< {EOS_NEG}', 1: f'≥ {EOS_NEG}'}),
}
strat_vars   = [_km_strat_map[v] for v in cox_sig['Variable']]
panel_labels = ['A', 'B', 'C'][:len(strat_vars)]

for idx_s, (col, titulo, gl) in enumerate(strat_vars):
    ax = fig.add_subplot(gs[idx_s, 0])

    # Franjas alternas por semestre (homogéneo con fig-b2-km-baseline)
    for _a, _b in [(0, 6), (12, 18), (24, 30)]:
        ax.axvspan(_a * 30.44, _b * 30.44,
                   color=C['grid'], alpha=0.35, zorder=0)

    groups = sorted(km_full[col].dropna().unique())

    for i, g in enumerate(groups):
        sub = km_full[km_full[col] == g]
        if len(sub) < 2:
            continue
        lb = gl.get(g, str(g))
        k = KaplanMeierFitter()
        k.fit(sub['T_SERO_ABS_X1'], sub['E_SERO_ABS_X1'],
              label=f'{lb} (n={len(sub)}, ev={int(sub["E_SERO_ABS_X1"].sum())})')
        k.plot_survival_function(
            ax=ax, ci_show=True,
            color=[C['blue'], C['red']][i % 2], lw=1.8,
        )

    # Log-rank (2 grupos)
    if len(groups) == 2:
        g0 = km_full[km_full[col] == groups[0]]
        g1 = km_full[km_full[col] == groups[1]]
        if len(g0) >= 2 and len(g1) >= 2:
            lr = logrank_test(
                g0['T_SERO_ABS_X1'], g1['T_SERO_ABS_X1'],
                g0['E_SERO_ABS_X1'], g1['E_SERO_ABS_X1'],
            )
            p = lr.p_value
            pc = C['red'] if p < 0.05 else C['gold']
            ax.text(
                0.97, 0.95, f'p = {p:.3f}', transform=ax.transAxes,
                ha='right', va='top', fontsize=11, fontweight='bold',
                color=pc,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                          alpha=0.92, edgecolor=pc),
            )

    ax.set(xlabel='Días desde T₀' if idx_s == 2 else '',
           ylabel='P(no negativización)',
           ylim=(-0.05, 1.05),
           title=f'{panel_labels[idx_s]}. {titulo}')
    ax.legend(frameon=False, fontsize=7, loc='lower left')
    ax.axhline(0.5, color=C['grid'], ls=':', lw=0.8)

    # Eje superior en meses (sólo en el último panel: libera la
    # esquina superior izquierda y evita colisionar con el título A)
    if idx_s == len(strat_vars) - 1:
        _sx = ax.secondary_xaxis(
            'top', functions=(lambda d: d / 30.44, lambda m: m * 30.44))
        _sx.set_xlabel('Meses desde T₀', fontsize=8)
        _sx.set_xticks([0, 6, 12, 18, 24, 30])

# ============================================================
# D. Forest plot (columna derecha, 1 eje por fila → alineación
# 1:1 exacta con los paneles KM homólogos de la izquierda)
# ------------------------------------------------------------
# Clave del rediseño: en lugar de un único Axes continuo sobre
# las tres filas (que con hspace > 0 provoca desalineación
# sistemática entre los puntos y los paneles KM), creamos un
# Axes forest independiente en cada celda gs[idx, 1]. Cada punto
# queda centrado verticalmente (ylim simétrico) en su propia
# celda → alineación perfecta con el panel KM de la misma fila.
# El texto HR/CI/p se imprime en línea a la derecha del CI_hi
# (ha='left') para que no se clipee nunca.
# ============================================================
if len(cox_sig) > 0:
    _x_text_start = cox_sig['CI_hi'].max() + 0.15
    _x_max_forest = max(cox_sig['CI_hi'].max() + 3.2, 6.5)

    _ax_fi_first = None
    for idx_s, (_, r) in enumerate(cox_sig.iterrows()):
        if _ax_fi_first is None:
            ax_fi = fig.add_subplot(gs[idx_s, 1])
            _ax_fi_first = ax_fi
        else:
            ax_fi = fig.add_subplot(gs[idx_s, 1], sharex=_ax_fi_first)

        ax_fi.errorbar(
            r['HR'], 0,
            xerr=[[r['HR'] - r['CI_lo']], [r['CI_hi'] - r['HR']]],
            fmt='o', color=C['red'], capsize=7, lw=2.4, ms=12,
            zorder=4,
        )
        ax_fi.axvline(1, color=C['muted'], ls='--', lw=1.3, zorder=3)

        # HR/CI/p en línea a la derecha del extremo superior del CI
        ax_fi.text(
            _x_text_start, 0,
            f"HR {r['HR']:.2f} ({r['CI_lo']:.2f}–{r['CI_hi']:.2f})   "
            f"p = {r['p']:.3f}   p$_{{adj}}$ = {r['p_adj']:.3f}",
            fontsize=10, color=C['red'], ha='left', va='center',
        )

        # Un único ytick: letra del panel KM homólogo
        ax_fi.set_yticks([0])
        ax_fi.set_yticklabels([f'≡ {panel_labels[idx_s]}'],
                              fontsize=13, fontweight='bold',
                              color=C['muted'])
        ax_fi.tick_params(axis='y', length=0, pad=8)
        ax_fi.set_ylim(-0.5, 0.5)   # simétrico → punto exactamente centrado
        ax_fi.set_xlim(-0.05, _x_max_forest)

        # Xlabel sólo en la fila inferior
        if idx_s == len(cox_sig) - 1:
            ax_fi.set_xlabel('Cociente de riesgos instantáneos (HR, IC 95 %)')
        else:
            ax_fi.tick_params(labelbottom=False)

        # Título sólo en la fila superior
        if idx_s == 0:
            ax_fi.set_title(
                f'D. Forest plot · {len(cox_sig)} covariables con '
                f'p < 0,05 · correspondencia 1:1 con paneles A–C'
            )
else:
    ax_empty = fig.add_subplot(gs[:, 1])
    ax_empty.text(0.5, 0.5, 'Sin covariables con p < 0,05',
                  ha='center', va='center', transform=ax_empty.transAxes,
                  fontsize=12, color=C['muted'])
    ax_empty.set(xticks=[], yticks=[])

plt.tight_layout()
plt.savefig('figures/fig-b3-predictors.png', dpi=300, bbox_inches='tight')
plt.show()
