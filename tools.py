# tools.py

import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables (DB credentials)
load_dotenv()

# Function to search documents by keyword from MySQL database
def search_documents(keyword):
    # Connect to MySQL database using environment variables
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = conn.cursor()

    # SQL query to search for keyword in title (case-insensitive, partial match)
    query = "SELECT title, publication_date FROM documents WHERE title LIKE %s LIMIT 5"
    cursor.execute(query, (f"%{keyword}%",))
    results = cursor.fetchall()

    # Clean up
    cursor.close()
    conn.close()

    # Format the result or return fallback
    if results:
        return "\n".join([f"{title} ({date})" for title, date in results])
    else:
        return "No documents found."
