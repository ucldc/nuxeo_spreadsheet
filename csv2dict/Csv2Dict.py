__author__ = 'glen'

import pprint
import csv
import unicodecsv

from time import localtime, strftime

class UTF8PrettyPrinter(pprint.PrettyPrinter):
   def format(self, object, context, maxlevels, level):
      if isinstance(object, unicode):
         return(object.encode('utf8'), True, False)
      return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

class Csv2Dict:

   def __init__(self, data_file):
      '''
      The Csv2Dict class reads a csv data file, the first line of which contains column names. Succeeding
      lines represent rows of data. Initially the column names are used as the keys to a list of dicts, one
      per row. There are methods for transforming those dicts into import records.
      '''

      print('Starting at %s' % strftime("%Y-%m-%d %H:%M:%S", localtime()))

      self.status = 0
      self.row_dicts = []
      self.meta_dicts = []

      with open(data_file, 'rb') as infile:

         # First row contains the column names
         csv_reader = unicodecsv.reader(infile, delimiter=('\t'), quotechar='|', encoding='utf-8')
         fields = next(csv_reader)

         print "Fields: %s" % fields

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

   def get_meta_dict(self, n=0):
      return self.meta_dicts[n]

   def new_dict(self, asset_path):
      #meta_dict = OrderedDict()
      meta_dict = {}
      meta_dict['path'] = "'%s'" % asset_path
      meta_dict['properties'] = {}
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
         self.meta_dicts[n]['properties']['dc:title'] = "'%s'" % title

   def verify_title(self, title):
      print "Verifying title: %s" % title
      return True if title else False

   def set_alt_title(self, alt_title, n):
      if self.verify_alt_title(alt_title):
         properties = self.get_meta_dict(n)['properties']
         if not 'ucldc_schema:alternativetitle' in properties.keys():
            print "Making alternativetitle item: %s" % alt_title
            properties['ucldc_schema:alternativetitle'] = ["'%s'" % alt_title]
         else:
            print "Adding alternativetitle item: %s" % alt_title
            properties['ucldc_schema:alternativetitle'].append("'%s'" % alt_title)

   def verify_alt_title(self, alt_title):
      print "Verifying alternative title: %s" % alt_title
      return True if alt_title else False

   def set_id(self, objid, n):
      if self.verify_id(objid):
         self.meta_dicts[n]['properties']['ucldc_schema:identifier'] = "'%s'" % objid

   def verify_id(self, id):
      print "Verifying id: %s" % id
      return True if id else False

   def set_local_id(self, local_id, n):
      if self.verify_local_id(local_id):
         if not 'ucldc_schema:localitendifier' in self.meta_dicts[n]['properties'].keys():
            print "Making localidentifier element, %s" % local_id
            self.meta_dicts[n]['properties']['ucldc_schema:localidentifier'] = [{'item': "'%s'" % local_id}]
         else:
            print "Adding localidentier item, %s" % local_id
            self.meta_dicts[n]['properties']['ucldc_schema:localidentifier'].append({'item': "'%s'" % local_id})

   def verify_local_id(self, local_id):
      print "Verifying localidentifier: %s" % local_id
      return True if local_id else False

   def set_type(self, type, n):
      if self.verify_type(type):
          self.meta_dicts[n]['properties']['ucldc_schema:type'] = "'%s'" % type

   def verify_type(self, type):
      print "Verifying type: %s" % type
      return True if type else False

   def set_campus_unit(self, unit, n):
      if self.verify_campus_unit(unit):
         if not 'ucldc_schema:campusunit' in self.meta_dicts[n]['properties'].keys():
            print "Making campusunit item: %s" % unit
            self.meta_dicts[n]['properties']['ucldc_schema:campusunit'] = ["'%s'" % unit]
         else:
            print "Adding campusunit item: %s" % unit
            self.meta_dicts[n]['properties']['ucldc_schema:campusunit'].append("'%s'" % unit)
   def verify_campus_unit(self, unit):
      print "Verifying campus unit: %s" % unit
      return True if unit else False

   def set_date(self, date, date_type, inclusive_start, inclusive_end, single, n):
      if self.verify_date(date, date_type, inclusive_start, inclusive_end, single):
         if not 'ucldc_schema:date' in self.meta_dicts[n]['properties'].keys():
            print "Making date item, %s %s %s %s %s" % (date, date_type, inclusive_start, inclusive_end, single)
            self.meta_dicts[n]['properties']['ucldc:date'] = [
               {'item': {'date': "'%s'" % date, 'datetype': "'%s'" % date_type, 'inclusivestart': "'%s'" % inclusive_start,
                'inclusiveend': "'%s'" % inclusive_end, 'single': "'%s'" % single}}
            ]
         else:
            print "Adding date item, %s %s %s %s %s" % (date, date_type, inclusive_start, inclusive_end, single)
            self.meta_dicts[n]['properties']['ucldc:date'].append(
               {'item': {'date': "'%s'" % date, 'datetype': "'%s'" % date_type, 'inclusivestart': "'%s'" % inclusive_start,
                'inclusiveend': "'%s'" % inclusive_end, 'single': "'%s'" % single}}
            )

   def verify_date(self, date, date_type, inclusive_start, inclusive_end, single):
      print "Verifying date: %s %s %s %s %s" % (date, date_type, inclusive_start, inclusive_end, single)
      return True if date else False

   def set_creator(self, name, name_type, role, source, authority_id, n):
      if self.verify_creator(name, name_type, role, source, authority_id):
         if not 'ucldc_schema:creator' in self.meta_dicts[n]['properties'].keys():
            print "Making creator item, %s %s %s %s %s" % (name, name_type, role, source, authority_id)
            self.meta_dicts[n]['properties']['ucldc_schema:creator'] = [
               {'item': {'name': "'%s'" % name, 'nametype': "'%s'" % name_type, 'role': "'%s'" % role,
                         'source': "'%s'" % source, 'authorityid': "'%s'" % authority_id}}
            ]
         else:
            print "Adding creator item, %s %s %s %s %s" % ( name, name_type, role, source, authority_id)
            self.meta_dicts[n]['properties']['ucldc_schema:creator'].append(
               {'item': {'name': "'%s'" % name, 'nametype':"'%s'" % name_type, 'role': "'%s'" % role,
                         'source': "'%s'" % source, 'authorityid': "'%s'" % authority_id}}
            )

   def verify_creator(self, name, type, role, source, authid):
      print "Verifying creator: %s" % name
      return True if name else False

   def set_contributor(self, name, name_type, role, source, auth_id, n):
      if self.verify_contributor(name, name_type, role, source, auth_id):
         if not 'ucldc_schema:contributor' in self.meta_dicts[n]['properties'].keys():
            print "Making contributor item, %s %s %s %s %s" % (name, name_type, role, source, auth_id)
            self.meta_dicts[n]['properties']['ucldc_schema:contributor'] = [
               {'item': {'name': "'%s'" % name, 'nametype': "'%s'" % name_type, 'role': "'%s'" % role,
                         'source': "'%s'" % source, 'authorityid': "'%s'" % auth_id}}
            ]
         else:
            print "Adding contributor item, %s %s %s %s %s" % (name, name_type, role, source, auth_id)
            self.meta_dicts[n]['properties']['ucldc_schema:contributor'].append(
               {'item': {'name': "'%s'" % name, 'nametype': "'%s'" % name_type, 'role': "'%s'" % role,
                         'source': "'%s'" % source, 'authorityid': "'%s'" % auth_id}}
            )

   def verify_contributor(self, name, name_type, role, source, auth_id):
      print "Verifying contributor: %s %s %s %s %s" % (name, name_type, role, source, auth_id)
      return True if name else False

   def set_physdesc(self, physical_description, n):
      if self.verify_physdesc(physical_description):
         print "Making physdesc element: %s" % physical_description
         self.meta_dicts[n]['properties']['ucldc_schema:physdesc'] = "'%s'" % physical_description

   def verify_physdesc(self, physical_description):
      print "Verifying phyical description: %s" % physical_description
      return True if physical_description else False

   def set_description(self, note, type, n):
      if self.verify_description(note, type):
         if not 'ucldc_schema:description' in self.meta_dicts[n]['properties'].keys():
            print "Making description item: %s %s" % (note, type)
            self.meta_dicts[n]['properties']['ucldc_schema:description'] =  [
               {'item': {'item': "'%s'" % note, 'type': "'%s'" % type}}]
         else:
            print "Adding description item: %s %s" % (note, type)
            self.meta_dicts[n]['properties']['ucldc_schema:description'].append(
               {'item': {'item': "'%s'" % note, 'type': "'%s'" % type}})

   def verify_description(self, note, type):
      print "Verifying description: %s %s" % (note, type)
      return True if note else False

   def set_extent(self, extent, n):
      if self.verify_extent(extent):
         print "Making extent element: %s" % extent
         self.meta_dicts[n]['properties']['ucldc_schema:extent'] = "'%s'" % extent

   def verify_extent(self, extent):
      print "Verifying extent: %s" % extent
      return True if extent else False

   def set_language(self, language, code, n):
      if self.verify_language(language, code):
         if not 'ucldc_schema:language' in self.meta_dicts[n]['properties'].keys():
            print "Making language item: %s %s" % (language, code)
            self.meta_dicts[n]['properties']['ucldc_schema:language'] = [
               {'item': {'language': "'%s'" % language, 'languagecode': "'%s'" % code}}
            ]
         else:
            print "Adding language item: %s %s" % (language, code)
            self.meta_dicts[n]['properties']['ucldc_schema:language'].append(
               {'item': {'language': "'%s'" % language, 'languagecode': "'%s'" % code}}
            )

   def verify_language(self, language, code):
      print "Verifying language: %s %s" % (language, code)
      return True if (language and code) else False

   def set_temporal_coverage(self, temporal_coverage, n):
      if self.verify_temporal_coverage(temporal_coverage):
         if not 'ucldc_schema:temporalcoverate' in self.meta_dicts[n]['properties'].keys():
            print "Making temporalcoverage item: %s" % temporal_coverage
            self.meta_dicts[n]['properties']['ucldc_schema:temporalcoverage'] = ["'%s'" % temporal_coverage]
         else:
            print "Adding temporalcoverage item: %s" % temporal_coverage
            self.meta_dicts[n]['properties']['ucldc_schema:temporalcoverage'].append("'%s'" % temporal_coverage)

   def verify_temporal_coverage(self, temporal_coverage):
      print "Verifying temporal coverage: %s" % temporal_coverage
      return True if temporal_coverage else False

   def set_transcription(self, transcription, n):
      if self.verify_transcription(transcription):
         print "Making transcription element: %s" % transcription
         self.meta_dicts[n]['properties']['ucldc_schema:transcription'] = "'%s'" % transcription

   def verify_transcription(self, transcription):
      print "Verifying transcription: %s" % transcription
      return True if transcription else False

   def set_access_restrictions(self, restrictions, n):
      if self.verify_access_restrictions(restrictions):
         print "Making accessrestrict element: %s" % restrictions
         self.meta_dicts[n]['properties']['ucldc_schema:accessrestrict'] = "'%s'" % restrictions

   def verify_access_restrictions(self, restrictions):
      print "Verifying access restrictions: %s" % restrictions
      return True if restrictions else False

   def set_rights_statement(self, statement, n):
      if self.verify_rights_statement(statement):
         print "Making rightsstatement element: %s" % statement
         self.meta_dicts[n]['properties']['ucldc_schema:rightsstatement'] = "'%s'" % statement

   def verify_rights_statement(self, statement):
      print "Verifying copyright statement: %s" % statement
      return True if statement else False

   def set_rights_status(self, status, n):
      if self.verify_rights_status(status):
         print "Making rightsstatus element: %s" % status
         self.meta_dicts[n]['properties']['ucldc_schema:rightsstatus'] = "'%s'" % status

   def verify_rights_status(self, status):
      print "Verifying copyright status: %s" % status
      return True if status else False

   def set_rights_holder(self, name, name_type, source, auth_id, n):
      if self.verify_rights_holder(name, name_type, source, auth_id):
         if not 'ucldc_schema:rightsholder' in self.meta_dicts[n]['properties'].keys():
            print "Making rightsholder item: %s %s %s %s" % (name, name_type, source, auth_id)
            self.meta_dicts[n]['properties']['ucldc_schema:rightsholder'] = [
               {'item': {'name': "'%s'" % name, 'nametype': "'%s'" % name_type,
                         'source': "'%s'" % source, 'authorityid': "'%s'" % auth_id}}
            ]
         else:
            print "Adding rightsholder item: %s %s %s %s" % (name, name_type, source, auth_id)
            self.meta_dicts[n]['properties']['ucldc_schema:rightsholder'].append(
               {'item': {'name': "'%s'" % name, 'nametype': "'%s'" % name_type,
                         'source': "'%s'" % source, 'authorityid': "'%s'" % auth_id}}
            )

   def verify_rights_holder(self, name, name_type, source, auth_id):
      print "Verifying rights holder: %s %s %s %s" % (name, name_type, source, auth_id)
      return True if name else False

   def set_rights_contact(self, contact, n):
      if self.verify_rights_contact(contact):
         print "Making rightscontact element: %s" % contact
         self.meta_dicts[n]['properties']['ucldc_schema:rightscontact'] = "'%s'" % contact

   def verify_rights_contact(self, contact):
      print "Verifying rights contact: %s" % contact
      return True if contact else False

   def set_rights_notice(self, notice, n):
      if self.verify_rights_notice(notice):
         print "Making rightsnotice element: %s" % notice
         self.meta_dicts[n]['properties']['ucldc_schema:rightsnotice'] = "'%s'" % notice

   def verify_rights_notice(self, notice):
      print "Verifying rights notice: %s" % notice
      return True if notice else False

   def set_rights_determination_date(self, date, n):
      if self.verify_rights_determination_date(date):
         print "Making rightsdeterminationdate element: %s" % date
         self.meta_dicts[n]['properties']['ucldc_schema:rightsdeterminationdate'] = "'%s'" % date

   def verify_rights_determination_date(self, date):
      print "Verifying rights determination date: %s" % date
      return True if date else False

   def set_rights_start_date(self, date, n):
      if self.verify_rights_start_date(date):
         print "Making rightsstartdate element: %s" % date
         self.meta_dicts[n]['properties']['ucldc_schema:rightstartdate'] = "'%s'" % date

   def verify_rights_start_date(self, date):
      print "Verifying rights start date: %s" % date
      return True if date else False

   def set_rights_end_date(self, date, n):
      if self.verify_rights_end_date(date):
         print "Making rightsenddate element: %s" % date
         self.meta_dicts[n]['properties']['ucldc_schema:rightsenddate'] = "'%s'" % date

   def verify_rights_end_date(self, date):
      print "Verifying rights end date: %s" % date
      return True if date else False

   def set_rights_jurisdiction(self, jurisdiction, n):
      if self.verify_rights_jurisdiction(jurisdiction):
         print "Making rightsjurisdiction element: %s" % jurisdiction
         self.meta_dicts[n]['properties']['ucldc_schema:rightsjurisdiction'] = "'%s'" % jurisdiction

   def verify_rights_jurisdiction(self, jurisdiction):
      print "Verifying rights jurisdiction: %s" % jurisdiction
      return True if jurisdiction else False

   def set_rights_note(self, note, n):
      if self.verify_rights_note(note):
         print "Making rightsnote element: %s" % note
         self.meta_dicts[n]['properties']['ucldc_schema:rightsnote'] = "'%s'" % note

   def verify_rights_note(self, note):
      print "Verifying rights note: %s" % note
      return True if note else False

   def set_collection(self, collection, n):
      if self.verify_collection(collection):
         if not 'ucldc_schema:collection' in self.meta_dicts[n]['properties'].keys():
            print "Making collection item: %s" % collection
            self.meta_dicts[n]['properties']['ucldc_schema:collection'] = ["'%s'" % collection]
         else:
            print "Adding collection item: %s" % collection
            self.meta_dicts[n]['properties']['ucldc_schema:collection'].append("'%s'" % collection)

   def verify_collection(self, collection):
      print "Verifying collection: %s" % collection
      return True if collection else False

   def set_related_resource(self, resource, n):
      if self.verify_related_resource(resource):
         if not 'ucldc_schema:relatedresource' in self.meta_dicts[n]['properties'].keys():
            print "Making relatedresource item: %s" % resource
            self.meta_dicts[n]['properties']['ucldc_schema:relatedresource'] = ["'%s'" % resource]
         else:
            print "Adding relatedresource item: %s" % resource
            self.meta_dicts[n]['properties']['ucldc_schema:relatedresource'].append("'%s'" % resource)

   def verify_related_resource(self, resource):
      print "Verifying related resource: %s" % resource
      return True if resource else False

   def set_source(self, source, n):
      if self.verify_source(source):
         self.meta_dicts[n]['properties']['ucldc_schema:source'] = "'%s'" % source

   def verify_source(self, source):
      print "Verifying source: %s" % source
      return True if source else False

   def set_subject_name(self, name, name_type, role, source, auth_id, n):
      if self.verify_subject_name(name, name_type, role, source, auth_id):
         if not 'ucldc_schema:subjectname' in self.meta_dicts[n]['properties'].keys():
            print "Making subjectname item: %s %s %s %s %s" % (name, name_type, role, source, auth_id)
            self.meta_dicts[n]['properties']['ucldc_schema:subjectname'] = [
               {'item' : {'name': "'%s'" % name, 'nametype': "'%s'" % name_type, 'role': "'%s'" % role,
                          'source': "'%s'" % source, 'authorityid': "'%s'" % auth_id}}
            ]
         else:
            print "Adding subjectname item: %s %s %s %s %s" % (name, name_type, role, source, auth_id)
            self.meta_dicts[n]['properties']['ucldc_schema:subjectname'].append(
               {'item' : {'name': "'%s'" % name, 'nametype': "'%s'" % name_type, 'role': "'%s'" % role,
                          'source': "'%s'" % source, 'authorityid': "'%s'" % auth_id}}
            )

   def verify_subject_name(self, name, name_type, role, source, auth_id):
      print "Verifying subject name: %s %s %s %s %s" % (name, name_type, role, source, auth_id)
      return True if name else False

   def set_place(self, name, source, coordinates, auth_id, n):
      if self.verify_place(name, source, coordinates, auth_id):
         if not 'ucldc_schema:place' in self.meta_dicts[n]['properties'].keys():
            print "Making place item: %s %s %s %s" % (name, source, coordinates, auth_id)
            self.meta_dicts[n]['properties']['ucldc_schema:place'] = [
               {'item': {'name': "'%s'" % name, 'source': "'%s'" % source,
                         'coordinates': "'%s'" % coordinates, 'authorityid': "'%s'" % auth_id}}
            ]
         else:
            print "Adding place item: %s %s %s %s" % (name, source, coordinates, auth_id)
            self.meta_dicts[n]['properties']['ucldc_schema:place'].append(
               {'item': {'name': "'%s'" % name, 'source': "'%s'" % source,
                         'coordinates': "'%s'" % coordinates, 'authorityid': "'%s'" % auth_id}}
            )

   def verify_place(self, name, source, coordinates, auth_id):
      print "Verifying place: %s %s %s %s" % (name, source, coordinates, auth_id)
      return True if name else False

   def set_subject_topic(self, heading, heading_type, source, auth_id, n):
      if self.verify_place(heading, heading_type, source, auth_id):
         if not 'ucldc_schema:subjecttopic' in self.meta_dicts[n]['properties'].keys():
            print "Making subjecttopic item: %s %s %s %s" % (heading, heading_type, source, auth_id)
            self.meta_dicts[n]['properties']['ucldc_schema:subjecttopic'] = [
               {'item': {'heading': "'%s'" % heading, 'headingtype': "'%s'" % heading_type,
                         'source': "'%s'" % source, 'authorityid': "'%s'" % auth_id}}
            ]
         else:
            print "Adding subjecttopic item: %s %s %s %s" % (heading, heading_type, source, auth_id)
            self.meta_dicts[n]['properties']['ucldc_schema:subjecttopic'].append(
               {'item': {'heading': "'%s'" % heading, 'headingtype': "'%s'" % heading_type,
                         'source': "'%s'" % source, 'authorityid': "'%s'" % auth_id}}
            )

   def verify_subject_topic(self, heading, heading_type, source, auth_id):
      print "Verifying subject topic: %s %s %s %s" % (heading, heading_type, source, auth_id)
      return True if heading else False

   def set_form_genre(self, heading, source, auth_id, n):
      if self.verify_form_genre(heading, source, auth_id):
         if not 'ucldc_schema:formgenre' in self.meta_dicts[n]['properties'].keys():
            print "Making formgenre item; %s %s %s" % (heading, source, auth_id)
            self.meta_dicts[n]['properties']['ucldc_schema:formgenre'] = [
               {'item': {'heading': "'%s'" % heading, 'source': "'%s'" % source, 'authorityid': "'%s'" % auth_id}}
            ]
         else:
            print "Adding formgenre item: %s %s %s" % (heading, source, auth_id)
            self.meta_dicts[n]['properties']['ucldc_schema:formgenre'].append(
               {'item': {'heading': "'%s'" % heading, 'source': "'%s'" % source, 'authorityid': "'%s'" % auth_id}}
            )

   def verify_form_genre(self, heading, source, auth_id):
      print "Verifying form genre: %s %s %s" % (heading, source, auth_id)
      return True if heading else False

   def set_provenance(self, provenance, n):
      if self.verify_provenance(provenance):
         if not 'ucldc:provenance' in self.meta_dicts[n]['properties'].keys():
            print "Making provenance item: %s" % provenance
            self.meta_dicts[n]['properties']['ucldc_schema:provenance'] = ["'%s'" % provenance]
         else:
            print "Making provenance item: %s" % provenance
            self.meta_dicts[n]['properties']['ucldc_schema:provenance'].append("'%s'" % provenance)

   def verify_provenance(self, provenance):
      print "Verifying provenance: %s" % provenance
      return True if provenance else False

   def set_physical_location(self, location, n):
      if self.verify_physical_location(location):
         print "Making phylocation element: %s" % location
         self.meta_dicts[n]['properties']['ucldc_schema:physlocation'] = "'%s'" % location

   def verify_physical_location(self, location):
      print "Verifying phyical location: %s" % location
      return True if location else False
