#!/usr/bin/env python3
"""Código de validación contra lifelines/sklearn/statsmodels.
   Ejecutar DESPUÉS de instalar las dependencias:
   pip install lifelines scikit-learn statsmodels
"""

# ═══ KAPLAN-MEIER ═══

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


# ═══ COX PH ═══

# ═══ VALIDACIÓN CONTRA LIFELINES COX ═══
from lifelines import CoxPHFitter
cph = CoxPHFitter()
cox_df = sub[['TIME_TO_SERONEG_M','EVENT_SERONEG','IGG_BASAL']].copy()
cph.fit(cox_df, 'TIME_TO_SERONEG_M', 'EVENT_SERONEG')
print(cph.summary[['coef','se(coef)','exp(coef)','p']])
print(f"\nlifelines coef: {cph.summary['coef'].values[0]:.6f}")
print(f"scratch   coef: {cox_igg['coef'].values[0]:.6f}")
print(f"Δ coef: {abs(cph.summary['coef'].values[0] - cox_igg['coef'].values[0]):.2e}")


# ═══ MICE ═══

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


# ═══ LMM ═══

# ═══ VALIDACIÓN CONTRA STATSMODELS ═══
import statsmodels.formula.api as smf
lmm = smf.mixedlm("log_igg ~ month + sexo_v + inmuno_dep + month:sexo_v + month:inmuno_dep",
                    long_df, groups=long_df["ID"],
                    re_formula="~month")
lmm_fit = lmm.fit(reml=True)
print(lmm_fit.summary())
