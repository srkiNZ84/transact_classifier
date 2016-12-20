#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import sys

print("Welcome to the Transaction Classifier!")

if len(sys.argv) < 2:
    print('Error: Need to specify file to load')
    print('Usage: transaction_classifier.py [CSV file to load]')
    sys.exit()

fileToLoad = sys.argv[1]

print('CSV file to load: ' + fileToLoad)
