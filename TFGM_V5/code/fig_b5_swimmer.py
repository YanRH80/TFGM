# ============================================================
# code/fig_b5_swimmer.py
# ------------------------------------------------------------
# Diagrama de nadador: solo pacientes clasificables (neg.
# sostenida, recidiva, persistencia). Excluye «no clasificable»
# y «no aplicable» para maximizar la densidad informativa.
#
# Elementos visuales:
#   ● IgG-ELISA (azul < 1,1 / rojo ≥ 1,1)
#   ★ Medición confirmadora de recidiva (estrella grande roja)
#   ◆ Dosis de ivermectina (rombo negro grande + etiqueta)
#   ■ Parasitología (verde neg / rojo pos)
#   Franjas semestrales alternas (coherente con fig-b2-km)
#
# Lee:    pac, pac_class_df, recidiva_detail, ser_post,
#         mic_post, seg, t0, cens_ser, SERO_NEG, C (namespace)
# Output: figures/fig-b5-swimmer.png
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

if 'pac_class' not in dir():
    exec(open('code/tab_b5_recidiva.py').read())

# ============================================================
# Filtrar: solo pacientes clasificados
# ============================================================
SHOW_CATS = ['Persistencia', 'Recidiva', 'Neg. sostenida']
df = (pac[['ID']].merge(pac_class_df, on='ID'))
df = df[df['categoria'].isin(SHOW_CATS)].copy()

# Seguimiento en meses
fu_ser = (cens_ser / 30.44).rename('fu_meses')
df = df.merge(fu_ser.reset_index(), on='ID')

# Orden: persistencia arriba, recidiva en medio, neg. sostenida abajo
CAT_ORDER = ['Persistencia', 'Recidiva', 'Neg. sostenida']
cat_rank = {c: i for i, c in enumerate(CAT_ORDER)}
df['cat_rank'] = df['categoria'].map(cat_rank)
df['sort_key'] = df['t_primera_neg'].fillna(9999)
df = df.sort_values(['cat_rank', 'sort_key'],
                    ascending=[True, False]).reset_index(drop=True)
n_pac = len(df)

# ============================================================
# Dosis de ivermectina (todas, con etiqueta)
# ============================================================
tto = seg[seg['DOSIS_IVM'].notna()][['ID', 'F_CONSULTA', 'DOSIS_IVM']].copy()
tto = tto.merge(t0.reset_index(), on='ID')
tto['meses'] = (tto['F_CONSULTA'] - tto['T0']).dt.days / 30.44
# Etiqueta abreviada
_dosis_lbl = {
    'MONO': '1×', 'DOBLE_CONSECUTIVA': '2×c',
    'DOBLE_SEPARADA': '2×s', 'CUADRUPLE': '4×', 'MULTIPLE': 'n×',
}
tto['lbl'] = tto['DOSIS_IVM'].map(_dosis_lbl).fillna('')

# ============================================================
# Colores por categoría
# ============================================================
CAT_COLOR = {
    'Neg. sostenida':  C['blue'],
    'Recidiva':        C['red'],
    'Persistencia':    C['gold'],
}

# ============================================================
# Figura
# ============================================================
fig, ax = plt.subplots(figsize=(13, max(7, n_pac * 0.38)))

# --- Franjas semestrales alternas ---
max_mes = df['fu_meses'].max()
sem = 0
while sem * 6 < max_mes + 6:
    if sem % 2 == 0:
        ax.axvspan(sem * 6, (sem + 1) * 6,
                   color=C['grid'], alpha=0.25, zorder=0)
    sem += 1

