import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Design-Einstellungen setzen
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# 1. Daten einlesen & bereinigen
df_charge = pd.read_csv('KTZH_00002282_00004563.csv')
df_charge = df_charge.dropna(subset=['jahr', 'stadt', 'aktiver_energieverbrauch'])
df_charge['jahr'] = df_charge['jahr'].astype(int)

# ---------------------------------------------------------
# A. Kreisdiagramm / Donut Chart (Circle Diagram)
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))
connector_counts = df_charge['connector_typ'].value_counts()
colors = ['#2b5c8f', '#d95f02', '#7570b3', '#e7298a']

ax.pie(
    connector_counts, 
    labels=connector_counts.index, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=colors[:len(connector_counts)],
    wedgeprops=dict(width=0.6, edgecolor='w') # Donut-Ausschnitt
)
ax.set_title('Verteilung der Connector-Typen (Kreisdiagramm)', fontsize=14, pad=20)
plt.tight_layout()
plt.savefig('eda_circle_diagram.png', dpi=300)
plt.show()

# ---------------------------------------------------------
# B. Streudiagramm (Spread Diagram)
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))

sns.scatterplot(
    data=df_charge, 
    x='aktive_ladeleistung', 
    y='aktiver_energieverbrauch', 
    hue='connector_typ', 
    alpha=0.6, 
    palette='tab10', 
    ax=ax
)

ax.set_title('Streudiagramm: Aktive Ladeleistung vs. Energieverbrauch', fontsize=14, pad=15)
ax.set_xlabel('Aktive Ladeleistung (kW)', fontsize=12, fontweight='bold')
ax.set_ylabel('Aktiver Energieverbrauch (kWh)', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('eda_spread_diagram.png', dpi=300)
plt.show()

# ---------------------------------------------------------
# C. Heatmap (Energieverbrauch nach Top-Städten und Jahr)
# ---------------------------------------------------------
# Top 10 Städte nach Gesamtenergieverbrauch ermitteln
top_cities = df_charge.groupby('stadt')['aktiver_energieverbrauch'].sum().nlargest(10).index

# Pivottabelle für die Heatmap erstellen
pivot_df = df_charge[df_charge['stadt'].isin(top_cities)].pivot_table(
    index='stadt', 
    columns='jahr', 
    values='aktiver_energieverbrauch', 
    aggfunc='sum', 
    fill_value=0
)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(
    pivot_df, 
    annot=True, 
    fmt=".0f", 
    cmap="YlGnBu", 
    cbar_kws={'label': 'Gesamtenergieverbrauch (kWh)'}, 
    ax=ax
)

ax.set_title('Heatmap: Energieverbrauch (kWh) der Top 10 Städte nach Jahr', fontsize=14, pad=15)
ax.set_xlabel('Jahr', fontsize=12, fontweight='bold')
ax.set_ylabel('Stadt / Gemeinde', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('eda_heatmap.png', dpi=300)
plt.show()