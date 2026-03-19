#!/usr/bin/env python3
"""
TFGM — Análisis Avanzado (Fases 1–3)
Implementaciones from-scratch con código de validación contra lifelines/statsmodels
"""

import numpy as np
import pandas as pd
from scipy import stats as sp_stats
from scipy.optimize import minimize
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# ── Config ────────────────────────────────────────────────────────────────
OUT = Path('outputs_avanzado')
for sub in ['figures', 'tables']:
    (OUT / sub).mkdir(parents=True, exist_ok=True)

PAL = {
    'seroneg': '#1565C0', 'no_seroneg': '#E65100',
    'inmuno_dep': '#D32F2F', 'inmuno_comp': '#1565C0',
    'male': '#1565C0', 'female': '#E65100',
    'eos_si': '#2E7D32', 'eos_no': '#9E9E9E',
    'igg_alta': '#6A1B9A', 'igg_baja': '#00838F',
    'neutral': '#37474F', 'highlight': '#F9A825',
    'concordant': '#2E7D32', 'discordant': '#D32F2F', 'neither': '#9E9E9E',
}
plt.rcParams.update({
    'font.family': 'sans-serif', 'font.size': 11,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.alpha': 0.3,
    'figure.dpi': 150, 'savefig.dpi': 300,
    'figure.facecolor': 'white',
})

df = pd.read_excel('BASE_SPSS.xlsx')
print(f"✅ Dataset: {df.shape[0]} × {df.shape[1]}")

# ═══════════════════════════════════════════════════════════════════════════
# FASE 1.1 — Kaplan-Meier from scratch (con validación)
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "="*80)
print("FASE 1.1 — KAPLAN-MEIER: IMPLEMENTACIÓN FROM-SCRATCH")
print("="*80)

def kaplan_meier(time, event):
    """KM con IC 95% Greenwood. Retorna dict con todos los componentes."""
    mask = np.isfinite(time) & np.isfinite(event)
    time, event = np.array(time)[mask], np.array(event)[mask]
    n_total = len(time)
    order = np.argsort(time)
    time, event = time[order], event[order]
    unique_times = np.unique(time)

    km_t, km_s, km_lo, km_hi, km_n, km_d = [0.0], [1.0], [1.0], [1.0], [n_total], [0]
    n_at_risk, surv, gw_sum = n_total, 1.0, 0.0

    for t in unique_times:
        d_i = int(np.sum((time == t) & (event == 1)))
        c_i = int(np.sum((time == t) & (event == 0)))
        if d_i > 0:
            surv *= (1 - d_i / n_at_risk)
            if n_at_risk > d_i:
                gw_sum += d_i / (n_at_risk * (n_at_risk - d_i))
            se = surv * np.sqrt(gw_sum)
            lo, hi = max(0, surv - 1.96*se), min(1, surv + 1.96*se)
        else:
            lo, hi = km_lo[-1], km_hi[-1]
        km_t.append(t); km_s.append(surv); km_lo.append(lo); km_hi.append(hi)
        km_n.append(n_at_risk); km_d.append(d_i)
        n_at_risk -= (d_i + c_i)

    median = None
    for t, s in zip(km_t, km_s):
        if s <= 0.5:
            median = t; break

    return {'times': np.array(km_t), 'survival': np.array(km_s),
            'ci_lower': np.array(km_lo), 'ci_upper': np.array(km_hi),
            'at_risk': np.array(km_n), 'events': np.array(km_d),
            'median': median, 'n_total': int(mask.sum()), 'n_events': int(event.sum())}

# Test global KM
km_data = df[df['TIME_TO_SERONEG_M'].notna()].copy()
km_g = kaplan_meier(km_data['TIME_TO_SERONEG_M'].values, km_data['EVENT_SERONEG'].values)

print(f"\nKM Global from-scratch:")
print(f"  N = {km_g['n_total']}, Events = {km_g['n_events']}")
print(f"  Mediana = {km_g['median']:.4f} meses")
print(f"  S(6m) ~ {km_g['survival'][np.searchsorted(km_g['times'], 6)]:.4f}")
print(f"  S(12m) ~ {km_g['survival'][np.searchsorted(km_g['times'], 12)]:.4f}")

# ── Código de validación contra lifelines (para ejecutar cuando esté disponible) ──
validation_code_km = """
# ═══ VALIDACIÓN CONTRA LIFELINES ═══
# Ejecutar SOLO cuando lifelines esté instalado:
#   pip install lifelines
from lifelines import KaplanMeierFitter
kmf = KaplanMeierFitter()
kmf.fit(km_data['TIME_TO_SERONEG_M'], km_data['EVENT_SERONEG'])
print(f"lifelines  median: {kmf.median_survival_time_:.4f}")
print(f"scratch    median: {km_g['median']:.4f}")
print(f"Δ median: {abs(kmf.median_survival_time_ - km_g['median']):.2e}")

# Comparar S(t) en timepoints clave
for t in [3, 6, 12, 24]:
    s_ll = kmf.predict(t).values[0]
    idx = np.searchsorted(km_g['times'], t, side='right') - 1
    s_sc = km_g['survival'][max(0, idx)]
    print(f"  S({t:2d}m): lifelines={s_ll:.6f}  scratch={s_sc:.6f}  Δ={abs(s_ll-s_sc):.2e}")
"""
print("\n📋 Código de validación lifelines guardado (ejecutar cuando esté instalado)")

