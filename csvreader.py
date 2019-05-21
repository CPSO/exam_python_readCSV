## CSV reader script
#cdatetime,address,district,beat,grid,crimedescr,ucr_ncic_code,latitude,longitude

# Imports
import csv
from consolemenu import *
from consolemenu.items import *

def main():
    setupMenu()


#Def for setting up the menu system.
##Function-items runs a def when called.
def setupMenu():
    menu = ConsoleMenu("K.E.A - Krime Enforcment Archive")
    function_item = FunctionItem("Show the Data", showDB)
    menu.append_item(function_item)
    menu.show()
       
# Scripts
def showDB():
    with open('db/crimedb.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            print(f'\t{row["cdatetime"]} works in the {row["address"]} department, and was born in {row["district"]}.')
            line_count += 1
        print(f'Processed {line_count} lines.')
    Screen().input('Press [Enter] to continue')
    

main()
pass