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
    function_item2 = FunctionItem("Search the Data", searchCrime)
    menu.append_item(function_item)
    menu.append_item(function_item2)
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
    

def searchCrime():
    crimeCode = input('what code?: ')
    with open('db/crimedb.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                 print(f'Column names are {", ".join(row)}')
                 line_count += 1
            if row['district'] == crimeCode:
                print(f'\t{row["cdatetime"]} works in the {row["address"]} department, and was born in {row["district"]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')
        Screen().input('Press [Enter] to continue')
       

    """
    ucr_ncic_codee = 2142
    with open('db/crimedb.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if row["ucr_ncic_codee"] == ucr_ncic_codee:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
            print(f'\t {row}')
            line_count += 1
        print(f'Processed {line_count} lines.')
        """
    

main()
pass