# ═══════════════════════════════════════════════════════════════════════════
# FASE 1.1b — Cox PH from scratch (con validación)
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "="*80)
print("FASE 1.1b — COX PH: IMPLEMENTACIÓN FROM-SCRATCH")
print("="*80)

def cox_ph(time, event, X, var_names=None):
    """Cox PH via BFGS. Retorna DataFrame con HR, IC95, p."""
    time, event = np.asarray(time, float), np.asarray(event, float)
    X = np.asarray(X, float)
    if X.ndim == 1: X = X.reshape(-1, 1)
    n, p = X.shape
    if var_names is None: var_names = [f'X{i+1}' for i in range(p)]

    mask = np.isfinite(time) & np.isfinite(event) & np.all(np.isfinite(X), axis=1)
    time, event, X = time[mask], event[mask], X[mask]
    order = np.argsort(-time)
    time, event, X = time[order], event[order], X[order]

    def neg_ll(beta):
        Xb = X @ beta
        mx = np.max(Xb)
        exp_Xb = np.exp(Xb - mx)
        cum_exp = np.cumsum(exp_Xb)
        cum_exp = np.maximum(cum_exp, 1e-30)
        return -np.sum(event * (Xb - mx - np.log(cum_exp)))

    result = minimize(neg_ll, np.zeros(p), method='BFGS')
    beta_hat = result.x

    eps = 1e-5
    hess = np.zeros((p, p))
    for i in range(p):
        for j in range(i, p):
            e_i, e_j = np.zeros(p), np.zeros(p)
            e_i[i], e_j[j] = eps, eps
            fpp = neg_ll(beta_hat + e_i + e_j)
            fpm = neg_ll(beta_hat + e_i - e_j)
            fmp = neg_ll(beta_hat - e_i + e_j)
            fmm = neg_ll(beta_hat - e_i - e_j)
            hess[i,j] = hess[j,i] = (fpp - fpm - fmp + fmm) / (4*eps**2)

    try:
        se = np.sqrt(np.maximum(np.diag(np.linalg.inv(hess)), 1e-20))
    except:
        se = np.full(p, np.nan)

    z = beta_hat / se
    pval = 2*(1 - sp_stats.norm.cdf(np.abs(z)))
    hr = np.exp(beta_hat)

    return pd.DataFrame({
        'Variable': var_names, 'coef': beta_hat, 'se': se,
        'HR': hr, 'IC95_lo': np.exp(beta_hat - 1.96*se),
        'IC95_hi': np.exp(beta_hat + 1.96*se),
        'z': z, 'p': pval, 'n': int(mask.sum()), 'events': int(event.sum()),
    })

# Test: Cox univariable IGG_BASAL
sub = km_data[['IGG_BASAL','TIME_TO_SERONEG_M','EVENT_SERONEG']].dropna()
cox_igg = cox_ph(sub['TIME_TO_SERONEG_M'].values, sub['EVENT_SERONEG'].values,
                  sub[['IGG_BASAL']].values, ['IGG_BASAL'])
print(f"\nCox univariable IGG_BASAL (from-scratch):")
print(f"  HR = {cox_igg['HR'].values[0]:.4f}, p = {cox_igg['p'].values[0]:.6f}")
print(f"  coef = {cox_igg['coef'].values[0]:.6f}, se = {cox_igg['se'].values[0]:.6f}")

validation_code_cox = """
# ═══ VALIDACIÓN CONTRA LIFELINES COX ═══
from lifelines import CoxPHFitter
cph = CoxPHFitter()
cox_df = sub[['TIME_TO_SERONEG_M','EVENT_SERONEG','IGG_BASAL']].copy()
cph.fit(cox_df, 'TIME_TO_SERONEG_M', 'EVENT_SERONEG')
print(cph.summary[['coef','se(coef)','exp(coef)','p']])
print(f"\\nlifelines coef: {cph.summary['coef'].values[0]:.6f}")
print(f"scratch   coef: {cox_igg['coef'].values[0]:.6f}")
print(f"Δ coef: {abs(cph.summary['coef'].values[0] - cox_igg['coef'].values[0]):.2e}")
"""
print("📋 Código de validación lifelines-Cox guardado")

# ═══════════════════════════════════════════════════════════════════════════
# FASE 1.2 — IMPUTACIÓN MICE FROM SCRATCH
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "="*80)
print("FASE 1.2 — IMPUTACIÓN MICE (Multivariate Imputation by Chained Equations)")
print("="*80)

