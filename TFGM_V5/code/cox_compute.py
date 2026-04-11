# ============================================================
# code/cox_compute.py
# ------------------------------------------------------------
# Cálculo Cox univariable sobre las 15 covariables preseleccionadas.
# Corrección BH–FDR. Lo consumen:
#   - code/fig_b3_forest.py      (p < 0,01)
#   - code/tab_cox_uni.py        (tabla completa ordenada por p)
#
# Lee:    cox_data, nice, ALPHA (del namespace)
# Escribe: cox_uni DataFrame (al namespace)
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

covs_uni = [
    'SEXO_V', 'EDAD', 'EDAD_ALTA',
    'INMUNO_SI', 'COMORB_SI', 'INMUNO_O_COMORB',
    'EOS_ALTA', 'EOS_MEDIANA',
    'SER_MEDIANA', 'SER_P75',
    'IGG_BASAL', 'EOS_BASAL',
    'MONO', 'RETRATADO', 'DX_PARA',
]

_cox_rows = []
for cov in covs_uni:
    _df = cox_data[['T_SERO_ABS_X1', 'E_SERO_ABS_X1', cov]].dropna()
    if _df[cov].nunique() < 2 or len(_df) < 5:
        continue
    try:
        _cph = CoxPHFitter()
        _cph.fit(_df, duration_col='T_SERO_ABS_X1', event_col='E_SERO_ABS_X1')
        _s = _cph.summary.loc[cov]
        _cox_rows.append({
            'Variable': cov,
            'n':        len(_df),
            'HR':       _s['exp(coef)'],
            'CI_lo':    _s['exp(coef) lower 95%'],
            'CI_hi':    _s['exp(coef) upper 95%'],
            'p':        _s['p'],
        })
    except Exception:
        pass

cox_uni = pd.DataFrame(_cox_rows).sort_values('p').reset_index(drop=True)
_reject, _p_adj, _, _ = multipletests(cox_uni['p'].values, alpha=ALPHA, method='fdr_bh')
cox_uni['p_adj'] = _p_adj
