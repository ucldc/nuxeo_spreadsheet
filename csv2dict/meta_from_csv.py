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
            
        alttitle_data = csv2dict.get_existing_data(filepath, 'localidentifier')
        if 'Alternative Title' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Alternative Title' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = 'alternativetitle'
                    try:
                        alttitle_data[numb-1] = row[key]
                    except:
                        alttitle_data.insert(numb-1, row[key])
            
            csv2dict.set_element('alternativetitle', alttitle_data, n)
        

        if 'Identifier' in row.keys():
            csv2dict.set_single_element('identifier', row['Identifier'], n)
            
        locid_data = csv2dict.get_existing_data(filepath, 'localidentifier')
        if 'Local Identifier' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Local Identifier' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = 'localidentifier'
                    try:
                        locid_data[numb-1][elem] = row[key]
                    except:
                        locid_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('localidentifier', locid_data, n)

        if 'Type' in row.keys():
            csv2dict.set_single_element('type', row['Type'], n)
        
        campusunit_data = csv2dict.get_existing_data(filepath, 'campusunit')
        if 'Campus/Unit' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Campus/Unit' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = 'campusunit'
                    try:
                        campusunit_data[numb-1][elem] = row[key]
                    except:
                        campusunit_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('campusunit', campusunit_data, n)

        num = 1
        date_data = csv2dict.get_existing_data(filepath, 'date')
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


        publisher_data = csv2dict.get_existing_data(filepath, 'publisher')
        if 'Publication/Origination Info' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Publication/Origination Info' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = 'publisher'
                    try:
                        publisher_data[numb-1][elem] = row[key]
                    except:
                        publisher_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('publisher', publisher_data, n)


        num = 1
        creator_data = csv2dict.get_existing_data(filepath, 'creator')
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
            csv2dict.set_single_element('physdesc', row['Format/Physical Description'], n)
        
        
        description_data = csv2dict.get_existing_data(filepath, 'description')
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
            csv2dict.set_single_element('extent', row['Extent'], n)
         
            
        language_data = csv2dict.get_existing_data(filepath, 'language')
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
         
        temporalcoverage_data = csv2dict.get_existing_data(filepath, 'temporalcoverage')
        if 'Temporal Coverage' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Temporal Coverage' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = key.split(' ')
                    if elem[-1].isdigit() == True:
                        elem = elem[0].lower()
                    else:
                        elem = elem[-1].lower()
                    try:
                        temporalcoverage_data[numb-1][elem] = row[key]
                    except:
                        temporalcoverage_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('temporalcoverage', temporalcoverage_data, n)
            
        if 'Transcription' in row.keys():
            csv2dict.set_single_element('transcription', row['Transcription'], n)
        
        if 'Access Restrictions' in row.keys():
            csv2dict.set_single_element('accessrestrict', row['Access Restrictions'], n)
        
        if 'Copyright Statement' in row.keys():
            csv2dict.set_single_element('rightsstatement', row['Copyright Statement'], n)
        
        if 'Copyright Status' in row.keys():
            csv2dict.set_single_element('rightsstatus', row['Copyright Status'], n)
        
            
        copyright_holder_data = csv2dict.get_existing_data(filepath, 'rightsholder')
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
        
		collection_data = csv2dict.get_existing_data(filepath, 'collection')
        if 'Collection' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Collection' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = 'collection'
                    try:
                        collection_data[numb-1][elem] = row[key]
                    except:
                        collection_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('collection', collection_data, n)

        relatedresource_data = csv2dict.get_existing_data(filepath, 'relatedresource')
        if 'Related Resource' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Related Resource' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = 'relatedresource'
                    try:
                        relatedresource_data[numb-1][elem] = row[key]
                    except:
                        relatedresource_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('relatedresource', relatedresource_data, n)

        if 'Source' in row.keys():
            csv2dict.set_single_element('source', row['Source'], n)
        
            
        subject_name_data = csv2dict.get_existing_data(filepath, 'subjectname')
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

        subject_topic_data = csv2dict.get_existing_data(filepath, 'subjecttopic')
        if 'Subject (Topic)' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Subject (Topic)' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    
                    elem = key.split(' ')
                    if elem[-1] == 'ID' or elem[-1] == 'Type':
                        elem = '{}{}'.format(elem[-2].lower(), elem[-1].lower())
                    else:
                        elem = elem[-1].lower()
                    try:
                        subject_topic_data[numb-1][elem] = row[key]
                    except:
                        subject_topic_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('subjecttopic', subject_topic_data, n)

        form_genre_data = csv2dict.get_existing_data(filepath, 'formgenre')
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
            
        provenance_data = csv2dict.get_existing_data(filepath, 'provenance')
        if 'Provenance' in str(row.keys()):
            for key in sorted(row.keys()):
                if 'Provenance' in key:
                    numb = int(re.findall(r'\d+', key)[0])
                    elem = key.split(' ')
                    if elem[-1].isdigit() == True:
                        elem = elem[0].lower()
                    else:
                        elem = elem[-1].lower()
                    try:
                        provenance_data[numb-1][elem] = row[key]
                    except:
                        provenance_data.insert(numb-1, {elem: row[key]})
            
            csv2dict.set_element('provenance', provenance_data, n)

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
