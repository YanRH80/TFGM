# ============================================================
# code/tab_b5_recidiva.py
# ------------------------------------------------------------
# Clasificación de pacientes por desenlace a largo plazo.
#
# Definición combinada (estricta OR flexible):
#   Recidiva = se detecta por CUALQUIERA de dos criterios:
#     Estricto: IgG ≥ 50 % del título basal tras negativ.
#       confirmada (2 IgG < 1,1 consec. ≥ 21 d) + ≥ 21 d.
#     Flexible: cualquier IgG ≥ 1,1 tras ≥ 21 d de 1 IgG < 1,1.
#   Recidiva parasitológica:
#       Coprocultivo/concentrado/PCR (+) tras ≥ 3 semanas de
#       negativ. parasitológica confirmada (2 negativos consec.).
#   Neg. sostenida: negativ. (1 o 2 mediciones) sin reconversión
#       durante ≥ 6 meses de seguimiento.
#   Persistencia: IgG ≥ 1,1 mantenida ≥ 3 semanas post-T₀.
#   No clasificable: seguimiento insuficiente.
#
# Inyecta pac_class (Series), pac_class_df (DataFrame) y
# recidiva_detail (dict: ID → tipo de recidiva) en namespace.
#
# Lee:    pac, ser_post, mic_post, SERO_NEG, CONFIG, cens_ser,
#         EXCL_SERO_IDS, MICRO_MIN (namespace)
# Output: stdout LaTeX table + figures/tab-b5-recidiva.md
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

RECIDIVA_GAP = CONFIG['RECIDIVA_GAP']       # 21 días
MIN_FU_SOSTENIDA = 180                       # 6 meses post-1ª neg


# ============================================================
# Clasificación serológica
# ============================================================
def _classify_sero(pid, sp, igg_basal):
    """Clasifica desenlace serológico.

    Recidiva serológica = IgG ≥ 50 % del título basal tras
    negativización confirmada + ≥ 3 semanas.

    Returns (cat, día_primera_neg, día_rebote).
    """
    meds = sp[sp['ID'] == pid].sort_values('dias')
    if len(meds) == 0:
        return 'No clasificable', np.nan, np.nan

    igg = meds['IGG'].values
    dias = meds['dias'].values

    neg_mask = igg < SERO_NEG
    if not neg_mask.any():
        if dias[-1] >= RECIDIVA_GAP:
            return 'Persistencia', np.nan, np.nan
        return 'No clasificable', np.nan, np.nan

    first_neg_idx = int(np.argmax(neg_mask))
    first_neg_dia = dias[first_neg_idx]

    # Negativ. confirmada: 2 consecutivas < 1,1, ≥ 21 d
    confirm_dia = np.nan
    for i in range(first_neg_idx, len(igg) - 1):
        if igg[i] < SERO_NEG and igg[i + 1] < SERO_NEG:
            if dias[i + 1] - dias[i] >= RECIDIVA_GAP:
                confirm_dia = dias[i + 1]
                break

    if np.isnan(confirm_dia):
        return 'No clasificable', first_neg_dia, np.nan

    # Umbral de recidiva: ≥ 50 % del título basal (si disponible)
    reb_thresh = 0.50 * igg_basal if pd.notna(igg_basal) else SERO_NEG

    for v, d in zip(igg, dias):
        if d > confirm_dia and v >= reb_thresh:
            return 'Recidiva sero.', first_neg_dia, d

    if dias[-1] - first_neg_dia >= MIN_FU_SOSTENIDA:
        return 'Neg. sostenida', first_neg_dia, np.nan

    return 'No clasificable', first_neg_dia, np.nan


# ============================================================
# Clasificación serológica FLEXIBLE (sensibilidad)
# ============================================================
def _classify_sero_flexible(pid, sp, igg_basal):
    """Clasificación flexible: negativización = 1 sola IgG < 1,1.

    Recidiva = cualquier IgG ≥ 1,1 al menos RECIDIVA_GAP días
    después de esa primera medición negativa.

    Returns (cat, día_primera_neg, día_rebote).
    """
    meds = sp[sp['ID'] == pid].sort_values('dias')
    if len(meds) == 0:
        return 'No clasificable', np.nan, np.nan

    igg = meds['IGG'].values
    dias = meds['dias'].values

    neg_mask = igg < SERO_NEG
    if not neg_mask.any():
        if dias[-1] >= RECIDIVA_GAP:
            return 'Persistencia', np.nan, np.nan
        return 'No clasificable', np.nan, np.nan

    first_neg_idx = int(np.argmax(neg_mask))
    first_neg_dia = dias[first_neg_idx]

    # Recidiva: cualquier IgG ≥ 1,1 al menos 21 d tras primera neg
    for v, d in zip(igg, dias):
        if d >= first_neg_dia + RECIDIVA_GAP and v >= SERO_NEG:
            return 'Recidiva sero.', first_neg_dia, d

    if dias[-1] - first_neg_dia >= MIN_FU_SOSTENIDA:
        return 'Neg. sostenida', first_neg_dia, np.nan

    return 'No clasificable', first_neg_dia, np.nan


