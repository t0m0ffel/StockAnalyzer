import psycopg2

STD_USER = 'postgres'
STD_PASSWORD = 'postgres'
STD_HOST = 'localhost'
STD_DB_NAME = 'stocks'

database_connection = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'"
                                       .format(STD_DB_NAME, STD_USER, STD_HOST, STD_PASSWORD))


def clear_stocks_table():
    database_connection.cursor().execute("DROP TABLE IF EXISTS  stock")
    with open('./tables/stock.sql', 'r') as SQLScript:
        database_connection.cursor().execute(SQLScript.read())
    database_connection.commit()


def clear_stock_quotes_table():
    database_connection.cursor().execute("DROP TABLE IF EXISTS  stock_quotes")
    with open('./tables/stock_quotes.sql', 'r') as SQLScript:
        database_connection.cursor().execute(SQLScript.read())
    database_connection.commit()
