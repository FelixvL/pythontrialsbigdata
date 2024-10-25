import pandas as pd
import matplotlib.pyplot as plt

# 1. Laad de consumentenbestedingen gegevens
df_consumentenbestedingen = pd.read_csv('docs/consumentenbestedingen.csv', sep=";")

# Zet de 'Value' kolom om naar numeriek (vervang komma door punt)
df_consumentenbestedingen['Value'] = df_consumentenbestedingen['Value'].str.replace(',', '.').astype(float)

# Groepeer de gegevens per jaar en sommeer de bestedingen
df_consumentenbestedingen_grouped = df_consumentenbestedingen.groupby('Perioden')['Value'].sum().reset_index()

# 2. Laad de periodecodes om leesbare jaartallen toe te voegen
df_perioden = pd.read_csv('docs/periodecodes.csv', sep=";")

# Koppel de consumentenbestedingen met de periodecodes op basis van 'Perioden' en 'Identifier'
df_consumentenbestedingen_grouped = df_consumentenbestedingen_grouped.merge(df_perioden[['Identifier', 'Title']], left_on='Perioden', right_on='Identifier')

# Controleer of de data correct is ingeladen
print("Gecombineerde consumentenbestedingen dataset:")
print(df_consumentenbestedingen_grouped.head())

# 3. Laad de inflatiegegevens
df_inflatie = pd.read_csv('docs/inflatie.csv', sep=";")

# Vervang komma's door punten en zet de Value-kolom om naar numeriek
df_inflatie['Value'] = df_inflatie['Value'].str.replace(',', '.').astype(float)

# Extracteer het jaar uit de 'Perioden' kolom (bijv. 1963MM01 -> 1963)
df_inflatie['Jaar'] = df_inflatie['Perioden'].str[:4]

# Bereken de gemiddelde inflatie per jaar
df_inflatie_yearly = df_inflatie.groupby('Jaar')['Value'].mean().reset_index()

# Controleer de inflatie dataset
print("Inflatie per jaar:")
print(df_inflatie_yearly.head())

# 4. Koppel de consumentenbestedingen met de inflatiegegevens op basis van het jaar ('Title' in consumentenbestedingen en 'Jaar' in inflatie)
df_merged = df_consumentenbestedingen_grouped.merge(df_inflatie_yearly, left_on='Title', right_on='Jaar')

# Controleer de gecombineerde dataset
print("Gecombineerde dataset met inflatie en consumentenbestedingen:")
print(df_merged.head())

# 5. Correlatieanalyse tussen inflatie en consumentenbestedingen
correlatie = df_merged[['Value_x', 'Value_y']].corr()
print("\nCorrelatie tussen consumentenbestedingen en inflatie:")
print(correlatie)

# 6. Plot de relatie tussen inflatie en consumentenbestedingen
plt.figure(figsize=(8,5))
plt.scatter(df_merged['Value_y'], df_merged['Value_x'])
plt.title('Relatie tussen Consumentenbestedingen en Inflatie')
plt.xlabel('Inflatie (%)')
plt.ylabel('Consumentenbestedingen (in miljoenen euro)')
plt.grid(True)
plt.show()
