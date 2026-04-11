# ============================================================
# code/_data.py
# ------------------------------------------------------------
# Carga BASE_EXCEL.xlsx y construye todos los dataframes
# que las figuras y tablas necesitan.
#
# Lee:    data/BASE_EXCEL.xlsx (5 hojas: bas, ser, eos, mic, seg)
# Escribe (en namespace):
#   - pac          : cohorte basal (44 filas)
#   - ev, ev_alt   : datos tiempo-evento (7 endpoints)
#   - cox_data     : datos para Cox univariable
#   - km_full      : datos para KM estratificado
#   - ser_long, eos_long : longitudinales
#   - ser_post, eos_post : post-T0
#   - cens_ser, cens_eos : tiempos de censura
#   - igg_med, igg_p75, eos_med, eos_p75 : cuantiles basales
#   - nice         : diccionario de etiquetas legibles
#
# Asume que _setup.py ya ha sido ejecutado.
# ============================================================

# Verificación: si se ejecuta standalone, primero cargar _setup
if 'C' not in dir():
    exec(open('code/_setup.py').read())

RUTA = 'data/BASE_EXCEL.xlsx'

bas_raw = pd.read_excel(RUTA, 'bas')
ser_raw = pd.read_excel(RUTA, 'ser')
eos_raw = pd.read_excel(RUTA, 'eos')
mic_raw = pd.read_excel(RUTA, 'mic')
seg_raw = pd.read_excel(RUTA, 'seg')

# ------------------------------------------------------------
# Limpieza por hoja
# ------------------------------------------------------------
bas = bas_raw.copy()
bas['ID'] = bas['ID'].astype(int)
bas['F_NAC'] = pd.to_datetime(bas['F_NAC'])

ser = ser_raw.copy()
ser['ID'] = ser['ID'].astype(int)
ser['F_SER'] = pd.to_datetime(ser['F_SER'])
ser['IGG_QUAL'] = ser['IGG'].where(ser['IGG'].apply(lambda x: isinstance(x, str)))
ser['IGG'] = pd.to_numeric(ser['IGG'], errors='coerce')

eos = eos_raw.copy()
eos['ID'] = eos['ID'].astype(int)
eos['F_EOS'] = pd.to_datetime(eos['F_EOS'])
eos['EOS'] = pd.to_numeric(eos['EOS'], errors='coerce')

mic = mic_raw[mic_raw['F_MIC'].notna()].copy()
mic['ID'] = mic['ID'].astype(int)
mic['F_MIC'] = pd.to_datetime(mic['F_MIC'])
mic['RESULTADO'] = pd.to_numeric(mic['RESULTADO'], errors='coerce')
mic.loc[mic['RESULTADO'].isna() & mic_raw.loc[mic.index, 'RESULTADO'].notna(),
        'RESULTADO'] = 1
mic['RESULTADO'] = mic['RESULTADO'].astype(int)

seg = seg_raw.copy()
seg['ID'] = seg['ID'].astype(int)
seg['F_CONSULTA'] = pd.to_datetime(seg['F_CONSULTA'])

# ------------------------------------------------------------
# T0 y mediciones basales
# ------------------------------------------------------------
t0 = seg[seg['DOSIS_IVM'].notna()].groupby('ID')['F_CONSULTA'].min().rename('T0')

ser_t = ser[['ID', 'F_SER', 'IGG', 'IGG_QUAL']].merge(t0.reset_index(), on='ID')
ser_t['dias'] = (ser_t['F_SER'] - ser_t['T0']).dt.days
ser_pre = ser_t[ser_t['dias'] <= 0]
idx = ser_pre.groupby('ID')['dias'].idxmax()
ser_basal = ser_pre.loc[idx, ['ID', 'IGG', 'IGG_QUAL']].rename(
    columns={'IGG': 'IGG_BASAL', 'IGG_QUAL': 'IGG_QUAL_BASAL'})

eos_t = eos[['ID', 'F_EOS', 'EOS']].merge(t0.reset_index(), on='ID')
eos_t['dias'] = (eos_t['F_EOS'] - eos_t['T0']).dt.days
eos_pre = eos_t[eos_t['dias'] <= 0]
idx2 = eos_pre.groupby('ID')['dias'].idxmax()
eos_basal = eos_pre.loc[idx2, ['ID', 'EOS']].rename(columns={'EOS': 'EOS_BASAL'})

