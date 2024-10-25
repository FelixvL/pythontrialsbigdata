import os
import pandas as pd
import matplotlib.pyplot as plt
import re  # Voor het opschonen van de bestandsnaam

# 1. Laad het MeasureCodes.csv bestand
df_measure_codes = pd.read_csv('docs/MeasureCodes.csv', sep=";")

# 2. Laad de consumentenbestedingen gegevens
df_consumentenbestedingen = pd.read_csv('docs/consumentenbestedingen.csv', sep=";")

# Zet de 'Value' kolom om naar numeriek (vervang komma door punt)
df_consumentenbestedingen['Value'] = df_consumentenbestedingen['Value'].str.replace(',', '.').astype(float)

# 3. Koppel de Measure codes aan de consumentenbestedingen dataset
df_consumentenbestedingen = df_consumentenbestedingen.merge(df_measure_codes[['Identifier', 'Title']], 
                                                            left_on='Measure', right_on='Identifier')

# 4. Laad de periodecodes om leesbare jaartallen toe te voegen
df_perioden = pd.read_csv('docs/periodecodes.csv', sep=";")

# Koppel de consumentenbestedingen met de periodecodes op basis van 'Perioden' en 'Identifier'
df_consumentenbestedingen_grouped = df_consumentenbestedingen.merge(df_perioden[['Identifier', 'Title']], left_on='Perioden', right_on='Identifier')

# 5. Laad de inflatiegegevens
df_inflatie = pd.read_csv('docs/inflatie.csv', sep=";")

# Vervang komma's door punten en zet de Value-kolom om naar numeriek
df_inflatie['Value'] = df_inflatie['Value'].str.replace(',', '.').astype(float)

# Extracteer het jaar uit de 'Perioden' kolom (bijv. 1963MM01 -> 1963)
df_inflatie['Jaar'] = df_inflatie['Perioden'].str[:4]

# Bereken de gemiddelde inflatie per jaar
df_inflatie_yearly = df_inflatie.groupby('Jaar')['Value'].mean().reset_index()

# Gebruik nu de juiste kolom om te mergen, in dit geval Title_y (controleer of het jaar in Title_x of Title_y zit)
df_merged = df_consumentenbestedingen_grouped.merge(df_inflatie_yearly, left_on='Title_y', right_on='Jaar')

# 6. Groepeer de data per sector en per jaar
df_sectoral = df_merged.groupby(['Title_x', 'Jaar'])[['Value_x', 'Value_y']].sum().reset_index()

# Maak een map voor de PNG-bestanden als die nog niet bestaat
os.makedirs("plots", exist_ok=True)

# Correlatieanalyse per sector en sla op als PNG
sectors = df_sectoral['Title_x'].unique()

for sector in sectors:
    # Maak de bestandsnaam schoon door ongewenste tekens te vervangen
    safe_sector_name = re.sub(r'[<>:"/\\|?*]', '_', sector)
    
    df_sector = df_sectoral[df_sectoral['Title_x'] == sector]
    correlatie = df_sector[['Value_x', 'Value_y']].corr()
    print(f"\nCorrelatie voor {sector}:")
    print(correlatie)

    # Scatterplot voor deze sector
    plt.figure(figsize=(8,5))
    plt.scatter(df_sector['Value_y'], df_sector['Value_x'])
    plt.title(f'Relatie tussen Consumentenbestedingen en Inflatie ({sector})')
    plt.xlabel('Inflatie (%)')
    plt.ylabel('Consumentenbestedingen (in miljoenen euro)')
    plt.grid(True)

    # Sla elke grafiek op als PNG-bestand in de 'plots' map
    plt.savefig(f"plots/{safe_sector_name}.png")
    plt.close()  # Sluit de figuur om geheugen te besparen

print("Alle grafieken zijn opgeslagen in de 'plots' map.")
