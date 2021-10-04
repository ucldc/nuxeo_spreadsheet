"""
This script allows the users to download metadata from Nuxeo
and save to either a Google Sheets spreadsheet or a local TSV file

It allows for metadata to be downloaded at the object level
(one spreadsheet row per parent-level digital object), or item level
(one spreadsheet row per any item, including each component of a complex object)

It also asks if all headers should be downloaded, or if properties with
null values in Nuxeo should be excluded from the export.

First written by Niqui O'Neill (UCLA Digital Library Program) in 2018.
"""
import os
import unicodecsv as csv
from pynux import utils

try:
    filepath = raw_input('Enter Nuxeo File Path: ')
except:
    filepath = input('Enter Nuxeo File Path: ')
try:
    choice = raw_input('Object Level (ENTER O) or Item Level (ENTER I): ')
except:
    choice = input('Object Level (ENTER O) or Item Level (ENTER I): ')
try:
    url = raw_input('Enter Google Sheet URL: ')
except:
    url = input('Enter Google Sheet URL: ')
try:
    all_headers = raw_input('All Headers? (Y/N): ')
except:
    all_headers = input('All Headers? (Y/N): ')

filepath = filepath.strip()
choice = choice.lower().strip()
url = url.strip()
all_headers = choice.lower().strip()


def get_title(data2, x):
    """gets title
    """
    data2['Title'] = x['properties']['dc:title']


def get_filepath(data2, x):
    """gets filepath
    """
    data2['File path'] = x['path']


def get_type(data2, x, all_headers):
    """gets type,
    inputs are dictionary (data2), nuxeo (x), all_headers input
    """
    if x['properties']['ucldc_schema:type'] != None and x['properties'][
            'ucldc_schema:type'] != '':
        data2['Type'] = x['properties']['ucldc_schema:type']
    elif all_headers == 'y':
        data2['Type'] = ''


def get_alt_title(data2, x, all_headers):
    altnumb = 0
    if type(x['properties']['ucldc_schema:alternativetitle']) == list and len(
            x['properties']['ucldc_schema:alternativetitle']) > 0:
        while altnumb < len(x['properties']['ucldc_schema:alternativetitle']):
            numb = altnumb + 1
            name = 'Alternative Title %d' % numb
            data2[name] = x['properties']['ucldc_schema:alternativetitle'][
                altnumb]
            altnumb += 1
    elif all_headers == 'y':
        data2['Alternative Title 1'] = ''


def get_identifier(data2, x, all_headers):
    if x['properties']['ucldc_schema:identifier'] != None and x['properties'][
            'ucldc_schema:identifier'] != '':
        data2['Identifier'] = x['properties']['ucldc_schema:identifier']
    elif all_headers == 'y':
        data2['Identifier'] = ''


def get_local_identifier(data2, x, all_headers):
    locnumb = 0
    if type(x['properties']['ucldc_schema:localidentifier']) == list and len(
            x['properties']['ucldc_schema:localidentifier']) > 0:
        while locnumb < len(x['properties']['ucldc_schema:localidentifier']):
            numb = locnumb + 1
            name = 'Local Identifier %d' % numb
            data2[name] = x['properties']['ucldc_schema:localidentifier'][
                locnumb]
            locnumb += 1
    elif all_headers == 'y':
        data2['Local Identifier 1'] = ''


def get_campus_unit(data2, x, all_headers):
    campnumb = 0
    if type(x['properties']['ucldc_schema:campusunit']) == list and len(
            x['properties']['ucldc_schema:campusunit']) > 0:
        while campnumb < len(x['properties']['ucldc_schema:campusunit']):
            numb = campnumb + 1
            name = 'Campus/Unit %d' % numb
            data2[name] = x['properties']['ucldc_schema:campusunit'][campnumb]
            campnumb += 1
    elif all_headers == 'y':
        data2['Campus/Unit 1'] = ''


