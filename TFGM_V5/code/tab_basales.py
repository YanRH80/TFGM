# ============================================================
# code/tab_basales.py
# ------------------------------------------------------------
# Tabla 1: Características basales de la cohorte (n = 44).
# Diseño editorial: filas consolidadas para orientar al lector
#   - Procedencia: Latinoamérica / África Subsah. / Europa u otros
#   - Modo dx: con vs sin confirmación parasitológica
#   - Régimen: dosis única vs múltiple (1 vs >1 dosis)
# Lee:    pac, ser_post, cens_ser, EOS_NEG (del namespace)
# Output: stdout LaTeX longtable + figures/tab-basales.md
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

n_total   = len(pac)
n_eos     = pac['EOS_BASAL'].notna().sum()
n_igg     = pac['IGG_BASAL'].notna().sum()
n_serpost = ser_post['ID'].nunique()
n_fem     = (pac['SEXO'] == 'M').sum()

# Procedencia consolidada: desagregamos Sudamérica y Centroamérica
# (más preciso que el agregado "Latinoamérica", que mezclaba dos
# regiones con epidemiología y movimientos migratorios distintos).
n_sudamer  = (pac['REGION'] == 'Am. Sur').sum()
n_centroam = (pac['REGION'] == 'Am. Central').sum()
n_afr      = (pac['REGION'] == 'Áfr. Subsah.').sum()
n_otros    = n_total - n_sudamer - n_centroam - n_afr

# Modo diagnóstico consolidado (con vs sin parasitología)
n_parasit    = len((sero_pos & mic_pos_ids) | (mic_pos_ids - sero_pos))  # cualquier mic+
n_no_parasit = n_total - n_parasit

# Régimen consolidado (única vs múltiple)
n_mono  = (pac['DOSIS_IVM'] == 'MONO').sum()
n_multi = n_total - n_mono

table_data = [
    ("Demográficas",                                              "",             "",                                                   "",                                          True,  False),
    ("Edad al diagnóstico, años (mediana, IQR)",                  str(n_total),   med_iqr(pac['EDAD']),                                 rng(pac['EDAD']),                            False, False),
    ("Sexo femenino, n (\\%)",                                    str(n_total),   n_pct(n_fem, n_total),                                "---",                                       False, False),
    ("",                                                          "",             "",                                                   "",                                          False, True),
    ("Procedencia geográfica",                                    "",             "",                                                   "",                                          True,  False),
    ("Sudamérica, n (\\%)",                                       str(n_total),   n_pct(n_sudamer, n_total),                            "---",                                       False, False),
    ("Centroamérica, n (\\%)",                                    str(n_total),   n_pct(n_centroam, n_total),                           "---",                                       False, False),
    ("África Subsahariana, n (\\%)",                              str(n_total),   n_pct(n_afr, n_total),                                "---",                                       False, False),
    ("Europa u otros, n (\\%)",                                   str(n_total),   n_pct(n_otros, n_total),                              "---",                                       False, False),
    ("",                                                          "",             "",                                                   "",                                          False, True),
    ("Modo diagnóstico",                                          "",             "",                                                   "",                                          True,  False),
    ("Con confirmación parasitológica, n (\\%)",                  str(n_total),   n_pct(n_parasit, n_total),                            "---",                                       False, False),
    ("Sin confirmación parasitológica, n (\\%)",                  str(n_total),   n_pct(n_no_parasit, n_total),                         "---",                                       False, False),
    ("",                                                          "",             "",                                                   "",                                          False, True),
    ("Analítica basal",                                           "",             "",                                                   "",                                          True,  False),
    ("IgG-ELISA basal, índice (mediana, IQR)",                    str(n_igg),     med_iqr(pac['IGG_BASAL'].dropna()),                   rng(pac['IGG_BASAL'].dropna()),              False, False),
    ("Eosinófilos basales, $\\times 10^3$/\\textmu L (mediana, IQR)", str(n_eos), med_iqr(pac['EOS_BASAL'].dropna()),                   rng(pac['EOS_BASAL'].dropna()),              False, False),
    ("Eosinofilia al diagnóstico ($\\geq$500 cel/\\textmu L), n (\\%)", str(n_eos), n_pct(int((pac['EOS_BASAL']>=EOS_NEG).sum()), n_eos), "---",                                     False, False),
    ("",                                                          "",             "",                                                   "",                                          False, True),
    ("Régimen de ivermectina",                                    "",             "",                                                   "",                                          True,  False),
    ("Dosis única, n (\\%)",                                      str(n_total),   n_pct(n_mono, n_total),                               "---",                                       False, False),
    ("Dosis múltiple ($>$1 dosis), n (\\%)",                      str(n_total),   n_pct(n_multi, n_total),                              "---",                                       False, False),
    ("",                                                          "",             "",                                                   "",                                          False, True),
    ("Comorbilidad basal y seguimiento",                          "",             "",                                                   "",                                          True,  False),
    ("Inmunodepresión basal, n (\\%)",                            str(n_total),   n_pct(pac['INMUNO_SI'].sum(), n_total),               "---",                                       False, False),
    ("Comorbilidad basal significativa, n (\\%)",                 str(n_total),   n_pct(pac['COMORB_SI'].sum(), n_total),               "---",                                       False, False),
    ("Seguimiento serológico, meses (mediana, IQR)",              str(n_serpost), med_iqr(cens_ser/30.44),                              rng(cens_ser/30.44),                         False, False),
]

print(r"""\begin{table}[H]
\centering
\caption{Características basales de la cohorte (n = 44).}
\label{tab-basales}
\small
\begin{tabular}{l c c c}
\toprule
\textbf{Variable} & \textbf{n} & \textbf{Valor} & \textbf{Rango} \\
\midrule""")
for var, nv, val, rang, is_hdr, is_sep in table_data:
    if is_sep:
        print(r"\midrule")
    elif is_hdr:
        print(f"\\multicolumn{{4}}{{l}}{{\\textit{{{var}}}}} \\\\")
    else:
        print(f"\\quad {var} & {nv} & {val} & {rang} \\\\")
print(r"""\bottomrule
\multicolumn{4}{l}{\footnotesize Variables continuas: mediana (IQR P25--P75). Rango = mínimo--máximo.} \\
\end{tabular}
\end{table}""")

# ------------------------------------------------------------
# Markdown export (para Google Docs / otras plataformas)
# ------------------------------------------------------------
def _md_clean(s):
    return (s.replace('\\%', '%').replace('\\textmu ', 'μ').replace('\\textmu', 'μ')
             .replace('\\geq', '≥').replace('$\\times 10^3$', '×10³')
             .replace('---', '—').replace('--', '–').replace('$', ''))

with open('figures/tab-basales.md', 'w', encoding='utf-8') as _f:
    _f.write("**Tabla 1. Características basales de la cohorte (n = 44).**\n\n")
    _f.write("| Variable | n | Valor | Rango |\n|---|---|---|---|\n")
    for var, nv, val, rang, is_hdr, is_sep in table_data:
        if is_sep or (not var and not nv):
            continue
        if is_hdr:
            _f.write(f"| **_{var}_** | | | |\n")
        else:
            _f.write(f"| {_md_clean(var)} | {nv} | {_md_clean(val)} | {_md_clean(rang)} |\n")
    _f.write("\n_Variables continuas: mediana (IQR P25–P75). Rango = mínimo–máximo._\n")