# --- Barras y marcadores por paciente ---
for i, row in df.iterrows():
    pid = row['ID']
    fu  = row['fu_meses']
    cat = row['categoria']
    col = CAT_COLOR[cat]

    # Barra de seguimiento
    ax.barh(i, fu, height=0.55, left=0,
            color=col, alpha=0.15, edgecolor=col, linewidth=0.6,
            zorder=2)

    # ● IgG post-T₀
    sp = ser_post[ser_post['ID'] == pid]
    for _, m in sp.iterrows():
        mes = m['dias'] / 30.44
        neg = m['IGG'] < SERO_NEG
        ax.scatter(mes, i, marker='o', s=32, zorder=5,
                   color=C['blue'] if neg else C['red'],
                   edgecolors='white', linewidths=0.4)

    # ★ Medición confirmadora de recidiva
    if pid in recidiva_detail and not np.isnan(row['t_rebote']):
        ax.scatter(row['t_rebote'] / 30.44, i,
                   marker='*', s=180, zorder=7,
                   color=C['red'], edgecolors='black', linewidths=0.5)

    # ◆ Dosis de ivermectina (rombos grandes + etiqueta)
    doses = tto[tto['ID'] == pid].sort_values('meses')
    for j, (_, d) in enumerate(doses.iterrows()):
        is_retreat = j > 0
        ax.scatter(d['meses'], i, marker='D',
                   s=55 if is_retreat else 35,
                   zorder=6, color='black' if not is_retreat else C['red'],
                   edgecolors='white', linewidths=0.4)
        if is_retreat:
            ax.annotate(d['lbl'], (d['meses'], i),
                        xytext=(0, -8), textcoords='offset points',
                        fontsize=6, ha='center', va='top',
                        color=C['red'], fontweight='bold')

    # ■ Parasitología post-T₀
    mp = mic_post[mic_post['ID'] == pid]
    for _, m in mp.iterrows():
        mes = m['dias'] / 30.44
        pos = m['RESULTADO'] == 1
        ax.scatter(mes, i + 0.18, marker='s', s=16, zorder=5,
                   color=C['red'] if pos else C['green'],
                   edgecolors='white', linewidths=0.3)

# --- Separadores de categoría ---
prev_cat = None
for i, row in df.iterrows():
    cat = row['categoria']
    if cat != prev_cat and prev_cat is not None:
        ax.axhline(i - 0.5, color=C['annot'], lw=0.8, ls='-', zorder=1)
    prev_cat = cat

# --- Etiquetas de categoría ---
prev_cat = None
for i, row in df.iterrows():
    cat = row['categoria']
    if cat != prev_cat:
        cat_rows = df[df['categoria'] == cat]
        y_mid = (cat_rows.index[0] + cat_rows.index[-1]) / 2
        ax.text(-0.6, y_mid, cat, fontsize=8, fontweight='bold',
                ha='right', va='center', color=CAT_COLOR[cat],
                clip_on=False)
        prev_cat = cat

# --- Eje x: semestres ---
ax.set_xticks(range(0, int(max_mes) + 6, 6))
ax.set_xlabel('Meses desde T₀')

# --- Eje y ---
ax.set_ylim(-0.5, n_pac - 0.5)
ax.invert_yaxis()
ax.set_yticks(range(n_pac))
ax.set_yticklabels([f'P{pid}' for pid in df['ID']], fontsize=7)
ax.set_title(f'Diagrama de nadador · Pacientes clasificables (n = {n_pac})')

# --- Leyenda ---
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=C['blue'],
           markersize=6, label=f'IgG < {SERO_NEG} (neg.)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=C['red'],
           markersize=6, label=f'IgG ≥ {SERO_NEG} (pos.)'),
    Line2D([0], [0], marker='*', color='w', markerfacecolor=C['red'],
           markersize=9, markeredgecolor='black',
           label='Confirmación recidiva'),
    Line2D([0], [0], marker='D', color='w', markerfacecolor='black',
           markersize=5, label='1ª dosis IVM'),
    Line2D([0], [0], marker='D', color='w', markerfacecolor=C['red'],
           markersize=6, label='Retratamiento IVM'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor=C['green'],
           markersize=5, label='Parasitología neg.'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor=C['red'],
           markersize=5, label='Parasitología pos.'),
]
ax.legend(handles=legend_elements, loc='lower right',
          fontsize=7, frameon=True, framealpha=0.92,
          ncol=2, handletextpad=0.3, columnspacing=1.0)

plt.tight_layout()
plt.savefig('figures/fig-b5-swimmer.png', dpi=300, bbox_inches='tight')
plt.show()
