# ============================================================
# code/fig_b5_spaghetti.py
# ------------------------------------------------------------
# Trayectorias individuales de IgG-ELISA en paneles separados
# por categoría de desenlace. Reemplaza el spaghetti global
# (confuso por superposición) por un panel-grid con 3 columnas:
#
#   A. Persistencia  |  B. Recidiva  |  C. Neg. sostenida
#
# Cada panel muestra trayectorias individuales + media grupal.
# Franjas semestrales y umbral 1,1 para coherencia visual.
#
# Lee:    pac, pac_class, ser_long, SERO_NEG, C (namespace)
# Output: figures/fig-b5-spaghetti.png
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

if 'pac_class' not in dir():
    exec(open('code/tab_b5_recidiva.py').read())

MAX_MESES = 36

# ============================================================
# Datos
# ============================================================
sp = ser_long[
    (ser_long['meses'] >= -1) & (ser_long['meses'] <= MAX_MESES)
    & ser_long['IGG'].notna()
].copy()
sp = sp.merge(pac_class.reset_index().rename(columns={'categoria': 'cat'}),
              on='ID', how='left')

PANELS = [
    ('Persistencia',    C['gold'],  'A. Persistencia'),
    ('Recidiva',        C['red'],   'B. Recidiva'),
    ('Neg. sostenida',  C['blue'],  'C. Neg. sostenida'),
]

# ============================================================
# Figura
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

for ax, (cat, col, titulo) in zip(axes, PANELS):
    # Franjas semestrales
    for _a, _b in [(0, 6), (12, 18), (24, 30)]:
        ax.axvspan(_a, _b, color=C['grid'], alpha=0.30, zorder=0)

    # Umbral
    ax.axhline(SERO_NEG, color=C['text'], ls='--', lw=1.0, alpha=0.5,
               zorder=4)

    # Trayectorias individuales
    cat_ids = pac_class[pac_class == cat].index
    sub = sp[sp['ID'].isin(cat_ids)]
    n_cat = len(cat_ids)

    for pid, grp in sub.groupby('ID'):
        g = grp.sort_values('meses')
        ax.plot(g['meses'], g['IGG'],
                color=col, alpha=0.40, lw=1.2, zorder=2)
        ax.scatter(g['meses'], g['IGG'],
                   color=col, alpha=0.50, s=14, zorder=3,
                   edgecolors='white', linewidths=0.3)

    # Media trimestral ± SE
    if n_cat >= 3:
        sub_c = sub.copy()
        sub_c['bin'] = (sub_c['meses'] / 3).round() * 3
        g = sub_c.groupby('bin')['IGG'].agg(['mean', 'std', 'count'])
        g = g[g['count'] >= 2]
        if len(g) >= 2:
            g['se'] = g['std'] / np.sqrt(g['count'])
            ax.fill_between(g.index,
                            g['mean'] - 1.96 * g['se'],
                            g['mean'] + 1.96 * g['se'],
                            color=col, alpha=0.12, zorder=5)
            ax.plot(g.index, g['mean'], color=col, lw=2.8,
                    zorder=6, label='Media ± IC 95 %')

    ax.set(title=f'{titulo} (n = {n_cat})',
           xlabel='Meses desde T₀',
           xlim=(-1, MAX_MESES))
    ax.legend(fontsize=7, frameon=False, loc='upper right')

axes[0].set_ylabel('IgG-ELISA (índice)')

# Y-lim: máximo razonable sin outliers extremos
y_max = min(sp['IGG'].quantile(0.98) * 1.1, 14)
axes[0].set_ylim(0, y_max)

fig.suptitle('Trayectorias individuales de IgG-ELISA por desenlace',
             fontsize=13, y=1.02)
plt.tight_layout()
plt.savefig('figures/fig-b5-spaghetti.png', dpi=300, bbox_inches='tight')
plt.show()
