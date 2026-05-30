import pyodbc

server = "localhost\\SQLEXPRESS"
database = "nyc_taxi_pipeline"

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

print("Trying to connect...")

try:
    conn = pyodbc.connect(conn_str)
    print("SUCCESS: Connected to SQL Server")
    conn.close()

except Exception as e:
    print("ERROR:", e)