import urllib.request 
import xml.etree.ElementTree as ET
import os
import time

list_of_categories=["cs.CE", "cs.ET", "astro-ph", "cs.RO","cs.SD", "cs.SE"]
for category in list_of_categories:
    url = "http://export.arxiv.org/api/query?search_query=cat:"+category+"&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending"
    data = urllib.request.urlopen(url).read()

    with open("arxiv_"+category+".xml", "w") as arxiv:
        arxiv.write(data.decode("utf-8"))
    tree = ET.parse("arxiv_"+category+".xml")
    root = tree.getroot()
    entries = root.findall('{http://www.w3.org/2005/Atom}entry')

    for entry in entries:
        id_element = entry.findall('{http://www.w3.org/2005/Atom}id')
        paper_id = id_element[0].text.split(".")[2]
        pdf_element = entry.findall('{http://www.w3.org/2005/Atom}link[@title="pdf"]')
        pdf_url = pdf_element[0].attrib.get("href")
        print("Downloading " +paper_id)
        urllib.request.urlretrieve(pdf_url, "./pdfs/arxiv_"+category+"_"+paper_id+".pdf")
        time.sleep(4)

    entries = root.findall("./feed/entry")

    time.sleep(4) 