# ============================================================
# code/cox_multi.py
# ------------------------------------------------------------
# Cox MULTIVARIABLE estratificado por sexo + validación AIC
# stepwise + Schoenfeld + VIF + C-statistic con bootstrap CI
# (1000 réplicas, con guard contra extremos) + potencia post-hoc
# (fórmula correcta de Schoenfeld 1983, con factor p×(1−p)).
#
# El stepwise forward por AIC se ejecuta sobre todas las
# covariables de cox_compute.py *excluyendo* SEXO_V (que ya
# violó proporcionalidad → se estratifica). Si AIC converge al
# mismo subconjunto pre-especificado [SER_MEDIANA, EOS_ALTA],
# el modelo final queda blindado frente a la crítica de
# "selección a posteriori" (stepwise_match = True).
#
# Lee:    cox_data, covs_uni, nice, ALPHA, CONFIG (namespace)
# Escribe (al namespace):
#   - multi_covs, df_multi, sm_cox, c_multi
#   - vif_values, sch_results, p_sexo
#   - _boot_hrs, _boot_c, _boot_ok, _c_boot_lo, _c_boot_hi
#   - _hr_det, _pow_2, _pow_15, _n_ev_power
#   - stepwise_selected, stepwise_match
# Output:  stdout LaTeX table + figures/tab-cox-multi.md
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

if 'cox_uni' not in dir():
    exec(open('code/cox_compute.py').read())

from lifelines.statistics import proportional_hazard_test as ph_test_fn
import warnings as _w

multi_covs = ['SER_MEDIANA', 'EOS_ALTA']

# ------------------------------------------------------------
# 1. Test de Schoenfeld (sin estratificar) sobre las covariables
#    finales + sexo, para justificar la estratificación.
# ------------------------------------------------------------
df_schoenfeld = cox_data[['T_SERO_ABS_X1', 'E_SERO_ABS_X1',
                           'SER_MEDIANA', 'EOS_ALTA', 'SEXO_V']].dropna()
cph_test = CoxPHFitter()
with _w.catch_warnings():
    _w.simplefilter("ignore")
    cph_test.fit(df_schoenfeld, duration_col='T_SERO_ABS_X1',
                 event_col='E_SERO_ABS_X1')
ph_result  = ph_test_fn(cph_test, df_schoenfeld, time_transform='rank')
ph_summary = ph_result.summary

sch_results = {}
for col in ['SER_MEDIANA', 'EOS_ALTA', 'SEXO_V']:
    if col in ph_summary.index.get_level_values(0):
        sch_results[col] = ph_summary.loc[col, 'p'].min()
    else:
        sch_results[col] = np.nan
p_sexo = sch_results.get('SEXO_V', np.nan)

# ------------------------------------------------------------
# 2. Cox multivariable estratificado por sexo
# ------------------------------------------------------------
df_multi = cox_data[['T_SERO_ABS_X1', 'E_SERO_ABS_X1',
                      'SER_MEDIANA', 'EOS_ALTA', 'SEXO_V']].dropna()
cph_multi = CoxPHFitter()
cph_multi.fit(df_multi, duration_col='T_SERO_ABS_X1',
              event_col='E_SERO_ABS_X1', strata=['SEXO_V'])
sm_cox = cph_multi.summary[['exp(coef)', 'exp(coef) lower 95%',
                             'exp(coef) upper 95%', 'p']].copy()
sm_cox.columns = ['HR', 'CI_lo', 'CI_hi', 'p']
c_multi = cph_multi.concordance_index_

# ------------------------------------------------------------
# 3. VIF de las dos covariables (colinealidad)
# ------------------------------------------------------------
vif_data = df_multi[multi_covs].dropna()
vif_X    = sm.add_constant(vif_data)
vif_values = {}
for i, cov in enumerate(multi_covs):
    vif_values[cov] = variance_inflation_factor(vif_X.values, i + 1)

# ------------------------------------------------------------
# 4. Forward stepwise por AIC (excluyendo SEXO_V) → validación
#    cruzada del subconjunto pre-especificado [SER_MEDIANA,
#    EOS_ALTA]. Replica el patrón de archivo/Selecto.qmd.
# ------------------------------------------------------------
_step_covs = [c for c in covs_uni if c != 'SEXO_V']
stepwise_selected = []
_best_aic = np.inf
_max_vars = 5  # margen suficiente para detectar sobreajuste

