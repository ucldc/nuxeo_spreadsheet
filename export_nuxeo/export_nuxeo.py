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

    fieldnames = sort_fieldnames(data)
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

    get_title(data2, nxdoc)
    get_filepath(data2, nxdoc)
    get_type(data2, nxdoc, all_headers)
    get_alt_title(data2, nxdoc, all_headers)
    get_identifier(data2, nxdoc, all_headers)
    get_local_identifier(data2, nxdoc, all_headers)
    get_campus_unit(data2, nxdoc, all_headers)
    get_date(data2, nxdoc, all_headers)
    get_publication(data2, nxdoc, all_headers)
    get_creator(data2, nxdoc, all_headers)
    get_contributor(data2, nxdoc, all_headers)
    get_format(data2, nxdoc, all_headers)
    get_description(data2, nxdoc, all_headers)
    get_extent(data2, nxdoc, all_headers)
    get_language(data2, nxdoc, all_headers)
    get_temporal_coverage(data2, nxdoc, all_headers)
    get_transcription(data2, nxdoc, all_headers)
    get_access_restrictions(data2, nxdoc, all_headers)
    get_rights_statement(data2, nxdoc, all_headers)
    get_rights_status(data2, nxdoc, all_headers)
    get_copyright_holder(data2, nxdoc, all_headers)
    get_copyright_info(data2, nxdoc, all_headers)
    get_collection(data2, nxdoc, all_headers)
    get_related_resource(data2, nxdoc, all_headers)
    get_source(data2, nxdoc, all_headers)
    get_subject_name(data2, nxdoc, all_headers)
    get_place(data2, nxdoc, all_headers)
    get_subject_topic(data2, nxdoc, all_headers)
    get_form_genre(data2, nxdoc, all_headers)
    get_provenance(data2, nxdoc, all_headers)
    get_physical_location(data2, nxdoc, all_headers)

    return data2


def get_title(data2, nxdoc):
    """gets title
    """
    data2["Title"] = nxdoc["properties"]["dc:title"]


def get_filepath(data2, nxdoc):
    """gets filepath
    """
    data2["File path"] = nxdoc["path"]


def get_type(data2, nxdoc, all_headers):
    """gets type,
    inputs are dictionary (data2), nuxeo (nxdoc), all_headers input
    """
    if nxdoc["properties"]["ucldc_schema:type"] is not None and nxdoc[
            "properties"]["ucldc_schema:type"] != "":
        data2["Type"] = nxdoc["properties"]["ucldc_schema:type"]
    elif all_headers == "y":
        data2["Type"] = ""


def get_alt_title(data2, nxdoc, all_headers):
    altnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:alternativetitle"],
            list) and len(
                nxdoc["properties"]["ucldc_schema:alternativetitle"]) > 0:
        while altnumb < len(
                nxdoc["properties"]["ucldc_schema:alternativetitle"]):
            numb = altnumb + 1
            name = "Alternative Title %d" % numb
            data2[name] = nxdoc["properties"]["ucldc_schema:alternativetitle"][
                altnumb]
            altnumb += 1
    elif all_headers == "y":
        data2["Alternative Title 1"] = ""


def get_identifier(data2, nxdoc, all_headers):
    if nxdoc["properties"]["ucldc_schema:identifier"] is not None and nxdoc[
            "properties"]["ucldc_schema:identifier"] != "":
        data2["Identifier"] = nxdoc["properties"]["ucldc_schema:identifier"]
    elif all_headers == "y":
        data2["Identifier"] = ""


def get_local_identifier(data2, nxdoc, all_headers):
    locnumb = 0
    if isinstance(nxdoc["properties"]["ucldc_schema:localidentifier"],
                  list) and len(
                      nxdoc["properties"]["ucldc_schema:localidentifier"]) > 0:
        while locnumb < len(
                nxdoc["properties"]["ucldc_schema:localidentifier"]):
            numb = locnumb + 1
            name = "Local Identifier %d" % numb
            data2[name] = nxdoc["properties"]["ucldc_schema:localidentifier"][
                locnumb]
            locnumb += 1
    elif all_headers == "y":
        data2["Local Identifier 1"] = ""


