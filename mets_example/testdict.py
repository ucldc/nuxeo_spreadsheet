#!/usr/bin/env python

properties_list = [['testkey', 'testing this key'],['ucldc_schema:description', [['item', 'The All American Canal, between Holtville etc.'], ['type', 'scopecontent']]], ['dictionary', [{'a': 'imadict', 'b': 'and so are you'}]]]

def format_properties( properties_list ):
  for l in properties_list:
    print l[0]
    if isinstance(l[1], str):
      print l[1]+' IS STR'
    elif isinstance(l[1], list):
      print str(l[1])+' IS LIST'
      if isinstance(l[1][0], dict):
         print str(l[1][0])+' IS DICT'
      elif isinstance(l[1][0], list):
         print str(l[1][0])+' IS LIST'
      elif isinstance(l[1][0], str):
         print str(l[1][0])+' IS STR'
    elif isinstance(l[1], dict):
      print str(l[1])+' IS ALSO A DICT'
    else:
      print str(l[1])+' IS UNKNOWN'
      print l[1].__class__


def format_element( el ):
  if isinstance(el, list) and len(el) == 2 and isinstance(el[0], str):
     return [{el[0]: [el[1]]}]

for l in properties_list:
  x = format_element(l)
  print x

#format_properties(properties_list)

