# ============================================================
# code/fig_b4_lmm.py
# ------------------------------------------------------------
# Figura 6: Trayectoria paramétrica (LMM) de log(IgG).
#
# Diseño editorial mejorado para lectura a primera vista:
#   - Dos paneles lado a lado en un único figure
#       A. Trayectoria global: spaghetti + recta + banda IC 95 %
#          de la media + umbral log(1,1) + línea vertical en
#          el tiempo de cruce LMM y mediana KM (anotaciones
#          separadas en la parte alta/baja del panel para
#          evitar superposición de iconos).
#       B. Comparación varones vs mujeres: rectas con sus
#          bandas IC 95 %, tiempos de cruce individuales y
#          p-valor de la interacción meses × sexo.
#   - Franjas grises alternas por semestre en ambos paneles.
#   - Fontsize base aumentado (11) y leyendas explícitas.
#
# Lee:    pac, ser_long, SERO_NEG, kmf (del namespace)
# Escribe: r_ser, b0, b1, r2m, r2c (al namespace)
# Output: figures/fig-b4-lmm.png
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

if 'kmf' not in dir():
    exec(open('code/fig_b2_km_baseline.py').read())

# ------------------------------------------------------------
# Construcción del dataset LMM (basal + seguimiento)
# ------------------------------------------------------------
_sero_pos_ids = set(pac[pac['IGG_BASAL'] >= SERO_NEG]['ID'])

lmm_basal = pac[pac['ID'].isin(_sero_pos_ids) & pac['IGG_BASAL'].notna()][['ID', 'IGG_BASAL']].copy()
lmm_basal['meses']   = 0.0
lmm_basal['log_igg'] = np.log(lmm_basal['IGG_BASAL'].clip(lower=0.01))
lmm_basal = lmm_basal[['ID', 'meses', 'log_igg']]

lmm_post = ser_long[
    (ser_long['dias'] > 0) & (ser_long['ID'].isin(_sero_pos_ids))
][['ID', 'dias', 'IGG']].dropna().copy()
lmm_post['log_igg'] = np.log(lmm_post['IGG'].clip(lower=0.01))
lmm_post['meses']   = lmm_post['dias'] / 30.44
lmm_post = lmm_post[['ID', 'meses', 'log_igg']]

lmm_ser = pd.concat([lmm_basal, lmm_post], ignore_index=True).sort_values(['ID', 'meses'])

# ------------------------------------------------------------
# Ajuste LMM (intercepto aleatorio + pendiente aleatoria si AIC menor)
# ------------------------------------------------------------
r_ri = smf.mixedlm("log_igg ~ meses", lmm_ser, groups=lmm_ser["ID"]).fit(reml=True)
try:
    r_rs = smf.mixedlm("log_igg ~ meses", lmm_ser, groups=lmm_ser["ID"],
                       re_formula="~meses").fit(reml=True)
    aic_ri = -2 * r_ri.llf + 2 * 3
    aic_rs = -2 * r_rs.llf + 2 * 5
    use_rs = aic_rs < aic_ri
except Exception:
    use_rs = False
    aic_ri, aic_rs = np.nan, np.nan
r_ser = r_rs if use_rs else r_ri

b0      = r_ser.fe_params['Intercept']
b1      = r_ser.fe_params['meses']
p_slope = r_ser.pvalues['meses']

# R² marginal y condicional
X_beta    = r_ser.fe_params['Intercept'] + r_ser.fe_params['meses'] * lmm_ser['meses']
var_fe    = np.var(X_beta)
var_re    = float(np.trace(r_ser.cov_re))
var_resid = r_ser.scale
r2m = var_fe / (var_fe + var_re + var_resid)
r2c = (var_fe + var_re) / (var_fe + var_re + var_resid)

# ------------------------------------------------------------
# Modelo con interacción sexo
# ------------------------------------------------------------
lmm_sex = lmm_ser.merge(pac[['ID', 'SEXO_V']], on='ID')
r_sex = smf.mixedlm("log_igg ~ meses * SEXO_V", lmm_sex, groups=lmm_sex["ID"]).fit(reml=True)
_p_inter = r_sex.pvalues['meses:SEXO_V']
_b_inter = r_sex.fe_params['meses:SEXO_V']
_b_meses = r_sex.fe_params['meses']
_slope_f = _b_meses
_slope_m = _b_meses + _b_inter
_b0_sex  = r_sex.fe_params['Intercept']
_b_sexo  = r_sex.fe_params['SEXO_V']
_n_m     = lmm_sex[lmm_sex['SEXO_V'] == 1]['ID'].nunique()
_n_f     = lmm_sex[lmm_sex['SEXO_V'] == 0]['ID'].nunique()

max_m = min(lmm_ser['meses'].max(), 36)
x_mod = np.linspace(0, max_m, 120)