def get_campus_unit(data2, nxdoc, all_headers):
    campnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:campusunit"],
            list) and len(nxdoc["properties"]["ucldc_schema:campusunit"]) > 0:
        while campnumb < len(nxdoc["properties"]["ucldc_schema:campusunit"]):
            numb = campnumb + 1
            name = "Campus/Unit %d" % numb
            data2[name] = nxdoc["properties"]["ucldc_schema:campusunit"][
                campnumb]
            campnumb += 1
    elif all_headers == "y":
        data2["Campus/Unit 1"] = ""


def get_date(data2, nxdoc, all_headers):
    datenumb = 0
    if isinstance(nxdoc["properties"]["ucldc_schema:date"],
                  list) and len(nxdoc["properties"]["ucldc_schema:date"]) > 0:
        while datenumb < len(nxdoc["properties"]["ucldc_schema:date"]):
            numb = datenumb + 1
            try:
                name = "Date %d" % numb
                if nxdoc["properties"]["ucldc_schema:date"][datenumb][
                        "date"] is not None and nxdoc["properties"][
                            "ucldc_schema:date"][datenumb]["date"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:date"][
                        datenumb]["date"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Date %d Type" % numb
                if nxdoc["properties"]["ucldc_schema:date"][datenumb][
                        "datetype"] is not None and nxdoc["properties"][
                            "ucldc_schema:date"][datenumb]["datetype"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:date"][
                        datenumb]["datetype"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Date %d Inclusive Start" % numb
                if nxdoc["properties"]["ucldc_schema:date"][datenumb][
                        "inclusivestart"] is not None and nxdoc["properties"][
                            "ucldc_schema:date"][datenumb][
                                "inclusivestart"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:date"][
                        datenumb]["inclusivestart"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Date %d Inclusive End" % numb
                if nxdoc["properties"]["ucldc_schema:date"][datenumb][
                        "inclusiveend"] is not None and nxdoc["properties"][
                            "ucldc_schema:date"][datenumb][
                                "inclusiveend"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:date"][
                        datenumb]["inclusiveend"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Date %d Single" % numb
                if nxdoc["properties"]["ucldc_schema:date"][datenumb][
                        "single"] is not None and nxdoc["properties"][
                            "ucldc_schema:date"][datenumb]["single"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:date"][
                        datenumb]["single"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            datenumb += 1
    elif all_headers == "y":
        data2["Date 1"] = ""
        data2["Date 1 Type"] = ""
        data2["Date 1 Inclusive Start"] = ""
        data2["Date 1 Inclusive End"] = ""
        data2["Date 1 Single"] = ""


def get_publication(data2, nxdoc, all_headers):
    pubnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:publisher"],
            list) and len(nxdoc["properties"]["ucldc_schema:publisher"]) > 0:
        while pubnumb < len(nxdoc["properties"]["ucldc_schema:publisher"]):
            numb = pubnumb + 1
            name = "Publication/Origination Info %d" % numb
            data2[name] = nxdoc["properties"]["ucldc_schema:publisher"][
                pubnumb]
            pubnumb += 1
    elif all_headers == "y":
        data2["Publication/Origination Info 1"] = ""


def get_creator(data2, nxdoc, all_headers):
    creatnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:creator"],
            list) and len(nxdoc["properties"]["ucldc_schema:creator"]) > 0:
        while creatnumb < len(nxdoc["properties"]["ucldc_schema:creator"]):
            numb = creatnumb + 1
            try:
                name = "Creator %d Name" % numb
                if nxdoc["properties"]["ucldc_schema:creator"][creatnumb][
                        "name"] is not None and nxdoc["properties"][
                            "ucldc_schema:creator"][creatnumb]["name"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:creator"][
                        creatnumb]["name"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Creator %d Name Type" % numb
                if nxdoc["properties"]["ucldc_schema:creator"][creatnumb][
                        "nametype"] is not None and nxdoc["properties"][
                            "ucldc_schema:creator"][creatnumb][
                                "nametype"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:creator"][
                        creatnumb]["nametype"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Creator %d Role" % numb
                if nxdoc["properties"]["ucldc_schema:creator"][creatnumb][
                        "role"] is not None and nxdoc["properties"][
                            "ucldc_schema:creator"][creatnumb]["role"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:creator"][
                        creatnumb]["role"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Creator %d Source" % numb
                if nxdoc["properties"]["ucldc_schema:creator"][creatnumb][
                        "source"] is not None and nxdoc["properties"][
                            "ucldc_schema:creator"][creatnumb]["source"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:creator"][
                        creatnumb]["source"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Creator %d Authority ID" % numb
                if nxdoc["properties"]["ucldc_schema:creator"][creatnumb][
                        "authorityid"] is not None and nxdoc["properties"][
                            "ucldc_schema:creator"][creatnumb][
                                "authorityid"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:creator"][
                        creatnumb]["authorityid"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            creatnumb += 1
    elif all_headers == "y":
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
            numb = contnumb + 1
            try:
                name = "Contributor %d Name" % numb
                if nxdoc["properties"]["ucldc_schema:contributor"][contnumb][
                        "name"] is not None and nxdoc["properties"][
                            "ucldc_schema:contributor"][contnumb]["name"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:contributor"][contnumb]["name"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Contributor %d Name Type" % numb
                if nxdoc["properties"]["ucldc_schema:contributor"][contnumb][
                        "nametype"] is not None and nxdoc["properties"][
                            "ucldc_schema:contributor"][contnumb][
                                "nametype"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:contributor"][contnumb]["nametype"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Contributor %d Role" % numb
                if nxdoc["properties"]["ucldc_schema:contributor"][contnumb][
                        "role"] is not None and nxdoc["properties"][
                            "ucldc_schema:contributor"][contnumb]["role"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:contributor"][contnumb]["role"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Contributor %d Source" % numb
                if nxdoc["properties"]["ucldc_schema:contributor"][contnumb][
                        "source"] is not None and nxdoc["properties"][
                            "ucldc_schema:contributor"][contnumb][
                                "source"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:contributor"][contnumb]["source"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Contributor %d Authority ID" % numb
                if nxdoc["properties"]["ucldc_schema:contributor"][contnumb][
                        "authorityid"] is not None and nxdoc["properties"][
                            "ucldc_schema:contributor"][contnumb][
                                "authorityid"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:contributor"][contnumb]["authorityid"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            contnumb += 1
    elif all_headers == "y":
        data2["Contributor 1 Name"] = ""
        data2["Contributor 1 Name Type"] = ""
        data2["Contributor 1 Role"] = ""
        data2["Contributor 1 Source"] = ""
        data2["Contributor 1 Authority ID"] = ""


def get_format(data2, nxdoc, all_headers):
    if nxdoc["properties"]["ucldc_schema:physdesc"] is not None and nxdoc[
            "properties"]["ucldc_schema:physdesc"] != "":
        data2["Format/Physical Description"] = nxdoc["properties"][
            "ucldc_schema:physdesc"]
    elif all_headers == "y":
        data2["Format/Physical Description"] = ""


def get_description(data2, nxdoc, all_headers):
    descnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:description"],
            list) and len(nxdoc["properties"]["ucldc_schema:description"]) > 0:
        while descnumb < len(nxdoc["properties"]["ucldc_schema:description"]):
            numb = descnumb + 1
            try:
                name = "Description %d Note" % numb
                if nxdoc["properties"]["ucldc_schema:description"][descnumb][
                        "item"] is not None and nxdoc["properties"][
                            "ucldc_schema:description"][descnumb]["item"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:description"][descnumb]["item"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Description %d Type" % numb
                if nxdoc["properties"]["ucldc_schema:description"][descnumb][
                        "type"] is not None and nxdoc["properties"][
                            "ucldc_schema:description"][descnumb]["type"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:description"][descnumb]["type"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            descnumb += 1
    elif all_headers == "y":
        data2["Description 1 Note"] = ""
        data2["Description 1 Type"] = ""


def get_extent(data2, nxdoc, all_headers):
    if nxdoc["properties"]["ucldc_schema:extent"] is not None and nxdoc[
            "properties"]["ucldc_schema:extent"] != "":
        data2["Extent"] = nxdoc["properties"]["ucldc_schema:extent"]
    elif all_headers == "y":
        data2["Extent"] = ""


def get_language(data2, nxdoc, all_headers):
    langnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:language"],
            list) and len(nxdoc["properties"]["ucldc_schema:language"]) > 0:
        while langnumb < len(nxdoc["properties"]["ucldc_schema:language"]):
            numb = langnumb + 1
            try:
                name = "Language %d" % numb
                if nxdoc["properties"]["ucldc_schema:language"][langnumb][
                        "language"] is not None and nxdoc["properties"][
                            "ucldc_schema:language"][langnumb][
                                "language"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:language"][
                        langnumb]["language"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Language %d Code" % numb
                if nxdoc["properties"]["ucldc_schema:language"][langnumb][
                        "languagecode"] is not None and nxdoc["properties"][
                            "ucldc_schema:language"][langnumb][
                                "languagecode"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:language"][
                        langnumb]["languagecode"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            langnumb += 1
    elif all_headers == "y":
        data2["Language 1"] = ""
        data2["Language 1 Code"] = ""


def get_temporal_coverage(data2, nxdoc, all_headers):
    tempnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:temporalcoverage"],
            list) and len(
                nxdoc["properties"]["ucldc_schema:temporalcoverage"]) > 0:
        while tempnumb < len(
                nxdoc["properties"]["ucldc_schema:temporalcoverage"]):
            numb = tempnumb + 1
            name = "Temporal Coverage %d" % numb
            data2[name] = nxdoc["properties"]["ucldc_schema:temporalcoverage"][
                tempnumb]
            tempnumb += 1
    elif all_headers == "y":
        data2["Temporal Coverage 1"] = ""


def get_transcription(data2, nxdoc, all_headers):
    if nxdoc["properties"]["ucldc_schema:transcription"] is not None and nxdoc[
            "properties"]["ucldc_schema:transcription"] != "":
        data2["Transcription"] = nxdoc["properties"][
            "ucldc_schema:transcription"]
    elif all_headers == "y":
        data2["Transcription"] = ""


def get_access_restrictions(data2, nxdoc, all_headers):
    if nxdoc["properties"]["ucldc_schema:accessrestrict"] is not None and nxdoc[
            "properties"]["ucldc_schema:accessrestrict"] != "":
        data2["Access Restrictions"] = nxdoc["properties"][
            "ucldc_schema:accessrestrict"]
    elif all_headers == "y":
        data2["Access Restrictions"] = ""


def get_rights_statement(data2, nxdoc, all_headers):
    if nxdoc["properties"][
            "ucldc_schema:rightsstatement"] is not None and nxdoc[
                "properties"]["ucldc_schema:rightsstatement"] != "":
        data2["Copyright Statement"] = nxdoc["properties"][
            "ucldc_schema:rightsstatement"]
    elif all_headers == "y":
        data2["Copyright Statement"] = ""


def get_rights_status(data2, nxdoc, all_headers):
    if nxdoc["properties"]["ucldc_schema:rightsstatus"] is not None and nxdoc[
            "properties"]["ucldc_schema:rightsstatus"] != "":
        data2["Copyright Status"] = nxdoc["properties"][
            "ucldc_schema:rightsstatus"]
    elif all_headers == "y":
        data2["Copyright Status"] = ""


def get_copyright_holder(data2, nxdoc, all_headers):
    rightsnumb = 0
    if isinstance(nxdoc["properties"]["ucldc_schema:rightsholder"],
                  list) and len(
                      nxdoc["properties"]["ucldc_schema:rightsholder"]) > 0:
        while rightsnumb < len(
                nxdoc["properties"]["ucldc_schema:rightsholder"]):
            numb = rightsnumb + 1
            try:
                name = "Copyright Holder %d Name" % numb
                if nxdoc["properties"]["ucldc_schema:rightsholder"][
                        rightsnumb]["name"] is not None and nxdoc[
                            "properties"]["ucldc_schema:rightsholder"][
                                rightsnumb]["name"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:rightsholder"][rightsnumb]["name"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Copyright Holder %d Name Type" % numb
                if nxdoc["properties"]["ucldc_schema:rightsholder"][
                        rightsnumb]["nametype"] is not None and nxdoc[
                            "properties"]["ucldc_schema:rightsholder"][
                                rightsnumb]["nametype"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:rightsholder"][rightsnumb]["nametype"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Copyright Holder %d Source" % numb
                if nxdoc["properties"]["ucldc_schema:rightsholder"][
                        rightsnumb]["source"] is not None and nxdoc[
                            "properties"]["ucldc_schema:rightsholder"][
                                rightsnumb]["source"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:rightsholder"][rightsnumb]["source"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Copyright Holder %d Authority ID" % numb
                if nxdoc["properties"]["ucldc_schema:rightsholder"][
                        rightsnumb]["authorityid"] is not None and nxdoc[
                            "properties"]["ucldc_schema:rightsholder"][
                                rightsnumb]["authorityid"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:rightsholder"][rightsnumb]["authorityid"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            rightsnumb += 1
    elif all_headers == "y":
        data2["Copyright Holder 1 Name"] = ""
        data2["Copyright Holder 1 Name Type"] = ""
        data2["Copyright Holder 1 Source"] = ""
        data2["Copyright Holder 1 Authority ID"] = ""


def get_copyright_info(data2, nxdoc, all_headers):
    if nxdoc["properties"]["ucldc_schema:rightscontact"] is not None and nxdoc[
            "properties"]["ucldc_schema:rightscontact"] != "":
        data2["Copyright Contact"] = nxdoc["properties"][
            "ucldc_schema:rightscontact"]
    elif all_headers == "y":
        data2["Copyright Contact"] = ""

    if nxdoc["properties"]["ucldc_schema:rightsnotice"] is not None and nxdoc[
            "properties"]["ucldc_schema:rightsnotice"] != "":
        data2["Copyright Notice"] = nxdoc["properties"][
            "ucldc_schema:rightsnotice"]
    elif all_headers == "y":
        data2["Copyright Notice"] = ""

    if nxdoc["properties"][
            "ucldc_schema:rightsdeterminationdate"] is not None and nxdoc[
                "properties"]["ucldc_schema:rightsdeterminationdate"] != "":
        data2["Copyright Determination Date"] = nxdoc["properties"][
            "ucldc_schema:rightsdeterminationdate"]
    elif all_headers == "y":
        data2["Copyright Determination Date"] = ""

    if nxdoc["properties"][
            "ucldc_schema:rightsstartdate"] is not None and nxdoc[
                "properties"]["ucldc_schema:rightsstartdate"] != "":
        data2["Copyright Start Date"] = nxdoc["properties"][
            "ucldc_schema:rightsstartdate"]
    elif all_headers == "y":
        data2["Copyright Start Date"] = ""

    if nxdoc["properties"]["ucldc_schema:rightsenddate"] is not None and nxdoc[
            "properties"]["ucldc_schema:rightsenddate"] != "":
        data2["Copyright End Date"] = nxdoc["properties"][
            "ucldc_schema:rightsenddate"]
    elif all_headers == "y":
        data2["Copyright End Date"] = ""

    if nxdoc["properties"][
            "ucldc_schema:rightsjurisdiction"] is not None and nxdoc[
                "properties"]["ucldc_schema:rightsjurisdiction"] != "":
        data2["Copyright Jurisdiction"] = nxdoc["properties"][
            "ucldc_schema:rightsjurisdiction"]
    elif all_headers == "y":
        data2["Copyright Jurisdiction"] = ""

    if nxdoc["properties"]["ucldc_schema:rightsnote"] is not None and nxdoc[
            "properties"]["ucldc_schema:rightsnote"] != "":
        data2["Copyright Note"] = nxdoc["properties"][
            "ucldc_schema:rightsnote"]
    elif all_headers == "y":
        data2["Copyright Note"] = ""


def get_collection(data2, nxdoc, all_headers):
    collnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:collection"],
            list) and len(nxdoc["properties"]["ucldc_schema:collection"]) > 0:
        while collnumb < len(nxdoc["properties"]["ucldc_schema:collection"]):
            numb = collnumb + 1
            name = "Collection %d" % numb
            data2[name] = nxdoc["properties"]["ucldc_schema:collection"][
                collnumb]
            collnumb += 1
    elif all_headers == "y":
        data2["Collection 1"] = ""


def get_related_resource(data2, nxdoc, all_headers):
    relnumb = 0
    if isinstance(nxdoc["properties"]["ucldc_schema:relatedresource"],
                  list) and len(
                      nxdoc["properties"]["ucldc_schema:relatedresource"]) > 0:
        while relnumb < len(
                nxdoc["properties"]["ucldc_schema:relatedresource"]):
            numb = relnumb + 1
            name = "Related Resource %d" % numb
            data2[name] = nxdoc["properties"]["ucldc_schema:relatedresource"][
                relnumb]
            relnumb += 1
    elif all_headers == "y":
        data2["Related Resource 1"] = ""


def get_source(data2, nxdoc, all_headers):
    if nxdoc["properties"]["ucldc_schema:source"] is not None and nxdoc[
            "properties"]["ucldc_schema:source"] != "":
        data2["Source"] = nxdoc["properties"]["ucldc_schema:source"]
    elif all_headers == "y":
        data2["Source"] = ""


def get_subject_name(data2, nxdoc, all_headers):
    subnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:subjectname"],
            list) and len(nxdoc["properties"]["ucldc_schema:subjectname"]) > 0:
        while subnumb < len(nxdoc["properties"]["ucldc_schema:subjectname"]):
            numb = subnumb + 1
            try:
                name = "Subject (Name) %d Name" % numb
                if nxdoc["properties"]["ucldc_schema:subjectname"][subnumb][
                        "name"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjectname"][subnumb]["name"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjectname"][subnumb]["name"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Name) %d Name Type" % numb
                if nxdoc["properties"]["ucldc_schema:subjectname"][subnumb][
                        "name_type"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjectname"][subnumb][
                                "name_type"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjectname"][subnumb]["name_type"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Name) %d Role" % numb
                if nxdoc["properties"]["ucldc_schema:subjectname"][subnumb][
                        "role"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjectname"][subnumb]["role"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjectname"][subnumb]["role"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Name) %d Source" % numb
                if nxdoc["properties"]["ucldc_schema:subjectname"][subnumb][
                        "source"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjectname"][subnumb][
                                "source"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjectname"][subnumb]["source"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Name) %d Authority ID" % numb
                if nxdoc["properties"]["ucldc_schema:subjectname"][subnumb][
                        "authorityid"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjectname"][subnumb][
                                "authorityid"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjectname"][subnumb]["authorityid"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            subnumb += 1
    elif all_headers == "y":
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
            numb = plcnumb + 1
            try:
                name = "Place %d Name" % numb
                if nxdoc["properties"]["ucldc_schema:place"][plcnumb][
                        "name"] is not None and nxdoc["properties"][
                            "ucldc_schema:place"][plcnumb]["name"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:place"][
                        plcnumb]["name"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Place %d Coordinates" % numb
                if nxdoc["properties"]["ucldc_schema:place"][plcnumb][
                        "coordinates"] is not None and nxdoc["properties"][
                            "ucldc_schema:place"][plcnumb]["coordinates"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:place"][
                        plcnumb]["coordinates"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Place %d Source" % numb
                if nxdoc["properties"]["ucldc_schema:place"][plcnumb][
                        "source"] is not None and nxdoc["properties"][
                            "ucldc_schema:place"][plcnumb]["source"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:place"][
                        plcnumb]["source"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Place %d Authority ID" % numb
                if nxdoc["properties"]["ucldc_schema:place"][plcnumb][
                        "authorityid"] is not None and nxdoc["properties"][
                            "ucldc_schema:place"][plcnumb]["authorityid"] != "":
                    data2[name] = nxdoc["properties"]["ucldc_schema:place"][
                        plcnumb]["authorityid"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            plcnumb += 1
    elif all_headers == "y":
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
            numb = topnumb + 1
            try:
                name = "Subject (Topic) %d Heading" % numb
                if nxdoc["properties"]["ucldc_schema:subjecttopic"][topnumb][
                        "heading"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjecttopic"][topnumb][
                                "heading"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjecttopic"][topnumb]["heading"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Topic) %d Heading Type" % numb
                if nxdoc["properties"]["ucldc_schema:subjecttopic"][topnumb][
                        "headingtype"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjecttopic"][topnumb][
                                "headingtype"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjecttopic"][topnumb]["headingtype"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Topic) %d Source" % numb
                if nxdoc["properties"]["ucldc_schema:subjecttopic"][topnumb][
                        "source"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjecttopic"][topnumb][
                                "source"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjecttopic"][topnumb]["source"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Subject (Topic) %d Authority ID" % numb
                if nxdoc["properties"]["ucldc_schema:subjecttopic"][topnumb][
                        "authorityid"] is not None and nxdoc["properties"][
                            "ucldc_schema:subjecttopic"][topnumb][
                                "authorityid"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:subjecttopic"][topnumb]["authorityid"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            topnumb += 1
    elif all_headers == "y":
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
            numb = formnumb + 1
            try:
                name = "Form/Genre %d Heading" % numb
                if nxdoc["properties"]["ucldc_schema:formgenre"][formnumb][
                        "heading"] is not None and nxdoc["properties"][
                            "ucldc_schema:formgenre"][formnumb][
                                "heading"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:formgenre"][formnumb]["heading"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Form/Genre %d Source" % numb
                if nxdoc["properties"]["ucldc_schema:formgenre"][formnumb][
                        "source"] is not None and nxdoc["properties"][
                            "ucldc_schema:formgenre"][formnumb]["source"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:formgenre"][formnumb]["source"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            try:
                name = "Form/Genre %d Authority ID" % numb
                if nxdoc["properties"]["ucldc_schema:formgenre"][formnumb][
                        "authorityid"] is not None and nxdoc["properties"][
                            "ucldc_schema:formgenre"][formnumb][
                                "authorityid"] != "":
                    data2[name] = nxdoc["properties"][
                        "ucldc_schema:formgenre"][formnumb]["authorityid"]
                elif all_headers == "y":
                    data2[name] = ""
            except:
                pass
            formnumb += 1
    elif all_headers == "y":
        data2["Form/Genre 1 Heading"] = ""
        data2["Form/Genre 1 Source"] = ""
        data2["Form/Genre 1 Authority ID"] = ""


def get_provenance(data2, nxdoc, all_headers):
    provnumb = 0
    if isinstance(
            nxdoc["properties"]["ucldc_schema:provenance"],
            list) and len(nxdoc["properties"]["ucldc_schema:provenance"]) > 0:
        while provnumb < len(nxdoc["properties"]["ucldc_schema:provenance"]):
            numb = provnumb + 1
            name = "Provenance %d" % numb
            data2[name] = nxdoc["properties"]["ucldc_schema:provenance"][
                provnumb]
            provnumb += 1
    elif all_headers == "y":
        data2["Provenance 1"] = ""


def get_physical_location(data2, nxdoc, all_headers):
    if nxdoc["properties"]["ucldc_schema:physlocation"] is not None and nxdoc[
            "properties"]["ucldc_schema:physlocation"] != "":
        data2["Physical Location"] = nxdoc["properties"][
            "ucldc_schema:physlocation"]
    elif all_headers == "y":
        data2["Physical Location"] = ""


def sort_fieldnames(data):
    """ ensures that File path, Title and Type are the first three rows
    """
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
