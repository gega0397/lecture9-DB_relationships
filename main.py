import random
import sqlite3
import models
import queries

con = sqlite3.connect("tutorial.db")

books = []
authors = []

for i in range(1, 6):
    author = models.Authors.get_author(i, con)
    author.get_books()
    authors.append(author)

for i in range(1, 6):
    book = models.Books.get_book(i, con)
    book.get_authors()
    books.append(book)

for book in books:
    print(book)

for author in authors:
    print(author)

con.close()

# cur.execute(queries.QUERIES["books"]["create"])
# cur.execute(queries.QUERIES["authors"]["create"])
# cur.execute(queries.QUERIES["book_authors"]["create"])
#
# con.commit()
#
# authors = []
# books = []
# for i in range(1, 6):
#     author = models.Authors(f"Author {i}", f"Last Name {i}", con=con, cur=cur)
#     author.create()
#     authors.append(author)
#
# for i in range(1, 6):
#     book = models.Books(
#         f"Book {i}", random.randint(100, 500), random.choice(queries.GENRE), random.choice(queries.COVER),
#         con=con, cur=cur)
#     book.create()
#     books.append(book)
#
# cur.execute(queries.QUERIES['book_authors']['insert'], (books[0].id, authors[0].id))
# cur.execute(queries.QUERIES['book_authors']['insert'], (books[0].id, authors[2].id))
# cur.execute(queries.QUERIES['book_authors']['insert'], (books[1].id, authors[2].id))
#
# con.commit()
