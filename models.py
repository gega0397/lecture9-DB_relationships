from queries import QUERIES


# todo: get many Books and  Authors from the database
# todo: modify or add author to a book


class Books:
    def __init__(self, book_name, book_length, book_genre, book_cover, *,
                 book_id=None, authors=None, con=None):
        self.id = book_id
        self.name = book_name
        self.length = book_length
        self.genre = book_genre
        self.cover = book_cover
        self.authors = [] if authors is None else authors
        self.con = con

    def create(self):
        cur = self.con.cursor()
        cur.execute(QUERIES["books"]["insert"], (self.name, self.length, self.genre, self.cover))
        self.id = cur.lastrowid
        if self.authors:
            cur.executemany(QUERIES["book_authors"]["insert"],
                            [(self.id, author.id) for author in self.authors])
        self.con.commit()
        cur.close()
        return self

    def __repr__(self):
        return (f"{self.name} - {self.genre} - {self.cover} - "
                f"{[f'{author.first_name} {author.last_name}' for author in self.authors]}")

    @classmethod
    def get_book(cls, con, where=None):
        cur = con.cursor()
        cur.execute(QUERIES["books"]["select"](where=where))
        res = cur.fetchone()
        if res is None:
            return None
        book = Books(res[1], res[2], res[3], res[4],
                     book_id=res[0],
                     con=con)
        book.get_authors()
        cur.close()
        return book

    def get_authors(self):
        cur = self.con.cursor()
        cur.execute(QUERIES["book_authors"]["select"](
            cols=['authors.id', 'authors.first_name', 'authors.last_name'],
            where={"book_id": self.id})
        )
        authors = cur.fetchall()
        self.authors = [Authors(first_name=author[1],
                                last_name=author[2],
                                author_id=author[0],
                                con=self.con
                                )
                        for author in authors]
        cur.close()
        return self

    def add_author(self, other):
        cur = self.con.cursor()
        if isinstance(other, Authors):
            cur.execute(QUERIES["book_authors"]["insert"], (self.id, other.id))
        elif isinstance(other, int):
            other = Authors.get_author(self.con, where={"id": other})
            if other:
                cur.execute(QUERIES["book_authors"]["insert"], (self.id, other.id))
        elif isinstance(other, list):
            cur.executemany(QUERIES["book_authors"]["insert"], [(self.id, author.id) if isinstance(author, Authors) else
                                                                (self.id, author) for author in other])
        self.con.commit()
        cur.close()
        return self


class Authors:
    def __init__(self, first_name, last_name, *,
                 author_id=None, books=None, con=None):
        self.id = author_id
        self.first_name = first_name
        self.last_name = last_name
        self.books = [] if books is None else books
        self.con = con

    def create(self):
        cur = self.con.cursor()
        cur.execute(QUERIES["authors"]["insert"], (self.first_name, self.last_name))
        self.id = cur.lastrowid
        if self.books:
            cur.executemany(QUERIES["book_authors"]["insert"], [(book.id, self.id) for book in self.books])
        self.con.commit()
        cur.close()
        return self

    @classmethod
    def get_author(cls, con, where=None):
        cur = con.cursor()
        cur.execute(QUERIES["authors"]["select"](where=where))
        res = cur.fetchone()
        if res is None:
            return None
        author = Authors(res[1], res[2], author_id=res[0],
                         con=con)
        author.get_books()
        cur.close()
        return author

    def get_books(self):
        cur = self.con.cursor()
        cur.execute(QUERIES["book_authors"]["select"](
            cols=['books.name', 'books.id', 'books.length', 'books.genre', 'books.cover'],
            where={"author_id": self.id})
        )
        books = cur.fetchall()
        self.books = [Books(book_name=book[0],
                            book_id=book[1],
                            book_length=book[2],
                            book_genre=book[3],
                            book_cover=book[4],
                            con=self.con
                            )
                      for book in books]
        cur.close()
        return self

    def add_book(self, other):
        cur = self.con.cursor()
        if isinstance(other, Books):
            cur.execute(QUERIES["book_authors"]["insert"], (other.id, self.id))
        elif isinstance(other, int):
            other = Books.get_book(self.con, where={"id": other})
            if other:
                cur.execute(QUERIES["book_authors"]["insert"], (other, self.id))
        elif isinstance(other, list):
            cur.executemany(QUERIES["book_authors"]["insert"], [(book.id, self.id) if isinstance(book, Books) else
                                                                (book, self.id) for book in other])
        self.con.commit()
        cur.close()
        return self

    def __repr__(self):
        return f"{self.id} - {self.first_name} {self.last_name} - {[book.name for book in self.books]}"
