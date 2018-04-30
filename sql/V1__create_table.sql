CREATE TABLE IF NOT EXISTS bankTransactions (
  id INTEGER PRIMARY KEY NOT NULL
  ,rowCreated DATETIME NOT NULL
  ,rowUpdated DATETIME NOT NULL
  ,processedDate DATETIME
  ,transactionDate DATETIME
  ,bankUniqueId INTEGER
  ,transactionType VARCHAR(30)
  ,transactionReference INTEGER
  ,transactionDescription TEXT
  ,transactionAmount REAL
);
