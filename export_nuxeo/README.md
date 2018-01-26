This script gets all metadata from Nuxeo. It requires the prerequisite instructions from nuxeo_spreadsheet to be followed: https://github.com/ucldc/nuxeo_spreadsheet/wiki. If writing to a Google sheet, make sure to follow step 3.

1. run script

        $ python nuxeo_get_metadata.py

1. Enter the filepath of nuxeo assets (i.e. /asset-library/UCLA/)

1. Enter O or I for Object or Item level. Object level gets all metadata from the filepath; Item level gets all metadata for the items one step below the filepath.

1. Enter google sheet URL. If you want the data written to a tsv and not a google sheet simply hit enter.

1. Enter 'Y' if you want all headers, even columns with no data to be written to the spreadsheet. Otherwise enter 'N' and only columns with data will be downloaded.

1. File will be downloaded or written to Google sheet based on choices.