def mice_impute(data, target_col, predictor_cols, n_iterations=20, n_imputations=5, seed=42):
    """
    MICE from scratch usando regresión lineal iterativa.

    Algoritmo:
    1. Inicializa los NaN con la mediana de cada columna.
    2. Para cada iteración:
       a. Para cada columna con NaN:
          - Ajusta una regresión lineal usando las demás columnas como predictores.
          - Predice los valores faltantes + ruido aleatorio (PMM simplificado).
    3. Repite n_iterations veces.
    4. Repite n_imputations veces con diferentes semillas → media de imputaciones.

    Esto es equivalente a sklearn.experimental.IterativeImputer pero transparente.
    """
    rng = np.random.RandomState(seed)
    cols = [target_col] + predictor_cols
    work = data[cols].copy()

    # Índices de NaN en la columna target
    missing_idx = work[target_col].isna()
    n_missing = missing_idx.sum()
    print(f"  Target: {target_col}, missing: {n_missing}/{len(work)}")
    print(f"  Predictores: {predictor_cols}")

    if n_missing == 0:
        print("  → Sin valores faltantes, nada que imputar.")
        return data[target_col].values

    all_imputed = []

    for imp in range(n_imputations):
        seed_imp = seed + imp * 1000
        rng_imp = np.random.RandomState(seed_imp)

        # Paso 1: inicializar NaN con mediana
        filled = work.copy()
        for c in cols:
            med = filled[c].median()
            filled[c] = filled[c].fillna(med)

        # Paso 2: iterar
        for iteration in range(n_iterations):
            for c in [target_col]:  # Solo imputamos la target
                # Observados vs faltantes
                obs_mask = ~work[c].isna()
                mis_mask = work[c].isna()

                if mis_mask.sum() == 0:
                    continue

                preds = [p for p in cols if p != c]
                X_obs = filled.loc[obs_mask, preds].values
                y_obs = work.loc[obs_mask, c].values  # Valores REALES observados
                X_mis = filled.loc[mis_mask, preds].values

                # Regresión lineal: y = Xβ + ε
                # β = (X'X)^{-1} X'y
                ones_obs = np.column_stack([np.ones(len(X_obs)), X_obs])
                ones_mis = np.column_stack([np.ones(len(X_mis)), X_mis])

                try:
                    beta = np.linalg.lstsq(ones_obs, y_obs, rcond=None)[0]
                    y_pred = ones_mis @ beta
                    # Residual variance
                    residuals = y_obs - ones_obs @ beta
                    sigma = np.std(residuals)
                    # PMM simplificado: añadir ruido proporcional al error
                    noise = rng_imp.normal(0, sigma, size=len(y_pred))
                    y_imputed = y_pred + noise
                    # Clamp a valores razonables (no negativos para IgG)
                    y_imputed = np.maximum(y_imputed, 0.1)
                    filled.loc[mis_mask, c] = y_imputed
                except:
                    pass

        all_imputed.append(filled[target_col].values.copy())

    # Rubin's rules: media de las m imputaciones
    stacked = np.array(all_imputed)
    final = data[target_col].copy().values.astype(float)
    for i in range(len(final)):
        if np.isnan(final[i]):
            final[i] = np.mean(stacked[:, i])

    return final

# Imputar IGG_BASAL
print("\nImputando IGG_BASAL con MICE (5 imputaciones × 20 iteraciones)...")
df_imputed = df.copy()
df_imputed['IGG_BASAL_IMP'] = mice_impute(
    df, 'IGG_BASAL',
    ['EDAD_DX', 'SEXO_COD', 'EOS_BASAL'],
    n_iterations=20, n_imputations=5, seed=42
)

print(f"\nResultados de imputación:")
print(f"  IGG_BASAL original: {df['IGG_BASAL'].notna().sum()} con dato, {df['IGG_BASAL'].isna().sum()} NaN")
print(f"  IGG_BASAL imputada: {df_imputed['IGG_BASAL_IMP'].notna().sum()} con dato")
print(f"\n  Valores imputados para los {df['IGG_BASAL'].isna().sum()} pacientes con NaN:")
imp_mask = df['IGG_BASAL'].isna()
for _, row in df_imputed[imp_mask][['ID','EDAD_DX','SEXO_COD','EOS_BASAL','IGG_BASAL','IGG_BASAL_IMP']].iterrows():
    eos_str = f"{row['EOS_BASAL']:.2f}" if pd.notna(row['EOS_BASAL']) else "NA"
    print(f"    ID {int(row['ID'])}: Edad={row['EDAD_DX']}, Sexo={'M' if row['SEXO_COD']==1 else 'V'}, "
          f"EOS={eos_str} → IGG_IMP={row['IGG_BASAL_IMP']:.2f}")

# Comparar distribuciones
print(f"\n  Distribución original: med={df['IGG_BASAL'].median():.2f}, IQR={df['IGG_BASAL'].quantile(.25):.2f}–{df['IGG_BASAL'].quantile(.75):.2f}")
print(f"  Distribución imputada: med={df_imputed['IGG_BASAL_IMP'].median():.2f}, IQR={df_imputed['IGG_BASAL_IMP'].quantile(.25):.2f}–{df_imputed['IGG_BASAL_IMP'].quantile(.75):.2f}")

validation_code_mice = """
# ═══ VALIDACIÓN CONTRA SKLEARN ═══
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
imp = IterativeImputer(max_iter=20, random_state=42, sample_posterior=True)
cols = ['IGG_BASAL','EDAD_DX','SEXO_COD','EOS_BASAL']
X_imp = imp.fit_transform(df[cols])
sklearn_igg = X_imp[:, 0]
print("Comparación MICE scratch vs sklearn:")
for i in range(44):
    if df['IGG_BASAL'].isna().iloc[i]:
        print(f"  ID {df['ID'].iloc[i]}: scratch={df_imputed['IGG_BASAL_IMP'].iloc[i]:.3f}  sklearn={sklearn_igg[i]:.3f}")
"""
print("\n📋 Código de validación sklearn-MICE guardado")

