import sqlite3
import pandas as pd

# Path to the places.sqlite file in the Firefox profile
places_db = '/path/to/your/places.sqlite'

# Connect to the SQLite database
conn = sqlite3.connect(places_db)
conn.text_factory = lambda b: b.decode(errors='ignore')  # Decode bytes with errors ignored
cursor = conn.cursor()

# Query to extract history data
query = """
SELECT
    moz_places.url,
    moz_places.title,
    moz_historyvisits.visit_date / 1000000 AS visit_date, -- Firefox stores timestamps in microseconds
    datetime(moz_historyvisits.visit_date/1000000, 'unixepoch', 'localtime') AS visit_datetime
FROM
    moz_places
JOIN
    moz_historyvisits ON moz_places.id = moz_historyvisits.place_id
ORDER BY
    visit_date DESC
"""

# Execute the query and fetch data
cursor.execute(query)
rows = cursor.fetchall()

# Close the database connection
conn.close()

# Convert the data into a pandas DataFrame
df = pd.DataFrame(rows, columns=['URL', 'Title', 'Visit Timestamp', 'Visit Datetime'])

# Save the DataFrame to a CSV file (UTF-8 format)
df.to_csv('firefox_history_backup.csv', index=False, encoding='utf-8-sig')

print("Backup completed successfully.")
