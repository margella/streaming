# producer_pg_to_kafka.py
import psycopg2
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

conn = psycopg2.connect(
    dbname="test_db", user="admin", password="admin", host="localhost", port=5433

)
cursor = conn.cursor()
"""
Предварительно добавить поле sent_to_kafka в таблицу user_logins:
    1. Выполнить команду в терминале docker exec -it kafka-postgres-1 psql -U admin -d test_db (войти в редактор PGSQL)
    2. Выполнить команду 
            ALTER TABLE user_logins ADD COLUMN IF NOT EXISTS sent_to_kafka BOOLEAN DEFAULT False;
"""
cursor.execute("SELECT id, username, event_type, extract(epoch FROM event_time) FROM user_logins WHERE sent_to_kafka = false OR sent_to_kafka IS NULL")
rows = cursor.fetchall()

for row in rows:
    record_id = row[0]
    data = {
        "user": row[1],
        "event": row[2],
        "timestamp": float(row[3])  # преобразуем Decimal → float
    }
    producer.send("user_events", value=data)
    print("Sent:", data)

    cursor.execute( """
        UPDATE user_logins
        SET sent_to_kafka = True
        WHERE id = %s 
        """, (record_id,))
    conn.commit()
    time.sleep(0.5)


