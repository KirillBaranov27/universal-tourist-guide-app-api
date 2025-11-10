import psycopg2
from app.core.config import settings

try:
    conn = psycopg2.connect(
        host=settings.POSTGRES_SERVER,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        port=settings.POSTGRES_PORT
    )
    print("✅ УСПЕХ: Подключение к PostgreSQL установлено!")
    print(f"✅ База данных: {settings.POSTGRES_DB}")
    
    # Проверим таблицы
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    print(f"✅ Таблицы в базе: {[table[0] for table in tables]}")
    
    conn.close()
except Exception as e:
    print(f"❌ ОШИБКА: {e}")