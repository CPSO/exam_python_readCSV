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
fieldnames = ['cdatetime', 'address', 'district', 'beat', 'grid',
              'crimedescr', 'ucr_ncic_code', 'latitude', 'longitude']

def main():
    setupMenu()


#Def for setting up the menu system.
##Function-items runs a def when called.
def setupMenu():
    """
    menu = ConsoleMenu("K.E.A - Krime Enforcment Archive")
    PrintTheData = FunctionItem("Show the data", showDB)
    MakeHTML = FunctionItem("Make Full HTML",makeHTML)
    MakeJSON = FunctionItem("Make Full JSON", makeJSON)
    SearchTheDB = FunctionItem("Search the data", searchCrime)
    AddEntry = FunctionItem("Add a new crime", writeToCSV)
    SearchRadius = FunctionItem("Search crime in a radius", searchCrimeRadius)
    menu.append_item(PrintTheData)
    menu.append_item(MakeHTML)
    menu.append_item(MakeJSON)
    menu.append_item(SearchTheDB)
    menu.append_item(AddEntry)
    menu.append_item(SearchRadius)
    menu.show()
    """
    options = {
        '1': showDB,
        '2': searchCrime,
        '3': searchCrimeRadius,
        '4': writeToCSV
    }
    menu = '1 - Search for a crime in the archive\n' \
           '2 - Add a new record to the database\n' \
           '3 - Export the database to JSON\n' \
           '4 - Export the database to HTML\n' \
           '0 - Exit'
    print('Hello! Welcome to the K.E.A - Krime Enforcment Archive!\n'
          'How can I help you today?\n' + menu)
    selection = input()
    is_running = should_run(selection)
    while is_running:
        try:
            if int(selection) <= len(options):
                options[selection]()
        except (KeyError,ValueError) as keye:
            print("No item on list with that ID")
            pass
        print('Is there anything else you want to do?\n' + menu)
        selection = input()
        is_running = should_run(selection)
    print('Thank you for using the Sacramento Police Database!')

    
       
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

        html_output += '<style> table { font-family: arial, sans-serif; border-collapse: collapse; width: 100%; } td, th { border: 1px solid #dddddd; text-align: left; padding: 8px; } tr:nth-child(even) { background-color: #dddddd; } </style>'

    html_file = open('html/searchhtml.html','w+')
    html_file = html_file.write(html_output)


    #JSON PART
    csvFilePath = "db/crimedb.csv"
    jsonFilePath = "json/search.json"
    arr = []
