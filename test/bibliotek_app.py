import sqlite3
import os

DB_NAME = 'library.db'

with sqlite3.connect(DB_NAME) as conn:
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        available INTEGER CHECK(available in (0,1)) DEFAULT 1
    );""")


def add_book(title: str, author: str, year: int, available=1):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title,author,year,available) VALUES(?,?,?,?)",
                       (title, author, year, available))
        conn.commit()
        print("Book is added")


def show_all_books():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        return cursor.execute("SELECT * FROM books").fetchall()


def show_available_books():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        return cursor.execute("SELECT * FROM books WHERE available = 1").fetchall()


def change_available_books(book_id, available):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        if not row:
            raise Bookidforchenge("Книги с таким id нет!")
        if row[0] == available:
            raise Bookchangeavailb("Статус книги уже такой же!")
        cursor.execute(
            "UPDATE books SET available = ? WHERE id = ?", (available, book_id))
        conn.commit()
        print("Status is changed")


def delete_book(book_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        if not cursor.fetchone():
            raise Bookidiszero("Такой книги нет в библиотеке!")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class Bookidiszero(Exception):
    pass


class Bookidforchenge(Exception):
    pass


class Bookchangeavailb(Exception):
    pass


while True:
    try:
        print("""
            PROGRAMM BOOKS LIBARY!
            1.Add book
            2.Show all books
            3.Show available books
            4.Change available books
            5.Delete book
            0.Exit
    """)
        try:
            i_a = int(input("Enter your action: "))
            if i_a > 5 or i_a < 0:
                raise ValueError
        except ValueError:
            print("Action must be a number!!!")
            continue
        if i_a == 1:
            try:
                print("(Enter'Q/q' if you want to exit)")
                title = str(input("Enter title: "))
                if (title == "Q") or (title == "q"):
                    print("Exit from 'Add book'")
                    continue
                author = str(input("Enter author: "))
                if (author == "Q") or (author == "q"):
                    print("Exit from 'Add book'")
                    continue
                year = int(input("Enter year: "))
                add_book(title=title, author=author, year=year)
            except ValueError as ve:
                print(ve)
        elif i_a == 2:
            print("All books:")
            for book in show_all_books():
                print(
                    f"ID: {book[0]} | {book[1]} by {book[2]} ({book[3]}) | Available: {'✔' if book[4] else '✘'}")
        elif i_a == 3:
            show_available_books()
            print("Available books:")
            for book in show_available_books():
                print(book)
        elif i_a == 4:
            try:
                input_chage_available = int(
                    input("Enter number '1' = available, '0' = not available: "))
                if (input_chage_available < 0) or (input_chage_available > 1):
                    raise Bookchangeavailb("The number must be '1' or '0'")
                if input_chage_available > 1 or input_chage_available < 0:
                    raise ValueError
                input_book_id = int(
                    input("Enter the id of book wich you want to change: "))
                if input_book_id <= 0:
                    raise Bookidiszero(
                        "Id below zero can't be used!!!")
                change_available_books(
                    book_id=input_book_id, available=input_chage_available)
            except ValueError as ve:
                print("Inpoted must be 'number'!!!")
            except Bookidiszero as be:
                print(be)
            except Bookidforchenge as bfc:
                print(bfc)
            except Bookchangeavailb as bca:
                print(bca)
        elif i_a == 5:
            try:
                input_delete_book = int(input(
                    "Enter the id of book wich you want to delete: "))
                delete_book(input_delete_book)
            except Bookidiszero as biz:
                print(biz)
            except ValueError:
                print("Inpoted must be 'number'!!!")
        elif i_a == 0:
            print("BYE!!!")
            clear_console()
            exit()
    except KeyboardInterrupt:
        print()
        print("Exit with Ctrl+C")
        exit()
