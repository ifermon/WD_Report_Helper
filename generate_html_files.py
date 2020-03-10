#!/usr/bin/env python3.7
""" This file takes a report that includes all report fields in a Workday 
    tenant and organizes them by business object. Then it generates a 
    unique HTML file for each business object. The approach is needed
    so that the collective files can be view from a filesystem
    (i.e. not using a web server) vs. using javascript to just
    load a json file on request.

    Right now the generated portions are of two types, parts that are 
    specific to the file being generated and parts that are specific
    the the report (i.e. it's the same for each file but it changes
    based on the output of the report that's being used for input)
    """
import json
import csv
from collections import defaultdict
import sys
from string import Template

__author__ = "Ivan Fermon"
__copyright__ = "Copyright 2020"
__credits__ = ["None", ]
__license__ = "MIT"
__maintainer__ = "Ivan Fermon"
__version__ = "1.0"
__status__ = "dev"

print(sys.version)  # We need to be on 3.7+

"""
    We will be reading the source file from csv format and putting each row into a dict.
        { 'Field': 'value',
          'Business_Object': 'value',
          etc...}
    The list of dicts, one for each row, is organized into lists, one for each Business_Object.
    Those lists are stored in a dict with the name of the Business_Object as the key
    Each one of those lists is the data that is unique to the file
    The total list of Business_Object names (e.g. the keys() to the master dict) 
    is the content that is unique to the report output, but the same in each file.
    
    We combine that with the html snippets that we'll load from strings from an include file and
    that's how we generate each file

    there are 4 replacement strings:
        - header_title - this is file specific
        - table_title - this is file specific
        - options - this is the same for all files
        - table_rows - this is file specific
"""
HTML_SELECT_ONLY = True
html_table_template_path = "html_table_template.html"
html_select_template_path = "html_select_template.html"
object_distribution_dir = "./dist"
index_distribution_dir = "./dist"
csv_file_path = "All_Fields.csv"  # Load the field definitions

#  allows me to add simple attributes to lists like file name


class List_w_Attr(list):
    pass

# Default template uses '$' which for clear reasons in an html template won't work


class My_Template(Template):
    delimiter = '&'


data = []
data_by_bus_obj = defaultdict(List_w_Attr)

''' So this is kind of a mess. Bootstrap-tables, in order to filter select on individual columns
    needs those columns to not have spaces in the names. So in order to be flexible I'm going to read
    the second line of the file, which has the headers if saved as csv from excel, convert all spaces
    to _s, then open the file again and read from third line but passing the headers I created as the headers.
    Then, when generating the HTML header helper file, for the values I'll change the _'s back to spaces '''

#  Open file and read 2nd line for headers
headers_wo_spaces = []
with open(csv_file_path) as csv_file:
    header_reader = csv.reader(csv_file)
    header_reader.__next__()  # skip the first row
    headers = header_reader.__next__()
    for h in headers:
        # Replace spaces with _'s or the column filtering won't work
        headers_wo_spaces.append(h.translate(str.maketrans(" ", "_")))

""" Read the CSV file  and generate the data """
with open(csv_file_path) as csv_file:
    csv_reader = csv.DictReader(csv_file, headers_wo_spaces)
    csv_reader.__next__()  # throw away the first row
    csv_reader.__next__()  # throw away the second row
    for row in csv_reader:
        data.append(row)
        fname_transformation = row['Business_Object'].maketrans(
            " /", "_-", "()")  # trans table to remove illegal chars
        data_by_bus_obj[row['Business_Object']].append(row)
        data_by_bus_obj[row['Business_Object']].fname = row['Business_Object'].translate(
            fname_transformation)
    headers = row.keys()

""" Load the html templates """
with open(html_table_template_path) as tmplate_file:
    table_template = My_Template(tmplate_file.read())
with open(html_select_template_path) as tmplate_file:
    index_template = My_Template(tmplate_file.read())

""" Now all my data is loaded from the source file, start generating the include strings """

""" Construct the html for the options """
option_str = ""  # javacript bootstrap-select formatting
option2_str = ""  # no javacript html5 only input datalist formatting
for key, value in data_by_bus_obj.items():
    option_str += '<option id="{0}">{1}</option>\n'.format(value.fname, key)
    option2_str += '<option id="./{0}.html" value="{1}" />'.format(
        value.fname, key)

""" 
    Now generate the files
"""
ctr = 0
for key, value in data_by_bus_obj.items():
    for r in value:
        v = r['Related_Business_Object_Name']
        if v in data_by_bus_obj:
            fname = data_by_bus_obj[v].fname
            r['Related_Business_Object_Name'] = '<a href="{0}.html">{1}</a>'.format(fname, v)
        # sys.exit(0)
    substitute_dict = {
        'header_title': key,
        'table_title': key,
        'options': option_str,
        'table_rows': json.dumps(value)
    }
    if (HTML_SELECT_ONLY):
        with open("{0}/{1}.html".format(object_distribution_dir, value.fname), "w") as f:
            f.write(table_template.substitute(substitute_dict))
        with open("{0}/selector.html".format(index_distribution_dir), "w") as f:
            f.write(index_template.substitute(substitute_dict))
    else:
        with open("{0}/{1}.html".format(object_distribution_dir, value.fname), "w") as f:
            f.write(table_template.substitute(substitute_dict))
        with open("{0}/index.html".format(index_distribution_dir), "w") as f:
            f.write(index_template.substitute(substitute_dict))
