import os
import psycopg2

# Параметры подключения к базе данных PostgreSQL
DB_NAME = "nginx_logs"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Подключение к базе данных
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Путь к директории с лог-файлами Nginx
log_dir = "/path/to/nginx/logs/"

# Чтение всех лог-файлов в директории
for filename in os.listdir(log_dir):
    if filename.endswith(".log"):
        with open(os.path.join(log_dir, filename), 'r') as file:
            for line in file:
                # Разбор строки лога и извлечение необходимых данных
                data = line.split()
                timestamp = data[3] + " " + data[4]
                remote_addr = data[0]
                request_method = data[5]
                request_uri = data[6]
                status_code = int(data[8])
                bytes_sent = int(data[9])

                # Вставка данных в базу данных
                cur.execute("INSERT INTO access_logs (timestamp, remote_addr, request_method, request_uri, status_code, bytes_sent) VALUES (%s, %s, %s, %s, %s, %s);",
                            (timestamp, remote_addr, request_method, request_uri, status_code, bytes_sent))
                conn.commit()

# Закрытие курсора и соединения с базой данных
cur.close()
conn.close()

print("Логи Nginx успешно перемещены в базу данных PostgreSQL.")

