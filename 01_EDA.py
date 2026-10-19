import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Design-Einstellungen setzen
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# 1. Daten laden
df_charge = pd.read_csv('KTZH_00002282_00004563.csv')
df_income = pd.read_csv('KANTON_ZUERICH_282.csv')

# 2. Datenbereinigung
df_charge_clean = df_charge.dropna(subset=['jahr', 'stadt', 'aktiver_energieverbrauch']).copy()
df_charge_clean['jahr'] = df_charge_clean['jahr'].astype(int)

# 3. Deskriptive Statistik
stats = df_charge_clean[['ladeleistung', 'aktiver_energieverbrauch', 'aktive_ladeleistung']].describe().T
print("--- Deskriptive Statistik ---")
print(stats[['mean', 'std', 'min', '50%', 'max']])

# 4. Aggregation nach Jahren
yearly = df_charge_clean.groupby('jahr').agg(
    ladevorgaenge=('id', 'count'),
    energie_kWh=('aktiver_energieverbrauch', 'sum'),
    avg_leistung_kW=('aktive_ladeleistung', 'mean')
).reset_index()

# 5. Visualisierung 1: Trend-Diagramm
fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

ax1.bar(yearly['jahr'] - 0.2, yearly['ladevorgaenge'], width=0.4, color='#2b5c8f', label='Ladevorgänge')
ax2.bar(yearly['jahr'] + 0.2, yearly['energie_kWh'], width=0.4, color='#d95f02', label='Energie (kWh)')

ax1.set_xlabel('Jahr', fontweight='bold')
ax1.set_ylabel('Anzahl Ladevorgänge', color='#2b5c8f', fontweight='bold')
ax2.set_ylabel('Gesamtenergieverbrauch (kWh)', color='#d95f02', fontweight='bold')
plt.title('Entwicklung der E-Ladevorgänge und des Energieverbrauchs im Kanton Zürich')
plt.tight_layout()
plt.savefig('eda_charging_trend.png', dpi=300)
plt.show()

# 6. Top 10 Städte & Connector-Verteilung
top_cities = df_charge_clean.groupby('stadt')['aktiver_energieverbrauch'].sum().sort_values(ascending=False).head(10)
connectors = df_charge_clean['connector_typ'].value_counts(normalize=True) * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
top_cities.plot(kind='barh', ax=ax1, color='#2b5c8f')
ax1.set_title('Top 10 Städte nach E-Energieverbrauch (kWh)')
ax1.invert_yaxis()

connectors.head(5).plot(kind='pie', ax=ax2, autopct='%1.1f%%', colors=['#2b5c8f', '#d95f02', '#7570b3'])
ax2.set_title('Verteilung der Steckertypen')
ax2.set_ylabel('')

plt.tight_layout()
plt.savefig('eda_top_cities_connectors.png', dpi=300)
plt.show()