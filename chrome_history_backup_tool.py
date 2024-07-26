import sqlite3
import pandas as pd
from datetime import datetime

# Path to your Chrome profile's History file
history_db = 'C:/Users/<Your Username>/AppData/Local/Google/Chrome/User Data/Default/History'

# Connect to the SQLite database
conn = sqlite3.connect(history_db)
conn.text_factory = lambda b: b.decode(errors='ignore')  # Decode bytes with errors ignored
cursor = conn.cursor()

# Query to extract history data
query = """
SELECT
    urls.url,
    urls.title,
    visits.visit_time / 1000000 - 11644473600 AS visit_time, -- Convert Chrome's microseconds since Windows epoch to Unix epoch
    datetime(visits.visit_time / 1000000 - 11644473600, 'unixepoch', 'localtime') AS visit_datetime
FROM
    urls
JOIN
    visits ON urls.id = visits.url
ORDER BY
    visit_time DESC
"""

# Execute the query and fetch data
cursor.execute(query)
rows = cursor.fetchall()

# Close the database connection
conn.close()

# Convert the data into a pandas DataFrame
df = pd.DataFrame(rows, columns=['URL', 'Title', 'Visit Timestamp', 'Visit Datetime'])

# Save the DataFrame to a CSV file (UTF-8 format)
df.to_csv('chrome_history_backup.csv', index=False, encoding='utf-8-sig')

print("Backup completed successfully.")
