#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import sys, os, pprint

print("Welcome to the Transaction Classifier!")

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
fileLines = transactionFile.readlines()

# TODO: We might want to add a "format guesser" if we wanted to support other
# formats/banks in the future

# TODO: Need to skip the top metadata section and headers
# TODO: We might want to keep the metadata section for future reference
headersSection = True
categories = {}
print('To finish classifying categories type \'end\'.')
for line in fileLines:
    #print('--- ' + line)

    if line == '\n' and headersSection:
        print('end of headers')
        headersSection = False
        continue

    if not headersSection:
        tokens = line.split(',')
        #print(str(tokens))

        print('Date: ' + tokens[0])
        print('Unique Id: ' + tokens[1])
        print('Tran Type: ' + tokens[2])
        print('Cheque Number: ' + tokens[3])
        print('Payee: ' + tokens[4])
        print('Memo: ' + tokens[5])
        print('Amount: ' + tokens[6])

        # TODO: Prompt user to classify transaction
        print('What type of transaction is this?')
        category = input()
        if category == 'end':
            break

        # TODO: Store the category (if new) and increment total
        if category not in categories.keys():
            categories[category] = float(tokens[6])
        else:
            categories[category] += float(tokens[6])

        print("Categories: " + str(categories))

print('All done!')
print('Totals are:')
pprint.pprint(categories)

transactionFile.close()

