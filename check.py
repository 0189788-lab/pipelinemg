import psycopg2, os
from dotenv import load_dotenv

load_dotenv('/app/.env')

try:
    conn = psycopg2.connect(
        user=os.getenv('SUPABASE_USER'),
        password=os.getenv('SUPABASE_PASSWORD'),
        host=os.getenv('SUPABASE_HOST'),
        port=os.getenv('SUPABASE_PORT'),
        dbname=os.getenv('SUPABASE_DBNAME')
    )
    cur = conn.cursor()

    print("--- Columnas de vw_cliente_genero ---")
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'vw_cliente_genero';")
    for row in cur.fetchall():
        print(row)

    print("--- Primeras 5 filas de vw_cliente_genero ---")
    cur.execute('SELECT * FROM vw_cliente_genero LIMIT 5;')
    for row in cur.fetchall():
        print(row)

except Exception as e:
    print("ERROR:", e)