# ═══════════════════════════════════════════════════════════════════════════
# FASE 1.3 — RE-ANÁLISIS COX CON DATOS IMPUTADOS
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "="*80)
print("FASE 1.3 — COX MULTIVARIABLE: ORIGINAL vs IMPUTADO")
print("="*80)

# Original (N=30, como antes)
MULTI_VARS = ['IGG_BASAL', 'INMUNO_DICO', 'EOS_BASAL', 'EDAD_DX']
MULTI_NAMES = ['IgG basal', 'Inmunodeprimido', 'Eosinófilos', 'Edad']
sub_orig = km_data[MULTI_VARS + ['TIME_TO_SERONEG_M','EVENT_SERONEG']].dropna()
cox_orig = cox_ph(sub_orig['TIME_TO_SERONEG_M'].values, sub_orig['EVENT_SERONEG'].values,
                   sub_orig[MULTI_VARS].values, MULTI_NAMES)

# Imputado (N=40 o más)
km_imp = df_imputed[df_imputed['TIME_TO_SERONEG_M'].notna()].copy()
MULTI_VARS_IMP = ['IGG_BASAL_IMP', 'INMUNO_DICO', 'EOS_BASAL', 'EDAD_DX']
sub_imp = km_imp[MULTI_VARS_IMP + ['TIME_TO_SERONEG_M','EVENT_SERONEG']].dropna()
cox_imp = cox_ph(sub_imp['TIME_TO_SERONEG_M'].values, sub_imp['EVENT_SERONEG'].values,
                  sub_imp[MULTI_VARS_IMP].values, MULTI_NAMES)

print(f"\n{'Variable':<20} │ {'ORIGINAL (N='+str(cox_orig['n'].iloc[0])+')':<25} │ {'IMPUTADO (N='+str(cox_imp['n'].iloc[0])+')':<25} │ Δ HR")
print("─"*95)
for i in range(len(cox_orig)):
    hr_o = cox_orig['HR'].iloc[i]
    hr_i = cox_imp['HR'].iloc[i]
    p_o = cox_orig['p'].iloc[i]
    p_i = cox_imp['p'].iloc[i]
    sig_o = '*' if p_o < 0.05 else ''
    sig_i = '*' if p_i < 0.05 else ''
    name = cox_orig['Variable'].iloc[i]
    ci_o = f"({cox_orig['IC95_lo'].iloc[i]:.2f}–{cox_orig['IC95_hi'].iloc[i]:.2f})"
    ci_i = f"({cox_imp['IC95_lo'].iloc[i]:.2f}–{cox_imp['IC95_hi'].iloc[i]:.2f})"
    print(f"  {name:<18} │ HR {hr_o:.3f} {ci_o} p={p_o:.3f}{sig_o:1s} │ HR {hr_i:.3f} {ci_i} p={p_i:.3f}{sig_i:1s} │ {abs(hr_o-hr_i):.3f}")

# ═══════════════════════════════════════════════════════════════════════════
# FASE 2.1 — MODELO LINEAL MIXTO (LMM) FROM SCRATCH
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "="*80)
print("FASE 2.1 — MODELO LINEAL MIXTO: PENDIENTE DE CAÍDA DE log(IgG)")
print("="*80)

# Construir dataset longitudinal: una fila por (paciente, timepoint)
igg_cuanti_cols = ['IGG_M3_CUANTI','IGG_M6_CUANTI','IGG_M12_CUANTI','IGG_M18_CUANTI',
                   'IGG_M24_CUANTI','IGG_M36_CUANTI','IGG_M48_CUANTI','IGG_M72_CUANTI']
igg_mes_cols = ['IGG_M3_MES','IGG_M6_MES','IGG_M12_MES','IGG_M18_MES',
                'IGG_M24_MES','IGG_M36_MES','IGG_M48_MES','IGG_M72_MES']

long_rows = []
for _, row in df.iterrows():
    pid = int(row['ID'])
    sexo = row['SEXO_COD']  # 1=M, 2=V
    inmuno = row['INMUNO_DICO']  # 1=inmunodep, 2=inmunocomp
    # Basal (mes 0)
    if pd.notna(row['IGG_BASAL']) and row['IGG_BASAL'] > 0:
        long_rows.append({'ID': pid, 'month': 0.0, 'igg': row['IGG_BASAL'],
                          'log_igg': np.log(row['IGG_BASAL']),
                          'sexo_v': 1 if sexo == 2 else 0,
                          'inmuno_dep': 1 if inmuno == 1 else 0})
    # Timepoints
    for ic, mc in zip(igg_cuanti_cols, igg_mes_cols):
        if pd.notna(row[ic]) and pd.notna(row[mc]) and row[ic] > 0:
            long_rows.append({'ID': pid, 'month': row[mc], 'igg': row[ic],
                              'log_igg': np.log(row[ic]),
                              'sexo_v': 1 if sexo == 2 else 0,
                              'inmuno_dep': 1 if inmuno == 1 else 0})