mic_t = mic.merge(t0.reset_index(), on='ID')
mic_t['dias'] = (mic_t['F_MIC'] - mic_t['T0']).dt.days
mic_pre = mic_t[mic_t['dias'] <= 0]
mic_basal = (mic_pre.groupby(['ID', 'TIPO'])['RESULTADO'].max().unstack()
                    .reset_index()
                    .rename(columns={'COPRO': 'COPRO_BASAL', 'MICRO': 'MICRO_BASAL'}))
mic_basal['MIC_BASAL'] = mic_basal[['COPRO_BASAL', 'MICRO_BASAL']].max(axis=1)

# ------------------------------------------------------------
# Cohorte basal pac (44 filas)
# ------------------------------------------------------------
pac = (bas.merge(t0.reset_index(), on='ID')
          .merge(ser_basal[['ID', 'IGG_BASAL', 'IGG_QUAL_BASAL']], on='ID', how='left')
          .merge(eos_basal[['ID', 'EOS_BASAL']], on='ID', how='left')
          .merge(mic_basal[['ID', 'MIC_BASAL']], on='ID', how='left'))

pac['EDAD'] = ((pac['T0'] - pac['F_NAC']).dt.days / 365.25).round(1)
pac['AN_ESP'] = pac['T0'].dt.year - pac['T_ESP'] + pac['T0'].dt.month / 12
pac['INMUNO_SI']  = (pac['INMUNO']  != 'NO').astype(int)
pac['COMORB_SI']  = (pac['COMORB']  != 'NO').astype(int)
pac['CONFEOS_SI'] = (pac['CONFEOS'] != 'NO').astype(int)
pac['SEXO_V']     = (pac['SEXO']    == 'V').astype(int)

pac['EOS_ALTA'] = np.where(pac['EOS_BASAL'].isna(), np.nan,
                            (pac['EOS_BASAL'] >= EOS_NEG).astype(int))
pac['SER_ALTA'] = np.where(pac['IGG_BASAL'].isna(), np.nan,
                            (pac['IGG_BASAL'] >= SERO_NEG).astype(int))

igg_med = pac['IGG_BASAL'].median()
igg_p75 = pac['IGG_BASAL'].quantile(0.75)
eos_med = pac['EOS_BASAL'].median()
eos_p75 = pac['EOS_BASAL'].quantile(0.75)

pac['SER_MEDIANA'] = np.where(pac['IGG_BASAL'].isna(), np.nan,
                               (pac['IGG_BASAL'] >= igg_med).astype(int))
pac['SER_P75']     = np.where(pac['IGG_BASAL'].isna(), np.nan,
                               (pac['IGG_BASAL'] >= igg_p75).astype(int))
pac['SER_TERCIL']  = pd.qcut(pac['IGG_BASAL'], q=3, labels=['Bajo', 'Medio', 'Alto'])

pac['EOS_MEDIANA'] = np.where(pac['EOS_BASAL'].isna(), np.nan,
                               (pac['EOS_BASAL'] >= eos_med).astype(int))
pac['EOS_P75']     = np.where(pac['EOS_BASAL'].isna(), np.nan,
                               (pac['EOS_BASAL'] >= eos_p75).astype(int))
pac['EOS_1000']    = np.where(pac['EOS_BASAL'].isna(), np.nan,
                               (pac['EOS_BASAL'] >= 1.0).astype(int))
pac['EOS_TERCIL']  = pd.qcut(pac['EOS_BASAL'], q=3, labels=['Bajo', 'Medio', 'Alto'])
pac['EOS_LIMPIA']  = np.where(pac['EOS_BASAL'].isna(), np.nan,
                               ((pac['EOS_BASAL'] >= EOS_NEG) & (pac['CONFEOS_SI'] == 0)).astype(int))
pac['EDAD_ALTA']   = (pac['EDAD'] >= pac['EDAD'].median()).astype(int)

primer_tto = (seg[seg['DOSIS_IVM'].notna()]
                .sort_values('F_CONSULTA').groupby('ID').first()[['DOSIS_IVM']])
pac = pac.merge(primer_tto.reset_index(), on='ID', how='left')
pac['MONO'] = (pac['DOSIS_IVM'] == 'MONO').astype(int)