def get_date(data2, x, all_headers):
    datenumb = 0
    if type(x['properties']['ucldc_schema:date']) == list and len(
            x['properties']['ucldc_schema:date']) > 0:
        while datenumb < len(x['properties']['ucldc_schema:date']):
            numb = datenumb + 1
            try:
                name = 'Date %d' % numb
                if x['properties']['ucldc_schema:date'][datenumb][
                        'date'] != None and x['properties'][
                            'ucldc_schema:date'][datenumb]['date'] != '':
                    data2[name] = x['properties']['ucldc_schema:date'][
                        datenumb]['date']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Date %d Type' % numb
                if x['properties']['ucldc_schema:date'][datenumb][
                        'datetype'] != None and x['properties'][
                            'ucldc_schema:date'][datenumb]['datetype'] != '':
                    data2[name] = x['properties']['ucldc_schema:date'][
                        datenumb]['datetype']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Date %d Inclusive Start' % numb
                if x['properties']['ucldc_schema:date'][datenumb][
                        'inclusivestart'] != None and x['properties'][
                            'ucldc_schema:date'][datenumb][
                                'inclusivestart'] != '':
                    data2[name] = x['properties']['ucldc_schema:date'][
                        datenumb]['inclusivestart']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Date %d Inclusive End' % numb
                if x['properties']['ucldc_schema:date'][datenumb][
                        'inclusiveend'] != None and x['properties'][
                            'ucldc_schema:date'][datenumb][
                                'inclusiveend'] != '':
                    data2[name] = x['properties']['ucldc_schema:date'][
                        datenumb]['inclusiveend']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Date %d Single' % numb
                if x['properties']['ucldc_schema:date'][datenumb][
                        'single'] != None and x['properties'][
                            'ucldc_schema:date'][datenumb]['single'] != '':
                    data2[name] = x['properties']['ucldc_schema:date'][
                        datenumb]['single']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            datenumb += 1
    elif all_headers == 'y':
        data2['Date 1'] = ''
        data2['Date 1 Type'] = ''
        data2['Date 1 Inclusive Start'] = ''
        data2['Date 1 Inclusive End'] = ''
        data2['Date 1 Single'] = ''


def get_publication(data2, x, all_headers):
    pubnumb = 0
    if type(x['properties']['ucldc_schema:publisher']) == list and len(
            x['properties']['ucldc_schema:publisher']) > 0:
        while pubnumb < len(x['properties']['ucldc_schema:publisher']):
            numb = pubnumb + 1
            name = 'Publication/Origination Info %d' % numb
            data2[name] = x['properties']['ucldc_schema:publisher'][pubnumb]
            pubnumb += 1
    elif all_headers == 'y':
        data2['Publication/Origination Info 1'] = ''


def get_creator(data2, x, all_headers):
    creatnumb = 0
    if type(x['properties']['ucldc_schema:creator']) == list and len(
            x['properties']['ucldc_schema:creator']) > 0:
        while creatnumb < len(x['properties']['ucldc_schema:creator']):
            numb = creatnumb + 1
            try:
                name = 'Creator %d Name' % numb
                if x['properties']['ucldc_schema:creator'][creatnumb][
                        'name'] != None and x['properties'][
                            'ucldc_schema:creator'][creatnumb]['name'] != '':
                    data2[name] = x['properties']['ucldc_schema:creator'][
                        creatnumb]['name']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Creator %d Name Type' % numb
                if x['properties']['ucldc_schema:creator'][creatnumb][
                        'nametype'] != None and x['properties'][
                            'ucldc_schema:creator'][creatnumb][
                                'nametype'] != '':
                    data2[name] = x['properties']['ucldc_schema:creator'][
                        creatnumb]['nametype']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Creator %d Role' % numb
                if x['properties']['ucldc_schema:creator'][creatnumb][
                        'role'] != None and x['properties'][
                            'ucldc_schema:creator'][creatnumb]['role'] != '':
                    data2[name] = x['properties']['ucldc_schema:creator'][
                        creatnumb]['role']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Creator %d Source' % numb
                if x['properties']['ucldc_schema:creator'][creatnumb][
                        'source'] != None and x['properties'][
                            'ucldc_schema:creator'][creatnumb]['source'] != '':
                    data2[name] = x['properties']['ucldc_schema:creator'][
                        creatnumb]['source']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Creator %d Authority ID' % numb
                if x['properties']['ucldc_schema:creator'][creatnumb][
                        'authorityid'] != None and x['properties'][
                            'ucldc_schema:creator'][creatnumb][
                                'authorityid'] != '':
                    data2[name] = x['properties']['ucldc_schema:creator'][
                        creatnumb]['authorityid']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            creatnumb += 1
    elif all_headers == 'y':
        data2['Creator 1 Name'] = ''
        data2['Creator 1 Name Type'] = ''
        data2['Creator 1 Role'] = ''
        data2['Creator 1 Source'] = ''
        data2['Creator 1 Authority ID'] = ''


