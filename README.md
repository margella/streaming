**Описание пайплайна:**

    1. Producer читает данные из таблицы user_logins в PostgreSQL
    2. Producer отправляет события в топик Kafka и использует флаг sent_to_kafka для предотвращения отправки дубликатов
    3. Consumer читает сообщения из Kafka
    4. Consumer отправляет данные для сохранения в ClickHouse

**Архитектура пайплайна:**

PostgreSQL (таблица user_logins) → Producer → Kafka Topic → Consumer → ClickHouse
    
**Как запустить пайплайн:**

    1. Запустить контейнеры в Докере (файл docker-compose; команда в терминале - docker-compose up -d)
    2. Запустить файлы producer.py и consumer.py последовательно в виртуальном окружении
        команды в терминале:
            1. .venv\Scriprs\activate
            2. python producer.py
                Проследить, как отправляются сообщения и в БД проставляется значение True для поля sent_to_kafka
                Для просмотра таблицы в БД подключиться к PGSQL через dbeaver по кредам из docker-compose.yml
            3. python consumer.py
                Проследить, как консьюмер обрабатывает сообщения
                Для просмотра вставки данных в таблицу в Кликхаусе подключиться через dbeaver по кредам из docker-compose.yml