for _step in range(_max_vars):
    _best_cov, _best_step_aic = None, np.inf
    for _cov in _step_covs:
        if _cov in stepwise_selected:
            continue
        _test = stepwise_selected + [_cov]
        _df_s = cox_data[['T_SERO_ABS_X1', 'E_SERO_ABS_X1', 'SEXO_V'] + _test].dropna()
        if _df_s[_cov].nunique() < 2 or len(_df_s) < 10:
            continue
        try:
            _cph_s = CoxPHFitter()
            with _w.catch_warnings():
                _w.simplefilter("ignore")
                _cph_s.fit(_df_s, duration_col='T_SERO_ABS_X1',
                           event_col='E_SERO_ABS_X1', strata=['SEXO_V'])
            _aic = -2 * _cph_s.log_likelihood_ + 2 * len(_test)
            if _aic < _best_step_aic:
                _best_step_aic = _aic
                _best_cov = _cov
        except Exception:
            pass
    if _best_cov and _best_step_aic < _best_aic:
        stepwise_selected.append(_best_cov)
        _best_aic = _best_step_aic
    else:
        break

stepwise_match = set(stepwise_selected) == set(multi_covs)

# ------------------------------------------------------------
# 5. Bootstrap (1000 réplicas) → C-statistic CI + HR por covar.
#    Guard contra extremos: si <500 réplicas exitosas o ancho
#    CI > 0,5 → no se reporta el CI bootstrap.
# ------------------------------------------------------------
np.random.seed(CONFIG['SEED'])
_boot_hrs  = {cov: [] for cov in multi_covs}
_boot_c    = []
_boot_fail = 0
for _ in range(1000):
    _idx = np.random.choice(len(df_multi), len(df_multi), replace=True)
    _bs  = df_multi.iloc[_idx].copy()
    try:
        _cph_b = CoxPHFitter()
        with _w.catch_warnings():
            _w.simplefilter("ignore")
            _cph_b.fit(_bs, duration_col='T_SERO_ABS_X1',
                       event_col='E_SERO_ABS_X1', strata=['SEXO_V'])
        for cov in multi_covs:
            _boot_hrs[cov].append(np.exp(_cph_b.params_[cov]))
        _boot_c.append(_cph_b.concordance_index_)
    except Exception:
        _boot_fail += 1
_boot_ok = 1000 - _boot_fail

if _boot_c:
    _c_boot_lo, _c_boot_hi = np.percentile(_boot_c, [2.5, 97.5])
else:
    _c_boot_lo, _c_boot_hi = np.nan, np.nan

_c_boot_stable = (_boot_ok >= 500) and ((_c_boot_hi - _c_boot_lo) < 0.5)

# ------------------------------------------------------------
# 6. Potencia post-hoc (Schoenfeld 1983)
#    HR detectable y potencia para HR=2,0 / HR=1,5 con
#    α = 0,05 bilateral, p₁ = 0,5 (asumiendo split equilibrado).
#    Fórmula incluyendo p × (1−p) → coincide con manuscrito.qmd.
# ------------------------------------------------------------
_n_ev_power = int(df_multi['E_SERO_ABS_X1'].sum())
_p_ratio    = 0.5
_z_alpha    = norm.ppf(1 - ALPHA / 2)
_z_beta     = norm.ppf(CONFIG['POWER'])
_denom_pwr  = np.sqrt(_n_ev_power * _p_ratio * (1 - _p_ratio))

_hr_det = np.exp((_z_alpha + _z_beta) / _denom_pwr)
_pow_2  = norm.cdf(_denom_pwr * abs(np.log(2.0)) - _z_alpha)
_pow_15 = norm.cdf(_denom_pwr * abs(np.log(1.5)) - _z_alpha)

