#! /usr/bin/env python

__author__ = 'glen'

import sys
reload(sys)
sys.setdefaultencoding("utf8")


import argparse
import os.path
from Csv2Dict import Csv2Dict
from pynux import utils
import re

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
        date_data = csv2dict.get_existing_data(filepath, 'date')
        '''while 'Date %d' % num in str(row.keys()):
            if 'Date %d' % num not in row.keys():
                row['Date %d' % num] = date_data[num-1]['date']
            if 'Date %d Type' % num not in row.keys():
                row['Date %d Type' % num] = date_data[num-1]['datetype']
            if 'Date %d Inclusive Start' % num not in row.keys():
                row['Date %d Inclusive Start' % num] = date_data[num-1]['inclusivestart']
            if 'Date %d Inclusive End' % num not in row.keys():
                row['Date %d Inclusive End' % num] = date_data[num-1]['inclusiveend']
            if 'Date %d Single' % num not in row.keys():
                row['Date %d Single' % num] = date_data[num-1]['single']
            csv2dict.set_date(row['Date %d' % num],
                                 row['Date %d Type' % num],
                                 row['Date %d Inclusive Start' % num],
                                 row['Date %d Inclusive End' % num],
                                 row['Date %d Single' % num], n)
            num += 1'''

        if 'Date' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Date' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = key.split(' ')
                    if elem[-1].isdigit() == True:
                        elem = elem[0].lower()
                    elif elem[-1] == 'Start' or elem[-1] == 'End':
                        elem = 'inclusive{}'.format(elem[-1].lower())
                    else:
                        elem = elem[-1].lower()
                    try:
                        date_data[numb-1][elem] = row[key]
                    except:
                        date_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('date', date_data, n)


        num = 1
        while 'Publication/Origination Info %d' % num in row.keys():
            csv2dict.set_publication_origination(row['Publication/Origination Info %d' % num], n)
            num += 1


        num = 1
        creator_data = csv2dict.get_existing_data(filepath, 'creator')
        '''while 'Creator %d ' % num in str(row.keys()):
            if 'Creator %d Name' % num not in row.keys():
                row['Creator %d Name' % num] = creator_data[num-1]['name']
            if 'Creator %d Name Type' % num not in row.keys():
                row['Creator %d Name Type' % num] = creator_data[num-1]['nametype']
            if 'Creator %d Role' % num not in row.keys():   
                row['Creator %d Role' % num] = creator_data[num-1]['role']
            if 'Creator %d Source' % num not in row.keys():
                row['Creator %d Source' % num] = creator_data[num-1]['source']
            if 'Creator %d Authority ID' % num not in row.keys():
                row['Creator %d Authority ID' % num] = creator_data[num-1]['authorityid']
                
            csv2dict.set_creator(row['Creator %d Name' % num],
                                 row['Creator %d Name Type' % num],
                                 row['Creator %d Role' % num],
                                 row['Creator %d Source' % num],
                                 row['Creator %d Authority ID' % num], n)
            num += 1'''
        if 'Creator' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Creator' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = key.split(' ')
                    if elem[-1] == 'ID' or elem[-1] == 'Type':
                        elem = '{}{}'.format(elem[-2].lower(), elem[-1].lower())
                    else:
                        elem = elem[-1].lower()
                    try:
                        creator_data[numb-1][elem] = row[key]
                    except:
                        creator_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('creator', creator_data, n)

        num = 1
        contributor_data = csv2dict.get_existing_data(filepath, 'creator')
        '''while 'Contributor %d ' % num in str(row.keys()):
            if 'Contributor %d Name' % num not in row.keys():
                row['Contributor %d Name' % num] = contributor_data[num-1]['name']
            if 'Contributor %d Name Type' % num not in row.keys():
                row['Contributor %d Name Type' % num] = contributor_data[num-1]['nametype']
            if 'Contributor %d Role' % num not in row.keys():   
                row['Contributor %d Role' % num] = contributor_data[num-1]['role']
            if 'Contributor %d Source' % num not in row.keys():
                row['Contributor %d Source' % num] = contributor_data[num-1]['source']
            if 'Contributor %d Authority ID' % num not in row.keys():
                row['Contributor %d Authority ID' % num] = contributor_data[num-1]['authorityid']
            csv2dict.set_contributor(row['Contributor %d Name' % num],
                                 row['Contributor %d Name Type' % num],
                                 row['Contributor %d Role' % num],
                                 row['Contributor %d Source' % num],
                                 row['Contributor %d Authority ID' % num], n)
            num += 1'''
        
        if 'Contributor' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Contributor' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = key.split(' ')
                    if elem[-1] == 'ID' or elem[-1] == 'Type':
                        elem = '{}{}'.format(elem[-2].lower(), elem[-1].lower())
                    else:
                        elem = elem[-1].lower()
                    try:
                        contributor_data[numb-1][elem] = row[key]
                    except:
                        contributor_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('contributor', contributor_data, n)

        if 'Format/Physical Description' in row.keys():
            csv2dict.set_physdesc(row['Format/Physical Description'], n)
        
        
        description_data = csv2dict.get_existing_data(filepath, 'description')
        '''num = 1
        while 'Description %d ' % num in str(row.keys()):
            if 'Description %d Note' % num not in row.keys():
                row['Description %d Note' % num] = description_data[num-1]['item']
            if 'Description %d Type' % num not in row.keys():
                row['Description %d Type' % num] = description_data[num-1]['type']
            csv2dict.set_description(row['Description %d Note' % num],
                                     row['Description %d Type' % num], n)
            num += 1'''
            
        if 'Description' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Description' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = key.split(' ')
                    if elem[-1] == 'note':
                        elem = 'item'
                    else:
                        elem = elem[-1].lower()
                    try:
                        description_data[numb-1][elem] = row[key]
                    except:
                        description_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('description', description_data, n)

        if 'Extent' in row.keys():
            csv2dict.set_extent(row['Extent'], n)
         
            
        language_data = csv2dict.get_existing_data(filepath, 'language')
        '''num = 1
        while 'Language %d' % num in str(row.keys()):
            if 'Language %d' % num not in row.keys():
                row['Language %d' % num] = language_data[num-1]['language']
            if 'Language %d Code' % num not in row.keys():
                row['Language %d Code' % num] = language_data[num-1]['code']
            csv2dict.set_language(row['Language %d' % num],
                                row['Language %d Code' % num], n)
            num += 1'''
        if 'Language' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Language' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = key.split(' ')
                    if elem[-1].isdigit() == True:
                        elem = elem[0].lower()
                    else:
                        elem = elem[-1].lower()
                    try:
                        language_data[numb-1][elem] = row[key]
                    except:
                        language_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('language', language_data, n)
        
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
        
            
        copyright_holder_data = csv2dict.get_existing_data(filepath, 'rightsholder')
        num = 1
        '''while 'Copyright Holder %d ' % num in str(row.keys()):
            if 'Copyright Holder %d Name' % num not in row.keys():
                 row['Copyright Holder %d Name' % num] = copyright_holder_data[num-1]['name']
            if 'Copyright Holder %d Name Type' % num not in row.keys():
                 row['Copyright Holder %d Name Type' % num] = copyright_holder_data[num-1]['nametype']
            if 'Copyright Holder %d Source' % num not in row.keys():
                row['Copyright Holder %d Source' % num] = copyright_holder_data[num-1]['source']
            if 'Copyright Holder %d Authority ID' % num not in row.keys():
                row['Copyright Holder %d Authority ID' % num] = copyright_holder_data[num-1]['authorityid']
            csv2dict.set_rights_holder(row['Copyright Holder %d Name' % num],
                                   row['Copyright Holder %d Name Type' % num],
                                   row['Copyright Holder %d Source' % num],
                                   row['Copyright Holder %d Authority ID' % num], n)
            num += 1'''
        if 'Copyright Holder' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Copyright Holder' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    
                    elem = key.split(' ')
                    if elem[-1] == 'ID' or elem[-1] == 'Type':
                        elem = '{}{}'.format(elem[-2].lower(), elem[-1].lower())
                    else:
                        elem = elem[-1].lower()
                    try:
                        copyright_holder_data[numb-1][elem] = row[key]
                    except:
                        copyright_holder_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('rightsholder', copyright_holder_data, n)

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
        
            
        subject_name_data = csv2dict.get_existing_data(filepath, 'subjectname')
        '''num = 1 
        while 'Subject (Name) %d' % num in str(row.keys()):
            if 'Subject (Name) %d Name'% num not in row.keys():
                row['Subject (Name) %d Name' % num] = subject_name_data[num-1]['name']
            if 'Subject (Name) %d Name Type' % num not in row.keys():
                row['Subject (Name) %d Name Type' % num] = subject_name_data[num-1]['nametype']
            if 'Subject (Name) %d Role' % num not in row.keys():
                row['Subject (Name) %d Role' % num] = subject_name_data[num-1]['role']
            if 'Subject (Name) %d Source' % num not in row.keys():
                row['Subject (Name) %d Source' % num] = subject_name_data[num-1]['source']
            if 'Subject (Name) %d Authority ID' % num not in row.keys():
                row['Subject (Name) %d Authority ID' % num] = subject_name_data[num-1]['authorityid']
            
            csv2dict.set_subject_name(row['Subject (Name) %d Name' % num],
                                      row['Subject (Name) %d Name Type' % num],
                                      row['Subject (Name) %d Role' % num],
                                      row['Subject (Name) %d Source' % num],
                                      row['Subject (Name) %d Authority ID' % num], n)
            num += 1'''
        if 'Subject (Name)' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Subject (Name)' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    
                    elem = key.split(' ')
                    if elem[-1] == 'ID' or elem[-1] == 'Type':
                        elem = '{}{}'.format(elem[-2].lower(), elem[-1].lower())
                    else:
                        elem = elem[-1].lower()
                    try:
                        subject_name_data[numb-1][elem] = row[key]
                    except:
                        subject_name_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('subjectname', subject_name_data, n)

        place_data = csv2dict.get_existing_data(filepath, 'place')
        '''num = 1
        while 'Place %d ' % num in str(row.keys()):
            if 'Place %d Name' % num not in row.keys():
                row['Place %d Name' % num] = place_data[num-1]['name']
            if 'Place %d Source' % num not in row.keys():
                row['Place %d Source' % num] = place_data[num-1]['source']
            if 'Place %d Coordinates' % num not in row.keys():
                row['Place %d Coordinates' % num] = place_data[num-1]['coordinates']
            if 'Place %d Authority ID' % num not in row.keys():
                row['Place %d Authority ID' % num] = place_data[num-1]['authorityid']
            csv2dict.set_place(row['Place %d Name' % num],
                               row['Place %d Source' % num],
                               row['Place %d Coordinates' % num],
                               row['Place %d Authority ID' % num], n)
            num += 1'''
        if 'Place' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Place' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    
                    elem = key.split(' ')
                    if elem[-1] == 'ID' or elem[-1] == 'Type':
                        elem = '{}{}'.format(elem[-2].lower(), elem[-1].lower())
                    else:
                        elem = elem[-1].lower()
                    try:
                        place_data[numb-1][elem] = row[key]
                    except:
                        place_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('place', place_data, n)

        form_genre_data = csv2dict.get_existing_data(filepath, 'subjecttopic')
        '''num = 1
        while 'Form/Genre %d ' % num in str(row.keys()):
            if 'Form/Genre %d Heading' % num not in row.keys():
                row['Form/Genre %d Heading' % num] = form_genre_data[num-1]['heading']
            if 'Form/Genre %d Heading Type' % num not in row.keys():
                row['Form/Genre %d Heading Type' % num] = form_genre_data[num-1]['headingtype']
            if 'Form/Genre %d Source' % num not in row.keys():
                row['Form/Genre %d Source' % num] = form_genre_data[num-1]['source']
            if 'Form/Genre %d Authority ID' not in row.keys():
                row['Form/Genre %d Authority ID' % num] = form_genre_data[num-1]['authorityid']
            csv2dict.set_form_genre(row['Form/Genre %d Heading' % num],
                                       row['Form/Genre %d Heading Type' % num],
                                       row['Form/Genre %d Source' % num],
                                       row['Form/Genre %d Authority ID' % num], n)
            num += 1'''
        if 'Form/Genre' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Form/Genre' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    
                    elem = key.split(' ')
                    if elem[-1] == 'ID' or elem[-1] == 'Type':
                        elem = '{}{}'.format(elem[-2].lower(), elem[-1].lower())
                    else:
                        elem = elem[-1].lower()
                    try:
                        form_genre_data[numb-1][elem] = row[key]
                    except:
                        form_genre_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('subjecttopic', form_genre_data, n)

        num = 1
        form_genre_data = csv2dict.get_existing_data(filepath, 'formgenre')
        '''while 'Form/Genre %d ' % num in str(row.keys()):
            if 'Form/Genre %d Heading' % num not in row.keys():
                row['Form/Genre %d Heading' % num] = form_genre_data[num-1]['heading']
            if 'Form/Genre %d Source' % num not in row.keys():
                row['Form/Genre %d Source' % num] = form_genre_data[num-1]['source']
            if 'Form/Genre %d Authority ID' not in row.keys():
                row['Form/Genre %d Authority ID' % num] = form_genre_data[num-1]['authorityid']
            csv2dict.set_form_genre(row['Form/Genre %d Heading' % num],
                                    row['Form/Genre %d Source' % num],
                                    row['Form/Genre %d Authority ID' % num], n)
            num += 1'''
                
        if 'Form/Genre' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Form/Genre' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = key.split(' ')
                    if elem[-1] == 'ID' or elem[-1] == 'Type':
                        elem = '{}{}'.format(elem[-2].lower(), elem[-1].lower())
                    else:
                        elem = elem[-1].lower()
                    try:
                        form_genre_data[numb-1][elem] = row[key]
                    except:
                        form_genre_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('formgenre', form_genre_data, n)
            
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