# Región geográfica (para Tabla 1 y cualquier análisis posterior)
region_map = {
    'ECUADOR':          'Am. Sur',
    'BOLIVIA':          'Am. Sur',
    'PERU':             'Am. Sur',
    'COLOMBIA':         'Am. Sur',
    'BRASIL':           'Am. Sur',
    'PARAGUAY':         'Am. Sur',
    'ARGENTINA':        'Am. Sur',
    'HONDURAS':         'Am. Central',
    'GUATEMALA':        'Am. Central',
    'EL SALVADOR':      'Am. Central',
    'MEXICO':           'Am. Central',
    'REP. DOMINICANA':  'Am. Central',
    'GUINEA ECUATORIAL':'Áfr. Subsah.',
    'SENEGAL':          'Áfr. Subsah.',
    'GAMBIA':           'Áfr. Subsah.',
    'GUINEA CONAKRY':   'Áfr. Subsah.',
    'CONGO':            'Áfr. Subsah.',
    'ITALIA':           'Europa',
    'ESPANA':           'Europa',
}
pac['REGION'] = pac['ORIGEN'].map(region_map).fillna('Otros')

n_ttos = seg[seg['DOSIS_IVM'].notna()].groupby('ID').size().rename('N_TTO')
pac = pac.merge(n_ttos.reset_index(), on='ID', how='left')
pac['RETRATADO'] = (pac['N_TTO'] > 1).astype(int)
pac['INMUNO_O_COMORB'] = ((pac['INMUNO_SI'] == 1) | (pac['COMORB_SI'] == 1)).astype(int)
pac['DX_PARA'] = pac['MIC_BASAL'].fillna(0).astype(int)

# ------------------------------------------------------------
# Exclusiones serológicas para análisis KM/Cox
# ------------------------------------------------------------
neg_basal_ids = pac[pac['IGG_QUAL_BASAL'] == 'NEG']['ID'].tolist()
EXCL_SERO_IDS = set(neg_basal_ids)
_ser_basal_t0 = ser_pre.loc[idx, ['ID', 'dias']].copy()
_ser_basal_t0['dias_abs'] = _ser_basal_t0['dias'].abs()

# ------------------------------------------------------------
# Datasets longitudinales y post-T0
# ------------------------------------------------------------
ser_long = ser_t[ser_t['IGG'].notna()].copy()
ser_long['meses'] = ser_long['dias'] / 30.44

eos_long = eos_t.copy()
eos_long['meses'] = eos_long['dias'] / 30.44

ser_post = ser_long[ser_long['dias'] > 0].copy()
eos_post = eos_long[eos_long['dias'] > 0].copy()
mic_post = mic_t[mic_t['dias'] > MICRO_MIN].sort_values(['ID', 'dias']).copy()