# ------------------------------------------------------------
# 7. Salida LaTeX (table)
# ------------------------------------------------------------
_step_str_tex = ', '.join(s.replace('_', r'\_') for s in stepwise_selected) if stepwise_selected else '---'
print(r"""\begin{table}[H]
\centering
\caption{Cox multivariable estratificado por sexo (n = """ + str(len(df_multi))
        + r""", eventos = """ + str(_n_ev_power) + r""").
Validación cruzada por AIC stepwise: """
        + ("\\textbf{converge} al mismo subconjunto pre-especificado [IgG-ELISA basal $\\geq$ mediana, eosinofilia al diagnóstico $\\geq$ 0,5]"
           if stepwise_match else
           f"selecciona [{_step_str_tex}], distinto del pre-especificado")
        + r""".}
\label{tab-cox-multi}
\small
\begin{tabular}{l c c c}
\toprule
\textbf{Variable} & \textbf{HR (IC 95\%)} & \textbf{p} & \textbf{VIF} \\
\midrule""")
for var, row in sm_cox.iterrows():
    name = nice.get(var, var).replace('>=', '$\\geq$').replace('≥', '$\\geq$')
    ci   = f"{row['HR']:.2f} ({row['CI_lo']:.2f}--{row['CI_hi']:.2f})"
    vifs = f"{vif_values.get(var, 0):.2f}" if var in vif_values else "---"
    print(f"{name} & {ci} & {row['p']:.3f} & {vifs} \\\\")
print(r"Sexo (varón) & \textit{Estratificada} & --- & --- \\")
print(r"\bottomrule")

_c_boot_str = (f" (IC 95\\% boot: {_c_boot_lo:.3f}--{_c_boot_hi:.3f})"
               if _c_boot_stable else "")
print(f"\\multicolumn{{4}}{{l}}{{\\footnotesize C-statistic: "
      f"{c_multi:.3f}{_c_boot_str}. Bootstrap: {_boot_ok}/1000 réplicas exitosas.}} \\\\")
print(f"\\multicolumn{{4}}{{l}}{{\\footnotesize Schoenfeld global: "
      f"SER\\_MEDIANA p = {sch_results['SER_MEDIANA']:.3f}; "
      f"EOS\\_ALTA p = {sch_results['EOS_ALTA']:.3f}; "
      f"SEXO p = {p_sexo:.3f} (estratificado).}} \\\\")
print(f"\\multicolumn{{4}}{{l}}{{\\footnotesize Potencia post-hoc "
      f"(Schoenfeld 1983): HR mín. detectable = {_hr_det:.2f}; "
      f"potencia HR=2,0: {_pow_2*100:.0f}\\%; HR=1,5: {_pow_15*100:.0f}\\%.}} \\\\")
print(r"""\end{tabular}
\end{table}""")

# ------------------------------------------------------------
# 8. Markdown export (espejo de la tabla LaTeX)
# ------------------------------------------------------------
with open('figures/tab-cox-multi.md', 'w', encoding='utf-8') as _f:
    _f.write(f"**Tabla 3. Cox multivariable estratificado por sexo "
             f"(n = {len(df_multi)}, eventos = {_n_ev_power}).**\n\n")
    _f.write("| Variable | HR (IC 95%) | p | VIF |\n|---|---|---|---|\n")
    for var, row in sm_cox.iterrows():
        nm  = nice.get(var, var).replace('$\\geq$', '≥')
        ci  = f"{row['HR']:.2f} ({row['CI_lo']:.2f}–{row['CI_hi']:.2f})"
        vfs = f"{vif_values.get(var, 0):.2f}" if var in vif_values else "—"
        _f.write(f"| {nm} | {ci} | {row['p']:.3f} | {vfs} |\n")
    _f.write("| Sexo (varón) | _Estratificada_ | — | — |\n\n")
    _f.write(f"_C-statistic: {c_multi:.3f}"
             f"{f' (IC 95% boot: {_c_boot_lo:.3f}–{_c_boot_hi:.3f})' if _c_boot_stable else ''}. "
             f"Bootstrap: {_boot_ok}/1000 réplicas exitosas._\n\n")
    _f.write(f"_Schoenfeld: SER_MEDIANA p = {sch_results['SER_MEDIANA']:.3f}; "
             f"EOS_ALTA p = {sch_results['EOS_ALTA']:.3f}; "
             f"SEXO p = {p_sexo:.3f} (estratificado)._\n\n")
    _f.write(f"_Potencia post-hoc (Schoenfeld 1983): "
             f"HR mín. detectable = {_hr_det:.2f}; "
             f"potencia HR=2,0: {_pow_2*100:.0f}%; HR=1,5: {_pow_15*100:.0f}%._\n\n")
    _f.write(f"_Validación AIC stepwise: "
             f"{'converge al subconjunto pre-especificado' if stepwise_match else 'selecciona [' + ', '.join(stepwise_selected) + ']'}._\n")