#read the csv and add the arr to a arrayn
    with open (csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for csvRow in csvReader:
            if csvRow[searchFilter] == serachInput:
                arr.append(csvRow)
    print(arr)

    # write the data to a json file
    with open(jsonFilePath, "w") as jsonFile:
        jsonFile.write(json.dumps(arr, indent = 4))
    Screen().input('Press [Enter] to continue')


    """
    csvFilePath = "db/crimedb.csv"
    jsonFilePath = "json/search.json"
    #read the csv and add the data to a dictionary
    data = {}
    with open (csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for csvRow in csvReader:
            if csvRow[searchFilter] == serachInput:
                id = csvRow["cdatetime"]
                data[id] = csvRow
    print(data)
    # write the data toa json file
    with open(jsonFilePath, "w") as jsonFile:
        jsonFile.write(json.dumps(data, indent = 4))
    Screen().input('Press [Enter] to continue')
    """

def searchCrimeRadius():
    jsonFilePath = "json/search.json"
    #Search Crime in a radius of 5km
    print('latitude,longitude')
    input_coordinate  = input('Please input a coordinate separated by a comma (latitude,longitude)\n').split(',')
    input_radius  = float(input('Please input desired radius in miles\n')) * 0.0145  # converts miles to long/lat
    
    
#read the csv and add the arr to a arrayn
    csvFilePath = "db/crimedb.csv"
    arr = []
    dataEntry = []
    html_output = ""
    with open (csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for row in csvReader:
            if float(row['latitude']) - float(input_coordinate[0]) <= input_radius and \
                    float(input_coordinate[0]) - float(row['latitude']) <= input_radius:
                if float(row['longitude']) - float(input_coordinate[1]) <= input_radius and \
                        float(input_coordinate[1]) - float(row['longitude']) <= input_radius:
                    arr.append(row)
                    dataEntry.append(f"<td>{row['cdatetime']}</td> <td>{row['address']}</td> <td>{row['district']}</td> <td>{row['beat']}</td> <td>{row['grid']}</td> <td>{row['crimedescr']}</td> <td>{row['ucr_ncic_code']}</td> <td>{row['latitude']}</td> <td>{row['longitude']}</td> ")
                    with open(jsonFilePath, "w") as jsonFile:
                        jsonFile.write(json.dumps(arr, indent = 4))
        
    # HTML
    html_output += '<table>\n' \
           '  <tr>\n' \
        f'    <th>{fieldnames[0]}</th>\n' \
        f'    <th>{fieldnames[1]}</th>\n' \
        f'    <th>{fieldnames[2]}</th>\n' \
        f'    <th>{fieldnames[3]}</th>\n' \
        f'    <th>{fieldnames[4]}</th>\n' \
        f'    <th>{fieldnames[5]}</th>\n' \
        f'    <th>{fieldnames[6]}</th>\n' \
        f'    <th>{fieldnames[7]}</th>\n' \
        f'    <th>{fieldnames[8]}</th>\n' \
           '  </tr>\n'
    
    html_output += '\n<tr>'
    for entry in dataEntry:
        html_output += f'\n\t<tr>{entry}</tr>'
    html_output += '\n</tr>'

    html_output += '\n</tr>'
    html_output += '</table>'
    html_output += f'<p>Search gave {len(dataEntry)} hits in the registerey</p>'
    html_output += '\n<style> table { font-family: arial, sans-serif; border-collapse: collapse; width: 100%; } td, th { border: 1px solid #dddddd; text-align: left; padding: 8px; } tr:nth-child(even) { background-color: #dddddd; } </style>'
    html_file = open('html/searchhtml.html','w+')
    html_file = html_file.write(html_output)

    

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
    html_output += '<table>'
    html_output += '<tr>'
    line_count = 0

    with open('db/crimedb.csv', 'r') as data_file:
        csv_data = csv.DictReader(data_file)

        for line in csv_data:
            if line_count == 0:
                text = (f'<th>{"</th> <th>".join(line)}</th>')
                html_output += text
                html_output += '</tr>'
                line_count += 1
            data.append(f"<td>{line['cdatetime']}</td> <td>{line['address']}</td> <td>{line['district']}</td> <td>{line['beat']}</td> <td>{line['grid']}</td> <td>{line['crimedescr']}</td> <td>{line['ucr_ncic_code']}</td> <td>{line['latitude']}</td> <td>{line['longitude']}</td> ")
        #html_output += f'<p>There are currently {len(data)} in the registerey</p>'

    

    for entry in data:
        html_output += f'\n\t<tr>{entry}</tr>'

    html_output += '</table>'

    html_output += '\n<style> table { font-family: arial, sans-serif; border-collapse: collapse; width: 100%; } td, th { border: 1px solid #dddddd; text-align: left; padding: 8px; } tr:nth-child(even) { background-color: #dddddd; } </style>'
    html_file = open('html/fullhtml.html','w+')
    html_file = html_file.write(html_output)


def makeJSON():
    csvFilePath = "db/crimedb.csv"
    jsonFilePath = "json/parsed.json"
    """
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
    """

    arr = []
#read the csv and add the arr to a arrayn

    with open (csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        print(csvReader)
        for csvRow in csvReader:
            arr.append(csvRow)
    # write the data to a json file
    with open(jsonFilePath, "w") as jsonFile:
        jsonFile.write(json.dumps(arr, indent = 4))

def should_run(user_input):
    if user_input == '0' or len(user_input) < 1:
        return False
    else:
        return True
main()
pass