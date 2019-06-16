## CSV reader script
#cdatetime,address,district,beat,grid,crimedescr,ucr_ncic_code,latitude,longitude

# Imports
import csv,json, io,sys,subprocess,os,platform
from html import escape

fieldnames = ['cdatetime', 'address', 'district', 'beat', 'grid',
              'crimedescr', 'ucr_ncic_code', 'latitude', 'longitude']

def main():
    setupMenu()

def get_input(text):
    print(text)
    return input(text)


#Def for setting up the menu system.
##Function-items runs a def when called.
def setupMenu():
    options = {
        '1': showDB,
        '2': searchCrime,
        '3': searchCrimeRadius,
        '4': writeToCSV,
        '5': makeHTML,
        '6': makeJSON
    }
    menu = '1 - Show Database\n' \
           '2 - Search for a crime\n' \
           '3 - Search for a crime on a area\n' \
           '4 - Add a new crime to the Database\n' \
           '5 - Make a HTML page\n' \
           '6 - Make a JSON page\n' \
           '0 - Exit'
    print('\nHello! Welcome to the K.E.A - Krime Enforcment Archive!\n'
          '\nHow can I help you today?\n' + menu)
    selection = input()
    is_running = should_run(selection)

    while is_running:
        try:
            if int(selection) <= len(options):
                options[selection]()
                
        except (KeyError,ValueError) as keye:
            print("\nNo item on list with that ID \n")
            print(keye)
            pass
        print('\nIs there anything else you want to do? \n' + menu)
        selection = input()
        is_running = should_run(selection)
    print('Thank you for using K.E.A - Krime Enforcment Archive')

    
       
