"""
This script allows the users to export descriptive metadata from Nuxeo
and save to either a Google Sheets spreadsheet or a local TSV file.

Default behavior downloads metadata at the object level
(one spreadsheet row per parent-level digital object)
and saves to a local TSV file. It includes column headers
only for properties that contain non-null and non-empty string values.

Command-line options allow the choice to export to Google Sheets,
export data at the item level (one row per item, including each
individual component of a complex object), or include all headers
(including those with null/blank values)

First written by Niqui O'Neill (UCLA Digital Library Program) in 2018.
"""
import os
import json
import argparse
import unicodecsv as csv
from pynux import utils
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def main():
    """ parse command-line args,
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("path",
                        nargs=1,
                        type=str,
                        help="Nuxeo file path to export metadata from")

    parser.add_argument(
        "--item-level",
        action="store_true",
        help=
        "export data for all items, including component items of complex objects."
    )

    parser.add_argument(
        "--all-headers",
        action="store_true",
        help="export data with all headers, even if values are blank")

    parser.add_argument("-s",
                        "--sheet",
                        type=str,
                        required=False,
                        help="Google Sheets destination URL")

    args = parser.parse_args()

    nuxeo_top_path = args.path[0].strip()
    item_level = args.item_level
    all_headers = args.all_headers
    gsheets_url = args.sheet
    if gsheets_url:
        gsheets_url = gsheets_url.strip()

    # google_error_text = (
    #     "\n*********\nWriting to Google document did not work."
    #     "Make sure that Google document has been shared "
    #     "with API key email address")

    metadata = get_metadata(nuxeo_top_path, item_level)
    fieldnames = make_fieldnames(metadata, all_headers)
    sheet_name = nuxeo_top_path.split("/")[-1].lower()

    if gsheets_url:
        write_gsheet(metadata, sheet_name, fieldnames, gsheets_url)

    else:
        sheet_name += ".tsv"
        write_csv(metadata, sheet_name, fieldnames, delimiter="\t")


def get_metadata(nuxeo_top_path, item_level=False):
    """ authorize nuxeo client,
        iterate over documents to retrieve and map metadata rows
        return list of dicts (1 dict = 1 metadata row)
    """

    nx = utils.Nuxeo()

    data = []
    if item_level:
        for doc in nx.children(nuxeo_top_path):
            for item in nx.children(doc["path"]):
                metadata_row = make_metadata_row(item)
                data.append(metadata_row)
    else:  # object level
        for doc in nx.children(nuxeo_top_path):
            metadata_row = make_metadata_row(doc)
            data.append(metadata_row)

    return data


def make_metadata_row(nxdoc):
    """ map Nuxeo JSON to flat data structure with human-readable labels
        (1 Nuxeo object = 1 metadata row)

        input: metadata for one Nuxeo object ('nxdoc',
            JSON document retrieved from Nuxeo)

        returns: flat dict that will become one spreadsheet row
            ('metadata_record')

            keys: spreadsheet column label (string)
            values: metadata value (string, list of strings, list of dicts)
    """

    metadata_record = {}

    # this json file groups fields by datatype,
    # matches spreadsheet labels to nuxeo properties
    with open("simple_ucldc.json", "r") as infile:
        ucldc_map = json.load(infile)

    metadata_record["File path"] = nxdoc.get("path")

    # single-value string fields
    for key, value in ucldc_map["string"].items():
        metadata_record[key] = nxdoc["properties"].get(value)

    # lists of strings
    for key, value in ucldc_map["string_list"].items():
        num = 0
        while num < len(nxdoc["properties"].get(value)):
            field_label = key % (num + 1)
            metadata_record[field_label] = nxdoc["properties"].get(value)[num]
            num += 1

    # lists of dicts
    for field, subfields in ucldc_map["complex_list"].items():
        num = 0
        field_data = nxdoc["properties"].get(field)
        while num < len(field_data):
            for key, value in subfields.items():
                field_label = key % (num + 1)
                metadata_record[field_label] = field_data[num].get(value)
            num += 1

    return metadata_record


def make_fieldnames(data, all_headers):
    """ ensures that File path, Title and Type are the first three rows
    """
    # TODO: sort complex fields correctly.
    # current code is sorting Heading 1, Heading 2, Source 1, Source 2
    # should be Heading 1, Source 1, Heading 2, Source 2

    fields_in_use = []
    for row in data:
        for key in row.keys():
            if key not in fields_in_use:
                fields_in_use.append(key)

    fieldnames = []

    if all_headers:
        with open("../csv2dict/columns.txt", "r") as infile:
            valid_columns = [i.strip() for i in infile.readlines()]
        for column in valid_columns:
            if "%" in column:
                num = 1
                fieldnames.append(column % num)
                num += 1
                while column % num in fields_in_use:
                    fieldnames.append(column % num)
                    num += 1
            else:
                fieldnames.append(column)
    else:
        fieldnames = ["File path", "Title", "Type"]
        for metadata_record in data:
            for key in metadata_record.keys():
                if key not in fieldnames:
                    fieldnames.append(key)

    return fieldnames


def write_csv(data, filename, fieldnames, delimiter=","):
    """ write out to csv/tsv file
    """
    with open(filename, "wb") as outfile:
        writer = csv.DictWriter(outfile,
                                delimiter=delimiter,
                                fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def write_gsheet(data, sheet_name, fieldnames, gsheets_url):
    """ create temp. csv, import to google sheets
    """
    temp = "temp.csv"
    write_csv(data, temp, fieldnames)
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "client_secret.json", scope)
    client = gspread.authorize(creds)
    with open(temp,
              encoding="utf8") as infile:  #opens and reads temporary csv file
        data = infile.read() + "\n"
    sheet_id = client.open_by_url(gsheets_url).id
    client.import_csv(sheet_id, data)  #writes csv file to google sheet
    client.open_by_key(sheet_id).sheet1.update_title(sheet_name)
    os.remove(temp)  #removes temporary csv


if __name__ == "__main__":
    main()
