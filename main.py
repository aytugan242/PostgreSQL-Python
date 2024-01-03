import psycopg2

# Функция, создающая структуру БД (таблицы)
def create_db(conn):
    cur.execute("""
    DROP TABLE phones;
    DROP TABLE clients;
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL
        );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id),
        phone_number VARCHAR(20) NOT NULL
        );
        """)
    print("Таблицы: clients, phones успешно созданы")

# Функция, позволяющая добавить нового клиента
def add_client(conn, first_name, last_name, email, phones=None):
  cur.execute(
      'INSERT INTO clients (first_name, last_name, email) VALUES (%s,%s,%s) RETURNING *;'
      , (first_name, last_name, email))
  print(cur.fetchone())

# Функция, позволяющая добавить телефон для существующего клиента
def add_phone(conn, client_id, phone_number):
    cur.execute(
        'INSERT INTO phones (client_id, phone_number) VALUES (%s, %s) RETURNING *;'
        , (client_id, phone_number))
    print(cur.fetchone())

# Функция, позволяющая изменить данные о клиенте
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone_number=None):
    if first_name:
        cur.execute("UPDATE clients SET first_name = %s WHERE id = %s", (first_name, client_id))
        print(f'Внесены новые изменения о клиенте Имя: {first_name} ')
    if last_name:
        cur.execute("UPDATE clients SET last_name = %s WHERE id = %s", (last_name, client_id))
        print(f'Внесены новые изменения о клиенте Фамилия: {last_name}')
    if email:
        cur.execute("UPDATE clients SET email = %s WHERE id = %s", (email, client_id))
        print(f'Внесены новые изменения о клиенте Email: {email}')
    if phone_number:
        cur.execute("UPDATE phones SET phone_number = %s WHERE client_id = %s", (phone_number, client_id))
        print(f'Внесены новые изменения о клиенте Телефон: {phone_number}')

# Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(conn, client_id, phone_number):
    cur.execute(
        'DELETE FROM phones WHERE client_id = %s AND phone_number = %s;'
        , (client_id, phone_number))
    print(f'Удален телефон - {phone_number} с client_id - {client_id}\n')

# Функция, позволяющая удалить существующего клиента
def delete_client(conn, client_id):
    cur.execute(
        'DELETE FROM phones WHERE client_id = %s;'
        'DELETE FROM clients WHERE id = %s;'
        , (client_id, client_id))
    print(f'Удаление клиента с client_id: {client_id}')

# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону
def find_client(conn, first_name=None, last_name=None, email=None, phone_number=None):
    print('\nПоиск ...')
    if first_name:
        cur.execute("SELECT * FROM clients JOIN phones ON clients.id = phones.client_id WHERE clients.first_name = %s", (first_name,))
        print(cur.fetchone())
    if last_name:
        cur.execute("SELECT * FROM clients JOIN phones ON clients.id = phones.client_id WHERE clients.last_name = %s", (last_name,))
        print(cur.fetchone())
    if email:
        cur.execute("SELECT * FROM clients JOIN phones ON clients.id = phones.client_id WHERE clients.email = %s", (email,))
        print(cur.fetchone())
    if phone_number:
        cur.execute("SELECT * FROM clients JOIN phones ON clients.id = phones.client_id WHERE clients.phone_number = %s", (phone_number,))
        print(cur.fetchone())

with psycopg2.connect(database="netology_bd", user="postgres", password="admin") as conn:
    with conn.cursor() as cur:
        create_db(conn)
        add_client(conn, 'Иван', 'Иванов', 'ivan@yandex.ru', phones=None)
        add_phone(conn, 1, '+79178747865')
        add_client(conn, 'Марат', 'Ибрагимов', 'marat@yandex.ru', phones=None)
        add_phone(conn, 2, '+79275555555')

        change_client(conn, 1, first_name = 'Вася', last_name = 'Петров', email = 'vasya@yandex.ru', phone_number = '+79178747888')
        delete_phone(conn, 1, '+79178747888')

        add_client(conn, 'Максим', 'Максимов', 'maks@yandex.ru', phones=None)
        add_phone(conn, 3, '+79198747885')
        delete_client(conn, 3)

        find_client(conn, first_name='Марат')

conn.close()