# ------------------------------------------------------------
# Función build_events: 7 endpoints tiempo-a-evento
# ------------------------------------------------------------
def build_events(ser_post_df, pac_df, eos_post_df, mic_post_df,
                 ser_long_df, eos_long_df, sero_neg, sero_drop,
                 excl_sero_ids=set()):
    sp = ser_post_df[~ser_post_df['ID'].isin(excl_sero_ids)].copy()
    sp['neg_abs'] = sp['IGG'] < sero_neg
    neg_sero_abs = (sp[sp['neg_abs']].sort_values('dias').groupby('ID').first()
                       [['dias', 'IGG']]
                       .rename(columns={'dias': 'T_NEG_SERO_ABS', 'IGG': 'IGG_NEG'}))

    sp_b = sp.merge(pac_df[['ID', 'IGG_BASAL']], on='ID')
    sp_b['neg_rel'] = sp_b['IGG'] < sp_b['IGG_BASAL'] * sero_drop
    neg_sero_rel = (sp_b[sp_b['neg_rel']].sort_values('dias').groupby('ID').first()
                       [['dias']].rename(columns={'dias': 'T_NEG_SERO_REL'}))

    sps = sp.sort_values(['ID', 'dias']).copy()
    sps['neg'] = sps['IGG'] < sero_neg
    sps['neg_prev'] = sps.groupby('ID')['neg'].shift(1)
    sps['doble_neg'] = sps['neg'] & sps['neg_prev']
    neg_sero_abs_x2 = (sps[sps['doble_neg']].groupby('ID').first()
                          [['dias']].rename(columns={'dias': 'T_NEG_SERO_ABS_X2'}))

    spr = sp_b.sort_values(['ID', 'dias']).copy()
    spr['neg_prev'] = spr.groupby('ID')['neg_rel'].shift(1)
    spr['doble'] = spr['neg_rel'] & spr['neg_prev']
    neg_sero_rel_x2 = (spr[spr['doble']].groupby('ID').first()
                          [['dias']].rename(columns={'dias': 'T_NEG_SERO_REL_X2'}))

    ep = eos_post_df.copy()
    ep['neg_abs'] = ep['EOS'] < EOS_NEG
    neg_eos = (ep[ep['neg_abs']].sort_values('dias').groupby('ID').first()
                  [['dias']].rename(columns={'dias': 'T_NEG_EOS_ABS'}))

    mp = mic_post_df.copy()
    mp['neg'] = mp['RESULTADO'] == 0
    mp['neg_prev'] = mp.groupby('ID')['neg'].shift(1)
    mp['doble'] = mp['neg'] & mp['neg_prev']
    neg_para = (mp[mp['doble']].groupby('ID').first()
                  [['dias']].rename(columns={'dias': 'T_NEG_PARA'}))
    n_evaluables = mp['ID'].nunique()

    cens_ser = ser_long_df[ser_long_df['dias'] > 0].groupby('ID')['dias'].max().rename('cens_ser')
    cens_eos = eos_long_df[eos_long_df['dias'] > 0].groupby('ID')['dias'].max().rename('cens_eos')
    cens_mic = (mp.groupby('ID')['dias'].max().rename('cens_mic')
                if len(mp) > 0 else pd.Series(dtype=float, name='cens_mic'))

    ev = pac_df[['ID']].copy()
    ev = ev.merge(cens_ser.reset_index(), on='ID', how='left')
    ev = ev.merge(cens_eos.reset_index(), on='ID', how='left')
    ev = ev.merge(cens_mic.reset_index(), on='ID', how='left')

    def add_event(ev, neg_df, time_col, cens_col, prefix):
        if len(neg_df) > 0:
            ev = ev.merge(neg_df[[time_col]].reset_index().rename(columns={time_col: '_t'}),
                          on='ID', how='left')
        else:
            ev['_t'] = np.nan
        ev[f'E_{prefix}'] = ev['_t'].notna().astype(int)
        ev[f'T_{prefix}'] = ev['_t'].fillna(ev[cens_col])
        ev = ev.drop(columns='_t')
        return ev

    ev = add_event(ev, neg_sero_abs,    'T_NEG_SERO_ABS',    'cens_ser', 'SERO_ABS_X1')
    ev = add_event(ev, neg_sero_abs_x2, 'T_NEG_SERO_ABS_X2', 'cens_ser', 'SERO_ABS_X2')
    ev = add_event(ev, neg_sero_rel,    'T_NEG_SERO_REL',    'cens_ser', 'SERO_REL_X1')
    ev = add_event(ev, neg_sero_rel_x2, 'T_NEG_SERO_REL_X2', 'cens_ser', 'SERO_REL_X2')
    ev = add_event(ev, neg_eos,         'T_NEG_EOS_ABS',     'cens_eos', 'EOS_ABS')
    ev = add_event(ev, neg_para,        'T_NEG_PARA',        'cens_mic', 'PARA')

    stats = {'sero_neg': sero_neg, 'sero_drop': sero_drop,
             'n_excl_sero': len(excl_sero_ids),
             'n_sero_abs_x1': ev['E_SERO_ABS_X1'].sum(),
             'n_sero_abs_x2': ev['E_SERO_ABS_X2'].sum(),
             'n_sero_rel_x1': ev['E_SERO_REL_X1'].sum(),
             'n_sero_rel_x2': ev['E_SERO_REL_X2'].sum(),
             'n_eos': ev['E_EOS_ABS'].sum(), 'n_para': ev['E_PARA'].sum(),
             'n_evaluables_para': n_evaluables}
    neg = {'neg_sero_abs': neg_sero_abs, 'neg_sero_abs_x2': neg_sero_abs_x2,
           'neg_sero_rel': neg_sero_rel, 'neg_sero_rel_x2': neg_sero_rel_x2,
           'neg_eos': neg_eos, 'neg_para': neg_para, 'ser_post_b': sp_b,
           'cens_ser': cens_ser, 'cens_eos': cens_eos, 'cens_mic': cens_mic}
    return ev, stats, neg


