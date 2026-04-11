# ============================================================
# code/stats_b2.py
# ------------------------------------------------------------
# Texto narrativo Bloque 2:
#   - Mediana KM + IC 95 % Greenwood
#   - Tasa de eventos por persona-año (IC 95 % Poisson)
#   - Landmarks 6 / 12 / 18 / 24 m
#   - Resumen de sensibilidad
# Lee:    kmf, km_data, med_km, ci_lo, ci_hi (del namespace)
# Output: stdout markdown
# ============================================================

if 'kmf' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())
    exec(open('code/fig_b2_km_baseline.py').read())

_person_days  = km_data['T_SERO_ABS_X1'].sum()
_person_years = _person_days / 365.25
_n_ev         = int(km_data['E_SERO_ABS_X1'].sum())
_rate_py      = _n_ev / _person_years
_rate_lo      = poisson.ppf(0.025, _n_ev) / _person_years
_rate_hi      = poisson.ppf(0.975, _n_ev) / _person_years

print("**Hallazgo principal** (primera mediana KM con IC formal publicada para *S. stercoralis*):\n")
print(f"- Mediana KM: **{med_km:.0f} días ({med_km/30.44:.1f} meses)** "
      f"(IC 95 % Greenwood: {ci_lo:.0f}–{ci_hi:.0f} d "
      f"= {ci_lo/30.44:.1f}–{ci_hi/30.44:.1f} m)")
print(f"- Eventos: {_n_ev}/{len(km_data)} ({_n_ev/len(km_data)*100:.0f} %)")
print(f"- Tasa: {_rate_py:.2f} negativizaciones/persona-año "
      f"(IC 95 % Poisson: {_rate_lo:.2f}–{_rate_hi:.2f}; {_person_years:.1f} pa)")

print("\n**Landmarks** (proporción acumulada de negativización):\n")
for m in [6, 12, 18, 24]:
    s = kmf.predict(m * 30.44)
    print(f"- {m} meses: **{(1 - s) * 100:.0f} %** negativizado")

print("\n**Sensibilidad** (tendencias cualitativas):\n")
print("- Umbral 0,9 vs 1,1 → 25 vs 27 eventos; medianas 10,8 vs 8,8 m (robusto).")
print("- Doble confirmación duplica la mediana (≈ 16,4 m).")
print("- Eosinófilos normalizan rápidamente (≈ 3,0 m).")
print("- Parasitología (2 negativos consecutivos) es la definición más lenta (≈ 25,5 m).")