# Scripts
def showDB():
    with open('db/crimedb.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            print(f'\t time: {row["cdatetime"]} adress: {row["address"]} district: {row["district"]}.')
            line_count += 1
        print(f'Processed {line_count} lines.')
        is_done = True
    return is_done


def searchCrime():
    searchChoise = [
        'cdatetime',
        'address',
        'district',
        'beat',
        'crimedescr',
        'ucr_ncic_code'
    ]
    menu = '0 - Search for Date and Time\n' \
           '1 - Search for Address\n' \
           '2 - Serach for District\n' \
           '3 - Search for Beat\n' \
           '4 - Search for Crime Descriptions\n' \
           '5 - Search for Code\n'
    print('Search Selected Enter search filter: \n' + menu)
    selectionSearch = input()
    convertInt = int(selectionSearch)
    is_running = True

    while is_running:
        try:
            pickedFilter = searchChoise[convertInt]
            if int(selectionSearch) <= len(searchChoise):
                print("value ok")
                is_running = False
        except (KeyError,ValueError, IndexError) as keye:
            print("\nNo item on list with that ID \n")
            pass
            print('Is there anything else you want to do?\n' + menu)
            selectionSearch = input()
            convertInt = int(selectionSearch)
            


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
                text = (f'<th>{"</th> <th>".join(row)}</th>')
                html_output += text
                line_count += 1
            if row[pickedFilter] == serachInput:
                dataEntry.append(f"<td>{row['cdatetime']}</td> <td>{row['address']}</td> <td>{row['district']}</td> <td>{row['beat']}</td> <td>{row['grid']}</td> <td>{row['crimedescr']}</td> <td>{row['ucr_ncic_code']}</td> <td>{row['latitude']}</td> <td>{row['longitude']}</td> ")
                line_count += 1
        numberOfEntrys = f'<p>Search gave {len(dataEntry)} hits in the registerey</p>'
        html_output += '\n</tr>'
        
        if (line_count > 1):
            print(f'Processed {line_count} lines.\n')
        else:
            print(f'No records found \n')
            pass
        html_output += '\n<tr>'

        for entry in dataEntry:
            html_output += f'\n\t<tr>{entry}</tr>'

        html_output += '\n</tr>'

        html_output += '<style> table { font-family: arial, sans-serif; border-collapse: collapse; width: 100%; } td, th { border: 1px solid #dddddd; text-align: left; padding: 8px; } tr:nth-child(even) { background-color: #dddddd; } </style>'
    
    html_file = open('html/search.html','w+')
    html_file = html_file.write(html_output)


    #JSON PART
    csvFilePath = "db/crimedb.csv"
    jsonFilePath = "json/search.json"
    arr = []
#read the csv and add the arr to a arrayn
    with open (csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for csvRow in csvReader:
            if csvRow[pickedFilter] == serachInput:
                arr.append(csvRow)

    # write the data to a json file
    with open(jsonFilePath, "w") as jsonFile:
        jsonFile.write(json.dumps(arr, indent = 4))



    #Code to open windows to show resaults of searches
    htmlFile = 'html\search.html'
    jsonFile = 'json\search.json'
    try:
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', htmlFile))
            subprocess.call(('open', jsonFile))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(htmlFile)
            os.startfile(jsonFile)
        else:                                   # linux variants
            subprocess.call(('xdg-open', htmlFile))
            subprocess.call(('xdg-open', jsonFile))
    except FileNotFoundError as fnfE:
        print("Unable to locate file")
    return line_count

def searchCrimeRadius():
    jsonFilePath = "json/search.json"
    #Search Crime in a radius of 5km
    print('latitude,longitude')
    input_coordinate  = input('Please input a coordinate separated by a comma (latitude,longitude)\n').split(',')
    input_radius  = float(input('Please input desired radius in miles\n')) * 0.0145  # converts miles to long/lat
    print(input_coordinate)
    print(input_radius)
    
    
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
    html_file = open('html/search.html','w+')
    html_file = html_file.write(html_output)

    

def writeToCSV():
    #https://pynative.com/python-input-function-get-user-input/
    csvFile = open('db/crimedb.csv', 'a', newline='')
    writer = csv.DictWriter(csvFile, delimiter=',', fieldnames=fieldnames)
    
    inputQuestion = 'Please input {0}\n'
    inputExample = 'Ex.: "{0}"\n'
    inputConfirmation = 'Is this the correct {0} (Y/n)? {1}\n'
    newEntry = {}

    entryBuilding = True
    while entryBuilding:
        date_sting_build = (input(inputQuestion.format('month')) + '/' +
                            input(inputQuestion.format('day of month')) + '/' +
                            input(inputQuestion.format('year')) + ' ' +
                            input(inputQuestion.format('hour')) + ':' +
                            input(inputQuestion.format('minute')))

        date = date_sting_build
        selection = input(inputConfirmation.format('date', date))
        if selection.lower() != 'n':
            entryBuilding = False
            newEntry['cdatetime'] = date
       
    entryBuilding = True
    while entryBuilding:
        address = input(inputQuestion.format('address') + inputExample.format('1234 DEMO STREET')).upper()
        selection = input(inputConfirmation.format('address', address))
        if selection.lower() != 'n':
            entryBuilding = False
            newEntry['address'] = address

    entryBuilding = True
    while entryBuilding:
        district = input(inputQuestion.format('district number') + inputExample.format('99'))
        selection = input(inputConfirmation.format('district', district))
        if selection.lower() != 'n':
            entryBuilding = False
            newEntry['district'] = district

    entryBuilding = True
    while entryBuilding:
        beat = input(inputQuestion.format('beat') + inputExample.format('99A')).upper()
        selection = input(inputConfirmation.format('beat', beat))
        if selection.lower() != 'n':
            entryBuilding = False
            newEntry['beat'] = beat

    entryBuilding = True
    while entryBuilding:
        grid = input(inputQuestion.format('grid') + inputExample.format('999'))
        selection = input(inputConfirmation.format('grid', grid))
        if selection.lower() != 'n':
            entryBuilding = False
            newEntry['grid'] = grid

    entryBuilding = True
    while entryBuilding:
        description = input(inputQuestion.format('a Description') +
                            inputExample.format('999 AWESOME-PYTHON')).upper()
        selection = input(inputConfirmation.format('description', description))
        if selection.lower() != 'n':
            entryBuilding = False
            newEntry['crimedescr'] = description

    entryBuilding = True
    while entryBuilding:
        ucr = input(inputQuestion.format('UCR number') + inputExample.format('2299'))
        selection = input(inputConfirmation.format('UCR number', ucr))
        if selection.lower() != 'n':
            entryBuilding = False
            newEntry['ucr_ncic_code'] = ucr

    entryBuilding = True
    while entryBuilding:
        coordinates = input(inputQuestion.format('coordinates, latitude first')
                            + inputExample.format('38.6374478,-121.3846125'))
        selection = input(f'Are these the correct coordinates (Y/n)? {coordinates}\n')
        if selection.lower() != 'n':
            entryBuilding = False
            coordinates = coordinates.split(',')
            newEntry['latitude'] = coordinates[0]
            if coordinates[1][0] == ' ':
                newEntry['longitude'] = coordinates[1][1:]
            else:
                newEntry['longitude'] = coordinates[1]

    entryBuilding = True
    while entryBuilding:
        selection = input(f'Is this entry correct (y/N)? {newEntry}\n')
        if selection.lower() == 'y':
            entryBuilding = False
            writer.writerow(newEntry)
            print('Entry added to the system!')
        else:
            selection = input('Are you sure you want to cancel (y/N)? Unsaved data will be lost\n')
            if selection.lower() == 'y':
                entryBuilding = False

    csvFile.close()


def makeHTML():    
#cdatetime,address,district,beat,grid,crimedescr,ucr_ncic_code,latitude,longitude
    filePath = 'html/fullhtml.html'
    if os.path.exists(filePath):
        os.remove(filePath)
    else:
        print("Can not delete the file as it doesn't exists")

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
    jsonFilePath = "json/fulljson.json"
    arr = []

    if os.path.exists(jsonFilePath):
        os.remove(jsonFilePath)
    else:
        print("Can not delete the file as it doesn't exists")
        
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