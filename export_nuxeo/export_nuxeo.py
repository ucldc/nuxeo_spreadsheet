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

    get_date(data2, nxdoc, all_headers)

    get_creator(data2, nxdoc, all_headers)
    get_contributor(data2, nxdoc, all_headers)
    get_description(data2, nxdoc, all_headers)
    get_language(data2, nxdoc, all_headers)
    get_copyright_holder(data2, nxdoc, all_headers)
    get_subject_name(data2, nxdoc, all_headers)
    get_place(data2, nxdoc, all_headers)
    get_subject_topic(data2, nxdoc, all_headers)
    get_form_genre(data2, nxdoc, all_headers)

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


def get_date(data2, nxdoc, all_headers):
    datenumb = 0
    if isinstance(nxdoc["properties"]["ucldc_schema:date"],
                  list) and len(nxdoc["properties"]["ucldc_schema:date"]) > 0:
        while datenumb < len(nxdoc["properties"]["ucldc_schema:date"]):
            num = datenumb + 1
            try:
                name = "Date %d" % num
                if nxdoc["properties"]["ucldc_schema:date"][datenumb][
                        "date"] is not None and nxdoc["properties"][
                            "ucldc_schema:date"][datenumb]["date"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:date"][
                        datenumb]["date"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Date %d Type" % num
                if nxdoc["properties"]["ucldc_schema:date"][datenumb][
                        "datetype"] is not None and nxdoc["properties"][
                            "ucldc_schema:date"][datenumb]["datetype"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:date"][
                        datenumb]["datetype"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Date %d Inclusive Start" % num
                if nxdoc["properties"]["ucldc_schema:date"][datenumb][
                        "inclusivestart"] is not None and nxdoc["properties"][
                            "ucldc_schema:date"][datenumb][
                                "inclusivestart"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:date"][
                        datenumb]["inclusivestart"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Date %d Inclusive End" % num
                if nxdoc["properties"]["ucldc_schema:date"][datenumb][
                        "inclusiveend"] is not None and nxdoc["properties"][
                            "ucldc_schema:date"][datenumb][
                                "inclusiveend"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:date"][
                        datenumb]["inclusiveend"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Date %d Single" % num
                if nxdoc["properties"]["ucldc_schema:date"][datenumb][
                        "single"] is not None and nxdoc["properties"][
                            "ucldc_schema:date"][datenumb]["single"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:date"][
                        datenumb]["single"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            datenumb += 1
    elif all_headers:
        data2["Date 1"] = ""
        data2["Date 1 Type"] = ""
        data2["Date 1 Inclusive Start"] = ""
        data2["Date 1 Inclusive End"] = ""
        data2["Date 1 Single"] = ""


def get_creator(data2, nxdoc, all_headers):
    creatnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:creator"],
            list) and len(nxdoc["properties"]["ucldc_schema:creator"]) > 0:
        while creatnumb < len(nxdoc["properties"]["ucldc_schema:creator"]):
            num = creatnumb + 1
            try:
                name = "Creator %d Name" % num
                if nxdoc["properties"]["ucldc_schema:creator"][creatnumb][
                        "name"] is not None and nxdoc["properties"][
                            "ucldc_schema:creator"][creatnumb]["name"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:creator"][
                        creatnumb]["name"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Creator %d Name Type" % num
                if nxdoc["properties"]["ucldc_schema:creator"][creatnumb][
                        "nametype"] is not None and nxdoc["properties"][
                            "ucldc_schema:creator"][creatnumb][
                                "nametype"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:creator"][
                        creatnumb]["nametype"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Creator %d Role" % num
                if nxdoc["properties"]["ucldc_schema:creator"][creatnumb][
                        "role"] is not None and nxdoc["properties"][
                            "ucldc_schema:creator"][creatnumb]["role"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:creator"][
                        creatnumb]["role"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Creator %d Source" % num
                if nxdoc["properties"]["ucldc_schema:creator"][creatnumb][
                        "source"] is not None and nxdoc["properties"][
                            "ucldc_schema:creator"][creatnumb]["source"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:creator"][
                        creatnumb]["source"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Creator %d Authority ID" % num
                if nxdoc["properties"]["ucldc_schema:creator"][creatnumb][
                        "authorityid"] is not None and nxdoc["properties"][
                            "ucldc_schema:creator"][creatnumb][
                                "authorityid"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:creator"][
                        creatnumb]["authorityid"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            creatnumb += 1
    elif all_headers:
        data2["Creator 1 Name"] = ""
        data2["Creator 1 Name Type"] = ""
        data2["Creator 1 Role"] = ""
        data2["Creator 1 Source"] = ""
        data2["Creator 1 Authority ID"] = ""


def get_contributor(data2, nxdoc, all_headers):
    contnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:contributor"],
            list) and len(nxdoc["properties"]["ucldc_schema:contributor"]) > 0:
        while contnumb < len(nxdoc["properties"]["ucldc_schema:contributor"]):
            num = contnumb + 1
            try:
                name = "Contributor %d Name" % num
                if nxdoc["properties"]["ucldc_schema:contributor"][contnumb][
                        "name"] is not None and nxdoc["properties"][
                            "ucldc_schema:contributor"][contnumb]["name"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:contributor"][contnumb]["name"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Contributor %d Name Type" % num
                if nxdoc["properties"]["ucldc_schema:contributor"][contnumb][
                        "nametype"] is not None and nxdoc["properties"][
                            "ucldc_schema:contributor"][contnumb][
                                "nametype"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:contributor"][contnumb]["nametype"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Contributor %d Role" % num
                if nxdoc["properties"]["ucldc_schema:contributor"][contnumb][
                        "role"] is not None and nxdoc["properties"][
                            "ucldc_schema:contributor"][contnumb]["role"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:contributor"][contnumb]["role"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Contributor %d Source" % num
                if nxdoc["properties"]["ucldc_schema:contributor"][contnumb][
                        "source"] is not None and nxdoc["properties"][
                            "ucldc_schema:contributor"][contnumb][
                                "source"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:contributor"][contnumb]["source"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Contributor %d Authority ID" % num
                if nxdoc["properties"]["ucldc_schema:contributor"][contnumb][
                        "authorityid"] is not None and nxdoc["properties"][
                            "ucldc_schema:contributor"][contnumb][
                                "authorityid"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:contributor"][contnumb]["authorityid"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            contnumb += 1
    elif all_headers:
        data2["Contributor 1 Name"] = ""
        data2["Contributor 1 Name Type"] = ""
        data2["Contributor 1 Role"] = ""
        data2["Contributor 1 Source"] = ""
        data2["Contributor 1 Authority ID"] = ""


def get_description(data2, nxdoc, all_headers):
    descnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:description"],
            list) and len(nxdoc["properties"]["ucldc_schema:description"]) > 0:
        while descnumb < len(nxdoc["properties"]["ucldc_schema:description"]):
            num = descnumb + 1
            try:
                name = "Description %d Note" % num
                if nxdoc["properties"]["ucldc_schema:description"][descnumb][
                        "item"] is not None and nxdoc["properties"][
                            "ucldc_schema:description"][descnumb]["item"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:description"][descnumb]["item"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Description %d Type" % num
                if nxdoc["properties"]["ucldc_schema:description"][descnumb][
                        "type"] is not None and nxdoc["properties"][
                            "ucldc_schema:description"][descnumb]["type"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:description"][descnumb]["type"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            descnumb += 1
    elif all_headers:
        data2["Description 1 Note"] = ""
        data2["Description 1 Type"] = ""


def get_language(data2, nxdoc, all_headers):
    langnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:language"],
            list) and len(nxdoc["properties"]["ucldc_schema:language"]) > 0:
        while langnumb < len(nxdoc["properties"]["ucldc_schema:language"]):
            num = langnumb + 1
            try:
                name = "Language %d" % num
                if nxdoc["properties"]["ucldc_schema:language"][langnumb][
                        "language"] is not None and nxdoc["properties"][
                            "ucldc_schema:language"][langnumb][
                                "language"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:language"][
                        langnumb]["language"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Language %d Code" % num
                if nxdoc["properties"]["ucldc_schema:language"][langnumb][
                        "languagecode"] is not None and nxdoc["properties"][
                            "ucldc_schema:language"][langnumb][
                                "languagecode"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:language"][
                        langnumb]["languagecode"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            langnumb += 1
    elif all_headers:
        data2["Language 1"] = ""
        data2["Language 1 Code"] = ""


def get_copyright_holder(data2, nxdoc, all_headers):
    rightsnumb = 0
    if isinstance(nxdoc["properties"]["ucldc_schema:rightsholder"],
                  list) and len(
                      nxdoc["properties"]["ucldc_schema:rightsholder"]) > 0:
        while rightsnumb < len(
                nxdoc["properties"]["ucldc_schema:rightsholder"]):
            num = rightsnumb + 1
            try:
                name = "Copyright Holder %d Name" % num
                if nxdoc["properties"]["ucldc_schema:rightsholder"][
                        rightsnumb]["name"] is not None and nxdoc[
                            "properties"]["ucldc_schema:rightsholder"][
                                rightsnumb]["name"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:rightsholder"][rightsnumb]["name"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Copyright Holder %d Name Type" % num
                if nxdoc["properties"]["ucldc_schema:rightsholder"][
                        rightsnumb]["nametype"] is not None and nxdoc[
                            "properties"]["ucldc_schema:rightsholder"][
                                rightsnumb]["nametype"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:rightsholder"][rightsnumb]["nametype"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Copyright Holder %d Source" % num
                if nxdoc["properties"]["ucldc_schema:rightsholder"][
                        rightsnumb]["source"] is not None and nxdoc[
                            "properties"]["ucldc_schema:rightsholder"][
                                rightsnumb]["source"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:rightsholder"][rightsnumb]["source"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Copyright Holder %d Authority ID" % num
                if nxdoc["properties"]["ucldc_schema:rightsholder"][
                        rightsnumb]["authorityid"] is not None and nxdoc[
                            "properties"]["ucldc_schema:rightsholder"][
                                rightsnumb]["authorityid"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:rightsholder"][rightsnumb]["authorityid"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            rightsnumb += 1
    elif all_headers:
        data2["Copyright Holder 1 Name"] = ""
        data2["Copyright Holder 1 Name Type"] = ""
        data2["Copyright Holder 1 Source"] = ""
        data2["Copyright Holder 1 Authority ID"] = ""


def get_subject_name(data2, nxdoc, all_headers):
    subnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:subjectname"],
            list) and len(nxdoc["properties"]["ucldc_schema:subjectname"]) > 0:
        while subnumb < len(nxdoc["properties"]["ucldc_schema:subjectname"]):
            num = subnumb + 1
            try:
                name = "Subject (Name) %d Name" % num
                if nxdoc["properties"]["ucldc_schema:subjectname"][subnumb][
                        "name"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjectname"][subnumb]["name"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjectname"][subnumb]["name"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Name) %d Name Type" % num
                if nxdoc["properties"]["ucldc_schema:subjectname"][subnumb][
                        "name_type"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjectname"][subnumb][
                                "name_type"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjectname"][subnumb]["name_type"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Name) %d Role" % num
                if nxdoc["properties"]["ucldc_schema:subjectname"][subnumb][
                        "role"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjectname"][subnumb]["role"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjectname"][subnumb]["role"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Name) %d Source" % num
                if nxdoc["properties"]["ucldc_schema:subjectname"][subnumb][
                        "source"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjectname"][subnumb][
                                "source"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjectname"][subnumb]["source"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Name) %d Authority ID" % num
                if nxdoc["properties"]["ucldc_schema:subjectname"][subnumb][
                        "authorityid"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjectname"][subnumb][
                                "authorityid"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjectname"][subnumb]["authorityid"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            subnumb += 1
    elif all_headers:
        data2["Subject (Name) 1 Name"] = ""
        data2["Subject (Name) 1 Name Type"] = ""
        data2["Subject (Name) 1 Role"] = ""
        data2["Subject (Name) 1 Source"] = ""
        data2["Subject (Name) 1 Authority ID"] = ""


def get_place(data2, nxdoc, all_headers):
    plcnumb = 0
    if isinstance(nxdoc["properties"]["ucldc_schema:place"],
                  list) and len(nxdoc["properties"]["ucldc_schema:place"]) > 0:
        while plcnumb < len(nxdoc["properties"]["ucldc_schema:place"]):
            num = plcnumb + 1
            try:
                name = "Place %d Name" % num
                if nxdoc["properties"]["ucldc_schema:place"][plcnumb][
                        "name"] is not None and nxdoc["properties"][
                            "ucldc_schema:place"][plcnumb]["name"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:place"][
                        plcnumb]["name"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Place %d Coordinates" % num
                if nxdoc["properties"]["ucldc_schema:place"][plcnumb][
                        "coordinates"] is not None and nxdoc["properties"][
                            "ucldc_schema:place"][plcnumb]["coordinates"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:place"][
                        plcnumb]["coordinates"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Place %d Source" % num
                if nxdoc["properties"]["ucldc_schema:place"][plcnumb][
                        "source"] is not None and nxdoc["properties"][
                            "ucldc_schema:place"][plcnumb]["source"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:place"][
                        plcnumb]["source"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Place %d Authority ID" % num
                if nxdoc["properties"]["ucldc_schema:place"][plcnumb][
                        "authorityid"] is not None and nxdoc["properties"][
                            "ucldc_schema:place"][plcnumb]["authorityid"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:place"][
                        plcnumb]["authorityid"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            plcnumb += 1
    elif all_headers:
        data2["Place 1 Name"] = ""
        data2["Place 1 Coordinates"] = ""
        data2["Place 1 Source"] = ""
        data2["Place 1 Authority ID"] = ""


def get_subject_topic(data2, nxdoc, all_headers):
    topnumb = 0
    if isinstance(nxdoc["properties"]["ucldc_schema:subjecttopic"],
                  list) and len(
                      nxdoc["properties"]["ucldc_schema:subjecttopic"]) > 0:
        while topnumb < len(nxdoc["properties"]["ucldc_schema:subjecttopic"]):
            num = topnumb + 1
            try:
                name = "Subject (Topic) %d Heading" % num
                if nxdoc["properties"]["ucldc_schema:subjecttopic"][topnumb][
                        "heading"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjecttopic"][topnumb][
                                "heading"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjecttopic"][topnumb]["heading"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Topic) %d Heading Type" % num
                if nxdoc["properties"]["ucldc_schema:subjecttopic"][topnumb][
                        "headingtype"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjecttopic"][topnumb][
                                "headingtype"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjecttopic"][topnumb]["headingtype"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Topic) %d Source" % num
                if nxdoc["properties"]["ucldc_schema:subjecttopic"][topnumb][
                        "source"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjecttopic"][topnumb][
                                "source"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjecttopic"][topnumb]["source"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Topic) %d Authority ID" % num
                if nxdoc["properties"]["ucldc_schema:subjecttopic"][topnumb][
                        "authorityid"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjecttopic"][topnumb][
                                "authorityid"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjecttopic"][topnumb]["authorityid"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            topnumb += 1
    elif all_headers:
        data2["Subject (Topic) 1 Heading"] = ""
        data2["Subject (Topic) 1 Heading Type"] = ""
        data2["Subject (Topic) 1 Source"] = ""
        data2["Subject (Topic) 1 Authority ID"] = ""


def get_form_genre(data2, nxdoc, all_headers):
    formnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:formgenre"],
            list) and len(nxdoc["properties"]["ucldc_schema:formgenre"]) > 0:
        while formnumb < len(nxdoc["properties"]["ucldc_schema:formgenre"]):
            num = formnumb + 1
            try:
                name = "Form/Genre %d Heading" % num
                if nxdoc["properties"]["ucldc_schema:formgenre"][formnumb][
                        "heading"] is not None and nxdoc["properties"][
                            "ucldc_schema:formgenre"][formnumb][
                                "heading"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:formgenre"][formnumb]["heading"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Form/Genre %d Source" % num
                if nxdoc["properties"]["ucldc_schema:formgenre"][formnumb][
                        "source"] is not None and nxdoc["properties"][
                            "ucldc_schema:formgenre"][formnumb]["source"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:formgenre"][formnumb]["source"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            try:
                name = "Form/Genre %d Authority ID" % num
                if nxdoc["properties"]["ucldc_schema:formgenre"][formnumb][
                        "authorityid"] is not None and nxdoc["properties"][
                            "ucldc_schema:formgenre"][formnumb][
                                "authorityid"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:formgenre"][formnumb]["authorityid"]
                elif all_headers:
                    data2[name] = ""
            except:
                pass
            formnumb += 1
    elif all_headers:
        data2["Form/Genre 1 Heading"] = ""
        data2["Form/Genre 1 Source"] = ""
        data2["Form/Genre 1 Authority ID"] = ""


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
