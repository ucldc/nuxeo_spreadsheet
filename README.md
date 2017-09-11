# Prerequisites
[Follow these instructions first](https://github.com/ucldc/nuxeo_spreadsheet/wiki), to install the prerequisites to run `nuxeo_spreadsheet`. 


# Using `nuxeo_spreadsheet`
`nuxeo_spreadsheet` constitutes a set of prototype Python scripts ("csv2dict"), which can be used to import metadata in a tab-delimited spreadsheet into  Nuxeo. Note that comma separated value-based spreadsheets (CSV) are not supported ("csv2dict" is a misnomer).

## 1. Upload files to a Project Folder in Nuxeo
Once you have the prerequisites in place, upload your content files into a Project Folder in Nuxeo.  Import the files through the Nuxeo UI, or use the <a href="https://registry.cdlib.org/documentation/docs/dams/bulk-import/">bulk import options</a>.

## 2. Get directory paths to the files
Next, generate a list of directory paths for the files in that Project Folder.  You'll need the path to the Project Folder; it's reflected in the URL in your browser view of Nuxeo. Make sure you are in your python environment (e.g., venv) and run this command. 
```
nxls /asset-library/UCX/Project_folder --show-only-path
```
Optionally, add the additional `>` command followed a .txt filename, to output the list of directory paths to a .txt file in your home directory (e.g., at `cd C:\Users\yourname\`):

```
nxls /asset-library/UCX/Project_folder --show-only-path > paths.txt 
```

If you're using miniconda within Windows, here's an overview of the process:

* Open the Command Prompt from the Start menu
* Activate your python environment.  In this example, we're activating a python environment named "venv": `activate venv`
* Run the command: `nxls /asset-library/UCX/Project_folder --show-only-path` 

## 3. Create metadata in tab-delimited spreadsheet
**Use [Nuxeo Spreadsheet Template](https://docs.google.com/spreadsheets/d/1vl4va-deIf3wo1s3J9VMG3k_TAJY4wYCtWFbFxTBoRk/edit#gid=0).** The first tab comprises the template; the second tab provides an example for reference purposes.  

Note with the following considerations:

* We'd suggest saving a copy of the template in Google Sheets, and working directly in the Google Sheets format to build out the metadata. We do not recommend using Excel (.xlsx), based on our initial tests (Excel can add additional quotes around text, and also introduce errors with special characters).

* The column headings in the tab-delimited spreadsheet need to *exactly* match the headings expected by the Python scripts constituting `nuxeo_spreadsheet`. You can double-check the headings by reviewing the columns.txt file in GitHub.

* In cases where metadata elements are repeatable in Nuxeo, you can append a numeric indicator after the column heading.  In the <a href="https://docs.google.com/spreadsheets/d/1JFiLA2eE6O2KDtSl3nHGpNU7zGP8Sk4p60GqOZtnUoM/edit#gid=0">Nuxeo Tab-Delimited Spreadsheet Template</a>, you can see examples of this for Creator.  When using this function, note that you must include columns for all complex data fields (e.g., if repeating Creator information, the following fields must be in place: `Creator # Name`, `Creator # Name Type`, `Creator # Role`, `Creator # Source`, and `Creator # Authority ID`).

* Each row in the spreadsheet can contain metadata for either a simple object, a parent-level record for a complex object, or a component for a complex object. The main thing to ensure is that the row corresponds to the correct <b>File Path</b> in Nuxeo.

* <b>File Path</b> (color-coded in red) is required for each row; additionally, either <b>Title</b>, <b>Type</b>, <b>Copyright Status</b>, and/or <b>Copyright Statement</b> is required, if and when the objects will be published in Calisphere. For additional information on the metadata requirements, see the <a href="https://registry.cdlib.org/documentation/docs/dams/metadata-model/">Nuxeo user guide</a>

* The <b>File Path</b> cell should contain the *exact* file directory path to the content file in Nuxeo, to be associated with the metadata record (e.g., "/asset-library/UCOP/nuxeo_tab_import_demo/ucm_li_1998_009_i.jpg").

* If using Google Sheets directly to create your metadata records, note that some of the fields have validation rules.  These fields are keyed to controlled vocabularies established in Nuxeo.

* Once you've completed the process of creating metadata records using the template, save a copy as a tab-delimited file.

![screen shot 2016-06-01 at 5 23 53 pm](https://cloud.githubusercontent.com/assets/227374/15734242/789b2380-2842-11e6-9427-a39f64eed608.png)

If using Google Sheets, download as tab separated value:

<img width="642" alt="screen shot 2016-06-01 at 9 59 58 pm" src="https://cloud.githubusercontent.com/assets/227374/15734442/9421a0c8-2844-11e6-8179-27e4397e8c4d.png">
 

## 4. Import metadata in tab-delimited spreadsheet into Nuxeo 
Load with `meta_from_csv.py`. This process will convert the metadata from the spreadsheet into Python dict outputs, and call pynux to import the Python dict outputs directly into Nuxeo.

```
usage: meta_from_csv.py [-h] --datafile DATAFILE [-d] [--loglevel LOGLEVEL]
                        [--rcfile RCFILE]

optional arguments:
  -h, --help           show this help message and exit
  --datafile DATAFILE  tab-delimited spreadsheet input file -- required
  -d, --dry-run        dry run
  --blankout           blank out all fields not set in sheet

common options for pynux commands:
  --loglevel LOGLEVEL  CRITICAL ERROR WARNING INFO DEBUG NOTSET, default is
                       ERROR
  --rcfile RCFILE      path to ConfigParser compatible ini file
```

Note for Windows: you may need to run `python meta_from_csv.py ...`
or edit the shebang. If you're using miniconda within Windows, here's an overview of the process:

* Open the Command Prompt from the Start menu
* Activate your python environment.  In this example, we're activating a python environment named "venv": `activate venv`
* Go to nuxeo_spreadsheet\csv2dict in your home directory, e.g.: `cd C:\Users\yourname\nuxeo_spreadsheet\csv2dict`
* Run the command.  In this example, the DATAFILE is the location of a tab-delimited file (named "tab-delimited-metadata.txt") that's on our Desktop. `python meta_from_csv.py --datafile C:\Users\yourname\Desktop\tab-delimited-metadata.txt`


# `mets_example`
Sample code for loading METS into Nuxeo
