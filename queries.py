GENRE = ['Classic', 'Drama', 'Romance', 'Satire', 'Horror', 'Science']
COVER = ['Paperback', 'Hardcover']

GENRES = ", ".join(f"'{genre}'" for genre in GENRE)
COVERS = ", ".join(f"'{cover}'" for cover in COVER)

create_table_books = f'''CREATE TABLE IF NOT EXISTS books
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        length INTEGER,
                        genre TEXT CHECK (genre IN ({GENRES})),
                        cover TEXT CHECK (cover in  ({COVERS}))
                        )'''

create_table_authors = '''CREATE TABLE IF NOT EXISTS authors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL
                        )'''

create_table_books_authors = '''CREATE TABLE IF NOT EXISTS book_authors (
                        book_id INTEGER,
                        author_id INTEGER,
                        FOREIGN KEY (book_id) REFERENCES books(id),
                        FOREIGN KEY (author_id) REFERENCES authors(id),
                        PRIMARY KEY (book_id, author_id)
                        )'''

insert_books = "INSERT INTO books (name, length, genre, cover) VALUES (?, ?, ?, ?)"

insert_authors = "INSERT INTO authors (first_name, last_name) VALUES (?, ?)"

insert_book_authors = "INSERT INTO book_authors (book_id, author_id) VALUES (?, ?)"

get_average_length_books = "SELECT AVG(length) FROM books"

get_max_length = "SELECT name FROM books ORDER BY length DESC LIMIT 1"


def select_book(*, cols: list = None, where: dict = None):
    cols = cols or ['*']
    query = f"SELECT {', '.join(cols)} FROM books"
    if where:
        query += " WHERE " + " AND ".join([f"{key} = '{value}'" for key, value in where.items()])
    return query


def select_author(*, cols: list = None, where: dict = None):
    cols = cols or ['*']
    query = f"SELECT {', '.join(cols)} FROM authors"
    if where:
        query += " WHERE " + " AND ".join([f"{key} = '{value}'" for key, value in where.items()])
    return query


def select_book_author(*, cols: list = None, where: dict = None):
    cols = cols or ['*']
    query = f"SELECT {', '.join(cols)} FROM book_authors"

    query += " JOIN books ON book_authors.book_id = books.id"
    query += " JOIN authors ON book_authors.author_id = authors.id"

    if where:
        query += " WHERE " + " AND ".join([f"{key} = '{value}'" for key, value in where.items()])
    return query


QUERIES = {
    "books": {
        'create': create_table_books,
        'insert': insert_books,
        'get_average_length': get_average_length_books,
        'select': select_book,
    },

    "authors": {
        'create': create_table_authors,
        'insert': insert_authors,
        'select': select_author,
    },
    "book_authors": {
        'create': create_table_books_authors,
        'insert': insert_book_authors,
        'select': select_book_author,
    }
}
