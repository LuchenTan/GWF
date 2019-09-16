"""
Simple, rough script to write metadata information from a filled csv template into an empty ISO19115 XML frame.
Metadata is given as Excel worksheets, use https://www.extendoffice.com/documents/excel/2972-excel-save-export-convert-multiple-all-sheets-to-csv-text.html to convert to CSV files.

Usage: python <filename.py> path_to_csv_dir
"""

import pandas as pd
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

# Load csv files
csv_dir = Path(sys.argv[1])
csv_files = list(csv_dir.glob('*.csv'))

csv_data = []
for f in csv_files:
    csv_data.append(pd.read_csv(f, encoding='ANSI', header=None, usecols=[0,1], dtype={0:str,1:str}, na_filter=False))

# Load XML template
ns = {
    'gmd':"http://www.isotc211.org/2005/gmd",
    '': "http://www.isotc211.org/2005/gmi",
    'functx':"http://www.functx.com",
    'gco': "http://www.isotc211.org/2005/gco", 
    'gmi':"http://www.isotc211.org/2005/gmi",
    'gml':"http://www.opengis.net/gml", 
    'gmx':"http://www.isotc211.org/2005/gmx", 
    'gsr':"http://www.isotc211.org/2005/gsr",
    'gss':"http://www.isotc211.org/2005/gss",
    'gts':"http://www.isotc211.org/2005/gts",
    'srv':"http://www.isotc211.org/2005/srv" ,
    'xlink':"http://www.w3.org/1999/xlink",
}

tree = ET.parse(Path(__file__).absolute().parent.parent / 'data' / 'iso19115_template.xml')
for k,v in ns.items():
    ET.register_namespace(k, v)
root = tree.getroot()

# Get XML fields that have a corresponding value in the CSVs
file = root.find('gmd:fileIdentifier', ns).find('gco:CharacterString', ns)
contact = root.find('gmd:contact', ns).find('gmd:CI_ResponsibleParty', ns).find('gmd:individualName', ns).find('gco:CharacterString', ns)
title = root.find("gmd:identificationInfo", ns).find("gmd:MD_DataIdentification", ns).find("gmd:citation", ns).find("gmd:CI_Citation",ns).find("gmd:title",ns).find('gco:CharacterString', ns)
purpose = root.find("gmd:identificationInfo", ns).find("gmd:MD_DataIdentification",ns).find("gmd:purpose",ns).find('gco:CharacterString', ns)
abstract = root.find("gmd:identificationInfo", ns).find("gmd:MD_DataIdentification",ns).find("gmd:abstract",ns).find('gco:CharacterString', ns)
maint_freq = root.find("gmd:metadataMaintenance", ns).find("gmd:MD_MaintenanceInformation", ns).find("gmd:maintenanceAndUpdateFrequency",ns)
access = root.find("gmd:identificationInfo",ns).find("gmd:MD_DataIdentification",ns).find("gmd:resourceConstraints",ns).find("gmd:MD_LegalConstraints",ns).find("gmd:accessConstraints",ns).find("gmd:MD_RestrictionCode",ns)
time = root.find("gmd:identificationInfo",ns).find("gmd:MD_DataIdentification",ns).find("gmd:extent",ns).find("gmd:EX_Extent",ns).find("gmd:temporalElement",ns).find("gmd:EX_TemporalExtent",ns).find("gmd:extent",ns).find('gml:TimePeriod',ns).find("gml:description",ns)
status = root.find("gmd:identificationInfo",ns).find("gmd:MD_DataIdentification",ns).find("gmd:status",ns).find("gmd:MD_ProgressCode",ns)

# Create one XML per CSV file, fill in the information from the CSVs.
for i, csv in enumerate(csv_data):
    file.text = csv_files[i].name
    contact.text = csv.loc[10,1]
    title.text = csv.loc[1,1]
    purpose.text = csv.loc[0,1]
    abstract.text = csv.loc[3,1]
    maint_freq.attrib['{http://www.isotc211.org/2005/gco}nilReason'] = csv.loc[7,1]
    access.text = csv.loc[5,1]
    time.text = csv.loc[4,1]
    status.text = csv.loc[6,1]
        
    tree.write(str(csv_files[i]).replace('.csv', '.xml'), encoding='utf-8')
