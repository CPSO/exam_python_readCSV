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
    menu.append_item(function_item)
    menu.append_item(function_item2)
    menu.append_item(function_item3)
    menu.append_item(function_item4)
    menu.append_item(function_item5)
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
    with open('db/crimedb.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                 print(f'Column names are {", ".join(row)}')
                 line_count += 1
            if row[searchFilter] == serachInput:
                print(f'\t{row["cdatetime"]} Adress: {row["address"]} District:{row["district"]} ' + f'\n Beat: {row["beat"]} Grid: {row["grid"]}'+
                    f'\t Crime Desc: {row["crimedescr"]} UCR_NCIC_CODE: {row["ucr_ncic_code"]} Latitude: {row["latitude"]} Longitude: {row["longitude"]} ')
                line_count += 1
        print(f'Processed {line_count} lines.')
        Screen().input('Press [Enter] to continue')

def searchCrimeRadius():
    #Search Crime in a radius of 5km
    print('latitude,longitude')
    searchLat = input('Enter Latitude: ')
    searchLong = input('Enter Longitude: ')

def writeToCSV():
   
    row = ['05/24/19 10:15', ' Danny', ' New York']
    with open('db/crimedb.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)
    csv_file.close()


def makeHTML():    
#cdatetime,address,district,beat,grid,crimedescr,ucr_ncic_code,latitude,longitude
    html_output = ''
    names = []

    with open('db/crimedb.csv', 'r') as data_file:
        csv_data = csv.DictReader(data_file)

        # We don't want first line of bad data
        next(csv_data)

        for line in csv_data:
            if line['cdatetime'] == 'No Reward':
                break
            names.append(f"{line['cdatetime']} {line['address']}")

        html_output += f'<p>There are currently {len(names)} public contributors. Thank You!</p>'

    html_output += '\n<ul>'

    for name in names:
        html_output += f'\n\t<li>{name}</li>'

    html_output += '\n</ul>'

    html_file = open('html/fullhtml.html','w+')
    html_file = html_file.write(html_output)
    
        

    

def backupHTML():
    with open ('db/crimedb.csv', 'r') as csv_file:
        csv_file = csv.DictReader(csv_file)
    #reader = csv.reader(open('db/crimedb.csv'),'r')
    htm_output = ""
    htmlFilePath = "html/fullhtml.html"

    #htmlFile = open ('html/fullhtml.html','w+')
    rownum = 0
    htm_output += ('<table>')

    for row in csv_file:
        if rownum == 0:
            htm_output += ('<tr>')
            for column in row:
                htm_output += ('<th>' + column + '</th>')
            htm_output += ('</tr>')
        else:
            htm_output += ('<tr>')
            for column in row:
                htm_output += ('<td>' + column + '</td>')
            htm_output += ('</tr>')
        rownum += 1

    htm_output += ('</table>')



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