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
import argparse
import unicodecsv as csv
from pynux import utils
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def main():
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

    nx = utils.Nuxeo()

    # google_error_text = (
    #     "\n*********\nWriting to Google document did not work."
    #     "Make sure that Google document has been shared "
    #     "with API key email address")

    data = []
    if item_level:
        for obj in nx.children(nuxeo_top_path):
            for item in nx.children(obj["path"]):
                metadata_row = process_metadata(item, all_headers)
                data.append(metadata_row)
    else:
        for obj in nx.children(nuxeo_top_path):
            metadata_row = process_metadata(obj, all_headers)
            data.append(metadata_row)

    fieldnames = make_fieldnames(data, all_headers)
    sheet_name = nuxeo_top_path.split("/")[-1].lower()

    if gsheets_url:
        write_gsheet(data, sheet_name, fieldnames, gsheets_url)

    else:
        sheet_name += ".tsv"
        write_csv(data, sheet_name, fieldnames, delimiter="\t")


def process_metadata(nxdoc, all_headers):
    """ map Nuxeo JSON to flat data structure with human-readable labels
    """

    data2 = {}

    get_single_string_fields(data2, nxdoc)
    get_string_list_fields(data2, nxdoc)
    get_dict_list_fields(data2, nxdoc)

    return data2


def get_single_string_fields(data2, nxdoc):
    """ map fields that are non-repeating string values
    """

    data2["File path"] = nxdoc.get("path")

    property_map = {
        "Title": "dc:title",
        "Identifier": "ucldc_schema:identifier",
        "Type": "ucldc_schema:type",
        "Format/Physical Description": "ucldc_schema:physdesc",
        "Extent": "ucldc_schema:extent",
        "Transcription": "ucldc_schema:transcription",
        "Access Restrictions": "ucldc_schema:accessrestrict",
        "Copyright Statement": "ucldc_schema:rightsstatement",
        "Copyright Status": "ucldc_schema:rightsstatus",
        "Copyright Contact": "ucldc_schema:rightscontact",
        "Copyright Notice": "ucldc_schema:rightsnotice",
        "Copyright Determination Date": "ucldc_schema:rightsdeterminationdate",
        "Copyright End Date": "ucldc_schema:rightsstartdate",
        "Copyright Jurisdiction": "ucldc_schema:rightsjurisdiction",
        "Copyright Note": "ucldc_schema:rightsnote",
        "Source": "ucldc_schema:source",
        "Physical Location": "ucldc_schema:physlocation"
    }

    for key, value in property_map.items():
        data2[key] = nxdoc["properties"].get(value)


def get_string_list_fields(data2, nxdoc):
    """ map fields that are flat lists of strings
    """

    property_map = {
        "Alternative Title %d": "ucldc_schema:alternativetitle",
        "Local Identifier %d": "ucldc_schema:localidentifier",
        "Campus/Unit %d": "ucldc_schema:campusunit",
        "Publication/Origination Info %d": "ucldc_schema:publisher",
        "Temporal Coverage %d": "ucldc_schema:temporalcoverage",
        "Collection %d": "ucldc_schema:collection",
        "Related Resource %d": "ucldc_schema:relatedresource",
        "Provenance %d": "ucldc_schema:provenance"
    }

    for key, value in property_map.items():
        num = 0
        while num < len(nxdoc["properties"].get(value)):
            field_label = key % (num + 1)
            data2[field_label] = nxdoc["properties"].get(value)[num]
            num += 1


def get_dict_list_fields(data2, nxdoc):
    """ map complex fields that are lists of dicts
    """
    complex_property_map = {
        "ucldc_schema:date": {
            "Date %d": "date",
            "Date %d Type": "datetype",
            "Date %d Inclusive Start": "inclusivestart",
            "Date %d Inclusive End": "inclusiveend",
            "Date %d Single": "single"
        },
        "ucldc_schema:creator": {
            "Creator %d Name": "name",
            "Creator %d Name Type": "nametype",
            "Creator %d Role": "role",
            "Creator %d Source": "source",
            "Creator %d Authority ID": "authorityid"
        },
        "ucldc_schema:contributor": {
            "Contributor %d Name": "name",
            "Contributor %d Name Type": "nametype",
            "Contributor %d Role": "role",
            "Contributor %d Source": "source",
            "Contributor %d Authority ID": "authorityid"
        },
        "ucldc_schema:description": {
            "Description %d Note": "item",
            "Description %d Type": "type"
        },
        "ucldc_schema:language": {
            "Language %d": "language",
            "Language %d Code": "languagecode"
        },
        "ucldc_schema:rightsholder": {
            "Copyright Holder %d Name": "name",
            "Copyright Holder %d Name Type": "nametype",
            "Copyright Holder %d Role": "role",
            "Copyright Holder %d Source": "source",
            "Copyright Holder %d Authority ID": "authorityid"
        },
        "ucldc_schema:subjectname": {
            "Contributor %d Name": "name",
            "Contributor %d Name Type": "nametype",
            "Contributor %d Role": "role",
            "Contributor %d Source": "source",
            "Contributor %d Authority ID": "authorityid"
        },
        "ucldc_schema:place": {
            "Place %d Name": "name",
            "Place %d Source": "source",
            "Place %d Coordinates": "coordinates",
            "Place %d Authority ID": "authorityid"
        },
        "ucldc_schema:subjecttopic": {
            "Subject (Topic) %d Heading": "heading",
            "Subject (Topic) %d Heading Type": "headingtype",
            "Subject (Topic) %d Source": "source",
            "Subject (Topic) %d Authority ID": "authorityid"
        },
        "ucldc_schema:formgenre": {
            "Form/Genre %d Heading": "heading",
            "Form/Genre %d Source": "source",
            "Form/Genre %d Authority ID": "authorityid"
        }
    }

    for field, subfields in complex_property_map.items():
        num = 0
        field_data = nxdoc["properties"].get(field)
        while num < len(field_data):
            for key, value in subfields.items():
                field_label = key % (num + 1)
                data2[field_label] = field_data[num].get(value)
            num += 1


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
        for data2 in data:
            for key in data2.keys():
                if key not in fieldnames:
                    fieldnames.append(key)

    return fieldnames


def write_csv(data, filename, fieldnames, delimiter=","):
    with open(filename, "wb") as outfile:
        writer = csv.DictWriter(outfile,
                                delimiter=delimiter,
                                fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def write_gsheet(data, sheet_name, fieldnames, gsheets_url):

    temp = "temp.csv"
    write_csv(data, temp, fieldnames)
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "client_secret.json", scope)
    client = gspread.authorize(creds)
    with open(temp, encoding="utf8") as f:  #opens and reads temporary csv file
        s = f.read() + "\n"
    sheet_id = client.open_by_url(gsheets_url).id
    client.import_csv(sheet_id, s)  #writes csv file to google sheet
    client.open_by_key(sheet_id).sheet1.update_title(sheet_name)
    os.remove(temp)  #removes temporary csv


if __name__ == "__main__":
    main()
