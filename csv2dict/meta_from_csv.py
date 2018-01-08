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

        if 'Title' in row.keys():
            csv2dict.set_title(row['Title'], n)
            
        num = 1
        while 'Alternative Title %d' % num in row.keys():
            csv2dict.set_alt_title(row['Alternative Title %d' % num], n)
            num += 1

        if 'Identifier' in row.keys():
            csv2dict.set_id(row['Identifier'], n)
            
        
        num = 1
        while 'Local Identifier %d' % num in row.keys():
            csv2dict.set_local_id(row['Local Identifier %d' % num], n)
            num += 1

        if 'Type' in row.keys():
            csv2dict.set_type(row['Type'], n)
        
        
        num = 1
        while 'Campus/Unit %d' % num in row.keys():
            csv2dict.set_campus_unit(row['Campus/Unit %d' % num], n)
            num += 1

        num = 1
        while 'Date %d' % num in str(row.keys()):
            if 'Date %d' % num not in row.keys():
                row['Date %d' % num] = ''
            if 'Date %d Type' % num not in row.keys():
                row['Date %d Type' % num] = ''
            if 'Date %d Inclusive Start' % num not in row.keys():
                row['Date %d Inclusive Start' % num] = ''
            if 'Date %d Inclusive End' % num not in row.keys():
                row['Date %d Inclusive End' % num] = ''
            if 'Date %d Single' % num not in row.keys():
                row['Date %d Single' % num] = ''
            csv2dict.set_date(row['Date %d' % num],
                                 row['Date %d Type' % num],
                                 row['Date %d Inclusive Start' % num],
                                 row['Date %d Inclusive End' % num],
                                 row['Date %d Single' % num], n)
            num += 1


        num = 1
        while 'Publication/Origination Info %d' % num in row.keys():
            csv2dict.set_publication_origination(row['Publication/Origination Info %d' % num], n)
            num += 1


        num = 1
        while 'Creator %d ' % num in str(row.keys()):
            if 'Creator %d Name' % num not in row.keys():
                row['Creator %d Name' % num] = ''
            if 'Creator %d Name Type' % num not in row.keys():
                row['Creator %d Name Type' % num] = ''
            if 'Creator %d Role' % num not in row.keys():   
                row['Creator %d Role' % num] = ''
            if 'Creator %d Source' % num not in row.keys():
                row['Creator %d Source' % num] = ''
            if 'Creator %d Authority ID' % num not in row.keys():
                row['Creator %d Authority ID' % num] = ''
                
            csv2dict.set_creator(row['Creator %d Name' % num],
                                 row['Creator %d Name Type' % num],
                                 row['Creator %d Role' % num],
                                 row['Creator %d Source' % num],
                                 row['Creator %d Authority ID' % num], n)
            num += 1

        num = 1
        while 'Contributor %d ' % num in str(row.keys()):
            if 'Contributor %d Name' % num not in row.keys():
                row['Contributor %d Name' % num] = ''
            if 'Contributor %d Name Type' % num not in row.keys():
                row['Contributor %d Name Type' % num] = ''
            if 'Contributor %d Role' % num not in row.keys():   
                row['Contributor %d Role' % num] = ''
            if 'Contributor %d Source' % num not in row.keys():
                row['Contributor %d Source' % num] = ''
            if 'Contributor %d Authority ID' % num not in row.keys():
                row['Contributor %d Authority ID' % num] = ''
            csv2dict.set_contributor(row['Contributor %d Name' % num],
                                 row['Contributor %d Name Type' % num],
                                 row['Contributor %d Role' % num],
                                 row['Contributor %d Source' % num],
                                 row['Contributor %d Authority ID' % num], n)
            num += 1

        if 'Format/Physical Description' in row.keys():
            csv2dict.set_physdesc(row['Format/Physical Description'], n)
        
            
        num = 1
        while 'Description %d ' % num in str(row.keys()):
            if 'Description %d Note' % num not in row.keys():
                row['Description %d Type' % num] = ''
            if 'Description %d Type' % num not in row.keys():
                row['Description %d Type' % num] = ''
            csv2dict.set_description(row['Description %d Note' % num],
                                     row['Description %d Type' % num], n)
            num += 1

        if 'Extent' in row.keys():
            csv2dict.set_extent(row['Extent'], n)
         
            
        num = 1
        while 'Language %d' % num in str(row.keys()):
            if 'Language %d' % num not in row.keys():
                row['Language %d' % num] = ''
            if 'Language %d Code' % num not in row.keys():
                row['Language %d Code' % num] = ''
            csv2dict.set_language(row['Language %d' % num],
                                row['Language %d Code' % num], n)
            num += 1
        
        num = 1
        while 'Temporal Coverage %d' % num in row.keys():
            csv2dict.set_temporal_coverage(row['Temporal Coverage %d' % num], n)
            num += 1    
        
        if 'Transcription' in row.keys():
            csv2dict.set_transcription(row['Transcription'], n)
        
        if 'Access Restrictions' in row.keys():
            csv2dict.set_access_restrictions(row['Access Restrictions'], n)
        
        if 'Copyright Statement' in row.keys():
            csv2dict.set_rights_statement(row['Copyright Statement'], n)
        
        if 'Copyright Status' in row.keys():
            csv2dict.set_rights_status(row['Copyright Status'], n)
        
            
        num = 1
        while 'Copyright Holder %d ' % num in str(row.keys()):
            if 'Copyright Holder %d Name' % num not in row.keys():
                 row['Copyright Holder %d Name' % num] = ''
            if 'Copyright Holder %d Name Type' % num not in row.keys():
                 row['Copyright Holder %d Name Type' % num] = ''
            if 'Copyright Holder %d Source' % num not in row.keys():
                row['Copyright Holder %d Source' % num] = ''
            if 'Copyright Holder %d Authority ID' % num not in row.keys():
                row['Copyright Holder %d Authority ID' % num] = ''
            csv2dict.set_rights_holder(row['Copyright Holder %d Name' % num],
                                   row['Copyright Holder %d Name Type' % num],
                                   row['Copyright Holder %d Source' % num],
                                   row['Copyright Holder %d Authority ID' % num], n)
            num += 1

        if 'Copyright Contact' in row.keys():
            csv2dict.set_rights_contact(row['Copyright Contact'], n)
        
        if 'Copyright Notice' in row.keys():
            csv2dict.set_rights_notice(row['Copyright Notice'], n)
        
        if 'Copyright Determination Date' in row.keys():    
            csv2dict.set_rights_determination_date(row['Copyright Determination Date'], n)
        
        if 'Copyright Start Date' in row.keys():
            csv2dict.set_rights_start_date(row['Copyright Start Date'], n)
        
        if 'Copyright End Date' in row.keys():
            csv2dict.set_rights_end_date(row['Copyright End Date'], n)
        
        if 'Copyright Jurisdiction' in row.keys():
            csv2dict.set_rights_jurisdiction(row['Copyright Jurisdiction'], n)
        
        if 'Copyright Note' in row.keys():    
            csv2dict.set_rights_note(row['Copyright Note'], n)
        
            
        num = 1
        while 'Collection %d' % num in row.keys():
            csv2dict.set_collection(row['Collection %d' % num], n)
            num += 1

        num = 1
        while 'Related Resource %d' % num in row.keys():
            csv2dict.set_related_resource(row['Related Resource %d' % num], n)
            num += 1

        if 'Source' in row.keys():
            csv2dict.set_source(row['Source'], n)
        
            
        num = 1
        while 'Subject (Name) %d' % num in str(row.keys()):
            if 'Subject (Name) %d Name'% num not in row.keys():
                row['Subject (Name) %d Name' % num] = ''
            if 'Subject (Name) %d Name Type' % num not in row.keys():
                row['Subject (Name) %d Name Type' % num] = ''
            if 'Subject (Name) %d Role' % num not in row.keys():
                row['Subject (Name) %d Role' % num] = ''
            if 'Subject (Name) %d Source' % num not in row.keys():
                row['Subject (Name) %d Source' % num] = ''
            if 'Subject (Name) %d Authority ID' % num not in row.keys():
                row['Subject (Name) %d Authority ID' % num] = ''
        	
            csv2dict.set_subject_name(row['Subject (Name) %d Name' % num],
                                      row['Subject (Name) %d Name Type' % num],
                                      row['Subject (Name) %d Role' % num],
                                      row['Subject (Name) %d Source' % num],
                                      row['Subject (Name) %d Authority ID' % num], n)
            num += 1

        num = 1
        while 'Place %d ' % num in str(row.keys()):
            if 'Place %d Name' % num not in row.keys():
                row['Place %d Name' % num] = ''
            if 'Place %d Source' % num not in row.keys():
                row['Place %d Source' % num] = ''
            if 'Place %d Coordinates' % num not in row.keys():
                row['Place %d Coordinates' % num] = ''
            if 'Place %d Authority ID' % num not in row.keys():
                row['Place %d Authority ID' % num] = ''
            csv2dict.set_place(row['Place %d Name' % num],
                               row['Place %d Source' % num],
                               row['Place %d Coordinates' % num],
                               row['Place %d Authority ID' % num], n)
            num += 1

        num = 1
        while 'Subject (Topic) %d ' % num in str(row.keys()):
            print "Calling set_subject_topic with: %s" % 'Subject (Topic) %d Heading' % num
            if 'Subject (Topic) %d Heading' % num not in row.keys():
                row['Subject (Topic) %d Heading' % num] = ''
            if 'Subject (Topic) %d Heading Type' % num not in row.keys():
                row['Subject (Topic) %d Heading Type' % num] = ''
            if 'Subject (Topic) %d Source' % num not in row.keys():
                row['Subject (Topic) %d Source' % num] = ''
            if 'Subject (Topic) %d Authority ID' not in row.keys():
                row['Subject (Topic) %d Authority ID' % num] = ''
            csv2dict.set_subject_topic(row['Subject (Topic) %d Heading' % num],
                                       row['Subject (Topic) %d Heading Type' % num],
                                       row['Subject (Topic) %d Source' % num],
                                       row['Subject (Topic) %d Authority ID' % num], n)
            num += 1

        num = 1
        while 'Form/Genre %d ' % num in str(row.keys()):
            if 'Form/Genre %d Heading' % num not in row.keys():
                row['Form/Genre %d Heading' % num] = ''
            if 'Form/Genre %d Source' % num not in row.keys():
                row['Form/Genre %d Source' % num] = ''
            if 'Form/Genre %d Authority ID' not in row.keys():
                row['Form/Genre %d Authority ID' % num] = ''
            csv2dict.set_form_genre(row['Form/Genre %d Heading' % num],
                                    row['Form/Genre %d Source' % num],
                                    row['Form/Genre %d Authority ID' % num], n)
            num += 1

        num = 1
        while 'Provenance %d' % num in row.keys():
            csv2dict.set_provenance(row['Provenance %d' % num], n)
            num += 1

        if 'Physical Location' in row.keys():
            csv2dict.set_physical_location(row['Physical Location'], n)
        
    

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
