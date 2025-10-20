# backend/test_db.py
import psycopg2
from decouple import config

try:
    conn = psycopg2.connect(
        dbname=config('DATABASE_NAME'),
        user=config('DATABASE_USER'),
        password=config('DATABASE_PASSWORD'),
        host=config('DATABASE_HOST'),
        port=config('DATABASE_PORT'),
        options='-c client_encoding=UTF8'
    )
    print("✅ Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"❌ Erro: {e}")