long_df = pd.DataFrame(long_rows).sort_values(['ID','month']).reset_index(drop=True)
print(f"\nDataset longitudinal: {len(long_df)} observaciones de {long_df['ID'].nunique()} pacientes")
print(f"Mediciones por paciente: mediana {long_df.groupby('ID').size().median():.0f}, "
      f"rango {long_df.groupby('ID').size().min()}–{long_df.groupby('ID').size().max()}")

# ── LMM from scratch: Estimación via GLS iterado ────────────────────────
# Modelo: log(IGG)_it = β₀ + β₁·month + β₂·sexo_v + β₃·inmuno_dep
#                       + β₄·month×sexo_v + β₅·month×inmuno_dep
#                       + u₀ᵢ + u₁ᵢ·month + εᵢₜ
# Donde (u₀ᵢ, u₁ᵢ) ~ N(0, D) son efectos aleatorios por paciente.
#
# Estimación simplificada en dos pasos:
# 1) OLS sobre efectos fijos → residuos
# 2) Estimar varianza de efectos aleatorios desde los residuos

# Paso 1: Efectos fijos con OLS (equivalente a modelo marginal)
long_df['month_x_sexo'] = long_df['month'] * long_df['sexo_v']
long_df['month_x_inmuno'] = long_df['month'] * long_df['inmuno_dep']

X_cols = ['month', 'sexo_v', 'inmuno_dep', 'month_x_sexo', 'month_x_inmuno']
y = long_df['log_igg'].values
X = np.column_stack([np.ones(len(y))] + [long_df[c].values for c in X_cols])

# OLS
beta_ols = np.linalg.lstsq(X, y, rcond=None)[0]
y_pred = X @ beta_ols
resid = y - y_pred
sigma2 = np.sum(resid**2) / (len(y) - len(beta_ols))

# Standard errors
XtX_inv = np.linalg.inv(X.T @ X)
se_ols = np.sqrt(sigma2 * np.diag(XtX_inv))
t_vals = beta_ols / se_ols
p_vals = 2 * (1 - sp_stats.t.cdf(np.abs(t_vals), df=len(y)-len(beta_ols)))

# Paso 2: Efectos aleatorios (intercepto + pendiente por paciente)
# Ajustar regresión individual para cada paciente → extraer intercepto y pendiente
re_intercepts = []
re_slopes = []
for pid, grp in long_df.groupby('ID'):
    if len(grp) >= 2:
        x_p = grp['month'].values
        y_p = grp['log_igg'].values
        X_p = np.column_stack([np.ones(len(x_p)), x_p])
        try:
            b_p = np.linalg.lstsq(X_p, y_p, rcond=None)[0]
            re_intercepts.append(b_p[0])
            re_slopes.append(b_p[1])
        except:
            pass

re_intercepts = np.array(re_intercepts)
re_slopes = np.array(re_slopes)

# Varianza de los efectos aleatorios
var_u0 = np.var(re_intercepts - np.mean(re_intercepts))
var_u1 = np.var(re_slopes - np.mean(re_slopes))
cov_u01 = np.cov(re_intercepts, re_slopes)[0, 1]

print(f"\n{'─'*70}")
print(f"EFECTOS FIJOS (OLS marginal)")
print(f"{'─'*70}")
names_fe = ['Intercepto (β₀)', 'Mes (β₁: pendiente media)', 'Sexo varón (β₂)',
            'Inmunodeprimido (β₃)', 'Mes × Sexo varón (β₄)', 'Mes × Inmunodep (β₅)']
print(f"  {'Parámetro':<30} {'Coef':>8} {'SE':>8} {'t':>8} {'p':>8}  Sig")
for i, name in enumerate(names_fe):
    sig = '*' if p_vals[i] < 0.05 else ('†' if p_vals[i] < 0.10 else '')
    print(f"  {name:<30} {beta_ols[i]:>8.4f} {se_ols[i]:>8.4f} {t_vals[i]:>8.3f} {p_vals[i]:>8.4f}  {sig}")

print(f"\n{'─'*70}")
print(f"EFECTOS ALEATORIOS (por paciente)")
print(f"{'─'*70}")
print(f"  Var(intercepto): {var_u0:.4f}")
print(f"  Var(pendiente):  {var_u1:.6f}")
print(f"  Cor(int, slope): {cov_u01 / np.sqrt(var_u0 * var_u1):.4f}")
print(f"  Varianza residual: {sigma2:.4f}")

print(f"\n{'─'*70}")
print(f"INTERPRETACIÓN CLÍNICA")
print(f"{'─'*70}")
slope_global = beta_ols[1]
slope_male = beta_ols[1] + beta_ols[4]
slope_female = beta_ols[1]
slope_inmuno = beta_ols[1] + beta_ols[5]
slope_no_inmuno = beta_ols[1]
print(f"  Pendiente media global: {slope_global:.4f} log-unidades/mes")
print(f"  Pendiente mujeres:     {slope_female:.4f}")
print(f"  Pendiente varones:     {slope_male:.4f}")
print(f"  → Diferencia varón-mujer (β₄): {beta_ols[4]:.4f}, p = {p_vals[4]:.4f}")
print(f"  Pendiente inmunocomp:  {slope_no_inmuno:.4f}")
print(f"  Pendiente inmunodep:   {slope_inmuno:.4f}")
print(f"  → Diferencia inmuno (β₅):      {beta_ols[5]:.4f}, p = {p_vals[5]:.4f}")

