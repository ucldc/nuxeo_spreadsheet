Python scripts for processing and migrating data into Nuxeo

### Requirements

You will need a python environment.

You will need to have pynux set up in the environment.

You will need information from the Nuxeo Administrator for setting up a `.pynuxrc` file.

These directions are for python 2.x.

```
virtualenv venv
. venv/bin/activate
pip install git+git://github.com/ucldc/pynux.git
pip install unicodecsv
```

## `csv2dict`
a project to develop a csv template approach

Once your `.pynuxrc` file is configured, create documents in Nuxeo.

Once your documents are created:
```
nxls /asset-library/UCX/Project_folder
```

Use those paths in the spreadsheet.  Load with `meta_from_csv.py`

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
sample code for loading METS into Nuxeo
