import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

# URL of the archived webpage
url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'

# Output file/database paths
db_name = 'Movies.db'
table_name = 'Top_25'
csv_path = '/home/project/top_25_films.csv'

# Download and parse the webpage
html_page = requests.get(url).text
soup = BeautifulSoup(html_page, 'html.parser')

# Find the first table of film rankings
table = soup.find('tbody')
rows = table.find_all('tr')

# List to store film data
film_data = []

# Extract top 25 films
for row in rows:
    cols = row.find_all('td')
    if len(cols) >= 4:
        film_info = {
            "Average Rank": cols[0].get_text(strip=True),
            "Film": cols[1].get_text(strip=True),
            "Year": cols[2].get_text(strip=True),
            "Rotten Tomatoes' Top 100": cols[3].get_text(strip=True)
        }
        film_data.append(film_info)
        if len(film_data) == 25:
            break

# Convert to DataFrame
df = pd.DataFrame(film_data)

# Convert Year to numeric to enable filtering
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Print Top 25 Films with Titles
print("=== Top 25 Films ===")
print(df[['Average Rank','Film', 'Year']])

# Filter films released in 2000s (2000–2009)
films_2000s = df[(df['Year'] >= 2000) & (df['Year'] <= 2009)]

# Print films released in the 2000s
print("\n=== Films Released in the 2000s ===")
print(films_2000s[['Average Rank','Film', 'Year']])

# Save to CSV and SQLite (optional)
df.to_csv(csv_path, index=False)
conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()