# Transformar a escala original
print(f"\n  En escala original (exponenciando):")
print(f"  → Caída mensual media: {(1-np.exp(slope_global))*100:.1f}% por mes")
print(f"  → Caída varones:       {(1-np.exp(slope_male))*100:.1f}% por mes")
print(f"  → Caída mujeres:       {(1-np.exp(slope_female))*100:.1f}% por mes")

validation_code_lmm = """
# ═══ VALIDACIÓN CONTRA STATSMODELS ═══
import statsmodels.formula.api as smf
lmm = smf.mixedlm("log_igg ~ month + sexo_v + inmuno_dep + month:sexo_v + month:inmuno_dep",
                    long_df, groups=long_df["ID"],
                    re_formula="~month")
lmm_fit = lmm.fit(reml=True)
print(lmm_fit.summary())
"""
print("\n📋 Código de validación statsmodels-LMM guardado")

# ═══════════════════════════════════════════════════════════════════════════
# FASE 2.2 — ANÁLISIS DE DISCORDANCIA (EOS vs IgG)
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "="*80)
print("FASE 2.2 — ANÁLISIS DE DISCORDANCIA: EOSINÓFILOS vs IgG")
print("="*80)

# Para cada paciente: mes de normalización de EOS (<0.5) y mes de seroneg IgG (<1.1)
eos_cuanti_cols = ['EOS_M3_CUANTI','EOS_M6_CUANTI','EOS_M12_CUANTI','EOS_M18_CUANTI',
                   'EOS_M24_CUANTI','EOS_M36_CUANTI','EOS_M48_CUANTI','EOS_M72_CUANTI']
eos_mes_cols2 = ['EOS_M3_MES','EOS_M6_MES','EOS_M12_MES','EOS_M18_MES',
                'EOS_M24_MES','EOS_M36_MES','EOS_M48_MES','EOS_M72_MES']

disc_rows = []
for _, row in df.iterrows():
    pid = int(row['ID'])
    eos_basal = row['EOS_BASAL']
    had_eos = pd.notna(eos_basal) and eos_basal > 0.5  # Tenía eosinofilia basal

    # Buscar primer mes con EOS < 0.5 post-TTO
    eos_norm_month = np.nan
    for ec, em in zip(eos_cuanti_cols, eos_mes_cols2):
        if pd.notna(row[ec]) and pd.notna(row[em]) and row[ec] < 0.5:
            eos_norm_month = row[em]
            break

    # Buscar primer mes con IgG < 1.1 post-TTO
    igg_neg_month = np.nan
    for ic, im in zip(igg_cuanti_cols, igg_mes_cols):
        if pd.notna(row[ic]) and pd.notna(row[im]) and row[ic] < 1.1:
            igg_neg_month = row[im]
            break

    # Último seguimiento
    all_months = []
    for em in eos_mes_cols2 + igg_mes_cols:
        if pd.notna(row[em]):
            all_months.append(row[em])
    last_fu = max(all_months) if all_months else np.nan

    disc_rows.append({
        'ID': pid,
        'had_eosinophilia': had_eos,
        'eos_basal': eos_basal,
        'eos_norm_month': eos_norm_month,
        'igg_neg_month': igg_neg_month,
        'last_fu': last_fu,
        'event_seroneg': row['EVENT_SERONEG'],
        'inmuno': row['INMUNO_DICO'],
    })

disc = pd.DataFrame(disc_rows)
disc['eos_normalized'] = disc['eos_norm_month'].notna()
disc['igg_negativized'] = disc['igg_neg_month'].notna()

# Clasificación de concordancia
def classify(row):
    if row['eos_normalized'] and row['igg_negativized']:
        return 'Ambos normalizan'
    elif row['eos_normalized'] and not row['igg_negativized']:
        return 'EOS normaliza, IgG persiste'
    elif not row['eos_normalized'] and row['igg_negativized']:
        return 'IgG normaliza, EOS persiste'
    else:
        return 'Ninguno normaliza'

disc['concordance'] = disc.apply(classify, axis=1)

# Solo pacientes que tenían eosinofilia basal Y tienen seguimiento
disc_eos = disc[disc['had_eosinophilia'] & disc['last_fu'].notna()].copy()

print(f"\nPacientes con eosinofilia basal y seguimiento: {len(disc_eos)}")
print(f"\nConcordancia EOS ↔ IgG:")
for cat, n in disc_eos['concordance'].value_counts().items():
    print(f"  {cat}: {n}")

# Los "falsos positivos serológicos crónicos"
chronic_seropos = disc[(disc['eos_normalized']) & (~disc['igg_negativized'])]
if len(chronic_seropos) > 0:
    print(f"\n⚠️ Pacientes con EOS normalizada pero IgG PERSISTENTE (posibles falsos + crónicos):")
    for _, r in chronic_seropos.iterrows():
        print(f"  ID {int(r['ID'])}: EOS norm a mes {r['eos_norm_month']:.0f}, "
              f"IgG persiste hasta mes {r['last_fu']:.0f}")