def get_contributor(data2, x, all_headers):
    contnumb = 0
    if type(x['properties']['ucldc_schema:contributor']) == list and len(
            x['properties']['ucldc_schema:contributor']) > 0:
        while contnumb < len(x['properties']['ucldc_schema:contributor']):
            numb = contnumb + 1
            try:
                name = 'Contributor %d Name' % numb
                if x['properties']['ucldc_schema:contributor'][contnumb][
                        'name'] != None and x['properties'][
                            'ucldc_schema:contributor'][contnumb]['name'] != '':
                    data2[name] = x['properties']['ucldc_schema:contributor'][
                        contnumb]['name']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Contributor %d Name Type' % numb
                if x['properties']['ucldc_schema:contributor'][contnumb][
                        'nametype'] != None and x['properties'][
                            'ucldc_schema:contributor'][contnumb][
                                'nametype'] != '':
                    data2[name] = x['properties']['ucldc_schema:contributor'][
                        contnumb]['nametype']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Contributor %d Role' % numb
                if x['properties']['ucldc_schema:contributor'][contnumb][
                        'role'] != None and x['properties'][
                            'ucldc_schema:contributor'][contnumb]['role'] != '':
                    data2[name] = x['properties']['ucldc_schema:contributor'][
                        contnumb]['role']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Contributor %d Source' % numb
                if x['properties']['ucldc_schema:contributor'][contnumb][
                        'source'] != None and x['properties'][
                            'ucldc_schema:contributor'][contnumb][
                                'source'] != '':
                    data2[name] = x['properties']['ucldc_schema:contributor'][
                        contnumb]['source']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Contributor %d Authority ID' % numb
                if x['properties']['ucldc_schema:contributor'][contnumb][
                        'authorityid'] != None and x['properties'][
                            'ucldc_schema:contributor'][contnumb][
                                'authorityid'] != '':
                    data2[name] = x['properties']['ucldc_schema:contributor'][
                        contnumb]['authorityid']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            contnumb += 1
    elif all_headers == 'y':
        data2['Contributor 1 Name'] = ''
        data2['Contributor 1 Name Type'] = ''
        data2['Contributor 1 Role'] = ''
        data2['Contributor 1 Source'] = ''
        data2['Contributor 1 Authority ID'] = ''


def get_format(data2, x, all_headers):
    if x['properties']['ucldc_schema:physdesc'] != None and x['properties'][
            'ucldc_schema:physdesc'] != '':
        data2['Format/Physical Description'] = x['properties'][
            'ucldc_schema:physdesc']
    elif all_headers == 'y':
        data2['Format/Physical Description'] = ''


def get_description(data2, x, all_headers):
    descnumb = 0
    if type(x['properties']['ucldc_schema:description']) == list and len(
            x['properties']['ucldc_schema:description']) > 0:
        while descnumb < len(x['properties']['ucldc_schema:description']):
            numb = descnumb + 1
            try:
                name = "Description %d Note" % numb
                if x['properties']['ucldc_schema:description'][descnumb][
                        'item'] != None and x['properties'][
                            'ucldc_schema:description'][descnumb]['item'] != '':
                    data2[name] = x['properties']['ucldc_schema:description'][
                        descnumb]['item']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = "Description %d Type" % numb
                if x['properties']['ucldc_schema:description'][descnumb][
                        'type'] != None and x['properties'][
                            'ucldc_schema:description'][descnumb]['type'] != '':
                    data2[name] = x['properties']['ucldc_schema:description'][
                        descnumb]['type']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            descnumb += 1
    elif all_headers == 'y':
        data2['Description 1 Note'] = ''
        data2['Description 1 Type'] = ''


def get_extent(data2, x, all_headers):
    if x['properties']['ucldc_schema:extent'] != None and x['properties'][
            'ucldc_schema:extent'] != '':
        data2['Extent'] = x['properties']['ucldc_schema:extent']
    elif all_headers == 'y':
        data2['Extent'] = ''


def get_language(data2, x, all_headers):
    langnumb = 0
    if type(x['properties']['ucldc_schema:language']) == list and len(
            x['properties']['ucldc_schema:language']) > 0:
        while langnumb < len(x['properties']['ucldc_schema:language']):
            numb = langnumb + 1
            try:
                name = "Language %d" % numb
                if x['properties']['ucldc_schema:language'][langnumb][
                        'language'] != None and x['properties'][
                            'ucldc_schema:language'][langnumb][
                                'language'] != '':
                    data2[name] = x['properties']['ucldc_schema:language'][
                        langnumb]['language']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = "Language %d Code" % numb
                if x['properties']['ucldc_schema:language'][langnumb][
                        'languagecode'] != None and x['properties'][
                            'ucldc_schema:language'][langnumb][
                                'languagecode'] != '':
                    data2[name] = x['properties']['ucldc_schema:language'][
                        langnumb]['languagecode']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            langnumb += 1
    elif all_headers == 'y':
        data2['Language 1'] = ''
        data2['Language 1 Code'] = ''


