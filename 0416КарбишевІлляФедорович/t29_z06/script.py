"""
T29.6 Скласти програму для роботи з базою даних, що містить інформацію
про власний сад. У БД зберігається інформація про рід дерев (яблуня, груша
тощо), сорт дерев, рік посадки, неформальне місце посадки. Для кожного
дерева зберігають також врожай по роках. Реалізувати функції додавання
роду дерев, додавання сорту, додавання дерева, додавання врожаю за заданий
рік, повернення інформації про всі дерева даного роду та про врожай
заданого дерева за заданий період років.

Рід_дерев
    Id_Код_роду
    Найменування_роду
Сорт_дерев
    Id_сорту_дерева
    Найменування_сорту
Дерева
    Id_дерева
    Id_Код_роду
    Id_сорту_дерева
Сад
    Id_дерева
    Рік_посадки
    Місце_посадки
Врожай
    Id_дерева
    Рік
    Врожай
"""

import sqlite3

DB_NAME = "garden.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS Harvest')
        cursor.execute('DROP TABLE IF EXISTS Garden')
        cursor.execute('DROP TABLE IF EXISTS Trees')
        cursor.execute('DROP TABLE IF EXISTS TreeSorts')
        cursor.execute('DROP TABLE IF EXISTS TreeSpecies')

        cursor.execute('''
            CREATE TABLE TreeSpecies (
                species_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE TreeSorts (
                sort_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE Trees (
                tree_id INTEGER PRIMARY KEY AUTOINCREMENT,
                species_id INTEGER,
                sort_id INTEGER,
                FOREIGN KEY (species_id) REFERENCES TreeSpecies(species_id),
                FOREIGN KEY (sort_id) REFERENCES TreeSorts(sort_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE Garden (
                tree_id INTEGER PRIMARY KEY,
                year_planted INTEGER,
                location TEXT,
                FOREIGN KEY (tree_id) REFERENCES Trees(tree_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE Harvest (
                tree_id INTEGER,
                year INTEGER,
                harvest_amount REAL,
                PRIMARY KEY (tree_id, year),
                FOREIGN KEY (tree_id) REFERENCES Trees(tree_id)
            )
        ''')

def add_species():
    name = input("Назва роду дерев: ")
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO TreeSpecies (name) VALUES (?)", (name,))
    print("Рід дерев додано.")

def add_sort():
    name = input("Назва сорту: ")
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO TreeSorts (name) VALUES (?)", (name,))
    print("Сорт дерев додано.")

def add_tree():
    species_id = int(input("ID роду дерев: "))
    sort_id = int(input("ID сорту дерев: "))
    year_planted = int(input("Рік посадки: "))
    location = input("Місце посадки: ")

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Trees (species_id, sort_id) VALUES (?, ?)", (species_id, sort_id))
        tree_id = cursor.lastrowid
        cursor.execute("INSERT INTO Garden (tree_id, year_planted, location) VALUES (?, ?, ?)",
                       (tree_id, year_planted, location))
    print(f"Дерево додано (ID: {tree_id}).")

def add_harvest():
    tree_id = int(input("ID дерева: "))
    year = int(input("Рік врожаю: "))
    harvest_amount = float(input("Врожай (кг): "))
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            INSERT OR REPLACE INTO Harvest (tree_id, year, harvest_amount)
            VALUES (?, ?, ?)
        ''', (tree_id, year, harvest_amount))
    print("Врожай додано.")

def list_trees_by_species():
    species_id = int(input("ID роду дерев: "))
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.tree_id, s.name, so.name, g.year_planted, g.location
            FROM Trees t
            JOIN TreeSpecies s ON t.species_id = s.species_id
            JOIN TreeSorts so ON t.sort_id = so.sort_id
            JOIN Garden g ON g.tree_id = t.tree_id
            WHERE t.species_id = ?
        ''', (species_id,))
        rows = cursor.fetchall()
        if rows:
            for r in rows:
                print(f"ID дерева: {r[0]}, Рід: {r[1]}, Сорт: {r[2]}, Посаджене: {r[3]}, Місце: {r[4]}")
        else:
            print("Дерев цього роду не знайдено.")

def show_harvest_by_years():
    tree_id = int(input("ID дерева: "))
    start_year = int(input("Початковий рік: "))
    end_year = int(input("Кінцевий рік: "))

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT year, harvest_amount
            FROM Harvest
            WHERE tree_id = ? AND year BETWEEN ? AND ?
            ORDER BY year
        ''', (tree_id, start_year, end_year))
        rows = cursor.fetchall()
        if rows:
            for r in rows:
                print(f"Рік: {r[0]}, Врожай: {r[1]} кг")
        else:
            print("Даних про врожай не знайдено.")

def main():
    init_db()
    while True:
        print("\n🌳 Меню:")
        print("1. Додати рід дерев")
        print("2. Додати сорт дерев")
        print("3. Додати дерево")
        print("4. Додати врожай")
        print("5. Показати всі дерева за родом")
        print("6. Показати врожай за період років")
        print("0. Вийти")
        choice = input("Ваш вибір: ")

        if choice == '1':
            add_species()
        elif choice == '2':
            add_sort()
        elif choice == '3':
            add_tree()
        elif choice == '4':
            add_harvest()
        elif choice == '5':
            list_trees_by_species()
        elif choice == '6':
            show_harvest_by_years()
        elif choice == '0':
            break
        else:
            print("Невірний вибір.")

if __name__ == '__main__':
    main()
