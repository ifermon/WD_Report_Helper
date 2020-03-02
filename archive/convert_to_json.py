import json
import csv
from collections import defaultdict
import sys

print(sys.version)

csv_file_path = "All_Fields.csv"  # Load the field definitions
json_file_path = "test.json"  # Take all the field definitions and convert to JSON format
html_table_headers = "table_headers_html.txt"  # Put the column headers into HTML for table use
html_table_data = "table_data_html.txt"  # Put the field definitions into HTML format for table use
master_object_list_path = "master_list.json"  # Put the master list of objects (fields grouped by object)
master_bus_obj_name_OPTION_path = "master_bus_obj_name_OPTION.txt"  # Put the master list of objects (fields grouped by object)
master_bus_obj_name_OPTION_select_path = "master_bus_obj_name_OPTION_select.txt"  # Put the master list of objects (fields grouped by object)

#  allows me to add simple attributes to lists
class list_with_attr(list):
    pass

data = []
data_by_bus_obj = defaultdict(list_with_attr)

''' So this is kind of a mess. Bootstrap-tables, in order to filter select on individual columns
    needs those columns to not have spaces in the names. So in order to be flexible I'm going to read
    the second line of the file, which has the headers if saved as csv from excel, convert all spaces
    to _s, then open the file again and read from third line but passing the headers I created as the headers.
    Then, when generating the HTML header helper file, for the values I'll change the _'s back to spaces '''

#  Open fiile and read 2nd line for headers
headers_wo_spaces = []
with open(csv_file_path) as csv_file:
    header_reader = csv.reader(csv_file)
    header_reader.__next__() # skip the first row
    headers = header_reader.__next__()
    for h in headers:
        headers_wo_spaces.append(h.translate(str.maketrans(" ","_")))

""" Read the CSV file """
with open(csv_file_path) as csv_file:
    csv_reader = csv.DictReader(csv_file, headers_wo_spaces)
    csv_reader.__next__() # throw away the first row
    csv_reader.__next__() # throw away the second row
    for row in csv_reader:
        data.append(row)
        fname_transformation = row['Business_Object'].maketrans(" /", "__", "()") # trans table to remove illegal chars 
        data_by_bus_obj[row['Business_Object']].append(row)
        data_by_bus_obj[row['Business_Object']].fname = row['Business_Object'].translate(fname_transformation)
    headers = row.keys()

""" Write the json file to dump all data in one file """
with open(json_file_path,"w") as json_file:
    json_file.write(json.dumps(data, indent=4))

""" Write json file for master list of business objects """
with open(master_object_list_path,"w") as master_bus_obj_name_file:
    master_bus_obj_name_file.write("[")
    comma = ""
    for k in data_by_bus_obj.keys():
        master_bus_obj_name_file.write("{}\n\t'{}'".format(comma, k))
        comma = ","
    master_bus_obj_name_file.write("\n]")

""" Write a helper file to format options for select search in html """
with open(master_bus_obj_name_OPTION_path, "w") as master_bus_obj_name_OPTION_file:
    for k, v in data_by_bus_obj.items():
        master_bus_obj_name_OPTION_file.write("<option data-tokens='{0}' id='{0}'>{1}</option>\n".format(v.fname, k))

''' Write a helper file for the table headers '''
with open(html_table_headers, "w") as headers_file:
    for column in headers:
        # headers_file.write("{{title: '{0}',field: '{0}', rowspan: 2, alight: 'center', valign: 'middle', sortable: true, footerFormatter: totalTextFormatter }},\n".format(column))
        headers_file.write("<th data-field='{0}' data-visible='true' data-filter-control='' data-resizeable-column-id='{0}' data-sortable='true'>{1}</th>\n".format(column, column.replace("_"," ")))

""" Put data into object specific json files"""
for key, value in data_by_bus_obj.items():
    with open("bus_objs/{}.json".format(value.fname), "w") as key_file:
        key_file.write(json.dumps(value, indent=4))
