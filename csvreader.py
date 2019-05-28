## CSV reader script
#cdatetime,address,district,beat,grid,crimedescr,ucr_ncic_code,latitude,longitude

# Imports
import csv
import json
from consolemenu import *
from consolemenu.items import *
from html import escape
import io
import sys

def main():
    setupMenu()


#Def for setting up the menu system.
##Function-items runs a def when called.
def setupMenu():
    menu = ConsoleMenu("K.E.A - Krime Enforcment Archive")
    function_item = FunctionItem("Show the Data", showDB)
    function_item2 = FunctionItem("Search the Data", searchCrime)
    function_item3 = FunctionItem("add item to csv", writeToCSV)
    function_item4 = FunctionItem("make new JSON", makeJSON)
    function_item5 = FunctionItem("make HTML", makeHTML)
    function_item6 = FunctionItem("make HTML", backupHTML)
    menu.append_item(function_item)
    menu.append_item(function_item2)
    menu.append_item(function_item3)
    menu.append_item(function_item4)
    menu.append_item(function_item5)
    menu.append_item(function_item6)
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
    #cdatetime,address,district,beat,grid,crimedescr,ucr_ncic_code,latitude,longitude
    print('cdatetime,address,district,beat,grid,crimedescr,ucr_ncic_code,latitude,longitude')
    searchFilter = input('What filter?: ')
    serachInput = input('What to search for?: ')
    html_output = ""
    dataEntry = []
    with open('db/crimedb.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        html_output += '<table>'
        html_output += '\n<tr>'
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'<th>{"</th>".join(row)}')
                text = (f'<th>{"</th> <th>".join(row)}</th>')
                html_output += text
                line_count += 1
            if row[searchFilter] == serachInput:
                dataEntry.append(f"<td>{row['cdatetime']}</td> <td>{row['address']}</td> <td>{row['district']}</td> <td>{row['beat']}</td> <td>{row['grid']}</td> <td>{row['crimedescr']}</td> <td>{row['ucr_ncic_code']}</td> <td>{row['latitude']}</td> <td>{row['longitude']}</td> ")
                line_count += 1
        numberOfEntrys = f'<p>Search gave {len(dataEntry)} hits in the registerey</p>'
        html_output += '\n</tr>'
        print(f'Processed {line_count} lines.')
        html_output += '\n<tr>'

        for entry in dataEntry:
            html_output += f'\n\t<tr>{entry}</tr>'

        html_output += '\n</tr>'

    html_file = open('html/searchhtml.html','w+')
    html_file = html_file.write(html_output)


    Screen().input('Press [Enter] to continue')

def searchCrimeRadius():
    #Search Crime in a radius of 5km
    print('latitude,longitude')
    searchLat = input('Enter Latitude: ')
    searchLong = input('Enter Longitude: ')

def writeToCSV():
   
    row = ['05/24/19 10:15', ' Bobby', ' New York']
    with open('db/crimedb.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)
    csv_file.close()


def makeHTML():    
#cdatetime,address,district,beat,grid,crimedescr,ucr_ncic_code,latitude,longitude
    html_output = ''
    data = []

    with open('db/crimedb.csv', 'r') as data_file:
        csv_data = csv.DictReader(data_file)

        for line in csv_data:
            data.append(f"{line['cdatetime']} {line['address']} {line['district']} {line['beat']} {line['grid']} {line['crimedescr']} {line['ucr_ncic_code']} {line['latitude']} {line['longitude']} ")
        html_output += f'<p>There are currently {len(data)} in the registerey</p>'

    html_output += '\n<ul>'
    

    for entry in data:
        html_output += f'\n\t<li>{entry}</li>'

    html_output += '\n</ul>'

    html_file = open('html/fullhtml.html','w+')
    html_file = html_file.write(html_output)
    
        

    

def backupHTML():
    Screen().input('Press [Enter] to continue')



def makeJSON():
    csvFilePath = "db/crimedb.csv"
    jsonFilePath = "json/parsed.json"
    #read the csv and add the data to a dictionary
    data = {}
    with open (csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for csvRow in csvReader:
            id = csvRow["cdatetime"]
            data[id] = csvRow
    print(data)
    # write the data toa json file
    with open(jsonFilePath, "w") as jsonFile:
        jsonFile.write(json.dumps(data, indent = 4))

    arr = []
#read the csv and add the arr to a arrayn

    with open (csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        print(csvReader)
        for csvRow in csvReader:
            arr.append(csvRow)

    print(arr)

    # write the data to a json file
    with open(jsonFilePath, "w") as jsonFile:
        jsonFile.write(json.dumps(arr, indent = 4))

main()
pass