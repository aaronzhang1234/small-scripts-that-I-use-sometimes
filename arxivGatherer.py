import urllib.request 
import xml.etree.ElementTree as ET
import os
import time
from datetime import date,datetime
import json


max_results = 10

raw_data = open("arxiv.json").read()
json_data = json.loads(raw_data)
list_of_categories=["cs.CE", "cs.ET", "astro-ph", "cs.RO","cs.SD", "cs.SE"]

for category in list_of_categories:
    category_path = "./pdfs/"+category
    if not os.path.isdir(category_path):
        os.makedirs(category_path)
    url = "http://export.arxiv.org/api/query?search_query=cat:"+category+"&start=0&max_results="+max_results+"&sortBy=submittedDate&sortOrder=descending"
    data = urllib.request.urlopen(url).read()

    print("Retrieving " + category)
    arxiv_xml_name = "arxiv_"+category+".xml"
    with open(arxiv_xml_name, "w") as arxiv:
        arxiv.write(data.decode("utf-8"))
    tree = ET.parse(arxiv_xml_name)
    root = tree.getroot()
    entries = root.findall('{http://www.w3.org/2005/Atom}entry')
    entry_delimiter = json_data[category]

    for idx,entry in enumerate(entries):
        id_element = entry.findall('{http://www.w3.org/2005/Atom}id')
        paper_id = id_element[0].text.split(".")[2]

        if idx == 0:
            first_id = paper_id

        if paper_id == json_data[category]:
            break

        title_element = entry.findall('{http://www.w3.org/2005/Atom}title')
        paper_title = title_element[0].text

        published_element = entry.findall('{http://www.w3.org/2005/Atom}published')        
        published_date = datetime.fromisoformat(published_element[0].text[:-1])

        pdf_element = entry.findall('{http://www.w3.org/2005/Atom}link[@title="pdf"]')
        pdf_url = pdf_element[0].attrib.get("href")

        print("Downloading " +paper_id)
        urllib.request.urlretrieve(pdf_url, category_path+"/arxiv_"+paper_id+".pdf")
        time.sleep(4)
    json_data[category] = first_id
    time.sleep(4) 
    if os.path.exists(arxiv_xml_name):
        os.remove(arxiv_xml_name)
with open("arxiv.json","w") as jsonFile:
    json.dump(json_data, jsonFile, sort_keys=True, indent = 4)