CREATE TABLE stock_quotes
(
  symbol VARCHAR(255),
  date   DATE,
  open   DOUBLE PRECISION,
  close  DOUBLE PRECISION,
  high   DOUBLE PRECISION,
  low    DOUBLE PRECISION,
  UNIQUE (symbol, date)
);