def get_temporal_coverage(data2, x, all_headers):
    tempnumb = 0
    if type(x['properties']['ucldc_schema:temporalcoverage']) == list and len(
            x['properties']['ucldc_schema:temporalcoverage']) > 0:
        while tempnumb < len(x['properties']['ucldc_schema:temporalcoverage']):
            numb = tempnumb + 1
            name = 'Temporal Coverage %d' % numb
            data2[name] = x['properties']['ucldc_schema:temporalcoverage'][
                tempnumb]
            tempnumb += 1
    elif all_headers == 'y':
        data2['Temporal Coverage 1'] = ''


def get_transcription(data2, x, all_headers):
    if x['properties']['ucldc_schema:transcription'] != None and x[
            'properties']['ucldc_schema:transcription'] != '':
        data2['Transcription'] = x['properties']['ucldc_schema:transcription']
    elif all_headers == 'y':
        data2['Transcription'] = ''


def get_access_restrictions(data2, x, all_headers):
    if x['properties']['ucldc_schema:accessrestrict'] != None and x[
            'properties']['ucldc_schema:accessrestrict'] != '':
        data2['Access Restrictions'] = x['properties'][
            'ucldc_schema:accessrestrict']
    elif all_headers == 'y':
        data2['Access Restrictions'] = ''


def get_rights_statement(data2, x, all_headers):
    if x['properties']['ucldc_schema:rightsstatement'] != None and x[
            'properties']['ucldc_schema:rightsstatement'] != '':
        data2['Copyright Statement'] = x['properties'][
            'ucldc_schema:rightsstatement']
    elif all_headers == 'y':
        data2['Copyright Statement'] = ''


def get_rights_status(data2, x, all_headers):
    if x['properties']['ucldc_schema:rightsstatus'] != None and x[
            'properties']['ucldc_schema:rightsstatus'] != '':
        data2['Copyright Status'] = x['properties'][
            'ucldc_schema:rightsstatus']
    elif all_headers == 'y':
        data2['Copyright Status'] = ''


def get_copyright_holder(data2, x, all_headers):
    rightsnumb = 0
    if type(x['properties']['ucldc_schema:rightsholder']) == list and len(
            x['properties']['ucldc_schema:rightsholder']) > 0:
        while rightsnumb < len(x['properties']['ucldc_schema:rightsholder']):
            numb = rightsnumb + 1
            try:
                name = 'Copyright Holder %d Name' % numb
                if x['properties']['ucldc_schema:rightsholder'][rightsnumb][
                        'name'] != None and x['properties'][
                            'ucldc_schema:rightsholder'][rightsnumb][
                                'name'] != '':
                    data2[name] = x['properties']['ucldc_schema:rightsholder'][
                        rightsnumb]['name']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Copyright Holder %d Name Type' % numb
                if x['properties']['ucldc_schema:rightsholder'][rightsnumb][
                        'nametype'] != None and x['properties'][
                            'ucldc_schema:rightsholder'][rightsnumb][
                                'nametype'] != '':
                    data2[name] = x['properties']['ucldc_schema:rightsholder'][
                        rightsnumb]['nametype']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Copyright Holder %d Source' % numb
                if x['properties']['ucldc_schema:rightsholder'][rightsnumb][
                        'source'] != None and x['properties'][
                            'ucldc_schema:rightsholder'][rightsnumb][
                                'source'] != '':
                    data2[name] = x['properties']['ucldc_schema:rightsholder'][
                        rightsnumb]['source']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Copyright Holder %d Authority ID' % numb
                if x['properties']['ucldc_schema:rightsholder'][rightsnumb][
                        'authorityid'] != None and x['properties'][
                            'ucldc_schema:rightsholder'][rightsnumb][
                                'authorityid'] != '':
                    data2[name] = x['properties']['ucldc_schema:rightsholder'][
                        rightsnumb]['authorityid']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            rightsnumb += 1
    elif all_headers == 'y':
        data2['Copyright Holder 1 Name'] = ''
        data2['Copyright Holder 1 Name Type'] = ''
        data2['Copyright Holder 1 Source'] = ''
        data2['Copyright Holder 1 Authority ID'] = ''


