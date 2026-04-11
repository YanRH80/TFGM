# ============================================================
# code/fig_b3_km_strat.py
# ------------------------------------------------------------
# Figura 4: KM estratificado 1×3 para las 3 covariables con
# p < 0,05 en Cox univariable:
#   1. SER_MEDIANA  — IgG basal ≥ mediana
#   2. SEXO         — varón / mujer
#   3. EOS_ALTA     — eosinófilos ≥ 0,5 ×10³/μL
# Log-rank test en cada panel. Bandas = IC 95 %.
#
# Lee:    km_full, igg_med, EOS_NEG, C (del namespace)
# Output: figures/fig-b3-km-strat.png
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

fig, axes_km = plt.subplots(1, 3, figsize=(15, 5))

strat_vars = [
    ('SER_MEDIANA', f'IgG ≥ mediana ({igg_med:.1f})',
        {0: f'< {igg_med:.1f}', 1: f'≥ {igg_med:.1f}'}),
    ('SEXO',        'Sexo',
        {'M': 'Mujer', 'V': 'Varón'}),
    ('EOS_ALTA',    f'Eosinófilos ≥ {EOS_NEG}',
        {0: f'< {EOS_NEG}', 1: f'≥ {EOS_NEG}'}),
]

for idx_s, (col, titulo, gl) in enumerate(strat_vars):
    ax = axes_km[idx_s]
    groups = sorted(km_full[col].dropna().unique())
    for i, g in enumerate(groups):
        sub = km_full[km_full[col] == g]
        if len(sub) < 2:
            continue
        lb = gl.get(g, str(g))
        k = KaplanMeierFitter()
        k.fit(sub['T_SERO_ABS_X1'], sub['E_SERO_ABS_X1'],
              label=f'{lb} (n={len(sub)}, ev={int(sub["E_SERO_ABS_X1"].sum())})')
        k.plot_survival_function(ax=ax, ci_show=True,
                                 color=[C['blue'], C['red']][i % 2], lw=1.8)

    # Log-rank 2 grupos
    if len(groups) == 2:
        g0 = km_full[km_full[col] == groups[0]]
        g1 = km_full[km_full[col] == groups[1]]
        if len(g0) >= 2 and len(g1) >= 2:
            lr = logrank_test(g0['T_SERO_ABS_X1'], g1['T_SERO_ABS_X1'],
                              g0['E_SERO_ABS_X1'], g1['E_SERO_ABS_X1'])
            p = lr.p_value
            pc = C['red'] if p < 0.05 else C['gold']
            ax.text(0.95, 0.95, f'p = {p:.3f}', transform=ax.transAxes,
                    ha='right', va='top', fontsize=14, fontweight='bold', color=pc,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                              alpha=0.9, edgecolor=pc))

    ax.set(xlabel='Días desde T₀',
           ylabel='P(no neg.)' if idx_s == 0 else '',
           ylim=(-0.05, 1.05), title=titulo)
    ax.legend(frameon=False, fontsize=7)
    ax.axhline(0.5, color=C['grid'], ls=':', lw=0.8)

plt.tight_layout()
plt.savefig('figures/fig-b3-km-strat.png', dpi=300, bbox_inches='tight')
plt.show()
