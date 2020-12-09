import urllib.request 
import xml.etree.ElementTree as ET
import os 
import time
from datetime import date,datetime
import json
from PyPDF2 import PdfFileReader, PdfFileWriter

list_of_categories=["cs.CE", "cs.ET", "astro-ph", "cs.RO","cs.SD", "cs.SE"]
json_path = "arxiv.json"
max_results = str(20)

def retrieve_xml_children(root, child_element):
    xpath_search = "{http://www.w3.org/2005/Atom}"+child_element
    return root.findall(xpath_search)

def retrieve_authors(entry):
    authors = []
    all_authors_xml = retrieve_xml_children(entry,"author")
    for author in all_authors_xml:
        authors_name = retrieve_xml_children(author, "name")
        for author_name in authors_name:
            authors.append(author_name.text)
    authors_string =  ", ".join(authors)
    return authors_string

def add_metadata_to_pdf(pdf_path, title, authors):
    file_in = open(pdf_path, "rb")
    reader = PdfFileReader(file_in, strict=False)
    writer = PdfFileWriter()

    writer.appendPagesFromReader(reader)
    #metadata = reader.getDocumentInfo()
    #writer.addMetadata(metadata)

    writer.addMetadata({
        '/Title':title,
        '/Author': authors
    })

    file_out = open(pdf_path, 'ab')
    writer.write(file_out)

    file_in.close()
    file_out.close()
    

if __name__ == "__main__":

    raw_data = open(json_path).read()
    json_data = json.loads(raw_data)

    json_data["last_updated"]=str(datetime.now())

    for category in list_of_categories:
        category_path = "./pdfs/"+category
        if not os.path.isdir(category_path):
            os.makedirs(category_path)
        url = "http://export.arxiv.org/api/query?search_query=cat:"+category+"&start=0&max_results="+max_results+"&sortBy=submittedDate&sortOrder=descending"
        data = urllib.request.urlopen(url).read()

        arxiv_xml_name = "arxiv_"+category+".xml"
        with open(arxiv_xml_name, "w") as arxiv:
            arxiv.write(data.decode("utf-8"))
        tree = ET.parse(arxiv_xml_name)
        root = tree.getroot()
        entries = retrieve_xml_children(root, "entry") 
        entry_delimiter = json_data[category]

        for idx,entry in enumerate(entries):
            id_element = retrieve_xml_children(entry,"id")
            paper_id = id_element[0].text.split(".")[2]

            if paper_id == entry_delimiter:
                break

            if idx == 0:
                json_data[category] = paper_id

            title_element = retrieve_xml_children(entry,'title')
            paper_title = title_element[0].text.replace('\n', " ")

            paper_authors = retrieve_authors(entry)
        
            pdf_element = retrieve_xml_children(entry,'link[@title="pdf"]')
            paper_url = pdf_element[0].attrib.get("href")

            path_to_download_paper = category_path+"/arxiv_"+paper_id+".pdf"

            try:
                urllib.request.urlretrieve(paper_url, path_to_download_paper)
                add_metadata_to_pdf(path_to_download_paper, paper_title, paper_authors)
            except:
                print("Error in retrieving " + paper_id)
            time.sleep(4)

        if os.path.exists(arxiv_xml_name):
            os.remove(arxiv_xml_name)

        time.sleep(4)

    with open(json_path,"w") as jsonFile:
        json.dump(json_data, jsonFile, sort_keys=True, indent = 4)
    print("Arxiv gathered 🥳 ! Happy Readings 🤓")

