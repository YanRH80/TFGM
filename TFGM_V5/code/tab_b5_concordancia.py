# ============================================================
# code/tab_b5_concordancia.py
# ------------------------------------------------------------
# Tabla de concordancia serología–eosinófilos (y parasitología
# si n evaluable ≥ 10) al hito de 12 meses post-T₀.
#
# Para cada paciente, se toma la medición más cercana a 12 meses
# dentro de una ventana de ±3 meses (9–15 m ≡ 274–457 d).
# Cohen's κ (IC 95 %) + McNemar exacto.
#
# Lee:    pac, ser_post, eos_post, mic_post, SERO_NEG, EOS_NEG,
#         EXCL_SERO_IDS, C (namespace)
# Output: stdout LaTeX table + figures/tab-b5-concordancia.md
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

HITO = 365              # 12 meses en días
VENTANA = 91            # ±3 meses
LO, HI = HITO - VENTANA, HITO + VENTANA


# ============================================================
# Encontrar la medición más cercana al hito por paciente
# ============================================================
def _closest(df, id_col, dias_col, val_col, lo, hi):
    sub = df[(df[dias_col] >= lo) & (df[dias_col] <= hi)].copy()
    sub['_dist'] = (sub[dias_col] - HITO).abs()
    idx = sub.groupby(id_col)['_dist'].idxmin()
    return sub.loc[idx, [id_col, val_col, dias_col]].set_index(id_col)


ser12 = _closest(ser_post, 'ID', 'dias', 'IGG', LO, HI)
ser12['sero_neg'] = (ser12['IGG'] < SERO_NEG).astype(int)

eos12 = _closest(eos_post, 'ID', 'dias', 'EOS', LO, HI)
eos12['eos_neg'] = (eos12['EOS'] < EOS_NEG).astype(int)

mic12 = _closest(mic_post, 'ID', 'dias', 'RESULTADO', LO, HI)
mic12['para_neg'] = (mic12['RESULTADO'] == 0).astype(int)


# ============================================================
# Cohen's κ + McNemar
# ============================================================
def _kappa_mcnemar(a, b, label_a, label_b):
    """Calcula κ, IC 95 % y McNemar exacto para dos vectores binarios."""
    from sklearn.metrics import cohen_kappa_score
    from scipy.stats import binomtest

    n = len(a)
    # Tabla 2×2
    tp = ((a == 1) & (b == 1)).sum()
    tn = ((a == 0) & (b == 0)).sum()
    fp = ((a == 0) & (b == 1)).sum()
    fn = ((a == 1) & (b == 0)).sum()

    kappa = cohen_kappa_score(a, b)
    # IC 95 % bootstrap (simple percentile, 2000 reps)
    np.random.seed(CONFIG['SEED'])
    k_boot = []
    for _ in range(2000):
        idx = np.random.choice(n, n, replace=True)
        if len(np.unique(a[idx])) < 2 or len(np.unique(b[idx])) < 2:
            continue
        k_boot.append(cohen_kappa_score(a[idx], b[idx]))
    k_boot = np.array(k_boot)
    ci_lo = np.percentile(k_boot, 2.5) if len(k_boot) > 100 else np.nan
    ci_hi = np.percentile(k_boot, 97.5) if len(k_boot) > 100 else np.nan

    # McNemar exacto: bajo H0, la discordancia b-c sigue Binom(b+c, 0.5)
    disc = fp + fn
    p_mcn = binomtest(min(fp, fn), disc, 0.5).pvalue if disc > 0 else 1.0

    return {
        'n': n, 'label_a': label_a, 'label_b': label_b,
        'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn,
        'kappa': kappa, 'ci_lo': ci_lo, 'ci_hi': ci_hi,
        'p_mcnemar': p_mcn,
        'concordancia': (tp + tn) / n,
    }


# ============================================================
# Pares a evaluar
# ============================================================
results = []

# Sero ↔ Eos
common_se = ser12.index.intersection(eos12.index)
if len(common_se) >= 5:
    a = ser12.loc[common_se, 'sero_neg'].values
    b = eos12.loc[common_se, 'eos_neg'].values
    results.append(_kappa_mcnemar(a, b, 'Seroneg.', 'Eos. norm.'))

# Sero ↔ Para
common_sp = ser12.index.intersection(mic12.index)
if len(common_sp) >= 10:
    a = ser12.loc[common_sp, 'sero_neg'].values
    b = mic12.loc[common_sp, 'para_neg'].values
    results.append(_kappa_mcnemar(a, b, 'Seroneg.', 'Para. neg.'))


# ============================================================
# LaTeX output
# ============================================================
if len(results) == 0:
    print(r"% tab_b5_concordancia: n evaluable insuficiente, tabla omitida")
else:
    print(r"""\begin{table}[H]
\centering
\caption{Concordancia entre biomarcadores al hito de 12 meses ($\pm$ 3 m).}
\label{tab-b5-concordancia}
\small
\begin{tabular}{l c c c c}
\toprule
\textbf{Par} & \textbf{n eval.} & \textbf{Concordancia} & \textbf{$\kappa$ (IC 95\%)} & \textbf{McNemar p} \\
\midrule""")
    for r in results:
        k_str = f"{r['kappa']:.2f} ({r['ci_lo']:.2f}--{r['ci_hi']:.2f})"
        p_str = f"{r['p_mcnemar']:.3f}"
        conc  = f"{r['concordancia'] * 100:.1f}\\%"
        pair  = f"{r['label_a']} vs.\\ {r['label_b']}"
        print(f"{pair} & {r['n']} & {conc} & {k_str} & {p_str} \\\\")

    # Tabla 2×2 detallada del primer par (sero ↔ eos) como nota al pie
    r0 = results[0]
    print(r"""\bottomrule
\multicolumn{5}{l}{\footnotesize """ +
          f"Tabla 2$\\times$2 ({r0['label_a']} vs.\\ {r0['label_b']}): "
          f"ambos neg.\\ = {r0['tn']}, "
          f"ambos pos.\\ = {r0['tp']}, "
          f"solo {r0['label_a']} = {r0['fn']}, "
          f"solo {r0['label_b']} = {r0['fp']}."
          + r"""} \\
\end{tabular}
\end{table}""")


# ============================================================
# Markdown export
# ============================================================
with open('figures/tab-b5-concordancia.md', 'w', encoding='utf-8') as _f:
    _f.write("**Tabla. Concordancia entre biomarcadores a 12 meses (± 3 m).**\n\n")
    if len(results) == 0:
        _f.write("_n evaluable insuficiente para concordancia a 12 meses._\n")
    else:
        _f.write("| Par | n eval. | Concordancia | κ (IC 95 %) | McNemar p |\n")
        _f.write("|---|---|---|---|---|\n")
        for r in results:
            k_str = f"{r['kappa']:.2f} ({r['ci_lo']:.2f}–{r['ci_hi']:.2f})"
            conc  = f"{r['concordancia'] * 100:.1f}%"
            pair  = f"{r['label_a']} vs. {r['label_b']}"
            _f.write(f"| {pair} | {r['n']} | {conc} | {k_str} | {r['p_mcnemar']:.3f} |\n")
        _f.write(f"\n_Ventana: 274–457 días post-T₀._\n")
