Python scripts for processing and migrating data into Nuxeo

### Requirements

You will need a python environment.

You will need to have pynux set up in the environment.

You will need information from the Nuxeo Administrator for setting up a `.pynuxrc` file.

These directions are for python 2.x.

```
virtualenv venv
. venv/bin/activate
pip install https://github.com/ucldc/nuxeo_spreadsheet/archive/master.zip
pip install unicodecsv
```

## `csv2dict`
A prototype comma-separated value (CSV) spreadsheet metadata import process, for use with Nuxeo.

1) Once your `.pynuxrc` file is configured, upload your content files into Nuxeo.  Import the files through the Nuxeo UI, or use the <a href="https://registry.cdlib.org/documentation/docs/dams/bulk-import/">bulk import options</a>.

2) Next, generate a list of content file directory paths:
```
nxls /asset-library/UCX/Project_folder
```

3) Use the <a href="https://docs.google.com/spreadsheets/d/1JFiLA2eE6O2KDtSl3nHGpNU7zGP8Sk4p60GqOZtnUoM/edit#gid=0">Nuxeo CSV Import Template</a> to format your metadata records. The first tab comprises the template; the second tab provides an example for reference purposes.  Note with the following considerations:

* Each row should contain metadata for either a simple object, or the parent-level record for a complex object
* The "File Path" cell should contain the exact file directory path to the content file in Nuxeo, to be associated with the metadata record (e.g., "/asset-library/UCOP/nuxeo_tab_import_demo/ucm_li_1998_009_i.jpg").
* If using Google Sheets directly to create your metadata records, note that some of the fields have validation rules.  These fields are keyed to controlled vocabularies established in Nuxeo.
* Once you've completed the process of creating metadata records using the template, save a copy as a comma-separated value (CSV) file. This 
* For additional information on each Nuxeo field, consult our <a href="https://registry.cdlib.org/documentation/docs/dams/metadata-model/">Nuxeo user guide</a>

4) Load with `meta_from_csv.py`

```
usage: meta_from_csv.py [-h] --datafile DATAFILE --rcfile RCFILE
                        [--loglevel LOGLEVEL]

optional arguments:
  -h, --help           show this help message and exit
  --datafile DATAFILE  CSV data input file -- required
  --rcfile RCFILE      Pynux resource file -- required
  --loglevel LOGLEVEL  Set Pynux logging level
```


## `mets_example`
Sample code for loading METS into Nuxeo
