import random
import sqlite3
import models
import queries


def main(con):
    books = []
    authors = []

    for i in range(1, 6):
        author = models.Authors.get_author(con, where={"id": i})
        author.get_books()
        authors.append(author)

    for i in range(1, 6):
        book = models.Books.get_book(con, where={"id": i})
        book.get_authors()
        books.append(book)

    for book in books:
        print(book)

    for author in authors:
        print(author)

    con.close()


def create_tables(con):
    cur = con.cursor()
    cur.execute(queries.QUERIES["books"]["create"])
    cur.execute(queries.QUERIES["authors"]["create"])
    cur.execute(queries.QUERIES["book_authors"]["create"])
    con.commit()
    cur.close()


def insert_data(con):
    authors = []
    books = []
    for i in range(1, 10):
        author = models.Authors(f"Author {i}", f"Last Name {i}", con=con)
        author.create()
        authors.append(author)

    for i in range(1, 10):
        book = models.Books(
            f"Book {i}", random.randint(100, 500), random.choice(queries.GENRE), random.choice(queries.COVER),
            con=con)
        book.create()
        books.append(book)

    cur = con.cursor()

    pairs = {(random.randint(1, 10), random.randint(1, 10)) for _ in range(10)}
    print(pairs)
    cur.executemany(queries.QUERIES['book_authors']['insert'], pairs)

    con.commit()
    cur.close()


if __name__ == '__main__':
    con = sqlite3.connect('books.db')
    #create_tables(con)
    #insert_data(con)
    main(con)
