import psycopg2

conn = psycopg2.connect(
    host='localhost',
    password='pgijtsaMS',
    port=54320,
    dbname='harvestdb',
    user='postgres'
)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abcdef"))
cur.execute("SELECT * FROM test;")
result = cur.fetchone()
print(result)
conn.commit()
cur.close()
conn.close()