# Umbral en escala log
_log_th = np.log(SERO_NEG)

# Cruces (global y por sexo)
t_cross_global = (_log_th - b0) / b1 if b1 < 0 else np.nan
t_cross_m      = (_log_th - (_b0_sex + _b_sexo)) / _slope_m if _slope_m < 0 else np.nan
t_cross_f      = (_log_th - _b0_sex) / _slope_f if _slope_f < 0 else np.nan
km_med_m       = kmf.median_survival_time_ / 30.44

# ------------------------------------------------------------
# Figura: 2 paneles lado a lado
# ------------------------------------------------------------
fig = plt.figure(figsize=(16, 7))
gs  = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], wspace=0.22)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1], sharey=axA)

# Límites comunes Y (con headroom generoso para las anotaciones)
_y_min = min(lmm_ser['log_igg'].min(), _log_th - 0.5) - 0.4
_y_max = max(lmm_ser['log_igg'].max(), _log_th + 0.5) + 0.9

def _add_semester_stripes(ax):
    """Franjas alternas por semestre (en meses)."""
    for _a, _b in [(0, 6), (12, 18), (24, 30)]:
        ax.axvspan(_a, _b, color=C['grid'], alpha=0.35, zorder=0)

# ============================================================
# Panel A. Trayectoria global
# ============================================================
_add_semester_stripes(axA)

# Spaghetti individual (gris para no competir con la recta global)
for pid, grp in lmm_ser.groupby('ID'):
    g = grp.sort_values('meses')
    axA.plot(g['meses'], g['log_igg'],
             color=C['muted'], alpha=0.30, lw=0.7, zorder=2)

# Banda IC 95 % de la media global
y_pred = b0 + b1 * x_mod
se_b0  = r_ser.bse_fe['Intercept']
se_b1  = r_ser.bse_fe['meses']
se_pred = np.sqrt(se_b0 ** 2 + x_mod ** 2 * se_b1 ** 2)
axA.fill_between(x_mod, y_pred - 1.96 * se_pred, y_pred + 1.96 * se_pred,
                 color=C['blue'], alpha=0.22, zorder=3,
                 label='IC 95 % de la media (LMM)')

# Recta global
axA.plot(x_mod, y_pred, color=C['blue'], lw=3.8, zorder=4,
         label=f'Recta LMM global: {b1:+.4f} log(IgG)/mes')

# Umbral horizontal
axA.axhline(_log_th, color=C['gold'], ls='--', lw=2.2,
            label=f'Umbral log({SERO_NEG:.1f}) = {_log_th:.2f}', zorder=5)

# Vertical en el cruce del LMM (anclamos en el umbral y desplazamos
# con offset en puntos para que el texto quede dentro del panel
# con independencia de los límites Y)
if not np.isnan(t_cross_global) and 0 < t_cross_global < max_m:
    axA.axvline(t_cross_global, color=C['blue'], ls=':', lw=1.8, zorder=5)
    axA.annotate(
        f'Cruce LMM: {t_cross_global:.1f} m',
        xy=(t_cross_global, _log_th),
        xytext=(12, 55),
        textcoords='offset points',
        fontsize=11, color=C['blue'], fontweight='bold',
        ha='left', va='center',
        arrowprops=dict(arrowstyle='->', color=C['blue'], lw=1.3),
    )

# Vertical en la mediana KM (referencia no paramétrica)
if km_med_m < np.inf and 0 < km_med_m < max_m:
    axA.axvline(km_med_m, color=C['red'], ls=':', lw=1.8, zorder=5)
    axA.annotate(
        f'Mediana KM: {km_med_m:.1f} m',
        xy=(km_med_m, _log_th),
        xytext=(-12, -55),
        textcoords='offset points',
        fontsize=11, color=C['red'], fontweight='bold',
        ha='right', va='center',
        arrowprops=dict(arrowstyle='->', color=C['red'], lw=1.3),
    )

# Caja de bondad de ajuste (esquina inferior derecha: el bottom-left
# está reservado para la anotación de la mediana KM)
_p_fmt_slope = 'p < 0,001' if p_slope < 0.001 else f'p = {p_slope:.3f}'
axA.text(
    0.98, 0.04,
    f'$R^2$ marg = {r2m:.2f}  |  $R^2$ cond = {r2c:.2f}\n'
    f'pendiente: {_p_fmt_slope}',
    transform=axA.transAxes, fontsize=10, va='bottom', ha='right',
    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
              alpha=0.92, edgecolor=C['grid']),
)

axA.set(xlabel='Meses desde T₀', ylabel='log(IgG-ELISA)',
        xlim=(0, max_m), ylim=(_y_min, _y_max),
        title=f'A. Trayectoria global  (n = {lmm_ser["ID"].nunique()} seropositivos)')