def get_copyright_info(data2, x, all_headers):
    if x['properties']['ucldc_schema:rightscontact'] != None and x[
            'properties']['ucldc_schema:rightscontact'] != '':
        data2['Copyright Contact'] = x['properties'][
            'ucldc_schema:rightscontact']
    elif all_headers == 'y':
        data2['Copyright Contact'] = ''

    if x['properties']['ucldc_schema:rightsnotice'] != None and x[
            'properties']['ucldc_schema:rightsnotice'] != '':
        data2['Copyright Notice'] = x['properties'][
            'ucldc_schema:rightsnotice']
    elif all_headers == 'y':
        data2['Copyright Notice'] = ''

    if x['properties']['ucldc_schema:rightsdeterminationdate'] != None and x[
            'properties']['ucldc_schema:rightsdeterminationdate'] != '':
        data2['Copyright Determination Date'] = x['properties'][
            'ucldc_schema:rightsdeterminationdate']
    elif all_headers == 'y':
        data2['Copyright Determination Date'] = ''

    if x['properties']['ucldc_schema:rightsstartdate'] != None and x[
            'properties']['ucldc_schema:rightsstartdate'] != '':
        data2['Copyright Start Date'] = x['properties'][
            'ucldc_schema:rightsstartdate']
    elif all_headers == 'y':
        data2['Copyright Start Date'] = ''

    if x['properties']['ucldc_schema:rightsenddate'] != None and x[
            'properties']['ucldc_schema:rightsenddate'] != '':
        data2['Copyright End Date'] = x['properties'][
            'ucldc_schema:rightsenddate']
    elif all_headers == 'y':
        data2['Copyright End Date'] = ''

    if x['properties']['ucldc_schema:rightsjurisdiction'] != None and x[
            'properties']['ucldc_schema:rightsjurisdiction'] != '':
        data2['Copyright Jurisdiction'] = x['properties'][
            'ucldc_schema:rightsjurisdiction']
    elif all_headers == 'y':
        data2['Copyright Jurisdiction'] = ''

    if x['properties']['ucldc_schema:rightsnote'] != None and x['properties'][
            'ucldc_schema:rightsnote'] != '':
        data2['Copyright Note'] = x['properties']['ucldc_schema:rightsnote']
    elif all_headers == 'y':
        data2['Copyright Note'] = ''


def get_collection(data2, x, all_headers):
    collnumb = 0
    if type(x['properties']['ucldc_schema:collection']) == list and len(
            x['properties']['ucldc_schema:collection']) > 0:
        while collnumb < len(x['properties']['ucldc_schema:collection']):
            numb = collnumb + 1
            name = 'Collection %d' % numb
            data2[name] = x['properties']['ucldc_schema:collection'][collnumb]
            collnumb += 1
    elif all_headers == 'y':
        data2['Collection 1'] = ''


def get_related_resource(data2, x, all_headers):
    relnumb = 0
    if type(x['properties']['ucldc_schema:relatedresource']) == list and len(
            x['properties']['ucldc_schema:relatedresource']) > 0:
        while relnumb < len(x['properties']['ucldc_schema:relatedresource']):
            numb = relnumb + 1
            name = 'Related Resource %d' % numb
            data2[name] = x['properties']['ucldc_schema:relatedresource'][
                relnumb]
            relnumb += 1
    elif all_headers == 'y':
        data2['Related Resource 1'] = ''


def get_source(data2, x, all_headers):
    if x['properties']['ucldc_schema:source'] != None and x['properties'][
            'ucldc_schema:source'] != '':
        data2['Source'] = x['properties']['ucldc_schema:source']
    elif all_headers == 'y':
        data2['Source'] = ''


def get_subject_name(data2, x, all_headers):
    subnumb = 0
    if type(x['properties']['ucldc_schema:subjectname']) == list and len(
            x['properties']['ucldc_schema:subjectname']) > 0:
        while subnumb < len(x['properties']['ucldc_schema:subjectname']):
            numb = subnumb + 1
            try:
                name = 'Subject (Name) %d Name' % numb
                if x['properties']['ucldc_schema:subjectname'][subnumb][
                        'name'] != None and x['properties'][
                            'ucldc_schema:subjectname'][subnumb]['name'] != '':
                    data2[name] = x['properties']['ucldc_schema:subjectname'][
                        subnumb]['name']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Subject (Name) %d Name Type' % numb
                if x['properties']['ucldc_schema:subjectname'][subnumb][
                        'name_type'] != None and x['properties'][
                            'ucldc_schema:subjectname'][subnumb][
                                'name_type'] != '':
                    data2[name] = x['properties']['ucldc_schema:subjectname'][
                        subnumb]['name_type']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Subject (Name) %d Role' % numb
                if x['properties']['ucldc_schema:subjectname'][subnumb][
                        'role'] != None and x['properties'][
                            'ucldc_schema:subjectname'][subnumb]['role'] != '':
                    data2[name] = x['properties']['ucldc_schema:subjectname'][
                        subnumb]['role']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Subject (Name) %d Source' % numb
                if x['properties']['ucldc_schema:subjectname'][subnumb][
                        'source'] != None and x['properties'][
                            'ucldc_schema:subjectname'][subnumb][
                                'source'] != '':
                    data2[name] = x['properties']['ucldc_schema:subjectname'][
                        subnumb]['source']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Subject (Name) %d Authority ID' % numb
                if x['properties']['ucldc_schema:subjectname'][subnumb][
                        'authorityid'] != None and x['properties'][
                            'ucldc_schema:subjectname'][subnumb][
                                'authorityid'] != '':
                    data2[name] = x['properties']['ucldc_schema:subjectname'][
                        subnumb]['authorityid']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            subnumb += 1
    elif all_headers == 'y':
        data2['Subject (Name) 1 Name'] = ''
        data2['Subject (Name) 1 Name Type'] = ''
        data2['Subject (Name) 1 Role'] = ''
        data2['Subject (Name) 1 Source'] = ''
        data2['Subject (Name) 1 Authority ID'] = ''