# ============================================================
# Clasificación parasitológica (recidiva)
# ============================================================
def _classify_para(pid, mp):
    """Detecta recidiva parasitológica.

    Recidiva = resultado (+) tras ≥ 3 semanas de 2 negativos
    consecutivos separados ≥ MICRO_MIN días.

    Returns (bool_recidiva, día_rebote).
    """
    meds = mp[mp['ID'] == pid].sort_values('dias')
    if len(meds) < 3:
        return False, np.nan

    res = meds['RESULTADO'].values
    d   = meds['dias'].values

    # Buscar negativ. confirmada parasitológica
    confirm_dia = np.nan
    for i in range(len(res) - 1):
        if res[i] == 0 and res[i + 1] == 0:
            if d[i + 1] - d[i] >= MICRO_MIN:
                confirm_dia = d[i + 1]
                break

    if np.isnan(confirm_dia):
        return False, np.nan

    # Positivo ≥ 3 semanas tras confirmación
    for r, dd in zip(res, d):
        if dd >= confirm_dia + RECIDIVA_GAP and r == 1:
            return True, dd

    return False, np.nan


# ============================================================
# Aplicar clasificación combinada (estricta OR flexible)
# ============================================================
rows = []
recidiva_detail = {}

for _, p in pac.iterrows():
    pid = p['ID']

    if pid in EXCL_SERO_IDS:
        rows.append({'ID': pid, 'categoria': 'No aplicable',
                     't_primera_neg': np.nan, 't_rebote': np.nan})
        continue

    # Ejecutar ambas clasificaciones serológicas
    s_cat, s_neg, s_reb = _classify_sero(pid, ser_post, p['IGG_BASAL'])
    f_cat, f_neg, f_reb = _classify_sero_flexible(pid, ser_post, p['IGG_BASAL'])
    para_rec, t_reb_para = _classify_para(pid, mic_post)

    # Recidiva si CUALQUIER criterio la detecta
    is_rec_strict = s_cat == 'Recidiva sero.'
    is_rec_flex   = f_cat == 'Recidiva sero.'

    if is_rec_strict or is_rec_flex or para_rec:
        cat = 'Recidiva'
        # Tiempo de rebote: el más temprano disponible
        rebs = [x for x in [s_reb, f_reb, t_reb_para] if pd.notna(x)]
        t_reb = min(rebs) if rebs else np.nan
        t_neg = s_neg if pd.notna(s_neg) else f_neg
        # Detalle del tipo
        tipos = []
        if is_rec_strict: tipos.append('sero-e')
        if is_rec_flex and not is_rec_strict: tipos.append('sero-f')
        if para_rec: tipos.append('para')
        recidiva_detail[pid] = '+'.join(tipos)
    else:
        # Neg. sostenida si CUALQUIER definición la otorga
        if s_cat == 'Neg. sostenida' or f_cat == 'Neg. sostenida':
            cat = 'Neg. sostenida'
        elif s_cat == 'Persistencia' or f_cat == 'Persistencia':
            cat = 'Persistencia'
        else:
            cat = 'No clasificable'
        t_neg = s_neg if pd.notna(s_neg) else f_neg
        t_reb = np.nan

    rows.append({'ID': pid, 'categoria': cat,
                 't_primera_neg': t_neg, 't_rebote': t_reb})

pac_class_df = pd.DataFrame(rows)
pac_class = pac_class_df.set_index('ID')['categoria']

# Datos auxiliares para la tabla
_pc = pac.merge(pac_class_df, on='ID')
_pc['fu_meses'] = cens_ser.reindex(_pc['ID']).values / 30.44


# ============================================================
# Tabla LaTeX
# ============================================================
CATS = ['Neg. sostenida', 'Recidiva', 'Persistencia', 'No clasificable']
_eval = _pc[_pc['categoria'].isin(CATS)]
n_eval = len(_eval)
n_excl = (_pc['categoria'] == 'No aplicable').sum()

# Desglose de tipo de recidiva
n_rec_sero_e = sum(1 for v in recidiva_detail.values() if 'sero-e' in v)
n_rec_sero_f = sum(1 for v in recidiva_detail.values() if 'sero-f' in v)
n_rec_para = sum(1 for v in recidiva_detail.values() if 'para' in v)