ev, ev_stats, ev_neg = build_events(
    ser_post, pac, eos_post, mic_post, ser_long, eos_long,
    sero_neg=SERO_NEG, sero_drop=SERO_DROP, excl_sero_ids=EXCL_SERO_IDS)
neg_sero_abs = ev_neg['neg_sero_abs']
cens_ser = ev_neg['cens_ser']
cens_eos = ev_neg['cens_eos']
n_evaluables = ev_stats['n_evaluables_para']

ev_alt, ev_alt_stats, ev_alt_neg = build_events(
    ser_post, pac, eos_post, mic_post, ser_long, eos_long,
    sero_neg=CONFIG['SERO_NEG_ALT'], sero_drop=SERO_DROP, excl_sero_ids=EXCL_SERO_IDS)

# ------------------------------------------------------------
# Sets auxiliares y datos para Cox/KM
# ------------------------------------------------------------
sero_pos = set(pac[(pac['IGG_BASAL'] >= SERO_NEG) |
                    ((pac['IGG_QUAL_BASAL'].notna()) & (pac['IGG_QUAL_BASAL'] != 'NEG'))]['ID'])
mic_pos_ids = set(mic_pre[mic_pre['RESULTADO'] == 1]['ID'])

PAC_COLS = ['ID', 'SEXO', 'SEXO_V', 'EDAD', 'INMUNO_SI', 'COMORB_SI',
            'EOS_ALTA', 'EOS_MEDIANA', 'EOS_P75', 'EOS_1000', 'EOS_TERCIL',
            'EOS_LIMPIA', 'EOS_BASAL',
            'SER_ALTA', 'SER_MEDIANA', 'SER_P75', 'SER_TERCIL', 'IGG_BASAL',
            'EDAD_ALTA', 'MONO', 'RETRATADO', 'INMUNO_O_COMORB', 'DX_PARA']

km_full = ev[['ID', 'T_SERO_ABS_X1', 'E_SERO_ABS_X1']].merge(pac[PAC_COLS], on='ID')
km_full = km_full[km_full['T_SERO_ABS_X1'] > 0]
cox_data = km_full.copy()

# ------------------------------------------------------------
# Diccionario de etiquetas legibles para variables Cox
# (todas las variables derivadas llevan calificador temporal
#  explícito: "al diagnóstico" / "basal" / "continua")
# ------------------------------------------------------------
nice = {
    'SEXO_V':          'Sexo (varón)',
    'EDAD':             'Edad al diagnóstico (años, continua)',
    'EDAD_ALTA':        f'Edad al diagnóstico ≥ {pac["EDAD"].median():.0f} años',
    'INMUNO_SI':        'Inmunodepresión basal',
    'COMORB_SI':        'Comorbilidad basal significativa',
    'INMUNO_O_COMORB':  'Inmunodepresión o comorbilidad basal',
    'EOS_ALTA':         f'Eosinofilia al diagnóstico ≥ {EOS_NEG} ×10³/µL',
    'EOS_MEDIANA':      f'Eosinófilos basales ≥ mediana ({eos_med:.2f} ×10³/µL)',
    'SER_MEDIANA':      f'IgG-ELISA basal ≥ mediana ({igg_med:.1f})',
    'SER_P75':          f'IgG-ELISA basal ≥ P75 ({igg_p75:.1f})',
    'IGG_BASAL':        'IgG-ELISA basal (índice, continua)',
    'EOS_BASAL':        'Eosinófilos basales (×10³/µL, continua)',
    'MONO':             'Dosis única de ivermectina',
    'RETRATADO':        'Retratamiento (>1 ciclo de ivermectina)',
    'DX_PARA':          'Diagnóstico parasitológico basal (coprocultivo/PCR)',
    'EOS_LIMPIA':       f'Eosinofilia al diagnóstico ≥ {EOS_NEG} ×10³/µL (sin confusor)',
    'EOS_P75':          f'Eosinófilos basales ≥ P75 ({eos_p75:.2f} ×10³/µL)',
    'EOS_1000':         'Eosinófilos basales ≥ 1,0 ×10³/µL',
}