def get_place(data2, x, all_headers):
    plcnumb = 0
    if type(x['properties']['ucldc_schema:place']) == list and len(
            x['properties']['ucldc_schema:place']) > 0:
        while plcnumb < len(x['properties']['ucldc_schema:place']):
            numb = plcnumb + 1
            try:
                name = 'Place %d Name' % numb
                if x['properties']['ucldc_schema:place'][plcnumb][
                        'name'] != None and x['properties'][
                            'ucldc_schema:place'][plcnumb]['name'] != '':
                    data2[name] = x['properties']['ucldc_schema:place'][
                        plcnumb]['name']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Place %d Coordinates' % numb
                if x['properties']['ucldc_schema:place'][plcnumb][
                        'coordinates'] != None and x['properties'][
                            'ucldc_schema:place'][plcnumb]['coordinates'] != '':
                    data2[name] = x['properties']['ucldc_schema:place'][
                        plcnumb]['coordinates']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Place %d Source' % numb
                if x['properties']['ucldc_schema:place'][plcnumb][
                        'source'] != None and x['properties'][
                            'ucldc_schema:place'][plcnumb]['source'] != '':
                    data2[name] = x['properties']['ucldc_schema:place'][
                        plcnumb]['source']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Place %d Authority ID' % numb
                if x['properties']['ucldc_schema:place'][plcnumb][
                        'authorityid'] != None and x['properties'][
                            'ucldc_schema:place'][plcnumb]['authorityid'] != '':
                    data2[name] = x['properties']['ucldc_schema:place'][
                        plcnumb]['authorityid']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            plcnumb += 1
    elif all_headers == 'y':
        data2['Place 1 Name'] = ''
        data2['Place 1 Coordinates'] = ''
        data2['Place 1 Source'] = ''
        data2['Place 1 Authority ID'] = ''


def get_subject_topic(data2, x, all_headers):
    topnumb = 0
    if type(x['properties']['ucldc_schema:subjecttopic']) == list and len(
            x['properties']['ucldc_schema:subjecttopic']) > 0:
        while topnumb < len(x['properties']['ucldc_schema:subjecttopic']):
            numb = topnumb + 1
            try:
                name = 'Subject (Topic) %d Heading' % numb
                if x['properties']['ucldc_schema:subjecttopic'][topnumb][
                        'heading'] != None and x['properties'][
                            'ucldc_schema:subjecttopic'][topnumb][
                                'heading'] != '':
                    data2[name] = x['properties']['ucldc_schema:subjecttopic'][
                        topnumb]['heading']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Subject (Topic) %d Heading Type' % numb
                if x['properties']['ucldc_schema:subjecttopic'][topnumb][
                        'headingtype'] != None and x['properties'][
                            'ucldc_schema:subjecttopic'][topnumb][
                                'headingtype'] != '':
                    data2[name] = x['properties']['ucldc_schema:subjecttopic'][
                        topnumb]['headingtype']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Subject (Topic) %d Source' % numb
                if x['properties']['ucldc_schema:subjecttopic'][topnumb][
                        'source'] != None and x['properties'][
                            'ucldc_schema:subjecttopic'][topnumb][
                                'source'] != '':
                    data2[name] = x['properties']['ucldc_schema:subjecttopic'][
                        topnumb]['source']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Subject (Topic) %d Authority ID' % numb
                if x['properties']['ucldc_schema:subjecttopic'][topnumb][
                        'authorityid'] != None and x['properties'][
                            'ucldc_schema:subjecttopic'][topnumb][
                                'authorityid'] != '':
                    data2[name] = x['properties']['ucldc_schema:subjecttopic'][
                        topnumb]['authorityid']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            topnumb += 1
    elif all_headers == 'y':
        data2['Subject (Topic) 1 Heading'] = ''
        data2['Subject (Topic) 1 Heading Type'] = ''
        data2['Subject (Topic) 1 Source'] = ''
        data2['Subject (Topic) 1 Authority ID'] = ''


