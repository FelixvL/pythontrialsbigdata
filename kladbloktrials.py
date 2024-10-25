import pandas as pd
import matplotlib.pyplot as plt

# Het Observations.csv-bestand laden
df_observations = pd.read_csv('docs/Observations.csv', sep=";")

# Data opschonen: vervang komma's en zet om naar numeriek
df_observations['Value'] = df_observations['Value'].str.replace(',', '.').astype(float)

# Filter om alleen volledige jaren (bijv. 1996JJ00) te selecteren
df_observations_yearly = df_observations[df_observations['Perioden'].str.endswith('JJ00')]

# Groepeer de gegevens per jaar en sommeer de bestedingen
df_observations_grouped = df_observations_yearly.groupby('Perioden')['Value'].sum().reset_index()

# Voeg een leesbare tijdsperiode toe vanuit PeriodenCodes.csv
df_perioden = pd.read_csv('docs/PeriodenCodes.csv', sep=";")
df_observations_grouped = df_observations_grouped.merge(df_perioden[['Identifier', 'Title']], left_on='Perioden', right_on='Identifier')

# Plot de data
plt.figure(figsize=(10,6))
plt.plot(df_observations_grouped['Title'], df_observations_grouped['Value'], marker='o')
plt.title('Ontwikkeling van Consumentenbestedingen per Jaar')
plt.xlabel('Jaar')
plt.ylabel('Totale Bestedingen (in miljoenen euro)')

# Minder x-as ticks laten zien voor een betere leesbaarheid
plt.xticks(rotation=45, ticks=df_observations_grouped['Title'][::2])  # Om de labels elke 2 jaar te tonen
plt.grid(True)
plt.tight_layout()
plt.show()
