__author__ = 'glen'

import sys
from Csv2Dict_py3 import Csv2Dict
from pprint import PrettyPrinter

pp = PrettyPrinter().pprint

if len(sys.argv) == 2:
   csv_data_file = sys.argv[1]
else:
   print ('A data file must be provided..')
   sys.exit(1)

print (csv_data_file)

# get and instance of the Csv2Dict class which must be initialized
# with the name of an input data (csv) file
csv2dict = Csv2Dict(csv_data_file)

if csv2dict.status != 0:
   print ('The Csv2Dict constructor reported and error (%d).' % csv2dict.status)
   sys.exit(csv2dict.status)

row_dicts = csv2dict.get_row_dicts()

for n in range(len(row_dicts)):
   print ('Metarow%3d) %s' % (n, str(row_dicts[n])))

for row in row_dicts:
   '''
   Csv2Dict.new_dict(path) creates a new dict with two keys, 'path' and 'properties'. The value of
   'path' is the asset_path, and the value of 'properties' is an empty dict to be filled in later.
   This whole structure is appended to a List of dicts, one dict for each row in the csv file, returning
   the new dict's position in the List.
   '''

   n = csv2dict.new_dict(row['File path'])

   csv2dict.set_title(row['Title'], n)
   csv2dict.set_alt_title(row['Alternative Title'], n)
   csv2dict.set_id(row['Identifier'], n)
   csv2dict.set_local_id(row['Local Identifier'], n)
   csv2dict.set_type(row['Type'], n)
   csv2dict.set_campus_unit(row['Campus/Unit'], n)
   csv2dict.set_date(row['Date'],
                     row['Date Type'],
                     row['Inclusive Start'],
                     row['Inclusive End'],
                     row['Single'], n)

   num = 1
   while 'Creator %d Name' % num in row.keys():
      csv2dict.set_creator(row['Creator %d Name' % num],
                           row['Creator %d Name Type' % num],
                           row['Creator %d Role' % num],
                           row['Creator %d Source' % num],
                           row['Creator %d Authority ID' % num], n)
      num += 1

   csv2dict.set_contributor(row['Contributor Name'],
                            row['Contributor Name Type'],
                            row['Contributor Role'],
                            row['Contributor Source'],
                            row['Contributor Authority ID'], n)

   csv2dict.set_physdesc(row['Format/Physical Description'], n)

   num = 1
   while 'Description %d Note' % num in row.keys():
      csv2dict.set_description(row['Description %d Note' % num],
                               row['Description %d Type' % num], n)
      num += 1

   csv2dict.set_extent(row['Extent'], n)
   csv2dict.set_language(row['Language'],
                         row['Language Code'], n)
   csv2dict.set_temporal_coverage(row['Temporal Coverage'], n)
   csv2dict.set_transcription(row['Transcription'], n)
   csv2dict.set_access_restrictions(row['Access Restrictions'], n)
   csv2dict.set_rights_statement(row['Copyright Statement'], n)
   csv2dict.set_rights_status(row['Copyright Status'], n)
   csv2dict.set_rights_holder(row['Copyright Holder Name'],
                              row['Copyright Holder Name Type'],
                              row['Copyright Holder Source'],
                              row['Copyright Holder Authority ID'], n)
   csv2dict.set_rights_contact(row['Copyright Contact'], n)
   csv2dict.set_rights_notice(row['Copyright Notice'], n)
   csv2dict.set_rights_determination_date(row['Copyright Determination Date'], n)
   csv2dict.set_rights_start_date(row['Copyright Start Date'], n)
   csv2dict.set_rights_end_date(row['Copyright End Date'], n)
   csv2dict.set_rights_jurisdiction(row['Copyright Jurisdiction'], n)
   csv2dict.set_rights_note(row['Copyright Note'], n)

   num = 1
   while 'Collection %d' % num in row.keys():
      csv2dict.set_collection(row['Collection %d' % num], n)
      num += 1

   csv2dict.set_related_resource(row['Related Resource'], n)
   csv2dict.set_source(row['Source'], n)

   num = 1
   while 'Subject (Name) %d Name' % num in row.keys():
      csv2dict.set_subject_name(row['Subject (Name) %d Name' % num],
                                row['Subject (Name) %d Name Type' % num],
                                row['Subject (Name) %d Role' % num],
                                row['Subject (Name) %d Source' % num],
                                row['Subject (Name) %d Authority ID' % num], n)
      num += 1

   num = 1
   while 'Place %d Name' % num in row.keys():
      csv2dict.set_place(row['Place %d Name' % num],
                         row['Place %d Source' % num],
                         row['Place %d Coordinates' % num],
                         row['Place %d Authority ID' % num], n)
      num += 1

   num = 1
   while 'Subject (Topic) %d Heading' % num in row.keys():
      csv2dict.set_subject_topic(row['Subject (Topic) %d Heading' % num],
                                 row['Subject (Topic) %d Heading Type' % num],
                                 row['Subject (Topic) %d Source' % num],
                                 row['Subject (Topic) %d Authority ID' % num], n)
      num += 1

   num = 1
   while 'Form/Genre %d Heading' % num in row.keys():
      csv2dict.set_form_genre(row['Form/Genre %d Heading' % num],
                              row['Form/Genre %d Source' % num],
                              row['Form/Genre %d Authority ID' % num], n)
      num += 1

   csv2dict.set_provenance(row['Provenance'], n)
   csv2dict.set_physical_location(row['Physical Location'], n)

csv2dict.print_meta_dicts('LOGS/latest_output.txt')

