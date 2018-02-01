CREATE TABLE stock
(
  id                SERIAL       NOT NULL
    CONSTRAINT stocks_pkey
    PRIMARY KEY,
  symbol            VARCHAR(255) NOT NULL,
  company_name      VARCHAR(255),
  stock_market_code VARCHAR(255) NOT NULL,
  openings          DOUBLE PRECISION [],
  CONSTRAINT stock_symbol_stock_market_code_key
  UNIQUE (symbol, stock_market_code)
);

CREATE UNIQUE INDEX stocks_id_uindex
  ON stock (id);

