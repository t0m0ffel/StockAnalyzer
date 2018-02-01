import datetime as dt
from datetime import date

import pandas_datareader as pdr
from matplotlib import style

from db_config import database_connection, clear_stock_quotes_table

style.use('ggplot')

first = dt.datetime(2017, 1, 30)
second = date.today()

cursor = database_connection.cursor()
cursor.execute("SELECT symbol FROM stock")
symbols = set([str(x[0]) for x in cursor.fetchall()])

clear_stock_quotes_table()
for symbol in symbols:
    cur = database_connection.cursor()
    try:
        df = pdr.get_data_google('AAPL', start=first, end=second)

        for index, row in df.iterrows():
            cur.execute("INSERT INTO stock_quotes (symbol, open, close, high, low,date) VALUES (%s,%s,%s,%s,%s,%s)",
                        (symbol, row['Open'], row['Close'], row['High'], row['Low'], index))
            database_connection.commit()


    except:
        cur.execute("DELETE FROM stock WHERE symbol = %s", (symbol,))
