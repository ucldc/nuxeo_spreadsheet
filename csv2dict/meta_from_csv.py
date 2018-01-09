#! /usr/bin/env python

__author__ = 'glen'

import sys
reload(sys)
sys.setdefaultencoding("utf8")


import argparse
import os.path
from Csv2Dict import Csv2Dict
from pynux import utils

def process_rows( csv2dict):
    row_dicts = csv2dict.get_row_dicts()

    for n in range(len(row_dicts)):
        print 'Metarow%3d) %s' % (n, str(row_dicts[n]))

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
        
        if 'Alternative Title' in str(row.keys()):
        	csv2dict.set_list_element('alternativetitle', 'Alternative Title', 
        						row, n)

        if 'Identifier' in row.keys():
            csv2dict.set_single_element('identifier', row['Identifier'], n)
            
        if 'Local Identifier' in str(row.keys()):
        	csv2dict.set_list_element('localidentifier', 'Local Identifier', 
        						row, n)
        						
        if 'Type' in row.keys():
            csv2dict.set_single_element('type', row['Type'], n)
        
        if 'Campus/Unit' in str(row.keys()):
            csv2dict.set_list_element('campusunit', 'Campus/Unit', 
        						row, n)

        if 'Date ' in str(row.keys()):
            csv2dict.set_dict_element('date', 'Date ', row, n)

        if 'Publication/Origination Info' in str(row.keys()):     
            csv2dict.set_list_element('publisher', 'Publication/Origination Info', row, n)

        if 'Creator ' in str(row.keys()):
            csv2dict.set_dict_element('creator', 'Creator ', row, n)

        if 'Contributor ' in str(row.keys()):
            csv2dict.set_dict_element('contributor', 'Contributor ', row, n)

        if 'Format/Physical Description' in row.keys():
            csv2dict.set_single_element('physdesc', row['Format/Physical Description'], n)
        
        if 'Description ' in str(row.keys()):
            csv2dict.set_dict_element('description', 'Description ', row, n)

        if 'Extent' in row.keys():
            csv2dict.set_single_element('extent', row['Extent'], n)
            
        if 'Language' in str(row.keys()):
            csv2dict.set_dict_element('language', 'Language ', row, n)
         
        if 'Temporal Coverage' in str(row.keys()):
            csv2dict.set_list_element('temporalcoverage', 'Temporal Coverage', row, n)
            
        if 'Transcription' in row.keys():
            csv2dict.set_single_element('transcription', row['Transcription'], n)
        
        if 'Access Restrictions' in row.keys():
            csv2dict.set_single_element('accessrestrict', row['Access Restrictions'], n)
        
        if 'Copyright Statement' in row.keys():
            csv2dict.set_single_element('rightsstatement', row['Copyright Statement'], n)
        
        if 'Copyright Status' in row.keys():
            csv2dict.set_single_element('rightsstatus', row['Copyright Status'], n)
        
        if 'Copyright Holder' in str(row.keys()):
            csv2dict.set_dict_element('rightsholder', 'Copyright Holder ', row, n)

        if 'Copyright Contact' in row.keys():
            csv2dict.set_single_element('rightscontact', row['Copyright Contact'], n)
        
        if 'Copyright Notice' in row.keys():
            csv2dict.set_single_element('rightsnotice', row['Copyright Notice'], n)
        
        if 'Copyright Determination Date' in row.keys():    
            csv2dict.set_single_element('rightsdeterminationdate', row['Copyright Determination Date'], n)
        
        if 'Copyright Start Date' in row.keys():
            csv2dict.set_single_element('rightsstartdate', row['Copyright Start Date'], n)
        
        if 'Copyright End Date' in row.keys():
            csv2dict.set_single_element('rightsenddate', row['Copyright End Date'], n)
        
        if 'Copyright Jurisdiction' in row.keys():
            csv2dict.set_single_element('rightsjurisdiction', row['Copyright Jurisdiction'], n)
        
        if 'Copyright Note' in row.keys():    
            csv2dict.set_single_element('rightsnote', row['Copyright Note'], n)
        
        if 'Collection' in str(row.keys()):
            csv2dict.set_list_element('collection', 'Collection', row, n)

        if 'Related Resource' in str(row.keys()):
            csv2dict.set_list_element('relatedresource', 'Related Resource', row, n)

        if 'Source' in row.keys():
            csv2dict.set_single_element('source', row['Source'], n)
        
        if 'Subject (Name) ' in str(row.keys()):
            csv2dict.set_dict_element('subjectname', 'Subject (Name) ', row, n)

        if 'Place ' in str(row.keys()):
            csv2dict.set_dict_element('place', 'Place ', row, n)

        if 'Subject (Topic) ' in str(row.keys()):
            csv2dict.set_dict_element('subjecttopic', 'Subject (Topic) ', row, n)

        if 'Form/Genre ' in str(row.keys()):
            csv2dict.set_dict_element('formgenre', 'Form/Genre ', row, n)
            
        if 'Provenance' in str(row.keys()):
            csv2dict.set_list_element('provenance', 'Provenance', row, n)

        if 'Physical Location' in row.keys():
            csv2dict.set_single_element('physlocation', row['Physical Location'], n)
        
    

def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("--datafile", type=str, required=True,
                         help="tab-delimited spreadsheet input file -- required")

    parser.add_argument('-d', '--dry-run', action='store_true',
                         help='dry run')

    parser.add_argument('--blankout', action='store_true',
                         help='blank out all fields not set in sheet')

    utils.get_common_options(parser)

    args = parser.parse_args()

    try:
        assert os.path.isfile( args.datafile )
    except AssertionError:
        print "Not a file: ", args.datafile
        sys.exit(2)

    csv_data_file = args.datafile
    print csv_data_file
    print args.rcfile
    print args.loglevel

    nx = utils.Nuxeo(rcfile=args.rcfile, loglevel=args.loglevel.upper())
    nuxeo_limit = 24

    # get and instance of the Csv2Dict class which must be initialized
    # with the name of an input data (csv) file

    csv2dict = Csv2Dict(csv_data_file, blankout=args.blankout)

    if csv2dict.status != 0:
        print 'The Csv2Dict constructor reported and error (%d).' % csv2dict.status
        sys.exit(csv2dict.status)

    process_rows(csv2dict)

    for n in range(csv2dict.get_meta_dict_length()):
        print "Loading payload %d" % n
        payload = csv2dict.get_meta_dict(n)
        print payload
        print payload['path']
        if not args.dry_run:
            uid = nx.get_uid(payload['path'])
            print "Returned UID: %d) %s." % (n, uid)
            nx.update_nuxeo_properties(payload, path=payload['path'])
            
    # csv2dict.print_meta_dicts('LOGS/latest_output.txt')

if __name__ == '__main__':

    main(sys.argv)
