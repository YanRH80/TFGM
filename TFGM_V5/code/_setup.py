# ============================================================
# code/_setup.py
# ------------------------------------------------------------
# Imports, paleta de colores, helpers, constantes globales.
# Se ejecuta una sola vez al inicio del Resultados.qmd.
# Independiente de los datos: NO carga Excel.
# ============================================================

import os, sys, warnings, logging
os.makedirs('figures', exist_ok=True)
logging.basicConfig(level=logging.WARNING)
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Patch
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
from collections import OrderedDict

from scipy.stats import (spearmanr, mannwhitneyu, probplot, shapiro,
                          chi2_contingency, fisher_exact, norm, binom)
from scipy.stats import chi2 as chi2_dist
from scipy.stats import t as t_dist
from scipy.stats import poisson

from statsmodels.stats.multitest import multipletests
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
import statsmodels.formula.api as smf

from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
from lifelines.plotting import add_at_risk_counts

# ------------------------------------------------------------
# Paleta de colores (sat + grises)
# ------------------------------------------------------------
SAT = ['#CC3311', '#0077BB', '#EE7733', '#009988',
       '#AA3377', '#33BBEE', '#EE3377']
GRI = ['#F2F2F2', '#DDDDDD', '#999999', '#555555', '#222222']
C = {
    'red':    SAT[0], 'blue':   SAT[1], 'gold':   SAT[2],
    'green':  SAT[3], 'purple': SAT[4], 'teal':   SAT[5],
    'orange': SAT[6],
    'bg':     GRI[0], 'grid':   GRI[1], 'muted':  GRI[2],
    'annot':  GRI[3], 'text':   GRI[4],
}

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.size': 10,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.alpha': 0.3, 'grid.linestyle': ':',
    'figure.dpi': 300, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'text.color': C['text'], 'axes.labelcolor': C['text'],
})

# ------------------------------------------------------------
# Constantes del estudio
# ------------------------------------------------------------
CONFIG = {
    'SERO_NEG': 1.1,
    'SERO_NEG_ALT': 0.9,
    'SERO_DROP_SALVADOR': 0.60,
    'EOS_NEG': 0.5,
    'MICRO_MIN': 7,
    'RECIDIVA_GAP': 21,
    'ALPHA': 0.05,
    'POWER': 0.80,
    'SEED': 42,
}
SERO_NEG  = CONFIG['SERO_NEG']
SERO_DROP = CONFIG['SERO_DROP_SALVADOR']
EOS_NEG   = CONFIG['EOS_NEG']
MICRO_MIN = CONFIG['MICRO_MIN']
ALPHA     = CONFIG['ALPHA']

# ------------------------------------------------------------
# Helpers de formateo
# ------------------------------------------------------------
def med_iqr(s):
    return f"{s.median():.1f} ({s.quantile(.25):.1f}--{s.quantile(.75):.1f})"

def n_pct(num, den):
    return f"{num} ({num/den*100:.1f}\\%)"

def rng(s):
    return f"{s.min():.1f}--{s.max():.1f}"
