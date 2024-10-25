import pandas as pd
import matplotlib.pyplot as plt

# Het Observations.csv-bestand laden
df_observations = pd.read_csv('docs/Observations.csv', sep=";")

# De eerste paar rijen van de data bekijken
print(df_observations.head())

# Informatie over de data weergeven (zoals kolommen, datatypes)
print(df_observations.info())

print("---")
df_perioden = pd.read_csv('docs/PeriodenCodes.csv', sep=";")

# De eerste paar rijen van de PeriodenCodes bekijken
print(df_perioden.head())

# Zorg ervoor dat de 'Value' kolom wordt omgezet naar een numeriek datatype (verwijder eerst de komma's)
df_observations['Value'] = df_observations['Value'].str.replace(',', '.').astype(float)

# Groepeer de gegevens per jaar en sommeer de bestedingen
df_observations_grouped = df_observations.groupby('Perioden')['Value'].sum().reset_index()

# Voeg een leesbare tijdsperiode toe vanuit PeriodenCodes.csv (gebruik de juiste kolomnaam 'Identifier' om te koppelen)
df_observations_grouped = df_observations_grouped.merge(df_perioden[['Identifier', 'Title']], left_on='Perioden', right_on='Identifier')

# Plot de data
plt.figure(figsize=(10,6))
plt.plot(df_observations_grouped['Title'], df_observations_grouped['Value'], marker='o')
plt.title('Ontwikkeling van Consumentenbestedingen per Jaar')
plt.xlabel('Jaar')
plt.ylabel('Totale Bestedingen (in miljoenen euro)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
