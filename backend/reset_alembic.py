import sqlite3
conn = sqlite3.connect("database/garden_manager.db")
conn.execute("UPDATE alembic_version SET version_num='339a4ae878d4'")
conn.commit()
conn.close()
print("Alembic reseteado a initial_schema")