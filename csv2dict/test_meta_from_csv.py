import unittest
import meta_from_csv
import valid_columns
from Csv2Dict import Csv2Dict
import os

class Test_CSVtoDict(unittest.TestCase):
    def setUp(self):
        self.datafile = "data/test_tsv.tsv"
        self.csv2dict = Csv2Dict(self.datafile)
        self.row_dicts = self.csv2dict.get_row_dicts()
        self.n = self.csv2dict.new_dict(self.row_dicts[0]['File path'])
            
    def test_alt_title(self):
        self.csv2dict.set_list_element('alternativetitle', 'Alternative Title', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:alternativetitle'], 
            [u'Test Alternative Title 1', u'Alternative Title 2', u'Alternative Title 3'])
    
    def test_loc_id(self):
        self.csv2dict.set_list_element('localidentifier', 'Local Identifier', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:localidentifier'], 
            [u'Local Identifier 1'])
    
    def test_campus_unit(self):
        self.csv2dict.set_list_element('campusunit', 'Campus/Unit', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:campusunit'], 
            [])
    def test_publisher(self):
        self.csv2dict.set_list_element('publisher', 'Publication/Origination Info', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:publisher'], 
            [u'Publisher:Publication Location'])
            
    def test_temporal_coverage(self):
        self.csv2dict.set_list_element('temporalcoverage', 'Temporal Coverage', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:temporalcoverage'], 
            [u'(34.052234, -118.243685)'])
    
    def test_collection(self):
        self.csv2dict.set_list_element('collection', 'Collection', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:collection'], 
            [u'Collection 2'])
     
    def test_related_resource(self):
        self.csv2dict.set_list_element('relatedresource', 'Related Resource', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:relatedresource'], 
            [u'Related Resource 1', u'Related Resource 2', u'Related Resource 23']) 
    
    def test_provenance(self):
        self.csv2dict.set_list_element('provenance', 'Provenance', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:provenance'], 
            [u'https://provenance.test']) 
   
    def test_date(self):
        self.csv2dict.set_dict_element('date', 'Date ', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:date'], 
            [{'date': u"1990",
            'datetype': u"Date 1 Type",
            'inclusivestart': u"1990",
            'inclusiveend': u"",
            'single': u""}]) 
    
    def test_creator(self):
        self.csv2dict.set_dict_element('creator', 'Creator ', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:creator'], 
            [{'name': 'Creator 1 Name', 'nametype': 'Creator 1 Name Type',
            'role': 'Creator 1 Role', 'source': 'Creator 1 Source',
            'authorityid': 'Creator 1 Authority ID'},
            {'name': 'Creator 2 Name', 'nametype': 'Creator 2 Name Type',
            'role': 'Creator 2 Role', 'source': 'Creator 2 Source',
            'authorityid': 'Creator 2 Authority ID'}
            ]) 
    
    def test_contributor(self):
        self.csv2dict.set_dict_element('contributor', 'Contributor ', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:contributor'], 
            [{'name': 'Contributor 1 Name', 'nametype': 'Contributor 1 Name Type',
            'role': 'Contributor 1 Role', 'source': 'Contributor 1 Source',
            'authorityid': 'Contributor 1 Authority ID'}
            ]) 
    
    def test_description(self):
        self.csv2dict.set_dict_element('description', 'Description ', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:description'], 
            [{'item':'Description 1 Note', 'type':'Description 1 Type'},
            {'item':'Description 2 Note', 'type':'Description 2 Type'}
            ]) 
    
    def test_language(self):
        self.csv2dict.set_dict_element('language', 'Language ', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:language'], 
            [{'language':'Language 1', 'languagecode':None}
            ]) 
            
    def test_subjectname(self):
        self.csv2dict.set_dict_element('subjectname', 'Subject (Name) ', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:subjectname'], 
            [{u'name': '',
            'nametype': 'Subject (Name) 1 Name Type',
            'role': 'Subject (Name) 1 Role',
            'source': '',
            'authorityid': ''}
            ]) 
    
    def test_place(self):
        self.csv2dict.set_dict_element('place', 'Place ', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:place'], 
            [{'name': "Place 1 Name",
            'source': "Place 1 Source",
            'coordinates': "Place 1 Coordinates",
            'authorityid': "Place 1 Authority ID"}
            ]) 
    
    def test_form_genre(self):
        print(self.n)
        self.csv2dict.set_dict_element('formgenre', 'Form/Genre ', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        #print(meta_dict['properties'])
        self.assertEqual(meta_dict['properties']['ucldc_schema:formgenre'], 
            [{'heading': "Form/Genre 1 Heading",
            'source': "Form/Genre 1 Source",
            'authorityid': ""},
            {'heading': "Form/Genre 2 Heading",
            'source': "Form/Genre 2 Source",
            'authorityid': "Form/Genre 2 Authority ID"},
            {'heading': "Form/Genre 3 Heading",
            'source': "Form/Genre 3 Source",
            'authorityid': "Form/Genre 3 Authority ID"},
            {'heading': "Form/Genre 4 Heading",
            'source': "Form/Genre 4 Source",
            'authorityid': ""},
            {'heading': "Form/Genre 5 Heading",
            'source': "Form/Genre 5 Source",
            'authorityid': ""},
            {'heading': "Form/Genre 6 Heading",
            'source': "Form/Genre 6 Source",
            'authorityid': ""}  
            ])
    
    def test_rights_holder(self):
        print(self.n)
        self.csv2dict.set_dict_element('rightsholder', 'Copyright Holder ', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        #print(meta_dict['properties'])
        self.assertEqual(meta_dict['properties']['ucldc_schema:rightsholder'], 
            [{'name': 'Copyright Holder 1 Name',
            'nametype': 'Copyright Holder 1 Name Type',
            'source': 'Copyright Holder 1 Source',
            'authorityid': 'Copyright Holder 1 Authority ID'}])
            
    def test_subjecttopic(self):
        self.csv2dict.set_dict_element('subjecttopic', 'Subject (Topic) ', self.row_dicts[0], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:subjecttopic'], 
            [{'heading': "Subject (Topic) 1 Heading",
            'source': "Subject (Topic) 1 Source",
            'headingtype': "Subject (Topic) 1 Heading Type",
            'authorityid': ""},
            {'heading': "Subject (Topic) 2 Heading",
            'source': "Subject (Topic) 2 Source",
            'headingtype': "Subject (Topic) 2 Heading Type",
            'authorityid': ""}
            ]) 
    
    def test_identifier(self):
        self.csv2dict.set_single_element('identifier', self.row_dicts[0]['Identifier'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:identifier'], 'Identifier')
    
    def test_type(self):
        self.csv2dict.set_single_element('type', self.row_dicts[0]['Type'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:type'], 'Type')

    def test_extent(self):
        self.csv2dict.set_single_element('extent', self.row_dicts[0]['Extent'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:extent'], 'Extent')
    
    def test_transcription(self):
        self.csv2dict.set_single_element('transcription', self.row_dicts[0]['Transcription'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:transcription'], 'Transcription')
    
    def test_accessrestrictions(self):
        self.csv2dict.set_single_element('accessrestrictions', self.row_dicts[0]['Access Restrictions'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:accessrestrictions'], 'Access Restrictions')
    
    def test_rightsstatement(self):
        self.csv2dict.set_single_element('rightsstatement', self.row_dicts[0]['Copyright Statement'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:rightsstatement'], 'Copyright Statement')
    
    def test_rightsstatus(self):
        self.csv2dict.set_single_element('rightsstatus', self.row_dicts[0]['Copyright Status'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:rightsstatus'], 'Copyright Status')
    
    def test_rightsnotice(self):
        self.csv2dict.set_single_element('rightsnotice', self.row_dicts[0]['Copyright Contact'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:rightsnotice'], 'Copyright Contact')
    
    def test_rightscontact(self):
        self.csv2dict.set_single_element('rightscontact', self.row_dicts[0]['Copyright Contact'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:rightscontact'], 'Copyright Contact')
    
    def test_rightsjurisdiction(self):
        self.csv2dict.set_single_element('rightsjurisdiction', self.row_dicts[0]['Copyright Jurisdiction'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:rightsjurisdiction'], 'Copyright Jurisdiction')
    
    def test_rightsnote(self):
        self.csv2dict.set_single_element('rightsnote', self.row_dicts[0]['Copyright Note'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:rightsnote'], 'Copyright Note')
    
    def test_source(self):
        self.csv2dict.set_single_element('source', self.row_dicts[0]['Source'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:source'], 'Source')
    
    def test_physlocation(self):
        self.csv2dict.set_single_element('physlocation', self.row_dicts[0]['Physical Location'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:physlocation'], 'Physical Location')
        
    def test_physdesc(self):
        self.csv2dict.set_single_element('physdesc', self.row_dicts[0]['Format/Physical Description'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertEqual(meta_dict['properties']['ucldc_schema:physdesc'], 'Format/Physical Description')

    def test_rightsdeterminationdate(self):
        self.csv2dict.set_single_element('rightsdeterminationdate', self.row_dicts[0]['Copyright Determination Date'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertRaises(KeyError, lambda: meta_dict['properties']['ucldc_schema:rightsdeterminationdate'])
        
    def test_rightsstartdate(self):
        self.csv2dict.set_single_element('rightsstartdate', self.row_dicts[0]['Copyright Start Date'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertRaises(KeyError, lambda: meta_dict['properties']['ucldc_schema:rightsstartdate'])
    
    def test_rightsenddate(self):
        self.csv2dict.set_single_element('rightsenddate', self.row_dicts[0]['Copyright End Date'], self.n)
        meta_dict = self.csv2dict.get_meta_dict(self.n)
        self.assertRaises(KeyError, lambda: meta_dict['properties']['ucldc_schema:rightsenddate'])
    
if __name__ == '__main__':
    unittest.main()
