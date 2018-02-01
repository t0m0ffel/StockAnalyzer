import string
import urllib.request as ur
import threading

from bs4 import BeautifulSoup

from db_config import database_connection

cursor = database_connection.cursor()
cursor.execute("SELECT symbol FROM stocks WHERE company_name IS NULL OR stock_market_code IS NULL")

incomplete_symbols = set([str(x[0]) for x in cursor.fetchall()])
cursor.execute("SELECT symbol FROM stocks")
existing_symbols = set([str(x[0]) for x in cursor.fetchall()])
print(len(existing_symbols))


class GrabSymbolPage(threading.Thread):
    def __init__(self, character, stock_market_code):
        threading.Thread.__init__(self)
        self.stock_market_code = stock_market_code
        self.character = character

    def run(self):
        html = ur.urlopen(
            "http://eoddata.com/stocklist/{}/{}.htm".format(self.stock_market_code, self.character)).read()
        soup = BeautifulSoup(html, "html.parser")

        quotes_table = soup.find("table", {"class": "quotes"})

        for row in quotes_table.findAll('tr'):
            col = row.findAll('td')
            if len(col) > 1:
                symbol = col[0].string
                company = col[1].string

                cur = database_connection.cursor()

                if symbol in existing_symbols:
                    if symbol in incomplete_symbols:
                        cur.execute("UPDATE stocks SET company_name= %s,stock_market_code= %s WHERE symbol=%s",
                                    (company, self.stock_market_code, symbol))

                        database_connection.commit()

                else:
                    try:
                        cur.execute("INSERT INTO stocks (symbol, company_name, stock_market_code) VALUES (%s,%s,%s)",
                                    (symbol, company, self.stock_market_code))

                        database_connection.commit()
                    except:
                        print(symbol, company, self.stock_market_code)


def main():
    max_threads = 200

    threads = []

    html = ur.urlopen("http://eoddata.com/symbols.aspx").read()
    soup = BeautifulSoup(html, "html.parser")

    select = soup.find("select")
    stock_market_codes = []
    for option in select.findAll('option'):
        stock_market_codes.append(option['value'])

    iterations = len(stock_market_codes) * len(string.ascii_uppercase)
    iteration = 0
    for stock_market_code in stock_market_codes:
        for character in string.ascii_uppercase:
            iteration += 1
            if iterations % 100:
                print(iteration, 'of', iterations)

            thread = GrabSymbolPage(character, stock_market_code)
            thread.start()
            threads.append(thread)
            if len(threads) >= max_threads:
                for thread in threads:
                    thread.join()


main()