def get_form_genre(data2, x, all_headers):
    formnumb = 0
    if type(x['properties']['ucldc_schema:formgenre']) == list and len(
            x['properties']['ucldc_schema:formgenre']) > 0:
        while formnumb < len(x['properties']['ucldc_schema:formgenre']):
            numb = formnumb + 1
            try:
                name = 'Form/Genre %d Heading' % numb
                if x['properties']['ucldc_schema:formgenre'][formnumb][
                        'heading'] != None and x['properties'][
                            'ucldc_schema:formgenre'][formnumb][
                                'heading'] != '':
                    data2[name] = x['properties']['ucldc_schema:formgenre'][
                        formnumb]['heading']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Form/Genre %d Source' % numb
                if x['properties']['ucldc_schema:formgenre'][formnumb][
                        'source'] != None and x['properties'][
                            'ucldc_schema:formgenre'][formnumb]['source'] != '':
                    data2[name] = x['properties']['ucldc_schema:formgenre'][
                        formnumb]['source']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            try:
                name = 'Form/Genre %d Authority ID' % numb
                if x['properties']['ucldc_schema:formgenre'][formnumb][
                        'authorityid'] != None and x['properties'][
                            'ucldc_schema:formgenre'][formnumb][
                                'authorityid'] != '':
                    data2[name] = x['properties']['ucldc_schema:formgenre'][
                        formnumb]['authorityid']
                elif all_headers == 'y':
                    data2[name] = ''
            except:
                pass
            formnumb += 1
    elif all_headers == 'y':
        data2['Form/Genre 1 Heading'] = ''
        data2['Form/Genre 1 Source'] = ''
        data2['Form/Genre 1 Authority ID'] = ''


def get_provenance(data2, x, all_headers):
    provnumb = 0
    if type(x['properties']['ucldc_schema:provenance']) == list and len(
            x['properties']['ucldc_schema:provenance']) > 0:
        while provnumb < len(x['properties']['ucldc_schema:provenance']):
            numb = provnumb + 1
            name = 'Provenance %d' % numb
            data2[name] = x['properties']['ucldc_schema:provenance'][provnumb]
            provnumb += 1
    elif all_headers == 'y':
        data2['Provenance 1'] = ''


def get_physical_location(data2, x, all_headers):
    if x['properties']['ucldc_schema:physlocation'] != None and x[
            'properties']['ucldc_schema:physlocation'] != '':
        data2['Physical Location'] = x['properties'][
            'ucldc_schema:physlocation']
    elif all_headers == 'y':
        data2['Physical Location'] = ''


def object_level(filepath):
    nx = utils.Nuxeo()
    data = []
    for n in nx.children(filepath):
        data2 = {}

        get_title(data2, n)
        get_filepath(data2, n)
        get_type(data2, n, all_headers)
        get_alt_title(data2, n, all_headers)
        get_identifier(data2, n, all_headers)
        get_local_identifier(data2, n, all_headers)
        get_campus_unit(data2, n, all_headers)
        get_date(data2, n, all_headers)
        get_publication(data2, n, all_headers)
        get_creator(data2, n, all_headers)
        get_contributor(data2, n, all_headers)
        get_format(data2, n, all_headers)
        get_description(data2, n, all_headers)
        get_extent(data2, n, all_headers)
        get_language(data2, n, all_headers)
        get_temporal_coverage(data2, n, all_headers)
        get_transcription(data2, n, all_headers)
        get_access_restrictions(data2, n, all_headers)
        get_rights_statement(data2, n, all_headers)
        get_rights_status(data2, n, all_headers)
        get_copyright_holder(data2, n, all_headers)
        get_copyright_info(data2, n, all_headers)
        get_collection(data2, n, all_headers)
        get_related_resource(data2, n, all_headers)
        get_source(data2, n, all_headers)
        get_subject_name(data2, n, all_headers)
        get_place(data2, n, all_headers)
        get_subject_topic(data2, n, all_headers)
        get_form_genre(data2, n, all_headers)
        get_provenance(data2, n, all_headers)
        get_physical_location(data2, n, all_headers)

        data.append(data2)

    fieldnames = [
        'File path', 'Title', 'Type'
    ]  #ensures that File path, Title and Type are the first three rows
    for data2 in data:
        for key, value in data2.items():
            if key not in fieldnames:
                fieldnames.append(key)

    return {
        'fieldnames':
        fieldnames,
        'data':
        data,
        'filename':
        "nuxeo_object_%s.tsv" %
        nx.get_metadata(path=filepath)['properties']['dc:title']
    }


