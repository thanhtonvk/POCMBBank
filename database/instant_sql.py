import sqlite3
def create_database():
    connection = sqlite3.connect('database/database.sqlite')
    connection.execute("""
                       create table Customer(
                           Id integer primary key autoincrement,
                           Name text,
                           PathFile text
                           )""")
    connection.execute("""
                       create table Signature(
                           Id integer primary key autoincrement,
                           IdCustomer integer not null,
                           PathSignature text,
                           Embedding text,
                           SignatureImage text
                       )
                       """)
    connection.commit()
    connection.close()