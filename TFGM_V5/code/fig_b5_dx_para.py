# ============================================================
# code/fig_b5_dx_para.py
# ------------------------------------------------------------
# Análisis de la potencia predictiva del diagnóstico
# parasitológico basal (DX_PARA) sobre la cinética de
# seronegativización.
#
# Panel izquierdo: KM estratificado por DX_PARA (0 vs 1)
# Panel derecho:   anotación de HR, IC 95 %, p-valor (Cox
#                  univariable) y potencia post-hoc (Schoenfeld).
#
# Lee:    pac, km_full, cox_uni, nice, SERO_NEG, C (namespace)
# Output: figures/fig-b5-dx-para.png
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

if 'cox_uni' not in dir():
    exec(open('code/cox_compute.py').read())

import math
from scipy.stats import norm

# ============================================================
# Datos Cox para DX_PARA
# ============================================================
r_dx = cox_uni[cox_uni['Variable'] == 'DX_PARA'].iloc[0]
hr, ci_lo, ci_hi, p_val = r_dx['HR'], r_dx['CI_lo'], r_dx['CI_hi'], r_dx['p']
p_adj = r_dx['p_adj']

# Potencia post-hoc (Schoenfeld 1983)
cd = cox_data.dropna(subset=['DX_PARA', 'T_SERO_ABS_X1', 'E_SERO_ABS_X1'])
n_events = int(cd['E_SERO_ABS_X1'].sum())
p1 = cd['DX_PARA'].mean()

za = norm.ppf(0.975)
zb_80 = norm.ppf(0.80)
hr_min_80 = math.exp((za + zb_80) / math.sqrt(n_events * p1 * (1 - p1)))
log_hr = math.log(hr)
var_log_hr = 1 / (n_events * p1 * (1 - p1))
z_obs = abs(log_hr) / math.sqrt(var_log_hr)
power_obs = norm.cdf(z_obs - za)

n_dx1 = int((cd['DX_PARA'] == 1).sum())
n_dx0 = int((cd['DX_PARA'] == 0).sum())
ev_dx1 = int(cd[cd['DX_PARA'] == 1]['E_SERO_ABS_X1'].sum())
ev_dx0 = int(cd[cd['DX_PARA'] == 0]['E_SERO_ABS_X1'].sum())

# ============================================================
# Figura
# ============================================================
fig, (ax_km, ax_ann) = plt.subplots(1, 2, figsize=(14, 5.5),
                                     gridspec_kw={'width_ratios': [1.4, 1]})

# --- Panel izquierdo: KM estratificado ---
for _a, _b in [(0, 6), (12, 18), (24, 30)]:
    ax_km.axvspan(_a * 30.44, _b * 30.44,
                  color=C['grid'], alpha=0.35, zorder=0)

groups = {
    0: (f'Sin confirmación parasitológica (n={n_dx0}, ev={ev_dx0})', C['blue']),
    1: (f'Con confirmación parasitológica (n={n_dx1}, ev={ev_dx1})', C['red']),
}

for g, (lb, col) in groups.items():
    sub = km_full[km_full['DX_PARA'] == g]
    if len(sub) < 2:
        continue
    k = KaplanMeierFitter()
    k.fit(sub['T_SERO_ABS_X1'], sub['E_SERO_ABS_X1'], label=lb)
    k.plot_survival_function(ax=ax_km, ci_show=True, color=col, lw=1.8)

# Log-rank
g0 = km_full[km_full['DX_PARA'] == 0].dropna(subset=['T_SERO_ABS_X1'])
g1 = km_full[km_full['DX_PARA'] == 1].dropna(subset=['T_SERO_ABS_X1'])
if len(g0) >= 2 and len(g1) >= 2:
    lr = logrank_test(
        g0['T_SERO_ABS_X1'], g1['T_SERO_ABS_X1'],
        g0['E_SERO_ABS_X1'], g1['E_SERO_ABS_X1'],
    )
    pc = C['red'] if lr.p_value < 0.05 else C['muted']
    ax_km.text(0.97, 0.95, f'Log-rank p = {lr.p_value:.3f}',
               transform=ax_km.transAxes, ha='right', va='top',
               fontsize=11, fontweight='bold', color=pc,
               bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                         alpha=0.92, edgecolor=pc))

_sx = ax_km.secondary_xaxis(
    'top', functions=(lambda d: d / 30.44, lambda m: m * 30.44))
_sx.set_xlabel('Meses desde T₀', fontsize=8)
_sx.set_xticks([0, 6, 12, 18, 24, 30])

ax_km.set(xlabel='Días desde T₀', ylabel='P(no negativización)',
          ylim=(-0.05, 1.05),
          title='A. KM estratificado por diagnóstico parasitológico basal')
ax_km.legend(frameon=False, fontsize=7, loc='lower left')
ax_km.axhline(0.5, color=C['grid'], ls=':', lw=0.8)

# --- Panel derecho: resumen estadístico ---
ax_ann.axis('off')
ax_ann.set_xlim(0, 10)
ax_ann.set_ylim(0, 10)
ax_ann.set_title('B. Resumen estadístico', loc='left', fontsize=11)

lines = [
    ('Variable', 'Dx. parasitológico basal (DX\\_PARA)'),
    ('',         f'Coprocultivo y/o microscopía (+)'),
    ('', ''),
    ('n evaluable', f'{len(cd)} (de 44)'),
    ('DX\\_PARA = 1',
     f'n = {n_dx1}, eventos = {ev_dx1}'),
    ('DX\\_PARA = 0',
     f'n = {n_dx0}, eventos = {ev_dx0}'),
    ('', ''),
    ('HR (IC 95 %)',
     f'{hr:.2f} ({ci_lo:.2f}–{ci_hi:.2f})'),
    ('p crudo', f'{p_val:.3f}'),
    ('p ajustado (BH-FDR)', f'{p_adj:.3f}'),
    ('', ''),
    ('Potencia post-hoc',
     f'{power_obs * 100:.1f} % para HR observado de {hr:.2f}'),
    ('HR mínimo detectable',
     f'{hr_min_80:.2f} (potencia 80 %, α = 0,05)'),
    ('', ''),
    ('Interpretación',
     'Estudio insuficientemente potente'),
    ('', f'para detectar HR < {hr_min_80:.1f} en DX\\_PARA'),
    ('', f'(p₁ = {p1:.2f}, {n_events} eventos).'),
]

y = 9.5
for label, value in lines:
    if label == '' and value == '':
        y -= 0.35
        continue
    if label:
        ax_ann.text(0.3, y, label, fontsize=9, fontweight='bold',
                    va='top', color=C['text'])
    ax_ann.text(4.0, y, value, fontsize=9, va='top', color=C['annot'])
    y -= 0.55

plt.tight_layout()
plt.savefig('figures/fig-b5-dx-para.png', dpi=300, bbox_inches='tight')
plt.show()
