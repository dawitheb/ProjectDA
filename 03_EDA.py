import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Design-Einstellungen setzen
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# Daten laden und bereinigen
df_charge = pd.read_csv('KTZH_00002282_00004563.csv').dropna(subset=['jahr', 'stadt', 'aktiver_energieverbrauch'])
df_income = pd.read_csv('KANTON_ZUERICH_282.csv').dropna(subset=['INDIKATOR_VALUE'])
df_income['INDIKATOR_VALUE'] = pd.to_numeric(df_income['INDIKATOR_VALUE'], errors='coerce')

# ---------------------------------------------------------
# 1. Boxplot: Energieverbrauch nach Stop-Typ
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
sns.boxplot(data=df_charge, x='stop_typ', y='aktiver_energieverbrauch', palette='Set2', ax=ax)
ax.set_title('1. Boxplot: Verteilung des Energieverbrauchs nach Stop-Typ', fontsize=13, pad=15)
ax.set_xlabel('Stop-Typ', fontweight='bold')
ax.set_ylabel('Aktiver Energieverbrauch (kWh)', fontweight='bold')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('eda_boxplot.png', dpi=300)
plt.show()

# ---------------------------------------------------------
# 2. Histogramm & KDE: Dichteverteilung der Ladeleistung
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
sns.histplot(df_charge['aktive_ladeleistung'].dropna(), kde=True, bins=30, color='#2b5c8f', ax=ax)
ax.set_title('2. Histogramm & KDE: Dichteverteilung der aktiven Ladeleistung (kW)', fontsize=13, pad=15)
ax.set_xlabel('Aktive Ladeleistung (kW)', fontweight='bold')
ax.set_ylabel('Häufigkeit', fontweight='bold')
plt.tight_layout()
plt.savefig('eda_histogram.png', dpi=300)
plt.show()

# ---------------------------------------------------------
# 3. Regressionsdiagramm: Einkommen vs. E-Energieverbrauch
# ---------------------------------------------------------
charge_muni = df_charge.groupby('stadt').agg(
    total_energy_kWh=('aktiver_energieverbrauch', 'sum')
).reset_index()

latest_income = df_income[df_income['INDIKATOR_JAHR'] == df_income['INDIKATOR_JAHR'].max()][['GEBIET_NAME', 'INDIKATOR_VALUE']]
latest_income.columns = ['stadt', 'avg_income_chf']

merged_df = pd.merge(charge_muni, latest_income, on='stadt', how='inner')

fig, ax = plt.subplots(figsize=(9, 5))
sns.regplot(data=merged_df, x='avg_income_chf', y='total_energy_kWh', color='#d95f02', ax=ax, scatter_kws={'s': 60, 'alpha': 0.7})
ax.set_title('3. Regressions-Diagramm: Steuerbares Einkommen vs. E-Energieverbrauch pro Gemeinde', fontsize=13, pad=15)
ax.set_xlabel('Durchschnittliches steuerbares Einkommen (CHF)', fontweight='bold')
ax.set_ylabel('Gesamtenergieverbrauch (kWh)', fontweight='bold')
plt.tight_layout()
plt.savefig('eda_regression_scatter.png', dpi=300)
plt.show()