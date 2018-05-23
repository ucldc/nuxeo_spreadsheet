#! /usr/bin/env python

__author__ = 'glen'

import sys
try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:
    from importlib import reload
    reload(sys)

import argparse
import os.path
from Csv2Dict import Csv2Dict
from pynux import utils

def process_rows(csv2dict):
    row_dicts = csv2dict.get_row_dicts()
    element_data = {
    "list_elements":[
    {'metadata_path':'alternativetitle', 'row_title':'Alternative Title'},
    {'metadata_path':'localidentifier', 'row_title':'Local Identifier'},
    {'metadata_path':'campusunit', 'row_title':'Campus/Unit'},
    {'metadata_path':'publisher', 'row_title':'Publication/Origination Info'},
    {'metadata_path':'temporalcoverage', 'row_title':'Temporal Coverage'} ,
    {'metadata_path':'collection', 'row_title':'Collection'},
    {'metadata_path':'relatedresource', 'row_title':'Related Resource'},
    {'metadata_path':'provenance', 'row_title':'Provenance'}
     ],
    "single_elements":[
    {'metadata_path':'identifier', 'row_title':'Identifier'},
    {'metadata_path':'type', 'row_title':'Type'},
    {'metadata_path':'physdesc', 'row_title':'Format/Physical Description'},
    {'metadata_path':'extent', 'row_title':'Extent'},
    {'metadata_path':'transcription', 'row_title':'Transcription'},
    {'metadata_path':'accessrestrict', 'row_title':'Access Restrictions'},
    {'metadata_path':'rightsstatement', 'row_title':'Copyright Statement'},
    {'metadata_path':'rightsstatus', 'row_title':'Copyright Status'},
    {'metadata_path':'rightscontact', 'row_title':'Copyright Contact'},
    {'metadata_path':'rightsnotice', 'row_title':'Copyright Notice'},
    {'metadata_path':'rightsdeterminationdate', 'row_title':'Copyright Determination Date'},
    {'metadata_path':'rightsstartdate', 'row_title':'Copyright Start Date'},
    {'metadata_path':'rightsenddate', 'row_title':'Copyright End Date'},
    {'metadata_path':'rightsjurisdiction', 'row_title':'Copyright Jurisdiction'},     
    {'metadata_path':'rightsnote', 'row_title':'Copyright Note'},
    {'metadata_path':'source', 'row_title':'Source'},
    {'metadata_path':'physlocation', 'row_title':'Physical Location'}
    ],     
    "dict_elements":[
    {'metadata_path':'date', 'row_title':'Date'},
    {'metadata_path':'creator', 'row_title':'Creator'},
    {'metadata_path':'contributor', 'row_title':'Contributor'},
    {'metadata_path':'description', 'row_title':'Description'},
    {'metadata_path':'language', 'row_title':'Language'},
    {'metadata_path':'subjectname', 'row_title':'Subject (Name)'},
    {'metadata_path':'place', 'row_title':'Place'},
    {'metadata_path':'subjecttopic', 'row_title':'Subject (Topic)'},
    {'metadata_path':'formgenre', 'row_title':'Form/Genre'},
    {'metadata_path':'rightsholder', 'row_title':'Copyright Holder'}
    ]
    }


    for n in range(len(row_dicts)):
        print('Metarow%3d) %s' % (n, str(row_dicts[n])))

    for row in row_dicts:
        '''
        Csv2Dict.new_dict(path) creates a new dict with two keys, 'path'
        and 'properties'. The value of 'path' is the asset_path, and
        the value of 'properties' is an empty dict to be filled in later.
        This structure is appended to a List of dicts, one dict for each
        row in the csv file, returning the new dict's position in the List.
        '''
        n = csv2dict.new_dict(row['File path'])
        filepath = row['File path']

        if 'Title' in row.keys():
            csv2dict.set_title(row['Title'], n)

        for key, value in element_data.items():
            for list_data in value:
                if key == 'list_elements':
                    if list_data['row_title'] in str(row.keys()):
                        csv2dict.set_list_element(list_data['metadata_path'], list_data['row_title'], row, n)
                if key == 'single_elements':
                    if list_data['row_title'] in row.keys():
                        csv2dict.set_single_element(list_data['metadata_path'], row[list_data['row_title']], n)
                if key == 'dict_elements':
                    formatted_row_title = '%s '%list_data['row_title']
                    if formatted_row_title in str(row.keys()):
                        csv2dict.set_dict_element(list_data['metadata_path'], formatted_row_title, row, n)


def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("--datafile", type=str, required=True,
                         help="tab-delimited spreadsheet input file -- required")

    parser.add_argument('-d', '--dry-run', action='store_true',
                         help='dry run')

    parser.add_argument('--blankout', action='store_true',
                         help='blank out all fields not set in sheet')

    parser.add_argument('--sheet', type=str, required=False,
                         help='Gets sheet from google spreadsheet using the sheet Title')

    utils.get_common_options(parser)

    args = parser.parse_args()

    try:
        assert os.path.isfile( args.datafile )
    except AssertionError:
        if 'google' in args.datafile:
            pass
        else:
            print("Not a file: ", args.datafile)
            sys.exit(2)

    csv_data_file = args.datafile
    print(csv_data_file)
    print(args.rcfile)
    print(args.loglevel)

    nx = utils.Nuxeo(rcfile=args.rcfile, loglevel=args.loglevel.upper())
    nuxeo_limit = 24

    # get and instance of the Csv2Dict class which must be initialized
    # with the name of an input data (csv) file

    csv2dict = Csv2Dict(csv_data_file, blankout=args.blankout, sheet=args.sheet, nx=nx)

    if csv2dict.status != 0:
        print('The Csv2Dict constructor reported and error (%d).' % csv2dict.status)
        sys.exit(csv2dict.status)

    process_rows(csv2dict)

    for n in range(csv2dict.get_meta_dict_length()):
        print("Loading payload %d" % n)
        payload = csv2dict.get_meta_dict(n)
        print(payload)
        print(payload['path'])
        if not args.dry_run:
            uid = nx.get_uid(payload['path'])
            print("Returned UID: %d) %s." % (n, uid))
            nx.update_nuxeo_properties(payload, path=payload['path'])
            
    # csv2dict.print_meta_dicts('LOGS/latest_output.txt')

if __name__ == '__main__':

    main(sys.argv)
