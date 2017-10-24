#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import sys, os, pprint, shelve, csv, requests, json
import logging
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections

print("Welcome to the Transaction Classifier!")

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

databaseName = 'transactionData'
esHostname = 'http://192.168.99.100:9200'
esIndexName = 'transactions'

# Connect to ElasticSearch and make sure indexes are there
#createIndex = requests.put(esHostname + '/' + esIndexName )
#createIndex.raise_for_status()

if len(sys.argv) < 2:
    logging.error('Error: Need to specify file to load')
    logging.error('Usage: transaction_classifier.py [CSV file to load]')
    sys.exit()

fileToLoad = sys.argv[1]

# Load file
#print('CSV file to load: ' + fileToLoad)
try:
    logging.info('Loading file ' + fileToLoad)
    transactionFile = open(fileToLoad)
except FileNotFoundError:
    logging.error('Error loading file: File not found \'' + fileToLoad + '\'')
except:
    logging.error('Error loading file: ', sys.exc_info())

# Read in file contents
logging.info('Reading file contents')
fileLines = list(transactionFile)

# TODO: We might want to add a "format guesser" if we wanted to support other
# formats/banks in the future

# TODO: Need to skip the top metadata section and headers
# TODO: We might want to keep the metadata section for future reference
headersSection = True
categories = {}
classifications = {}
print('To finish classifying categories type \'end\'.')

# Load database file with existing list of transactions and
# classifications
try:
    #TODO: Put the categories in ElasticSearch as well
    logging.info('using ' + databaseName + ' to store classified data')
    transactionFile = shelve.open(databaseName)
    if 'categories' in transactionFile:
        logging.debug('Loaded database categories are: ' + str(transactionFile['categories']))
        categories = transactionFile['categories']

    if 'classifications' in transactionFile:
        logging.debug('Loaded database classifications are: ' + str(transactionFile['classifications']))
        classifications = transactionFile['classifications']

except:
    logging.error('Error opening database file: ', sys.exc_info())


for line in fileLines:
    logging.debug('--- Current line is ' + line)

    if line == "\n" and headersSection:
        logging.debug('Reached the end of headers')
        headersSection = False
        continue

    if not headersSection:
        sections = line.split(',')

        # TODO: Really should make this a dictionary or a proper object type

        transactionRecord = {"Date": sections[0], "Unique Id": sections[1]}

        # Skip if transaction is already in DB
        if sections[1] in classifications:
            logging.info('Skipping transaction as it is already been classified as ' + classifications[sections[1]])
            continue

        # TODO: Skip putting into ElasticSearch if it's already in there

        # Put the data into elasticsearch
        #putDataRequest = requests.put('http://' + esHostname + '/' + \
        #esIndexName + '/transactionRecord', data = json.dumps(transactionRecord))

        print('Date: ' + sections[0])
        print('Unique Id: ' + sections[1])
        print('Tran Type: ' + sections[2])
        print('Cheque Number: ' + sections[3])
        print('Payee: ' + sections[4])
        print('Memo: ' + sections[5])
        print('Amount: ' + sections[6])

        # Prompt user to classify transaction
        print('#-----------#\nWhat type of transaction is this?')
        category = input()
        if category == 'end':
            break

        # TODO: Check that the user hasn't entered a blank sections

        # Save the Unique ID and category
        classifications[sections[1]] = category

        # Store the category (if new) and increment total
        if category not in categories.keys():
            categories[category] = float(sections[6])
        else:
            categories[category] += float(sections[6])

        #print("Categories: " + str(categories))

# Save the data to an actual file
logging.info('Saving to database file...')
transactionFile['categories'] = categories
transactionFile['classifications'] = classifications
transactionFile.close()

logging.info('All done!')
logging.debug('categorized transactions:')
logging.debug(pprint.pprint(classifications))

logging.debug('Totals are:')
logging.debug(pprint.pprint(categories))
for category in categories:
    logging.debug('' + category + ', ' + str(categories[category]))
