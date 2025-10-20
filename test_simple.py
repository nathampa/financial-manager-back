# backend/test_simple.py
import sys
import os

# Força UTF-8 ANTES de importar psycopg2
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PGCLIENTENCODING'] = 'UTF8'
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'

print("Importando psycopg2...")

try:
    import psycopg2
    print("✅ psycopg2 importado com sucesso!")
    
    # Testa conexão MÍNIMA
    print("Tentando conectar...")
    
    conn = psycopg2.connect(
        "postgresql://postgres:12345678@127.0.0.1:5432/financial_manager"
    )
    
    print("✅ CONECTOU!")
    conn.close()
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()