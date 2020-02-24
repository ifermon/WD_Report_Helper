import json
import csv
from collections import defaultdict

csv_file_path = "test.csv"
json_file_path = "test.json"
html_table_headers = "table_headers_html.txt"
html_table_data = "table_data_html.txt"

data = []
data_by_bus_obj = defaultdict(list)

""" Read the CSV file """
with open(csv_file_path) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        """id = row['Field']
        data[id] = row"""
        data.append(row)
        data_by_bus_obj[row['Business Object']].append(row)
    headers = row.keys()

""" Write the json file """
with open(json_file_path,"w") as json_file:
    json_file.write(json.dumps(data, indent=4))

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
        headers_file.write("{{title: '{0}',field: '{0}', rowspan: 2, alight: 'center', valign: 'middle', sortable: true, footerFormatter: totalTextFormatter }},\n".format(column))
        # headers_file.write("<th data-field=\"{0}\">{0}</th>\n".format(column))

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

""" PUt data into object specific json files"""
for key, value in data_by_bus_obj.items():
    t = key.maketrans(" /", "__", "()")
    with open("bus_objs/{}.json".format(key.translate(t)), "w") as key_file:
        key_file.write(json.dumps(value, indent=4))
