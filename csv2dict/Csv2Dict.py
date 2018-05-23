__author__ = 'glen'

import os
import pprint
import csv
import unicodecsv
import json
import copy
import re

from time import localtime, strftime
from pynux import utils
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import valid_columns

class UTF8PrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return(object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

class Csv2Dict:



    def __init__(self, data_file, sheet, nx, blankout=False):
        '''
        The Csv2Dict class reads a csv data file, the first line of which contains column names. Succeeding
        lines represent rows of data. Initially the column names are used as the keys to a list of dicts, one
        per row. There are methods for transforming those dicts into import records.
        '''

        print('Starting at %s' % strftime("%Y-%m-%d %H:%M:%S", localtime()))

        self.status = 0
        self.row_dicts = []
        self.meta_dicts = []
        self.blankout = blankout
        self.sheet = sheet
        self.nx = nx
        self.data = {}

        self.meta_dict_properties_template = {}

        if blankout:
            blankout_ucldc_file_name = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'blank-ucldc.json',
            )
            with open(blankout_ucldc_file_name, 'r') as blankout_ucldc_file:
                self.meta_dict_properties_template = json.load(blankout_ucldc_file).get('properties', {})
        
        if 'google' in data_file:
            scope = ['https://spreadsheets.google.com/feeds']
            creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
            client = gspread.authorize(creds)
            spreadsheet = client.open_by_url(data_file)
            if sheet == None:
                sheet = client.open(spreadsheet.title).sheet1
            else:
                sheet = client.open(spreadsheet.title).worksheet(sheet)
            fields = sheet.row_values(1)
            valid_columns.validate(fields)
            self.row_dicts = sheet.get_all_records()
        else:
            with open(data_file, 'rb') as infile:
                # First row contains the column names
                csv_reader = unicodecsv.DictReader(infile, delimiter=('\t'), quotechar='|', encoding='utf-8')
                fields = csv_reader.fieldnames
            
                print("Fields: %s" % fields)
                valid_columns.validate(fields)

                # The rest of the rows contain data
                for row in csv_reader:
                    if len(fields) == len(row):
                        print("Another row: %s" % row)
                        self.row_dicts.append(row)
                        
                    else:
                        print("Incorrect number of fields in row!")
                        self.status += 1

    # format_string is probably not needed for a csv file,
    def format_string(self, value_str):
        values = value_str.split('\n')
        values = [v.strip() for v in values]
        return ' '.join(values)

    def print_meta_dicts(self, outfile='data_out.txt'):
        with open(outfile, 'wb') as fout:
            #pp = pprint.PrettyPrinter(stream=fout)
            pp = UTF8PrettyPrinter(stream=fout)
            for row in self.meta_dicts:
                pp.pprint(row)

    def status(self):
        return self.status

    def get_row_dict(self, n):
        return self.row_dicts[n]

    def get_row_dicts(self):
        return self.row_dicts

    def get_keys(self, n=0):
        return self.row_dicts[n].keys()

    def get_row_values(self, n=0):
        return self.row_dicts[n].values()

    def get_meta_dict_length(self):
        return len(self.meta_dicts)

    def get_meta_dict(self, n=0):
        return self.meta_dicts[n]

    def new_dict(self, asset_path):
        #meta_dict = OrderedDict()
        meta_dict = {}
        meta_dict['path'] = "%s" % asset_path
        meta_dict['properties'] = copy.deepcopy(self.meta_dict_properties_template)
        self.meta_dicts.append(meta_dict)
        return len(self.meta_dicts)-1

    def set_title(self, title, n):
        if self.verify_title(title):
            self.meta_dicts[n]['properties']['dc:title'] = "%s" % title

    def verify_title(self, title):
        print("Verifying title: %s" % title)
        return True if title else False

    def get_existing_data(self, filepath, metadata_path):
        if self.blankout == True:
            return []
        else:
            if self.data.get(filepath, None) == None:
                self.data[filepath] = nx.get_metadata(path=filepath)
            return self.data[filepath]['properties']['ucldc_schema:{}'.format(metadata_path)]

    def set_list_element(self, metadata_path, row_title, row, n):
        filepath = row['File path']
        element_list = self.get_existing_data(filepath, metadata_path)
        if row_title in str(row.keys()):
            for key in sorted(row.keys()):
                if row_title in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    try:
                        element_list[numb-1] = row[key]
                    except:
                        element_list.insert(numb-1, row[key])
        element_list = self.verify_list(element_list, metadata_path)
        print("Making %s item: %s" % (metadata_path, element_list))
        self.meta_dicts[n]['properties']['ucldc_schema:{}'.format(metadata_path)] = element_list

    def set_dict_element(self, metadata_path, row_title, row, n):
        filepath = row['File path']
        element_list = self.get_existing_data(filepath, metadata_path)
        if row_title in str(row.keys()):
            for key in sorted(row.keys()):
                if row_title in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = key.split(' ')
                    if elem[-1].isdigit() == True:
                        elem = elem[0].lower()
                    elif elem[-1] == 'ID' and elem[-2] == 'Authority':
                        elem = '{}{}'.format(elem[-2].lower(), elem[-1].lower())
                    elif elem[-1] == 'Type' and elem[-2] == 'Name' or elem[-2] == 'Heading':
                        elem = '{}{}'.format(elem[-2].lower(), elem[-1].lower())
                    elif elem[-1] == 'Start' or elem[-1] == 'End':
                        elem = 'inclusive{}'.format(elem[-1].lower())
                    elif elem[-1] == 'Type' and 'Date' in elem:
                        elem = 'date{}'.format(elem[-1].lower())
                    elif elem[-1] == 'Note':
                        elem = 'item'
                    else:
                        elem = elem[-1].lower()
                    try:
                        element_list[numb-1][elem] = row[key]
                    except:
                        element_list.insert(numb-1, {elem: row[key]})
        element_list = self.verify_list(element_list, metadata_path)
        print("Making %s item: %s" % (metadata_path, element_list))
        self.meta_dicts[n]['properties']['ucldc_schema:{}'.format(metadata_path)] = element_list


    def set_single_element(self, metadata_path, element, n):
        if self.verify_single(element, metadata_path):
            print("Making %s item: %s" % (metadata_path, element))
            self.meta_dicts[n]['properties']['ucldc_schema:{}'.format(metadata_path)] = element

    def verify_single(self, element, metadata_path):
        print('Verifying {}: {}'.format(metadata_path, element))
        if element != None and element != '':
            return True
        else:
            return False

    def verify_list(self, element_list, metadata_path):
        print('Verifying {}: {}'.format(metadata_path, element_list))
        for i, item in enumerate(element_list):
            if type(item) == dict:
                if all(value == '' for value in item.values()) or all(value == None for value in item.values()):
                    del element_list[i]
            else:
                if item == '' or item == 'None':
                    del element_list[i]
        return element_list
