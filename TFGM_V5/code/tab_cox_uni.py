# ============================================================
# code/tab_cox_uni.py
# ------------------------------------------------------------
# Tabla 2: Cox univariable — SOLO las variables NO significativas
# (p crudo ≥ 0,05). Las significativas se presentan en la
# Figura 5 (code/fig_b3_predictors.py), así que esta tabla es
# complementaria y no duplica información.
#
# Lee:    cox_uni, nice (del namespace)
# Output: stdout LaTeX longtable + figures/tab-cox-uni.md
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

if 'cox_uni' not in dir():
    exec(open('code/cox_compute.py').read())

cox_nosig = cox_uni[cox_uni['p'] >= 0.05].copy().sort_values('p')

# ------------------------------------------------------------
# LaTeX longtable
# ------------------------------------------------------------
print(r"""\begin{longtable}{l c r@{\hspace{0.5em}}l c c}
\caption{Cox univariable: covariables NO significativas (p $\geq$ 0,05)
con corrección BH--FDR. Las covariables con p $<$ 0,05 se representan
en la Figura~\ref{fig-b3-predictors}.}
\label{tab-cox-uni} \\
\toprule
\textbf{Variable} & \textbf{n} & \multicolumn{2}{c}{\textbf{HR (IC 95\%)}} & \textbf{p crudo} & \textbf{p\textsubscript{adj}} \\
\midrule
\endfirsthead
\toprule
\textbf{Variable} & \textbf{n} & \multicolumn{2}{c}{\textbf{HR (IC 95\%)}} & \textbf{p crudo} & \textbf{p\textsubscript{adj}} \\
\midrule
\endhead
\bottomrule
\endfoot""")

for _, r in cox_nosig.iterrows():
    nm     = nice.get(r['Variable'], r['Variable'])
    hr_str = f"{r['HR']:.2f} ({r['CI_lo']:.2f}--{r['CI_hi']:.2f})"
    p_str  = f"{r['p']:.3f}"
    padj_s = f"{r['p_adj']:.3f}"
    print(f"{nm} & {int(r['n'])} & {hr_str} & & {p_str} & {padj_s} \\\\")

print(r"""\bottomrule
\end{longtable}""")

# ------------------------------------------------------------
# Markdown export
# ------------------------------------------------------------
with open('figures/tab-cox-uni.md', 'w', encoding='utf-8') as _f:
    _f.write("**Tabla 2. Cox univariable: covariables NO significativas "
             "(p ≥ 0,05).**\n\n")
    _f.write("| Variable | n | HR (IC 95%) | p crudo | p_adj |\n|---|---|---|---|---|\n")
    for _, r in cox_nosig.iterrows():
        nm     = nice.get(r['Variable'], r['Variable'])
        hr_str = f"{r['HR']:.2f} ({r['CI_lo']:.2f}–{r['CI_hi']:.2f})"
        p_str  = f"{r['p']:.3f}"
        padj_s = f"{r['p_adj']:.3f}"
        _f.write(f"| {nm} | {int(r['n'])} | {hr_str} | {p_str} | {padj_s} |\n")
    _f.write("\n_Las covariables con p < 0,05 (significativas) se muestran "
             "en la Figura 5 (forest plot + KM estratificado)._\n")
