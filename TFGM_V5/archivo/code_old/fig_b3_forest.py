# ============================================================
# code/fig_b3_forest.py
# ------------------------------------------------------------
# Figura 5: Forest plot de las variables con p < 0,01 en Cox
# univariable. HR, IC 95 %, p crudo, p BH–FDR.
#
# Lee:    cox_uni, nice, C (del namespace)
# Output: figures/fig-b3-forest.png
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

if 'cox_uni' not in dir():
    exec(open('code/cox_compute.py').read())

cox_sig_forest = cox_uni[cox_uni['p'] < 0.01].copy().sort_values('HR')

fig, ax_f = plt.subplots(figsize=(7, 3))

if len(cox_sig_forest) > 0:
    for i, (_, r) in enumerate(cox_sig_forest.iterrows()):
        ax_f.errorbar(r['HR'], i,
                      xerr=[[r['HR'] - r['CI_lo']], [r['CI_hi'] - r['HR']]],
                      fmt='o', color=C['red'], capsize=5, lw=2, ms=8)
        ax_f.annotate(
            f"HR {r['HR']:.2f} ({r['CI_lo']:.2f}–{r['CI_hi']:.2f})"
            f"   p = {r['p']:.3f}   p$_{{adj}}$ = {r['p_adj']:.3f}",
            xy=(max(r['CI_hi'] + 0.1, 1.5), i),
            fontsize=8, color=C['red'], va='center',
        )
    ax_f.axvline(1, color=C['muted'], ls='--', lw=1)
    ax_f.set_yticks(range(len(cox_sig_forest)))
    ax_f.set_yticklabels(
        [nice.get(r['Variable'], r['Variable']) for _, r in cox_sig_forest.iterrows()],
        fontsize=8,
    )
    ax_f.set(xlabel='HR (IC 95 %)',
             title=f'Forest plot: {len(cox_sig_forest)} covariables con p < 0,01')
    ax_f.invert_yaxis()

plt.tight_layout()
plt.savefig('figures/fig-b3-forest.png', dpi=300, bbox_inches='tight')
plt.show()