print(r"""\begin{table}[H]
\centering
\caption{Clasificación por desenlace serológico a largo plazo """
      + f"(n evaluable = {n_eval}; {n_excl} excl.\\ seroneg.\\ basal)."
      + r"""}
\label{tab-b5-recidiva}
\small
\begin{tabular}{l c c c c}
\toprule
\textbf{Categoría} & \textbf{n (\%)} & \textbf{Seg.\ (meses)} & \textbf{IgG basal} & \textbf{T neg.\ (meses)} \\
 & & \textit{med (IQR)} & \textit{med (IQR)} & \textit{med (IQR)} \\
\midrule""")

for cat in CATS:
    sub = _eval[_eval['categoria'] == cat]
    n = len(sub)
    if n == 0:
        continue
    pct = f"{n} ({n / n_eval * 100:.1f}\\%)"
    fu  = med_iqr(sub['fu_meses']) if n > 1 else f"{sub['fu_meses'].iloc[0]:.1f}"
    igg = (med_iqr(sub['IGG_BASAL'].dropna())
           if sub['IGG_BASAL'].notna().sum() > 1 else '---')
    tn  = sub['t_primera_neg'].dropna() / 30.44
    tn_s = med_iqr(tn) if len(tn) > 1 else (f"{tn.iloc[0]:.1f}" if len(tn) == 1 else '---')
    # Anotar tipo de recidiva
    extra = ''
    if cat == 'Recidiva':
        parts = []
        if n_rec_sero_e: parts.append(f'{n_rec_sero_e} sero.\\ estricta')
        if n_rec_sero_f: parts.append(f'{n_rec_sero_f} sero.\\ flexible')
        if n_rec_para: parts.append(f'{n_rec_para} para.')
        extra = f' \\footnotesize{{({", ".join(parts)})}}'
    print(f"{cat}{extra} & {pct} & {fu} & {igg} & {tn_s} \\\\")

print(r"""\bottomrule
\multicolumn{5}{l}{\footnotesize Seg.\ = seguimiento post-T$_0$.\ %
T neg.\ = tiempo a primera IgG $<$ 1,1.} \\
\multicolumn{5}{l}{\footnotesize Recidiva sero.\ estricta: IgG $\geq$ %
50\,\% del título basal tras negativ.\ confirmada (2 IgG $<$ 1,1 %
consec.\ $\geq$ 21\,d).} \\
\multicolumn{5}{l}{\footnotesize Recidiva sero.\ flexible: cualquier %
IgG $\geq$ 1,1 tras $\geq$ 21\,d de 1 medición negativa.} \\
\multicolumn{5}{l}{\footnotesize Recidiva para.: coprocultivo/PCR (+) %
tras negativ.\ parasitológica confirmada $\geq$ 21\,d.} \\
\end{tabular}
\end{table}""")


# ============================================================
# Markdown export
# ============================================================
def _mc(s):
    return s.replace('\\%', '%').replace('--', '–')

with open('figures/tab-b5-recidiva.md', 'w', encoding='utf-8') as _f:
    _f.write(f"**Tabla. Clasificación por desenlace "
             f"(n evaluable = {n_eval}).**\n\n")
    _f.write("| Categoría | n (%) | Seg. (meses) | IgG basal | T neg. (meses) |\n")
    _f.write("|---|---|---|---|---|\n")
    for cat in CATS:
        sub = _eval[_eval['categoria'] == cat]
        n = len(sub)
        if n == 0:
            continue
        pct = f"{n} ({n / n_eval * 100:.1f}%)"
        fu  = _mc(med_iqr(sub['fu_meses'])) if n > 1 else f"{sub['fu_meses'].iloc[0]:.1f}"
        igg = _mc(med_iqr(sub['IGG_BASAL'].dropna())) if sub['IGG_BASAL'].notna().sum() > 1 else '—'
        tn  = sub['t_primera_neg'].dropna() / 30.44
        tn_s = _mc(med_iqr(tn)) if len(tn) > 1 else (f"{tn.iloc[0]:.1f}" if len(tn) == 1 else '—')
        _f.write(f"| {cat} | {pct} | {fu} | {igg} | {tn_s} |\n")
    _f.write(f"\n_Recidiva sero. estricta: IgG ≥ 50 % del título basal "
             f"tras negativ. confirmada (2 IgG < 1,1 consec. ≥ 21 d). "
             f"Recidiva sero. flexible: cualquier IgG ≥ 1,1 tras ≥ 21 d "
             f"de 1 medición negativa. Recidiva para.: positivo "
             f"tras negativ. parasitológica confirmada ≥ 21 d._\n")
