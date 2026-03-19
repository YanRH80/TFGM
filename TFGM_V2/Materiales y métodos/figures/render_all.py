#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_all.py — Generate all figure PNGs for the paper.
Run from project root: python figures/render_all.py
"""

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from pathlib import Path

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Helvetica', 'Arial']

OUT = Path(__file__).parent
DPI = 300


def fig_timeline():
    """Figure 1: Clinical timeline with VAS, EuroQol, CSI."""
    data = {
        'Year': [2016, 2017, 2018, 2020, 2021, 2022, 2023, 2025, 2026],
        'VAS': [0, 6, 8, 8, 10, 3, 8, 9, 6],
        'EuroQol': [100, 75, 50, 50, 20, 80, 40, 30, 50],
        'CSI': [15, 30, 45, 50, 70, 35, 55, 50, 40]
    }
    df = pd.DataFrame(data)
    df['VAS_Norm'] = df['VAS'] * 10

    fig, ax = plt.subplots(figsize=(12, 5.5))

    ax.plot(df['Year'], df['VAS_Norm'], color='#E74C3C', linewidth=3.5,
            marker='o', markersize=9, label='Pain (VAS x10)')
    ax.plot(df['Year'], df['EuroQol'], color='#3498DB', linewidth=2.5,
            linestyle='--', marker='s', markersize=8, label='QoL (EuroQol)')
    ax.plot(df['Year'], df['CSI'], color='#F39C12', linewidth=2.5,
            linestyle='-.', marker='^', markersize=8, label='Sensitization (CSI)')

    ax.axvspan(2020.8, 2021.4, color='#FADBD8', alpha=0.5)
    ax.text(2021.1, 105, 'CRISIS', color='#C0392B', ha='center',
            fontweight='bold', fontsize=9)
    ax.axvspan(2021.9, 2022.5, color='#D4EFDF', alpha=0.5)
    ax.text(2022.2, 105, 'FALSE\nRELIEF', color='#27AE60', ha='center',
            fontweight='bold', fontsize=9)
    ax.axvspan(2025.8, 2026.2, color='#D6EAF8', alpha=0.6)
    ax.text(2026, 98, 'CURRENT\nIMPROVEMENT', color='#2980B9', ha='center',
            fontweight='bold', fontsize=9)

    ax.set_ylabel("Normalized Scale (0-100)", fontsize=11, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.set_ylim(-5, 120)
    ax.set_xlim(2015.5, 2026.5)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3,
              frameon=False, fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.annotate('Baseline CSI: 15\n(Predisposition)',
                xy=(2016, 15), xytext=(40, 10), textcoords='offset points',
                ha='left', fontsize=9, color='#D35400', fontweight='bold',
                arrowprops=dict(arrowstyle="->", color='#F39C12', linewidth=1.5))
    ax.annotate('"Sitting\nSign"', (2018, 80), xytext=(0, 30),
                textcoords='offset points', ha='center', fontsize=9,
                fontweight='bold',
                arrowprops=dict(arrowstyle="->", color='black', linewidth=2))
    ax.annotate('Pilates\n(Iatrogenesis)', (2023, 80), xytext=(0, 25),
                textcoords='offset points', ha='center', fontsize=9,
                fontweight='bold',
                arrowprops=dict(arrowstyle="->", color='black', linewidth=2))
    ax.annotate('Myofascial Dx\n(Vaginal Palpation)', (2026, 60),
                xytext=(-40, 15), textcoords='offset points', ha='right',
                fontsize=9, fontweight='bold',
                arrowprops=dict(arrowstyle="->", color='black', linewidth=1.5))

    plt.tight_layout()
    fig.savefig(OUT / "fig-timeline.png", dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"  ✓ fig-timeline.png ({DPI} dpi)")


# ── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Rendering figures...")
    fig_timeline()
    # Add more figures here as needed:
    # fig_something_else()
    print("Done.")
