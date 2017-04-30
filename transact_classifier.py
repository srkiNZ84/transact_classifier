#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import sys, os, pprint, shelve, csv, requests, json
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections

print("Welcome to the Transaction Classifier!")

databaseName = 'transactionData'
esHostname = 'http://192.168.99.100:9200'
esIndexName = 'transactions'

# Connect to ElasticSearch and make sure indexes are there
createIndex = requests.put(esHostname + '/' + esIndexName )
createIndex.raise_for_status()

if len(sys.argv) < 2:
    print('Error: Need to specify file to load')
    print('Usage: transaction_classifier.py [CSV file to load]')
    sys.exit()

fileToLoad = sys.argv[1]

# Load file
#print('CSV file to load: ' + fileToLoad)
try:
    transactionFile = open(fileToLoad)
except FileNotFoundError:
    print('Error loading file: File not found \'' + fileToLoad + '\'')
except:
    print('Error loading file: ', sys.exc_info())

# Read in file contents
fileLines = list(transactionReader)

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
    transactionFile = shelve.open(databaseName)
    if 'categories' in transactionFile:
        print('database categories are: ' + str(transactionFile['categories']))
        categories = transactionFile['categories']

    if 'classifications' in transactionFile:
        print('database classifications are: ' + str(transactionFile['classifications']))
        classifications = transactionFile['classifications']

except:
    print('Error opening database file: ', sys.exc_info())


for line in fileLines:
    #print('--- ' + line)

    if line == [] and headersSection:
        print('end of headers')
        headersSection = False
        continue

    if not headersSection:
        # TODO: Really should make this a dictionary or a proper object type
        print('Date: ' + line[0])
        print('Unique Id: ' + line[1])
        print('Tran Type: ' + line[2])
        print('Cheque Number: ' + line[3])
        print('Payee: ' + line[4])
        print('Memo: ' + line[5])
        print('Amount: ' + line[6])

        transactionRecord = {"Date": line[0], "Unique Id": line[1]}

        # Skip if transaction is already in DB
        if line[1] in classifications:
            print('Skipping transaction as it is already been classified as ' + classifications[line[1]])
            continue

        # TODO: Skip putting into ElasticSearch if it's already in there

        # Put the data into elasticsearch
        putDataRequest = requests.put('http://' + esHostname + '/' + \
        esIndexName + '/transactionRecord', data = json.dumps(transactionRecord))

        # Prompt user to classify transaction
        print('#-----------#\nWhat type of transaction is this?')
        category = input()
        if category == 'end':
            break

        # TODO: Check that the user hasn't entered a blank line

        # Save the Unique ID and category
        classifications[line[1]] = category

        # Store the category (if new) and increment total
        if category not in categories.keys():
            categories[category] = float(line[6])
        else:
            categories[category] += float(line[6])

        print("Categories: " + str(categories))

# Save the data to an actual file
print('Saving to file...')
transactionFile['categories'] = categories
transactionFile['classifications'] = classifications
transactionFile.close()

print('All done!')
print('categorized transactions:')
pprint.pprint(classifications)

print('Totals are:')
pprint.pprint(categories)
for category in categories:
    print('' + category + ', ' + str(categories[category]))
