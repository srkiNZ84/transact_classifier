#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import sqlite3
import datetime
import logging
import os
import csv
import datetime

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

sqlite_file = 'transactionsDB.sqlite'
exportFiles = ['Export20171024213137.csv']

try:
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
except Exception as ex:
    logging.error('Something went wrong: ' + str(ex))

for exportFileName in exportFiles:
    headerSection = True
    with open(exportFileName) as exportFile:

        rowReader = csv.reader(exportFile)

        for row in rowReader:
            if len(row) == 0 and headerSection:
                logging.debug('Reached end of headers')
                headerSection = False
                continue
            elif headerSection:
                continue
            else:
                try:
                    c.execute("INSERT INTO `bankTransactions`( \
                            `rowCreated`,\
                            `rowUpdated`,\
                            `processedDate`,\
                            `transactionDate`,\
                            `bankUniqueId`,\
                            `transactionType`,\
                            `transactionReference`,\
                            `transactionDescription`,\
                            `transactionAmount`)\
                    VALUES (\
                        '" + str(datetime.datetime.now()) + "',\
                        '" + str(datetime.datetime.now()) + "',\
                        '"+ row[0] + "',\
                        '"+ row[1] + "',\
                        '"+ row[2] + "',\
                        '"+ row[3] + "',\
                        '"+ row[4] + "',\
                        '"+ row[5] + "',\
                        '"+ row[6] + "');")
                    conn.commit()
                except sqlite3.IntegrityError as ie:
                    logging.debug('Integrity error: ' + str(ie))
                    logging.debug('Assuming it is a duplicate')
                except Exception as ex:
                    logging.debug('Error inserting row into DB: ' + str(ex))

conn.close()

