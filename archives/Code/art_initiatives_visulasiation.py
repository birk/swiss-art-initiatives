# This script fetches art initiative data from Wikidata, filters out records with both start and end dates,
# and generates a time series plot of the number of initiatives per year, saving the data and plot as files.

# Running the Python Script

# 1. Install Required Packages
# Before running the script, ensure you have the necessary Python packages installed.
# You can install them using pip. Open your terminal or command prompt and run:
# pip install SPARQLWrapper pandas matplotlib seaborn

# 2. Save the Python Script
# Copy the provided Python script into a file. For example, name the file fetch_and_plot.py.

# 3. Execute the Script
# Navigate to the directory where you saved fetch_and_plot.py using your terminal or command prompt.
# Run the script with:
# python fetch_and_plot.py

# 4. Check the Output
# - CSV File: The script will generate a file named projects.csv in the same directory where the script is located.
#   This CSV file contains the filtered data.
# - Plot Image: The script will also create a plot image named art_initiatives_plot.png, saved in the same directory.
#   This image shows a line plot of the number of art initiatives over the years.

# 5. Review the Results
# - CSV File: Open projects.csv with any text editor or spreadsheet application (like Excel or Google Sheets) to view the filtered data.
# - Plot Image: Open art_initiatives_plot.png with an image viewer to see the plot.


from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the SPARQL endpoint and query
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
query = """
SELECT ?item ?itemLabel ?start_date ?end_date
WHERE
{
  ?item wdt:P1343 wd:Q130250557.
  ?item wdt:P571 ?start_date.
  OPTIONAL { ?item wdt:P576 ?end_date. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
}
"""

# Set the query and return format
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

# Execute the query and fetch the results
results = sparql.query().convert()

# Convert results to a DataFrame
data = results['results']['bindings']
df = pd.json_normalize(data)

# Rename columns for convenience
df.rename(columns={
    'item.value': 'item',
    'itemLabel.value': 'label',
    'start_date.value': 'from_date',
    'end_date.value': 'to_date'
}, inplace=True)

# Save the DataFrame to a CSV file
df.to_csv('projects.csv', index=False)

# Handle Incomplete Dates
def parse_date(date_str):
    for fmt in ('%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d', '%Y-%m', '%Y'):
        try:
            return pd.to_datetime(date_str, format=fmt, errors='coerce')
        except ValueError:
            continue
    return pd.NaT

# Apply the parsing function
df['start_date'] = df['from_date'].apply(parse_date)
df['end_date'] = df['to_date'].apply(parse_date)

# Drop rows with missing start or end dates
df = df.dropna(subset=['start_date', 'end_date'])

# Feature Engineering
df['start_year'] = df['start_date'].dt.year

# Aggregate data by year (only considering start years)
annual_counts = df.groupby('start_year').size().reset_index(name='count')

# Create a time series
annual_counts.set_index('start_year', inplace=True)
ts_data = annual_counts['count']

# Enhanced Visualization with Seaborn
plt.figure(figsize=(14, 7))
sns.set(style="whitegrid")  # Set the background style
palette = sns.color_palette("crest", n_colors=1)  # Set a custom color palette

# Create the line plot with a label
sns.lineplot(x=ts_data.index, y=ts_data, label='Number of Initiatives', marker='o', color=palette[0], linewidth=2)

# Customize plot appearance
plt.xlabel('Year', fontsize=14, fontweight='bold')
plt.ylabel('Number of Initiatives', fontsize=14, fontweight='bold')
plt.title('Realtime Swiss Art Initiatives based on Wikidata', fontsize=16, fontweight='bold')
plt.legend(fontsize=12)  # Ensure the legend is included
plt.grid(True, linestyle='--', alpha=0.7)

# Add a background color to the plot area
plt.gca().set_facecolor('#f5f5f5')

# Save and show the plot
plt.tight_layout()
plt.savefig('art_initiatives_plot.png', dpi=300)  # Save the plot as a high-resolution image
plt.show()
