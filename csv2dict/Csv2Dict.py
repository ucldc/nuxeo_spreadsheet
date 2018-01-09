__author__ = 'glen'

import os
import pprint
import csv
import unicodecsv
import json
import copy

from time import localtime, strftime
from pynux import utils

import valid_columns

class UTF8PrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return(object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

class Csv2Dict:



    def __init__(self, data_file, blankout=False):
        '''
        The Csv2Dict class reads a csv data file, the first line of which contains column names. Succeeding
        lines represent rows of data. Initially the column names are used as the keys to a list of dicts, one
        per row. There are methods for transforming those dicts into import records.
        '''

        print('Starting at %s' % strftime("%Y-%m-%d %H:%M:%S", localtime()))

        self.status = 0
        self.row_dicts = []
        self.meta_dicts = []

        self.meta_dict_properties_template = {}

        if blankout:
            blankout_ucldc_file_name = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'blank-ucldc.json',
            )
            with open(blankout_ucldc_file_name, 'r') as blankout_ucldc_file:
                self.meta_dict_properties_template = json.load(blankout_ucldc_file).get('properties', {})


        with open(data_file, 'rb') as infile:

            # First row contains the column names
            csv_reader = unicodecsv.reader(infile, delimiter=('\t'), quotechar='|', encoding='utf-8')
            fields = next(csv_reader)

            print "Fields: %s" % fields
            valid_columns.validate(fields)

            # The rest of the rows contain data
            for row in csv_reader:
                if len(fields) == len(row):
                    print "Another row: %s" % row

                    #row_dict = OrderedDict()
                    row_dict = {}

                    for i in range(len(fields)):
                        row_dict[fields[i]] = row[i]
                    self.row_dicts.append(row_dict)
                else:
                    print "Incorrect number of fields in row!"
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

    def set_file_path(self, file_path, n):
        if self.verify_file_path(file_path):
            pass

    def verify_file_path(self, file_path):
        print "Verifying file path: %s" % file_path
        return True if file_path else False

    def set_title(self, title, n):
        if self.verify_title(title):
            self.meta_dicts[n]['properties']['dc:title'] = "%s" % title

    def verify_title(self, title):
        print "Verifying title: %s" % title
        return True if title else False

    def set_alt_title(self, alt_title, n):
        if self.verify_alt_title(alt_title):
            properties = self.get_meta_dict(n)['properties']
            if not 'ucldc_schema:alternativetitle' in properties.keys():
                print "Making alternativetitle item: %s" % alt_title
                properties['ucldc_schema:alternativetitle'] = ["%s" % alt_title]
            else:
                print "Adding alternativetitle item: %s" % alt_title
                properties['ucldc_schema:alternativetitle'].append("%s" % alt_title)

    def verify_alt_title(self, alt_title):
        print "Verifying alternative title: %s" % u'alt_title'
        return True if alt_title else False

    def set_id(self, objid, n):
        if self.verify_id(objid):
            self.meta_dicts[n]['properties']['ucldc_schema:identifier'] = "%s" % objid

    def verify_id(self, id):
        print "Verifying id: %s" % id
        return True if id else False

    def set_local_id(self, local_id, n):
        if self.verify_local_id(local_id):
            if not 'ucldc_schema:localidentifier' in self.meta_dicts[n]['properties'].keys():
                print "Making localidentifier element, %s" % local_id
                self.meta_dicts[n]['properties']['ucldc_schema:localidentifier'] = ["%s" % local_id]
            else:
                print "Adding localidentier item, %s" % local_id
                self.meta_dicts[n]['properties']['ucldc_schema:localidentifier'].append("%s" % local_id)

    def verify_local_id(self, local_id):
        print "Verifying localidentifier: %s" % local_id
        return True if local_id else False

    def set_type(self, type, n):
        if self.verify_type(type):
            self.meta_dicts[n]['properties']['ucldc_schema:type'] = "%s" % type

    def verify_type(self, type):
        print "Verifying type: %s" % type
        return True if type else False

    def set_campus_unit(self, unit, n):
        if self.verify_campus_unit(unit):
            if not 'ucldc_schema:campusunit' in self.meta_dicts[n]['properties'].keys():
                print "Making campusunit item: %s" % unit
                self.meta_dicts[n]['properties']['ucldc_schema:campusunit'] = ["%s" % unit]
            else:
                print "Adding campusunit item: %s" % unit
                self.meta_dicts[n]['properties']['ucldc_schema:campusunit'].append("%s" % unit)
    def verify_campus_unit(self, unit):
        print "Verifying campus unit: %s" % unit
        return True if unit else False

    def set_date(self, date, date_type, inclusive_start, inclusive_end, single, n):
        date_dict = {'date': "%s" % date,
                     'datetype': "%s" % date_type,
                     'inclusivestart': "%s" % inclusive_start,
                     'inclusiveend': "%s" % inclusive_end,
                     'single': "%s" % single}

        if self.verify_date(date_dict):
            if not 'ucldc_schema:date' in self.meta_dicts[n]['properties'].keys():
                print "Making date item, %s %s %s %s %s" % (date, date_type, inclusive_start, inclusive_end, single)
                self.meta_dicts[n]['properties']['ucldc_schema:date'] = [date_dict]
            else:
                print "Adding date item, %s %s %s %s %s" % (date, date_type, inclusive_start, inclusive_end, single)
                self.meta_dicts[n]['properties']['ucldc_schema:date'].append(date_dict)

    def verify_date(self, date_dict):
        print "Verifying date: %s" % (date_dict)
        if all(value == '' for value in date_dict.values()) == True:
        	return False
        else:
        	return True

    def set_publication_origination(self, info, n):
        if self.verify_publication_origination(info):
            self.meta_dicts[n]['properties']['ucldc_schema:publisher'] = ["%s" % info]

    def verify_publication_origination(self, info):
        print "Verifying info: %s" % info
        return True if info else False

    def set_creator(self, name, name_type, role, source, authority_id, n):
    	creator_dict = {'name': "%s" % name, 'nametype': "%s" % name_type,
                            'role': "%s" % role, 'source': "%s" % source,
                            'authorityid': "%s" % authority_id}
        if self.verify_creator(creator_dict):
            if not 'ucldc_schema:creator' in self.meta_dicts[n]['properties'].keys():
                print "Making creator item, %s %s %s %s %s" % (name, name_type, role, source, authority_id)
                self.meta_dicts[n]['properties']['ucldc_schema:creator'] = [ creator_dict ]
            else:
                print "Adding creator item, %s %s %s %s %s" % ( name, name_type, role, source, authority_id)
                self.meta_dicts[n]['properties']['ucldc_schema:creator'].append(creator_dict)

    def verify_creator(self, creator_dict):
        print "Verifying creator: %s" % creator_dict
        if all(value == '' for value in creator_dict.values()) == True:
        	return False
        else:
        	return True

    def set_contributor(self, name, name_type, role, source, auth_id, n):

        contributor_dict = {'name': "%s" % name,
                            'nametype': "%s" % name_type,
                            'role': "%s" % role,
                            'source': "%s" % source,
                            'authorityid': "%s" % auth_id}

        if self.verify_contributor(contributor_dict):
            if not 'ucldc_schema:contributor' in self.meta_dicts[n]['properties'].keys():
                print "Making contributor item, %s %s %s %s %s" % (name, name_type, role, source, auth_id)
                self.meta_dicts[n]['properties']['ucldc_schema:contributor'] = [contributor_dict]
            else:
                print "Adding contributor item, %s %s %s %s %s" % (name, name_type, role, source, auth_id)
                self.meta_dicts[n]['properties']['ucldc_schema:contributor'].append(contributor_dict)

    def verify_contributor(self,  contributor_dict):
        print "Verifying contributor: %s" % (contributor_dict)
        if all(value == '' for value in contributor_dict.values()) == True:
        	return False
        else:
        	return True

    def set_physdesc(self, physical_description, n):
        if self.verify_physdesc(physical_description):
            print "Making physdesc element: %s" % physical_description
            self.meta_dicts[n]['properties']['ucldc_schema:physdesc'] = "%s" % physical_description

    def verify_physdesc(self, physical_description):
        print "Verifying phyical description: %s" % physical_description
        return True if physical_description else False

    def set_description(self, note, type, n):

        description_dict = {'item': "%s" % note, 'type': "%s" % type}

        if self.verify_description(description_dict):
            if not 'ucldc_schema:description' in self.meta_dicts[n]['properties'].keys():
                print "Making description item: %s %s" % (note, type)
                self.meta_dicts[n]['properties']['ucldc_schema:description'] =  [description_dict]
            else:
                print "Adding description item: %s %s" % (note, type)
                self.meta_dicts[n]['properties']['ucldc_schema:description'].append(description_dict)

    def verify_description(self, description_dict):
        print "Verifying description: %s" % (description_dict)
        if all(value == '' for value in description_dict.values()) == True:
        	return False
        else:
        	return True

    def set_extent(self, extent, n):
        if self.verify_extent(extent):
            print "Making extent element: %s" % extent
            self.meta_dicts[n]['properties']['ucldc_schema:extent'] = "%s" % extent

    def verify_extent(self, extent):
        print "Verifying extent: %s" % extent
        return True if extent else False

    def set_language(self, language, code, n):

        language_dict = {'language': "%s" % language,
                         'languagecode': "%s" % code}

        if self.verify_language(language_dict):
            if not 'ucldc_schema:language' in self.meta_dicts[n]['properties'].keys():
                print "Making language item: %s %s" % (language, code)
                self.meta_dicts[n]['properties']['ucldc_schema:language'] = [language_dict]
            else:
                print "Adding language item: %s %s" % (language, code)
                self.meta_dicts[n]['properties']['ucldc_schema:language'].append(language_dict)

    def verify_language(self, language_dict):
        print "Verifying language: %s" % (language_dict)
        if all(value == '' for value in language_dict.values()) == True:
        	return False
        else:
        	return True

    def set_temporal_coverage(self, temporal_coverage, n):
        if self.verify_temporal_coverage(temporal_coverage):
            if not 'ucldc_schema:temporalcoverate' in self.meta_dicts[n]['properties'].keys():
                print "Making temporalcoverage item: %s" % temporal_coverage
                self.meta_dicts[n]['properties']['ucldc_schema:temporalcoverage'] = ["%s" % temporal_coverage]
            else:
                print "Adding temporalcoverage item: %s" % temporal_coverage
                self.meta_dicts[n]['properties']['ucldc_schema:temporalcoverage'].append("%s" % temporal_coverage)

    def verify_temporal_coverage(self, temporal_coverage):
        print "Verifying temporal coverage: %s" % temporal_coverage
        return True if temporal_coverage else False

    def set_transcription(self, transcription, n):
        if self.verify_transcription(transcription):
            print "Making transcription element: %s" % transcription
            self.meta_dicts[n]['properties']['ucldc_schema:transcription'] = "%s" % transcription

    def verify_transcription(self, transcription):
        print "Verifying transcription: %s" % transcription
        return True if transcription else False

    def set_access_restrictions(self, restrictions, n):
        if self.verify_access_restrictions(restrictions):
            print "Making accessrestrict element: %s" % restrictions
            self.meta_dicts[n]['properties']['ucldc_schema:accessrestrict'] = "%s" % restrictions

    def verify_access_restrictions(self, restrictions):
        print "Verifying access restrictions: %s" % restrictions
        return True if restrictions else False

    def set_rights_statement(self, statement, n):
        if self.verify_rights_statement(statement):
            print "Making rightsstatement element: %s" % statement
            self.meta_dicts[n]['properties']['ucldc_schema:rightsstatement'] = "%s" % statement

    def verify_rights_statement(self, statement):
        print "Verifying copyright statement: %s" % statement
        return True if statement else False

    def set_rights_status(self, status, n):
        if self.verify_rights_status(status):
            print "Making rightsstatus element: %s" % status
            self.meta_dicts[n]['properties']['ucldc_schema:rightsstatus'] = "%s" % status

    def verify_rights_status(self, status):
        print "Verifying copyright status: %s" % status
        return True if status else False

    def set_rights_holder(self, name, name_type, source, auth_id, n):

        rights_holder_dict = {'name': "%s" % name,
                              'nametype': "%s" % name_type,
                              'source': "%s" % source,
                              'authorityid': "%s" % auth_id}

        if self.verify_rights_holder(rights_holder_dict):
            if not 'ucldc_schema:rightsholder' in self.meta_dicts[n]['properties'].keys():
                print "Making rightsholder item: %s %s %s %s" % (name, name_type, source, auth_id)
                self.meta_dicts[n]['properties']['ucldc_schema:rightsholder'] = [rights_holder_dict]
            else:
                print "Adding rightsholder item: %s %s %s %s" % (name, name_type, source, auth_id)
                self.meta_dicts[n]['properties']['ucldc_schema:rightsholder'].append(rights_holder_dict)

    def verify_rights_holder(self, rights_holder_dict):
        print "Verifying rights holder: %s" % (rights_holder_dict)
        if all(value == '' for value in rights_holder_dict.values()) == True:
        	return False
        else:
        	return True

    def set_rights_contact(self, contact, n):
        if self.verify_rights_contact(contact):
            print "Making rightscontact element: %s" % contact
            self.meta_dicts[n]['properties']['ucldc_schema:rightscontact'] = "%s" % contact

    def verify_rights_contact(self, contact):
        print "Verifying rights contact: %s" % contact
        return True if contact else False

    def set_rights_notice(self, notice, n):
        if self.verify_rights_notice(notice):
            print "Making rightsnotice element: %s" % notice
            self.meta_dicts[n]['properties']['ucldc_schema:rightsnotice'] = "%s" % notice

    def verify_rights_notice(self, notice):
        print "Verifying rights notice: %s" % notice
        return True if notice else False

    def set_rights_determination_date(self, date, n):
        if self.verify_rights_determination_date(date):
            print "Making rightsdeterminationdate element: %s" % date
            self.meta_dicts[n]['properties']['ucldc_schema:rightsdeterminationdate'] = "%s" % date

    def verify_rights_determination_date(self, date):
        print "Verifying rights determination date: %s" % date
        return True if date else False

    def set_rights_start_date(self, date, n):
        if self.verify_rights_start_date(date):
            print "Making rightsstartdate element: %s" % date
            self.meta_dicts[n]['properties']['ucldc_schema:rightsstartdate'] = "%s" % date

    def verify_rights_start_date(self, date):
        print "Verifying rights start date: %s" % date
        return True if date else False

    def set_rights_end_date(self, date, n):
        if self.verify_rights_end_date(date):
            print "Making rightsenddate element: %s" % date
            self.meta_dicts[n]['properties']['ucldc_schema:rightsenddate'] = "%s" % date

    def verify_rights_end_date(self, date):
        print "Verifying rights end date: %s" % date
        return True if date else False

    def set_rights_jurisdiction(self, jurisdiction, n):
        if self.verify_rights_jurisdiction(jurisdiction):
            print "Making rightsjurisdiction element: %s" % jurisdiction
            self.meta_dicts[n]['properties']['ucldc_schema:rightsjurisdiction'] = "%s" % jurisdiction

    def verify_rights_jurisdiction(self, jurisdiction):
        print "Verifying rights jurisdiction: %s" % jurisdiction
        return True if jurisdiction else False

    def set_rights_note(self, note, n):
        if self.verify_rights_note(note):
            print "Making rightsnote element: %s" % note
            self.meta_dicts[n]['properties']['ucldc_schema:rightsnote'] = "%s" % note

    def verify_rights_note(self, note):
        print "Verifying rights note: %s" % note
        return True if note else False

    def set_collection(self, collection, n):
        if self.verify_collection(collection):
            if not 'ucldc_schema:collection' in self.meta_dicts[n]['properties'].keys():
                print "Making collection item: %s" % collection
                self.meta_dicts[n]['properties']['ucldc_schema:collection'] = ["%s" % collection]
            else:
                print "Adding collection item: %s" % collection
                self.meta_dicts[n]['properties']['ucldc_schema:collection'].append("%s" % collection)

    def verify_collection(self, collection):
        print "Verifying collection: %s" % collection
        return True if collection else False

    def set_related_resource(self, resource, n):
        if self.verify_related_resource(resource):
            if not 'ucldc_schema:relatedresource' in self.meta_dicts[n]['properties'].keys():
                print "Making relatedresource item: %s" % resource
                self.meta_dicts[n]['properties']['ucldc_schema:relatedresource'] = ["%s" % resource]
            else:
                print "Adding relatedresource item: %s" % resource
                self.meta_dicts[n]['properties']['ucldc_schema:relatedresource'].append("%s" % resource)

    def verify_related_resource(self, resource):
        print "Verifying related resource: %s" % resource
        return True if resource else False

    def set_source(self, source, n):
        if self.verify_source(source):
            self.meta_dicts[n]['properties']['ucldc_schema:source'] = "%s" % source

    def verify_source(self, source):
        print "Verifying source: %s" % source
        return True if source else False

    def set_subject_name(self, name, name_type, role, source, auth_id, n):
        subject_name_dict = {'name': "%s" % name,
                             'nametype': "%s" % name_type,
                             'role': "%s" % role,
                             'source': "%s" % source,
                             'authorityid': "%s" % auth_id}
        if self.verify_subject_name(subject_name_dict):
            if not 'ucldc_schema:subjectname' in self.meta_dicts[n]['properties'].keys():
                print "Making subjectname item: %s %s %s %s %s" % (name, name_type, role, source, auth_id)
                self.meta_dicts[n]['properties']['ucldc_schema:subjectname'] = [subject_name_dict]
            else:
                print "Adding subjectname item: %s %s %s %s %s" % (name, name_type, role, source, auth_id)
                self.meta_dicts[n]['properties']['ucldc_schema:subjectname'].append(subject_name_dict)

    def verify_subject_name(self, subject_name_dict):
        print "Verifying subject name: %s" % (subject_name_dict)
        if all(value == '' for value in subject_name_dict.values()) == True:
        	return False
        else:
        	return True

    #place_items.append({'item': [{'source': source, 'name': name}]})
    def set_place(self, name, source, coordinates, auth_id, n):

        place_dict = {'name': "%s" % name,
                      'source': "%s" % source,
                      'coordinates': "%s" % coordinates,
                      'authorityid': "%s" % auth_id}

        if self.verify_place(place_dict):
            if not 'ucldc_schema:place' in self.meta_dicts[n]['properties'].keys():
                print "Making place item: %s %s %s %s" % (name, source, coordinates, auth_id)
                self.meta_dicts[n]['properties']['ucldc_schema:place'] = [place_dict]
            else:
                print "Adding place item: %s %s %s %s" % (name, source, coordinates, auth_id)
                self.meta_dicts[n]['properties']['ucldc_schema:place'].append(place_dict)

    def verify_place(self, place_dict):
        print "Verifying place: %s" % (place_dict)
        if all(value == '' for value in place_dict.values()) == True:
        	return False
        else:
        	return True

    def set_subject_topic(self, heading, heading_type, source, auth_id, n):
    	subject_topic_dict =  {'heading': "%s" % heading,
                                   'headingtype': "%s" % heading_type,
                                   'source': "%s" % source,
                                   'authorityid': "%s" % auth_id}
        if self.verify_subject_topic(subject_topic_dict):
            if not 'ucldc_schema:subjecttopic' in self.meta_dicts[n]['properties'].keys():
                print "Making subjecttopic item: %s %s %s %s" % (heading, heading_type, source, auth_id)
                self.meta_dicts[n]['properties']['ucldc_schema:subjecttopic'] = [subject_topic_dict]
            else:
                print "Adding subjecttopic item: %s %s %s %s" % (heading, heading_type, source, auth_id)
                self.meta_dicts[n]['properties']['ucldc_schema:subjecttopic'].append(subject_topic_dict)

    def verify_subject_topic(self, subject_topic_dict):
        print "Verifying subject topic: %s" % (subject_topic_dict)
        if all(value == '' for value in subject_topic_dict.values()) == True:
        	return False
        else:
        	return True

    def set_form_genre(self, heading, source, auth_id, n):
    	form_genre_dict = {'heading': "%s" % heading,
                               'source': "%s" % source,
                               'authorityid': "%s" % auth_id}

        if self.verify_form_genre(form_genre_dict):
            if not 'ucldc_schema:formgenre' in self.meta_dicts[n]['properties'].keys():
                print "Making formgenre item; %s %s %s" % (heading, source, auth_id)
                self.meta_dicts[n]['properties']['ucldc_schema:formgenre'] = [form_genre_dict]
            else:
                print "Skipping second genreform"
                print "Adding formgenre item: %s %s %s" % (heading, source, auth_id)
                self.meta_dicts[n]['properties']['ucldc_schema:formgenre'].append(form_genre_dict)

    def verify_form_genre(self, form_genre_dict):
        print "Verifying form genre: %s" % (form_genre_dict)
        if all(value == '' for value in form_genre_dict.values()) == True:
        	return False
        else:
        	return True

    def set_provenance(self, provenance, n):
        if self.verify_provenance(provenance):
            if not 'ucldc_schema:provenance' in self.meta_dicts[n]['properties'].keys():
                print "Making provenance item: %s" % provenance
                self.meta_dicts[n]['properties']['ucldc_schema:provenance'] = ["%s" % provenance]
            else:
                print "Making provenance item: %s" % provenance
                self.meta_dicts[n]['properties']['ucldc_schema:provenance'].append("%s" % provenance)

    def verify_provenance(self, provenance):
        print "Verifying provenance: %s" % provenance
        return True if provenance else False

    def set_physical_location(self, location, n):
        if self.verify_physical_location(location):
            print "Making phylocation element: %s" % location
            self.meta_dicts[n]['properties']['ucldc_schema:physlocation'] = "%s" % location

    def verify_physical_location(self, location):
        print "Verifying phyical location: %s" % location
        return True if location else False
    
    def get_existing_data(self, filepath, metadata_path):
    	nx = utils.Nuxeo()
        data = nx.get_metadata(path=filepath)
        return data['properties']['ucldc_schema:{}'.format(metadata_path)]
    
    def set_element(self, metadata_path, dict_list, n):
    	dict_list = self.verify_list(dict_list)
    	print(dict_list)
    	print "Making %s item: %s" % (metadata_path, dict_list)
    	self.meta_dicts[n]['properties']['ucldc_schema:{}'.format(metadata_path)] = dict_list
    
    def verify_list(self, dict_list):
    	for i, dict in enumerate(dict_list):
            if all(value == '' for value in dict.values()) or all(value == None for value in dict.values()):
                del dict_list[i]
        return dict_list
