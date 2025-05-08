import requests
import mysql.connector
from datetime import datetime, timedelta

def fetch_federal_data():
    today = datetime.today().date()
    last_week = today - timedelta(days=7)
    
    url = f"https://www.federalregister.gov/api/v1/documents.json?per_page=100&order=newest&conditions[publication_date][gte]={last_week}&conditions[publication_date][lte]={today}"
    response = requests.get(url)
    data = response.json()["results"]
    return data

def store_data_to_mysql(data):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="User@189",
        database="federal_data"
    )
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title TEXT,
        document_type VARCHAR(255),
        publication_date DATE
    )
    """)

    for doc in data:
        cursor.execute("""
            INSERT INTO documents (title, document_type, publication_date)
            VALUES (%s, %s, %s)
        """, (
            doc.get("title"),
            doc.get("document_type"),
            doc.get("publication_date")
        ))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    data = fetch_federal_data()
    store_data_to_mysql(data)
