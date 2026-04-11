# ============================================================
# code/fig_b2_sensitivity.py
# ------------------------------------------------------------
# Figura 4: Análisis de sensibilidad — 7 definiciones de endpoint.
# Formato homogéneo con la KM primaria (fig-b2-km-baseline):
#   - Franjas grises alternas por semestre (0-6, 12-18, 24-30 m)
#   - Eje x en días + eje secundario en meses
#   - Línea 0,5 de referencia
#
# Curvas mostradas:
#   - IgG < 1,1            (primaria, con banda IC 95 %)
#   - IgG < 1,1 doble conf.
#   - IgG < 0,9
#   - Caída relativa ≥ 40 %
#   - Caída relativa doble conf.
#   - Eosinófilos < 0,5 × 10³/µL
#   - Parasitología 2 negativos consecutivos
#
# Lee:    ev, ev_alt, SERO_DROP, C (del namespace)
# Output: figures/fig-b2-sensitivity.png
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

km_curves = [
    ('SERO_ABS_X1', 'IgG < 1,1 *',                        C['blue'],   '-',  2.5, ev),
    ('SERO_ABS_X2', 'IgG < 1,1 (doble)',                  C['blue'],   '--', 1.2, ev),
    ('SERO_ABS_X1', 'IgG < 0,9',                          C['teal'],   '-',  1.8, ev_alt),
    ('SERO_REL_X1', f'Caída ≥ {(1 - SERO_DROP) * 100:.0f} %', C['gold'], '-',  1.8, ev),
    ('SERO_REL_X2', 'Caída rel. (doble)',                 C['gold'],   '--', 1.2, ev),
    ('EOS_ABS',     'Eosinófilos < 0,5',                  C['green'],  '-.', 1.5, ev),
    ('PARA',        'Parasitología (2 neg.)',             C['purple'], ':',  1.5, ev),
]

fig, ax = plt.subplots(figsize=(10, 6))

# Franjas alternas por semestre (homogéneo con fig-b2-km-baseline)
for _a, _b in [(0, 6), (12, 18), (24, 30)]:
    ax.axvspan(_a * 30.44, _b * 30.44,
               color=C['grid'], alpha=0.35, zorder=0)

for pf, label, color, ls, lw, ev_src in km_curves:
    data = ev_src[ev_src[f'T_{pf}'] > 0].copy()
    if len(data) < 2:
        continue
    k = KaplanMeierFitter()
    k.fit(data[f'T_{pf}'], data[f'E_{pf}'], label=label)
    ci_show = (pf == 'SERO_ABS_X1' and ev_src is ev)
    k.plot_survival_function(
        ax=ax, ci_show=ci_show, color=color, ls=ls, lw=lw,
        ci_alpha=0.08 if ci_show else 0,
    )

ax.axhline(0.5, color=C['grid'], ls=':', lw=0.8)
ax.set(xlabel='Días desde T₀', ylabel='P(no negativización)',
       ylim=(-0.05, 1.05),
       title='Sensibilidad: 7 definiciones alternativas de endpoint')
ax.legend(frameon=True, loc='upper right', fontsize=8,
          facecolor='white', framealpha=0.9, edgecolor=C['grid'])

# Eje secundario en meses (homogéneo con la figura KM baseline)
_secx = ax.secondary_xaxis(
    'top', functions=(lambda d: d / 30.44, lambda m: m * 30.44))
_secx.set_xlabel('Meses desde T₀', fontsize=9)
_secx.set_xticks([0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30])

plt.tight_layout()
plt.savefig('figures/fig-b2-sensitivity.png', dpi=300, bbox_inches='tight')
plt.show()
