# ============================================================
# code/fig_b2_spaghetti.py
# ------------------------------------------------------------
# Figura 2 (NUEVA): Trayectorias individuales de IgG-ELISA y
# eosinófilos superpuestas (twin-axis), como contexto visual
# previo a la curva KM primaria.
#
#   - IgG-ELISA (eje izquierdo, azul) con spaghetti individual,
#     media trimestral ± IC 95 % y umbral 1,1
#   - Eosinófilos (eje derecho, verde) con spaghetti individual,
#     media trimestral ± IC 95 % y umbral 0,5
#   - Franjas grises alternas por semestre (0-6, 12-18, 24-30 m)
#   - Eje superior secundario en meses (coherente con fig-b2-km)
#   - Anotación de la mediana KM de seronegativización para
#     anclar la interpretación al análisis de supervivencia
#
# Lee:    ser_long, eos_long, ev, SERO_NEG, EOS_NEG, C (namespace)
# Output: figures/fig-b2-spaghetti.png
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

MAX_MESES = 36  # misma ventana efectiva que el KM baseline (30-36 m)

# ------------------------------------------------------------
# Datos para trayectorias (incluye basal + post-T₀)
# ------------------------------------------------------------
ser_plot = ser_long[
    (ser_long['meses'] >= -1) & (ser_long['meses'] <= MAX_MESES)
    & ser_long['IGG'].notna()
].copy()

eos_plot = eos_long[
    (eos_long['meses'] >= -1) & (eos_long['meses'] <= MAX_MESES)
    & eos_long['EOS'].notna()
].copy()

# ------------------------------------------------------------
# Figura (twin-axis con escalas diferentes pero tiempo común)
# ------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()
# twin-axis no hereda la configuración global, así que ocultamos
# las spines top/right y la rejilla para evitar duplicaciones
ax2.spines['top'].set_visible(False)
ax2.grid(False)

# Franjas alternas por semestre (meses → expresadas en el eje de meses)
for _a, _b in [(0, 6), (12, 18), (24, 30)]:
    ax1.axvspan(_a, _b, color=C['grid'], alpha=0.35, zorder=0)

# ------------------------------------------------------------
# Spaghetti individual
# ------------------------------------------------------------
for pid, grp in ser_plot.groupby('ID'):
    g = grp.sort_values('meses')
    ax1.plot(g['meses'], g['IGG'],
             color=C['blue'], alpha=0.18, lw=0.8, zorder=2)

for pid, grp in eos_plot.groupby('ID'):
    g = grp.sort_values('meses')
    ax2.plot(g['meses'], g['EOS'],
             color=C['green'], alpha=0.15, lw=0.8, zorder=2)

# ------------------------------------------------------------
# Media trimestral ± IC 95 % (bin de 3 meses)
# ------------------------------------------------------------
def _trimestral(df, ycol, min_n=3):
    df = df.copy()
    df['bin'] = (df['meses'] / 3).round() * 3
    g = df.groupby('bin')[ycol].agg(['mean', 'std', 'count'])
    g = g[g['count'] >= min_n]
    g['se'] = g['std'] / np.sqrt(g['count'])
    return g

ms = _trimestral(ser_plot, 'IGG', min_n=3)
me = _trimestral(eos_plot, 'EOS', min_n=5)

ax1.fill_between(ms.index,
                 ms['mean'] - 1.96 * ms['se'],
                 ms['mean'] + 1.96 * ms['se'],
                 color=C['blue'], alpha=0.22, zorder=3)
l_igg_mean, = ax1.plot(ms.index, ms['mean'],
                       color=C['blue'], lw=3.2, zorder=4,
                       label='IgG media trimestral (IC 95 %)')

ax2.fill_between(me.index,
                 me['mean'] - 1.96 * me['se'],
                 me['mean'] + 1.96 * me['se'],
                 color=C['green'], alpha=0.20, zorder=3)
l_eos_mean, = ax2.plot(me.index, me['mean'],
                       color=C['green'], lw=3.2, zorder=4,
                       label='Eosinófilos media trimestral (IC 95 %)')

# ------------------------------------------------------------
# Umbrales
# ------------------------------------------------------------
l_igg_th = ax1.axhline(SERO_NEG, color=C['blue'], ls='--', lw=1.4,
                       alpha=0.9, zorder=5,
                       label=f'Umbral IgG-ELISA ({SERO_NEG:.1f})')
l_eos_th = ax2.axhline(EOS_NEG, color=C['green'], ls='--', lw=1.4,
                       alpha=0.9, zorder=5,
                       label=f'Umbral eosinófilos ({EOS_NEG:.1f})')

# ------------------------------------------------------------
# Anclar con mediana KM de seronegativización (referencia
# al análisis de supervivencia que viene a continuación)
# ------------------------------------------------------------
_kmt = ev[ev['T_SERO_ABS_X1'] > 0].copy()
_kmf = KaplanMeierFitter().fit(_kmt['T_SERO_ABS_X1'], _kmt['E_SERO_ABS_X1'])
_med_km = _kmf.median_survival_time_ / 30.44
if _med_km < np.inf:
    ax1.axvline(_med_km, color=C['red'], ls=':', lw=1.5, alpha=0.8, zorder=5)
    ax1.annotate(
        f'Mediana KM\n{_med_km:.1f} m',
        xy=(_med_km, SERO_NEG),
        xytext=(_med_km + 1.8, SERO_NEG + 1.7),
        fontsize=9, color=C['red'], fontweight='bold',
        arrowprops=dict(arrowstyle='->', color=C['red'], lw=1.0),
    )

# ------------------------------------------------------------
# Ejes y etiquetas
# ------------------------------------------------------------
ax1.set_xlabel('Meses desde T₀')
ax1.set_ylabel('← IgG-ELISA (índice)', color=C['blue'])
ax2.set_ylabel('Eosinófilos (×10³/µL) →', color=C['green'])
ax1.tick_params(axis='y', labelcolor=C['blue'])
ax2.tick_params(axis='y', labelcolor=C['green'])
ax1.set_xlim(-1, MAX_MESES)
ax1.set_xticks([0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36])

ax1.set_title(
    'Trayectorias individuales de IgG-ELISA y eosinófilos post-tratamiento\n'
    f'(n = {ser_plot["ID"].nunique()} con serología · '
    f'{eos_plot["ID"].nunique()} con eosinófilos)',
    fontsize=11,
)

# Leyenda combinada de ambos ejes
legend_handles = [l_igg_mean, l_igg_th, l_eos_mean, l_eos_th]
ax1.legend(handles=legend_handles, frameon=True, fontsize=9, loc='upper right',
           facecolor='white', framealpha=0.92, edgecolor=C['grid'],
           ncol=1)

plt.tight_layout()
plt.savefig('figures/fig-b2-spaghetti.png', dpi=300, bbox_inches='tight')
plt.show()