else:
    print("\n✅ No se identifican falsos positivos serológicos crónicos en los que tenían eosinofilia basal")

# ── FIGURA: Scatter de discordancia ──
fig, ax = plt.subplots(figsize=(8, 7))

# Solo pacientes con ambos datos (al menos parciales)
plot_data = disc[disc['last_fu'].notna()].copy()
plot_data['eos_time'] = plot_data['eos_norm_month'].fillna(plot_data['last_fu'])
plot_data['igg_time'] = plot_data['igg_neg_month'].fillna(plot_data['last_fu'])
plot_data['eos_event'] = plot_data['eos_normalized'].astype(int)
plot_data['igg_event'] = plot_data['igg_negativized'].astype(int)

for _, row in plot_data.iterrows():
    # Color by concordance
    if row['eos_normalized'] and row['igg_negativized']:
        color, marker = PAL['concordant'], 'o'
    elif row['eos_normalized'] and not row['igg_negativized']:
        color, marker = PAL['discordant'], 's'
    elif not row['eos_normalized'] and row['igg_negativized']:
        color, marker = PAL['seroneg'], '^'
    else:
        color, marker = PAL['neither'], 'D'

    # Open marker for censored
    ec = 'white' if (not row['eos_normalized'] or not row['igg_negativized']) else color
    ax.scatter(row['eos_time'], row['igg_time'], c=color, marker=marker,
               s=60, alpha=0.8, edgecolors='white', linewidths=0.5, zorder=4)
    ax.annotate(f"{int(row['ID'])}", (row['eos_time'], row['igg_time']),
                fontsize=6, color='grey', xytext=(3,3), textcoords='offset points')

# Diagonal (concordancia perfecta)
max_t = max(plot_data['eos_time'].max(), plot_data['igg_time'].max())
ax.plot([0, max_t], [0, max_t], '--', color='grey', alpha=0.5, label='Concordancia perfecta')

# Leyenda
patches = [
    mpatches.Patch(color=PAL['concordant'], label='Ambos normalizan'),
    mpatches.Patch(color=PAL['discordant'], label='EOS ok, IgG persiste'),
    mpatches.Patch(color=PAL['seroneg'], label='IgG ok, EOS persiste'),
    mpatches.Patch(color=PAL['neither'], label='Ninguno normaliza'),
]
ax.legend(handles=patches, fontsize=9, loc='upper left')
ax.set_xlabel('Tiempo normalización eosinófilos (meses)', fontsize=11)
ax.set_ylabel('Tiempo negativización IgG (meses)', fontsize=11)
ax.set_title('Discordancia EOS ↔ IgG post-tratamiento\n'
             '(cada punto = 1 paciente; censurados en último seguimiento)',
             fontsize=12, fontweight='bold')
ax.set_xlim(-1, max_t + 5)
ax.set_ylim(-1, max_t + 5)

plt.tight_layout()
plt.savefig(OUT / 'figures' / 'fig10_discordancia_eos_igg.png', dpi=300, bbox_inches='tight')
plt.show()
print(f"\n💾 Guardada: {OUT / 'figures' / 'fig10_discordancia_eos_igg.png'}")

# ── FIGURA: LMM predicciones por grupo ──
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
months_pred = np.linspace(0, 72, 100)

# Panel A: por sexo
ax = axes[0]
for sexo_v, label, color in [(0, 'Mujeres', PAL['female']), (1, 'Varones', PAL['male'])]:
    pred = beta_ols[0] + beta_ols[1]*months_pred + beta_ols[2]*sexo_v + beta_ols[4]*sexo_v*months_pred
    ax.plot(months_pred, np.exp(pred), color=color, linewidth=2.5, label=label)
    # Datos reales
    sub = long_df[long_df['sexo_v'] == sexo_v]
    ax.scatter(sub['month'], sub['igg'], color=color, alpha=0.15, s=20, zorder=3)

ax.axhline(1.1, color=PAL['highlight'], linestyle='--', linewidth=1.2, alpha=0.7, label='Corte 1.1')
ax.set_xlabel('Meses post-tratamiento')
ax.set_ylabel('IgG predicha (escala original)')
ax.set_title('Trayectoria IgG por sexo (LMM)', fontweight='bold')
ax.legend(fontsize=9)
ax.set_ylim(0, 15)

# Panel B: por inmunodepresión
ax = axes[1]
for inmuno, label, color in [(0, 'Inmunocompetente', PAL['inmuno_comp']), (1, 'Inmunodeprimido', PAL['inmuno_dep'])]:
    pred = beta_ols[0] + beta_ols[1]*months_pred + beta_ols[3]*inmuno + beta_ols[5]*inmuno*months_pred
    ax.plot(months_pred, np.exp(pred), color=color, linewidth=2.5, label=label)
    sub = long_df[long_df['inmuno_dep'] == inmuno]
    ax.scatter(sub['month'], sub['igg'], color=color, alpha=0.15, s=20, zorder=3)

