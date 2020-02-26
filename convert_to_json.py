import json
import csv
from collections import defaultdict
import sys

print(sys.version)

csv_file_path = "test.csv"  # Load the field definitions
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

""" Read the CSV file """
with open(csv_file_path) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)
        t = row['Business Object'].maketrans(" /", "__", "()") # trans table to remove illegal chars 
        data_by_bus_obj[row['Business Object']].append(row)
        data_by_bus_obj[row['Business Object']].fname = row['Business Object'].translate(t)
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
        master_bus_obj_name_OPTION_file.write("<option data-token='{0}' id='{0}'>{1}</option>\n".format(v.fname, k))


""" Write a helper file to format options for select search """
''' with open(master_bus_obj_name_OPTION_path, "w") as master_bus_obj_name_OPTION_file:
    for k in data_by_bus_obj.keys():
        master_bus_obj_name_OPTION_file.write("<option>{}</option>\n".format(k)) '''



""" Write the header helper file
        title: 'Item ID',
        field: 'id',
        rowspan: 2,
        align: 'center',
        valign: 'middle',
        sortable: true,
        footerFormatter: totalTextFormatter
"""
with open(html_table_headers, "w") as headers_file:
    for column in headers:
        # headers_file.write("{{title: '{0}',field: '{0}', rowspan: 2, alight: 'center', valign: 'middle', sortable: true, footerFormatter: totalTextFormatter }},\n".format(column))
        headers_file.write("<th data-field=\"{0}\" data-sortable='true'>{0}</th>\n".format(column))

""" Write the row data helper file 
with open(html_table_data, "w") as data_file:
    for row in data.values():
        line = ""
        for value in row.values():
            line = "{}\n\t<td>{}</td>".format(line, value)
        data_file.write("<tr>{}\n</tr>\n".format(line))

for key in data_by_bus_obj.keys():
    t = key.maketrans(" /", "__", "()")
    with open("bus_objs/{}.html".format(key.translate(t)), "w") as key_file:
        for row in data_by_bus_obj[key]:
            line = ""
            for value in row.values():
                line = "{}\n\t<td>{}</td>".format(line, value)
            key_file.write("<tr>{}\n</tr>\n".format(line))
"""

""" Put data into object specific json files"""
for key, value in data_by_bus_obj.items():
    with open("bus_objs/{}.json".format(value.fname), "w") as key_file:
        key_file.write(json.dumps(value, indent=4))