def item_level(filepath):
    nx = utils.Nuxeo()
    data = []
    for n in nx.children(filepath):
        for x in nx.children(n['path']):
            data2 = {}
            get_title(data2, x)
            get_filepath(data2, x)
            get_type(data2, x, all_headers)
            get_alt_title(data2, x, all_headers)
            get_identifier(data2, x, all_headers)
            get_local_identifier(data2, x, all_headers)
            get_campus_unit(data2, x, all_headers)
            get_date(data2, x, all_headers)
            get_publication(data2, x, all_headers)
            get_creator(data2, x, all_headers)
            get_contributor(data2, x, all_headers)
            get_format(data2, x, all_headers)
            get_description(data2, x, all_headers)
            get_extent(data2, x, all_headers)
            get_language(data2, x, all_headers)
            get_temporal_coverage(data2, x, all_headers)
            get_transcription(data2, x, all_headers)
            get_access_restrictions(data2, x, all_headers)
            get_rights_statement(data2, x, all_headers)
            get_rights_status(data2, x, all_headers)
            get_copyright_holder(data2, x, all_headers)
            get_copyright_info(data2, x, all_headers)
            get_collection(data2, x, all_headers)
            get_related_resource(data2, x, all_headers)
            get_source(data2, x, all_headers)
            get_subject_name(data2, x, all_headers)
            get_place(data2, x, all_headers)
            get_subject_topic(data2, x, all_headers)
            get_form_genre(data2, x, all_headers)
            get_provenance(data2, x, all_headers)
            get_physical_location(data2, x, all_headers)
            data.append(data2)

    fieldnames = [
        'File path', 'Title', 'Type'
    ]  #ensures that File path, Title and Type are the first three rows
    for data2 in data:
        for key, value in data2.items():
            if key not in fieldnames:
                fieldnames.append(key)

    return {
        'fieldnames':
        fieldnames,
        'data':
        data,
        'filename':
        "nuxeo_item_%s.tsv" %
        nx.get_metadata(path=filepath)['properties']['dc:title']
    }


# returns dictionary with fieldnames, data and filename;
# This is used for google functions and writing to tsv
# if google function not chosen


def google_object(filepath, url):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    obj = object_level(filepath)
    nx = utils.Nuxeo()
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scope)
    client = gspread.authorize(creds)
    with open("temp.csv", "wb") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=obj['fieldnames'])
        writer.writeheader()
        for row in obj['data']:
            writer.writerow(row)
    with open("temp.csv", encoding="utf8") as f:
        s = f.read() + '\n'
    sheet_id = client.open_by_url(url).id
    client.import_csv(sheet_id, s)
    client.open_by_key(sheet_id).sheet1.update_title(
        "nuxeo_object_%s" %
        nx.get_metadata(path=filepath)['properties']['dc:title'])
    os.remove("temp.csv")


def google_item(filepath, url):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    item = item_level(filepath)
    nx = utils.Nuxeo()
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scope)
    client = gspread.authorize(creds)
    with open("temp.csv", "wb") as csvfile:  #creates temporary csv file
        writer = csv.DictWriter(csvfile, fieldnames=item['fieldnames'])
        writer.writeheader()
        for row in item['data']:
            writer.writerow(row)
    with open("temp.csv",
              encoding="utf8") as f:  #opens and reads temporary csv file
        s = f.read() + '\n'
    sheet_id = client.open_by_url(url).id
    client.import_csv(sheet_id, s)  #writes csv file to google sheet
    client.open_by_key(sheet_id).sheet1.update_title(
        "nuxeo_item_%s" %
        nx.get_metadata(path=filepath)['properties']['dc:title'])
    os.remove("temp.csv")  #removes temporary csv


if choice == "o":
    if 'http' in url:
        try:
            google_object(filepath, url)
        except:
            print("\n*********\nWriting to Google document did not work."
                  "Make sure that Google document has been shared "
                  "with API key email address")
    else:
        obj = object_level(filepath)
        with open(obj['filename'], "wb") as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=obj['fieldnames'],
                                    delimiter="\t")
            writer.writeheader()
            for row in obj['data']:
                writer.writerow(row)
elif choice == "i":
    if 'http' in url:
        try:
            google_item(filepath, url)
        except:
            print("\n*********\nWriting to Google document did not work."
                  "Make sure that Google document has been shared "
                  "with API key email address")
    else:
        item = item_level(filepath)
        with open(item['filename'], "wb") as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=item['fieldnames'],
                                    delimiter="\t")
            writer.writeheader()
            for row in item['data']:
                writer.writerow(row)
