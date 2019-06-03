## CSV reader script
#cdatetime,address,district,beat,grid,crimedescr,ucr_ncic_code,latitude,longitude

# Imports
import csv,json, io,sys,subprocess,os,platform
from html import escape

fieldnames = ['cdatetime', 'address', 'district', 'beat', 'grid',
              'crimedescr', 'ucr_ncic_code', 'latitude', 'longitude']

def main():
    setupMenu()


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
    

def searchCrime():
    #cdatetime,address,district,beat,grid,crimedescr,ucr_ncic_code,latitude,longitude
    #print('cdatetime,address,district,beat,grid,crimedescr,ucr_ncic_code,latitude,longitude')
    searchChoise = [
        'showDB',
        'searchCrime',
        'searchCrimeRadius',
        'writeToCSV',
        'makeHTML',
        'makeJSON'
    ]
    print(searchChoise)
    menu = '1 - address\n' \
           '2 - district\n' \
           '3 - Search for a crime on a area\n' \
           '4 - Add a new crime to the Database\n' \
           '5 - Make a HTML page\n' \
           '6 - Make a JSON page\n' \
           '0 - Exit'
    print('Search Selected Enter search filter: ?\n' + menu)
    selectionSearch = input()
    pickedFilter = searchChoise[selectionSearch]
    print(pickedFilter)
    is_running = True
    while is_running:
        try:
            if int(selectionSearch) <= len(searchChoise):
                print("OK")
                is_running = False
        except (KeyError,ValueError) as keye:
            print("No item on list with that ID")
            pass



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
            if csvRow[searchFilter] == serachInput:
                arr.append(csvRow)
    print(arr)

    # write the data to a json file
    with open(jsonFilePath, "w") as jsonFile:
        jsonFile.write(json.dumps(arr, indent = 4))


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