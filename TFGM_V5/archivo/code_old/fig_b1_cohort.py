# ============================================================
# code/fig_b1_cohort.py
# ------------------------------------------------------------
# Figura 1: Descripción de la cohorte (4 paneles)
#   A. País de origen
#   B. Modo diagnóstico (serología / parasitología / clínico)
#   C. Régimen de ivermectina (mono/doble/cuádruple)
#   D. Inmunodepresión / comorbilidad
# Lee:    pac, sero_pos, mic_pos_ids, C (del namespace)
# Output: figures/fig-b1-cohort.png
# ============================================================

if 'pac' not in dir():
    exec(open('code/_setup.py').read())
    exec(open('code/_data.py').read())

fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# ------------------------------------------------------------
# A. Origen
# ------------------------------------------------------------
ax = axes[0, 0]
region_map = {
    'ECUADOR':'Am. Sur','BOLIVIA':'Am. Sur','PERU':'Am. Sur','COLOMBIA':'Am. Sur',
    'BRASIL':'Am. Sur','PARAGUAY':'Am. Sur','ARGENTINA':'Am. Sur',
    'HONDURAS':'Am. Central','GUATEMALA':'Am. Central','EL SALVADOR':'Am. Central',
    'MEXICO':'Am. Central','REP. DOMINICANA':'Am. Central',
    'GUINEA ECUATORIAL':'Áfr. Subsah.','SENEGAL':'Áfr. Subsah.','GAMBIA':'Áfr. Subsah.',
    'GUINEA CONAKRY':'Áfr. Subsah.','CONGO':'Áfr. Subsah.',
    'ITALIA':'Europa','ESPANA':'Europa',
}
rpal = {'Am. Sur': C['blue'], 'Am. Central': C['gold'],
        'Áfr. Subsah.': C['teal'], 'Europa': C['muted']}
pac['REGION'] = pac['ORIGEN'].map(region_map).fillna('Otros')
orig = pac['ORIGEN'].value_counts()
otros = orig[orig < 2]
if len(otros):
    orig = orig[orig >= 2]
    orig['Otros'] = otros.sum()
orig = orig.sort_values()
bar_c = [C['muted'] if o == 'Otros'
         else rpal.get(pac[pac['ORIGEN'] == o]['REGION'].iloc[0], C['muted'])
         for o in orig.index]
ax.barh(range(len(orig)), orig.values, color=bar_c, edgecolor='white', height=0.7)
ax.set_yticks(range(len(orig)))
ax.set_yticklabels(orig.index, fontsize=7)
for i, v in enumerate(orig.values):
    ax.text(v + 0.15, i, str(v), va='center', fontsize=7, color=C['annot'])
ax.set(xlabel='n', title='A. País de origen')
rc = pac['REGION'].value_counts()
ax.legend(
    handles=[Patch(facecolor=v, label=f'{k} ({rc.get(k, 0)})')
             for k, v in rpal.items() if rc.get(k, 0) > 0],
    frameon=False, fontsize=7, loc='lower right',
)

# ------------------------------------------------------------
# B. Modo diagnóstico
# ------------------------------------------------------------
ax = axes[0, 1]
n_so = len(sero_pos - mic_pos_ids)
n_sp = len(sero_pos & mic_pos_ids)
n_po = len(mic_pos_ids - sero_pos)
n_cl = 44 - len(sero_pos | mic_pos_ids)
dx_rows = [
    ('Serología',     n_so, C['blue']),
    ('Sero+Para',     n_sp, C['teal']),
    ('Parasitología', n_po, C['purple']),
    ('Clínico-epi',   n_cl, C['muted']),
]
for i, (l, v, c) in enumerate(dx_rows):
    ax.barh(i, v, color=c, edgecolor='white', height=0.6)
    if v > 0:
        ax.text(v + 0.2, i, f'{v} ({v/44*100:.0f}%)',
                va='center', fontsize=8, fontweight='bold')
ax.set_yticks(range(4))
ax.set_yticklabels([r[0] for r in dx_rows], fontsize=8)
ax.set(xlabel='n', title='B. Modo diagnóstico')

# ------------------------------------------------------------
# C. Régimen IVM
# ------------------------------------------------------------
ax = axes[1, 0]
ro  = ['MONO', 'DOBLE_CONSECUTIVA', 'DOBLE_SEPARADA', 'CUADRUPLE']
rl  = ['Mono', 'Doble\ncons.', 'Doble\nsep.', 'Cuádr.']
rcc = [C['green'], C['blue'], C['gold'], C['red']]
rv  = [(pac['DOSIS_IVM'] == r).sum() for r in ro]
ax.bar(range(4), rv, color=rcc, edgecolor='white', width=0.6)
for i, v in enumerate(rv):
    ax.text(i, v + 0.3, f'{v} ({v/44*100:.0f}%)',
            ha='center', fontsize=8, fontweight='bold')
ax.set_xticks(range(4))
ax.set_xticklabels(rl, fontsize=7)
ax.set(ylabel='n', title='C. Régimen IVM', ylim=(0, max(rv) + 5))

# ------------------------------------------------------------
# D. Inmunodepresión / comorbilidad
# ------------------------------------------------------------
ax = axes[1, 1]
cats = [
    ('Inmunodepresión', int(pac['INMUNO_SI'].sum()), C['red']),
    ('Comorbilidad',    int(pac['COMORB_SI'].sum()), C['blue']),
    ('Sin ambas',       int(((pac['INMUNO_SI'] == 0) & (pac['COMORB_SI'] == 0)).sum()), C['muted']),
]
for i, (l, v, c) in enumerate(cats):
    ax.barh(i, v, color=c, edgecolor='white', height=0.5)
    ax.text(v + 0.2, i, f'{v}/44 ({v/44*100:.0f}%)',
            va='center', fontsize=8, fontweight='bold')
ax.set_yticks(range(3))
ax.set_yticklabels([c[0] for c in cats], fontsize=8)
ax.set(xlabel='n', title='D. Inmuno/comorbilidad', xlim=(0, 30))

plt.tight_layout()
plt.savefig('figures/fig-b1-cohort.png', dpi=300, bbox_inches='tight')
plt.show()
