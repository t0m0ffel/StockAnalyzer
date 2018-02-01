import psycopg2

STD_USER = 'postgres'
STD_PASSWORD = 'postgres'
STD_HOST = 'localhost'
STD_DB_NAME = 'stocks'

database_connection = psycopg2.connect(
    "dbname='" + STD_DB_NAME + "' user='" + STD_USER + "' host='" + STD_HOST + "' password='" + STD_PASSWORD + "'")
