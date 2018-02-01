import string
import threading
import urllib.request as ur

from bs4 import BeautifulSoup

from db_config import database_connection, clear_stocks_table


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
                try:
                    cur.execute("INSERT INTO stock (symbol, company_name, stock_market_code) VALUES (%s,%s,%s)",
                            (symbol, company, self.stock_market_code))
                except:
                    pass
                database_connection.commit()


def main():
    max_threads = 10

    threads = []

    html = ur.urlopen("http://eoddata.com/symbols.aspx").read()
    soup = BeautifulSoup(html, "html.parser")

    select = soup.find("select")
    stock_market_codes = []
    for option in select.findAll('option'):
        stock_market_codes.append(option['value'])

    print(stock_market_codes)
    characters = [*string.ascii_uppercase, *range(10)]
    iterations = len(stock_market_codes) * len(characters)
    iteration = 0
    for stock_market_code in stock_market_codes:
        for character in characters:
            iteration += 1
            print('Iteration', iteration, 'of', iterations)

            thread = GrabSymbolPage(character, stock_market_code)
            thread.start()
            threads.append(thread)
            if len(threads) >= max_threads:
                for thread in threads:
                    thread.join()

                threads = []
    if len(threads) > 0:
        for thread in threads:
            thread.join()

    print('Done')


clear_stocks_table()
main()