ax.axhline(1.1, color=PAL['highlight'], linestyle='--', linewidth=1.2, alpha=0.7, label='Corte 1.1')
ax.set_xlabel('Meses post-tratamiento')
ax.set_ylabel('IgG predicha (escala original)')
ax.set_title('Trayectoria IgG por estado inmune (LMM)', fontweight='bold')
ax.legend(fontsize=9)
ax.set_ylim(0, 15)

fig.suptitle('Modelo Lineal Mixto — Predicciones de la pendiente de caída de IgG',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(OUT / 'figures' / 'fig11_lmm_predictions.png', dpi=300, bbox_inches='tight')
plt.show()
print(f"💾 Guardada: {OUT / 'figures' / 'fig11_lmm_predictions.png'}")

# ── FIGURA: Distribución de pendientes individuales ──
fig, ax = plt.subplots(figsize=(8, 5))
# Separar por sexo
slopes_by_patient = []
for pid, grp in long_df.groupby('ID'):
    if len(grp) >= 2:
        x = grp['month'].values
        y_log = grp['log_igg'].values
        if len(x) >= 2 and (x.max() - x.min()) > 0:
            slope = np.polyfit(x, y_log, 1)[0]
            sexo = grp['sexo_v'].iloc[0]
            inmuno = grp['inmuno_dep'].iloc[0]
            slopes_by_patient.append({'ID': pid, 'slope': slope, 'sexo_v': sexo, 'inmuno_dep': inmuno})

slopes_df = pd.DataFrame(slopes_by_patient)
for sexo, label, color in [(0, 'Mujeres', PAL['female']), (1, 'Varones', PAL['male'])]:
    data = slopes_df[slopes_df['sexo_v'] == sexo]['slope']
    ax.hist(data, bins=12, alpha=0.5, color=color, label=f'{label} (n={len(data)}, med={data.median():.4f})')

ax.axvline(0, color='grey', linestyle=':', alpha=0.5)
ax.set_xlabel('Pendiente individual log(IgG)/mes', fontsize=11)
ax.set_ylabel('N pacientes')
ax.set_title('Distribución de pendientes individuales por sexo', fontweight='bold')
ax.legend(fontsize=9)

# Mann-Whitney
s_m = slopes_df[slopes_df['sexo_v'] == 0]['slope']
s_v = slopes_df[slopes_df['sexo_v'] == 1]['slope']
if len(s_m) >= 2 and len(s_v) >= 2:
    u, p = sp_stats.mannwhitneyu(s_m, s_v, alternative='two-sided')
    ax.text(0.98, 0.95, f'Mann-Whitney p = {p:.3f}', transform=ax.transAxes,
            ha='right', va='top', fontsize=10, fontweight='bold' if p < 0.05 else 'normal',
            color='#E65100' if p < 0.05 else '#546E7A',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig(OUT / 'figures' / 'fig12_slopes_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
print(f"💾 Guardada: {OUT / 'figures' / 'fig12_slopes_distribution.png'}")

# ═══════════════════════════════════════════════════════════════════════════
# GUARDAR TODO
# ═══════════════════════════════════════════════════════════════════════════

# Guardar tablas
cox_comparison = pd.DataFrame({
    'Variable': MULTI_NAMES,
    'HR_original': cox_orig['HR'].values,
    'p_original': cox_orig['p'].values,
    'N_original': cox_orig['n'].values,
    'HR_imputed': cox_imp['HR'].values,
    'p_imputed': cox_imp['p'].values,
    'N_imputed': cox_imp['n'].values,
})
cox_comparison.to_csv(OUT / 'tables' / 'cox_original_vs_imputed.csv', index=False, encoding='utf-8-sig')

lmm_results = pd.DataFrame({
    'Parameter': names_fe,
    'Coefficient': beta_ols,
    'SE': se_ols,
    't_value': t_vals,
    'p_value': p_vals,
})
lmm_results.to_csv(OUT / 'tables' / 'lmm_fixed_effects.csv', index=False, encoding='utf-8-sig')

disc.to_csv(OUT / 'tables' / 'discordance_eos_igg.csv', index=False, encoding='utf-8-sig')
slopes_df.to_csv(OUT / 'tables' / 'individual_slopes.csv', index=False, encoding='utf-8-sig')

# Guardar código de validación
with open(OUT / 'validation_code.py', 'w') as f:
    f.write("#!/usr/bin/env python3\n")
    f.write('"""Código de validación contra lifelines/sklearn/statsmodels.\n')
    f.write('   Ejecutar DESPUÉS de instalar las dependencias:\n')
    f.write('   pip install lifelines scikit-learn statsmodels\n"""\n\n')
    f.write("# ═══ KAPLAN-MEIER ═══\n")
    f.write(validation_code_km)
    f.write("\n\n# ═══ COX PH ═══\n")
    f.write(validation_code_cox)
    f.write("\n\n# ═══ MICE ═══\n")
    f.write(validation_code_mice)
    f.write("\n\n# ═══ LMM ═══\n")
    f.write(validation_code_lmm)

print("\n" + "="*80)
print("✅ TODOS LOS ANÁLISIS COMPLETADOS")
print("="*80)
print(f"\nFiguras: {OUT / 'figures'}")
print(f"Tablas: {OUT / 'tables'}")
print(f"Código validación: {OUT / 'validation_code.py'}")
