# ============================================================
# code/fig_b2_km_baseline.py
# ------------------------------------------------------------
# Figura 2: Curva KM primaria (IgG < 1,1) con landmarks 6/12/18/24 m.
# *** PRESENTADA SOLA, sin la sensibilidad junto al lado. ***
# *** Los landmarks (puntos diamante) resumen la proporción
#     acumulada de negativización para evitar la redundancia
#     con la figura de sensibilidad.                          ***
#
# Lee:    ev, C (del namespace)
# Escribe: km_data, kmf, med_km, ci_lo, ci_hi (al namespace)
# Output: figures/fig-b2-km-baseline.png
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

# ------------------------------------------------------------
# Ajuste KM
# ------------------------------------------------------------
km_data = ev[ev['T_SERO_ABS_X1'] > 0].copy()
kmf = KaplanMeierFitter()
kmf.fit(km_data['T_SERO_ABS_X1'], km_data['E_SERO_ABS_X1'], label='IgG < 1.1')

# IC 95 % Greenwood sobre la mediana (inversión de CI envolventes)
# - ci_lo (tiempo temprano) = primer t en que el envolvente INFERIOR de S(t) cae a 0,5
# - ci_hi (tiempo tardío)   = primer t en que el envolvente SUPERIOR de S(t) cae a 0,5
med_km = kmf.median_survival_time_
_ci_sf = kmf.confidence_interval_survival_function_
_ci_lo_col, _ci_hi_col = _ci_sf.columns[0], _ci_sf.columns[1]
_early = _ci_sf[_ci_sf[_ci_lo_col] <= 0.5]  # envolvente inferior toca 0,5 antes
_late  = _ci_sf[_ci_sf[_ci_hi_col] <= 0.5]  # envolvente superior toca 0,5 después
ci_lo = _early.index[0] if len(_early) > 0 else np.nan
ci_hi = _late.index[0]  if len(_late)  > 0 else np.nan

# ------------------------------------------------------------
# Figura (1 panel, sin sensibilidad)
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))

# Franjas alternas por semestre (0-6, 12-18, 24-30 meses) en gris muy
# claro para marcar visualmente las zonas pares sin recargar la curva.
for _a, _b in [(0, 6), (12, 18), (24, 30)]:
    ax.axvspan(_a * 30.44, _b * 30.44,
               color=C['grid'], alpha=0.35, zorder=0)

kmf.plot_survival_function(ax=ax, ci_show=True, color=C['blue'], lw=2)

# Marcas de censura
censored = km_data[km_data['E_SERO_ABS_X1'] == 0]
for _, row in censored.iterrows():
    ax.plot(row['T_SERO_ABS_X1'],
            kmf.survival_function_at_times(row['T_SERO_ABS_X1']).values[0],
            '|', color=C['annot'], ms=8, mew=1.5, zorder=3)

# Mediana y su IC 95% Greenwood
if med_km < np.inf:
    ax.axhline(0.5, color=C['grid'], ls=':', lw=0.8)
    ax.axvline(med_km, color=C['red'], ls='--', lw=1, alpha=0.7)
    ci_txt = (f'Mediana: {med_km:.0f} d ({med_km/30.44:.1f} m)\n'
              f'IC 95%: {ci_lo:.0f}–{ci_hi:.0f} d')
    ax.text(med_km + 15, 0.55, ci_txt,
            color=C['red'], fontsize=8, fontweight='bold')

# Landmarks a 6, 12, 18 y 24 meses (puntos diamante + % negativizado)
for m in [6, 12, 18, 24]:
    t_d = m * 30.44
    s_t = kmf.predict(t_d)
    neg_pct = (1 - s_t) * 100
    ax.plot(t_d, s_t, 'D', color=C['gold'], ms=7, zorder=5)
    ax.annotate(f'{m} m\n{neg_pct:.0f}%',
                xy=(t_d, s_t), xytext=(t_d + 15, s_t + 0.06),
                fontsize=7, color=C['gold'], fontweight='bold')

ax.set(xlabel='Días desde T₀', ylabel='P(no negativización)',
       ylim=(-0.05, 1.05),
       title=(f'Kaplan–Meier: tiempo hasta seronegativización (IgG-ELISA < {SERO_NEG:.1f}) '
              f'— n = {len(km_data)}, eventos = {int(km_data["E_SERO_ABS_X1"].sum())}'))
ax.legend().remove()

# Eje x secundario en meses, alineado con el eje de días
_secx = ax.secondary_xaxis(
    'top', functions=(lambda d: d / 30.44, lambda m: m * 30.44))
_secx.set_xlabel('Meses desde T₀', fontsize=9)
_secx.set_xticks([0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30])

add_at_risk_counts(kmf, ax=ax, rows_to_show=['At risk'])

plt.tight_layout()
plt.savefig('figures/fig-b2-km-baseline.png', dpi=300, bbox_inches='tight')
plt.show()
