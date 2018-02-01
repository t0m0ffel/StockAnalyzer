CREATE TABLE stocks
(
  id                SERIAL NOT NULL
    CONSTRAINT stocks_pkey
    PRIMARY KEY,
  symbol            VARCHAR(255),
  company_name      VARCHAR(255),
  stock_market_code VARCHAR(255)
);

CREATE UNIQUE INDEX stocks_id_uindex
  ON stocks (id);