axA.legend(frameon=True, fontsize=9, loc='upper right',
           facecolor='white', framealpha=0.92, edgecolor=C['grid'])

# ============================================================
# Panel B. Comparación varones vs mujeres
# ============================================================
_add_semester_stripes(axB)

# Spaghetti individual, bicolor por sexo (muy tenue)
for pid, grp in lmm_sex.groupby('ID'):
    g  = grp.sort_values('meses')
    sx = g['SEXO_V'].iloc[0]
    col = C['blue'] if sx == 1 else C['red']
    axB.plot(g['meses'], g['log_igg'],
             color=col, alpha=0.12, lw=0.7, zorder=2)

# Rectas por sexo (con bandas IC 95 % aproximadas)
y_m = (_b0_sex + _b_sexo) + _slope_m * x_mod
y_f =  _b0_sex              + _slope_f * x_mod

# Bandas IC 95 % aproximadas usando se_pred del modelo combinado
# (no exacto, pero adecuado para una comparación visual)
_se_m = np.sqrt(r_sex.bse_fe['Intercept'] ** 2
                + r_sex.bse_fe['SEXO_V'] ** 2
                + x_mod ** 2 * (r_sex.bse_fe['meses'] ** 2
                                + r_sex.bse_fe['meses:SEXO_V'] ** 2))
_se_f = np.sqrt(r_sex.bse_fe['Intercept'] ** 2
                + x_mod ** 2 * r_sex.bse_fe['meses'] ** 2)

axB.fill_between(x_mod, y_m - 1.96 * _se_m, y_m + 1.96 * _se_m,
                 color=C['blue'], alpha=0.18, zorder=3)
axB.fill_between(x_mod, y_f - 1.96 * _se_f, y_f + 1.96 * _se_f,
                 color=C['red'], alpha=0.18, zorder=3)

axB.plot(x_mod, y_m, color=C['blue'], lw=3.0, ls='-',
         label=f'Varones: {_slope_m:+.4f}/mes  (n = {_n_m})',
         zorder=4)
axB.plot(x_mod, y_f, color=C['red'], lw=3.0, ls='--',
         label=f'Mujeres: {_slope_f:+.4f}/mes  (n = {_n_f})',
         zorder=4)

# Umbral
axB.axhline(_log_th, color=C['gold'], ls='--', lw=2.2,
            label=f'Umbral log({SERO_NEG:.1f})', zorder=5)

# Verticales en los cruces por sexo (anotaciones con offset en
# puntos para evitar colisiones con el título o la leyenda).
# Colocamos el rótulo de varones ABAJO y el de mujeres ARRIBA
# para que coincida con la posición vertical real de cada recta
# (la recta de mujeres desciende más lentamente y queda por
# encima; la de varones, por debajo).
if not np.isnan(t_cross_m) and 0 < t_cross_m < max_m:
    axB.axvline(t_cross_m, color=C['blue'], ls=':', lw=1.5, zorder=5)
    axB.annotate(
        f'Varones: {t_cross_m:.1f} m',
        xy=(t_cross_m, _log_th),
        xytext=(10, -48),
        textcoords='offset points',
        fontsize=11, color=C['blue'], fontweight='bold',
        ha='left', va='center',
        arrowprops=dict(arrowstyle='->', color=C['blue'], lw=1.2),
    )
if not np.isnan(t_cross_f) and 0 < t_cross_f < max_m:
    axB.axvline(t_cross_f, color=C['red'], ls=':', lw=1.5, zorder=5)
    axB.annotate(
        f'Mujeres: {t_cross_f:.1f} m',
        xy=(t_cross_f, _log_th),
        xytext=(-10, 48),
        textcoords='offset points',
        fontsize=11, color=C['red'], fontweight='bold',
        ha='right', va='center',
        arrowprops=dict(arrowstyle='->', color=C['red'], lw=1.2),
    )

# p-valor de la interacción (esquina inferior izquierda, separada
# de las anotaciones que están en el centro del panel)
_p_fmt = f'p = {_p_inter:.3f}' if _p_inter >= 0.001 else 'p < 0,001'
_ns_fmt = ' (NS)' if _p_inter >= 0.05 else ''
axB.text(
    0.02, 0.04,
    f'Interacción meses × sexo\n{_p_fmt}{_ns_fmt}',
    transform=axB.transAxes, fontsize=10, va='bottom',
    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
              alpha=0.92, edgecolor=C['grid']),
)

axB.set(xlabel='Meses desde T₀', ylabel='',
        xlim=(0, max_m),
        title='B. Estratificación por sexo')
axB.legend(frameon=True, fontsize=9, loc='upper right',
           facecolor='white', framealpha=0.92, edgecolor=C['grid'])

plt.tight_layout()
plt.savefig('figures/fig-b4-lmm.png', dpi=300, bbox_inches='tight')
plt.show()
