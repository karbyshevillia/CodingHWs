"""
T29.5 Скласти програму для роботи з базою даних, що містить інформацію
про постачальників товару. Для кожного постачальника вказано його назву та
контактні дані. У окремих таблицях БД зберігаються дані про товари а також
дані про постачальників товарів. Реалізувати функції додавання
постачальника, додавання товару, фіксації факту, що постачальник постачає
певний товар а також пошуку за назвою товару усіх постачальників, що
постачають товар та пошуку за назвою постачальника усіх товарів, що
постачає постачальник.

Товар
    Id_Код_товару
    Найменування_товару
Постачальник
    Id_Код_постачальника
    Назва_ постачальника
    Контактні_дані_постачальника
Поставка_товарів
    Id_Код_постачальника
    Id_Код_товару
    Кількість_одиниць_товару
    Загальна_ціна
"""

import sqlite3

DB_NAME = 'suppliers.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Suppliers (
                supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Supplies (
                supplier_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                total_price REAL,
                PRIMARY KEY (supplier_id, product_id),
                FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id),
                FOREIGN KEY (product_id) REFERENCES Products(product_id)
            )
        ''')

def add_supplier():
    name = input("Назва постачальника: ")
    contact = input("Контактні дані: ")
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO Suppliers (name, contact) VALUES (?, ?)", (name, contact))
    print("Постачальника додано.")

def add_product():
    name = input("Назва товару: ")
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO Products (name) VALUES (?)", (name,))
    print("Товар додано.")

def record_supply():
    supplier_id = int(input("ID постачальника: "))
    product_id = int(input("ID товару: "))
    quantity = int(input("Кількість одиниць: "))
    total_price = float(input("Загальна ціна: "))
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            INSERT OR REPLACE INTO Supplies (supplier_id, product_id, quantity, total_price)
            VALUES (?, ?, ?, ?)
        ''', (supplier_id, product_id, quantity, total_price))
    print("Поставку зафіксовано.")

def find_suppliers_by_product():
    product_name = input("Назва товару для пошуку постачальників: ")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.supplier_id, s.name, s.contact
            FROM Suppliers s
            JOIN Supplies sp ON s.supplier_id = sp.supplier_id
            JOIN Products p ON p.product_id = sp.product_id
            WHERE p.name LIKE ?
        ''', (f'%{product_name}%',))
        results = cursor.fetchall()
        if results:
            for r in results:
                print(f"ID: {r[0]}, Назва: {r[1]}, Контакт: {r[2]}")
        else:
            print("Постачальників не знайдено.")

def find_products_by_supplier():
    supplier_name = input("Назва постачальника для пошуку товарів: ")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.product_id, p.name
            FROM Products p
            JOIN Supplies sp ON p.product_id = sp.product_id
            JOIN Suppliers s ON s.supplier_id = sp.supplier_id
            WHERE s.name LIKE ?
        ''', (f'%{supplier_name}%',))
        results = cursor.fetchall()
        if results:
            for r in results:
                print(f"ID: {r[0]}, Назва товару: {r[1]}")
        else:
            print("Товарів не знайдено.")

def main():
    init_db()
    while True:
        print("\nМеню:")
        print("1. Додати постачальника")
        print("2. Додати товар")
        print("3. Зафіксувати поставку")
        print("4. Знайти постачальників за товаром")
        print("5. Знайти товари за постачальником")
        print("0. Вийти")

        choice = input("Ваш вибір: ")

        if choice == '1':
            add_supplier()
        elif choice == '2':
            add_product()
        elif choice == '3':
            record_supply()
        elif choice == '4':
            find_suppliers_by_product()
        elif choice == '5':
            find_products_by_supplier()
        elif choice == '0':
            break
        else:
            print("Невідомий вибір. Спробуйте ще.")

if __name__ == '__main__':
    main()
