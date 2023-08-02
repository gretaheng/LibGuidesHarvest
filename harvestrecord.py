import requests
from bs4 import BeautifulSoup
import collections
collections.Callable = collections.abc.Callable
import xml.etree.ElementTree as ET
import os
import copy

x = requests.get('https://lgapi-us.libapps.com/1.1/guides?status=1&guide_types=1&sort_by=name&site_id=5772&key=fake&expand=profile')
r = x.json()
idl = []
for d in r:
	idl.append(d['id'])

base = "https://libguides.sdsu.edu/oai.php?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:libguides.com:guides/"


with open(r'downloadedRecord.txt', 'w') as fp:
	for i in idl:
		url = base+str(i)
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'xml')
		fname = "harvested_records1/"+str(i)+".xml"
		f = open(fname, "w", encoding="utf-8")
		atext = soup.prettify().replace("<title>\n      ","<title>\n      SDSU Library Guide to ").replace('<OAI-PMH xmlns:="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">','<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">').replace('','').replace('<setSpec>\n     guides\n    </setSpec>\n','<setSpec>guides</setSpec>\n').replace('<dc xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">','<oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">').replace('</dc>','</oai_dc:dc>').replace('title>','dc:title>').replace('creator>','dc:creator>').replace('publisher>','dc:publisher>').replace('date>','dc:date>').replace('date>\n     <identifier>','date>\n     <dc:identifier>').replace('</identifier>\n    </oai_dc:dc>','</dc:identifier>\n    </oai_dc:dc>')
		if "description>" in atext:
			atext = atext.replace('description>','dc:description>')
		if "subject>" in atext:
			atext = atext.replace('subject>','dc:subject>')
		f.write(atext) 
		f.close()
		fp.write("%s\n" % i)

path = 'harvested_records1'
allf = []
for filename in os.listdir(path):
    if not filename.endswith('.xml'):
        continue
    else:
        allf.append(path+"/"+filename)

for findex in range(len(allf)):
    with open(allf[findex], 'r',encoding="utf8") as f:
        s = f.read()
        if findex == 0:
            allr = s.split("record>")[0][:-1]
        content = "<record>" + s.split("record>")[1] + "record>" 
        allr += content
        if findex == len(allf)-1:
            allr += s.split("record>")[2]
allr=allr.replace(">     ",">").replace('    </','</').replace('verb="GetRecord"','verb="ListRecords"').replace("<GetRecord>","<ListRecords>").replace("</GetRecord>","</ListRecords>")
fn_new = "output1011.xml"
with open(fn_new, "w",encoding="utf8") as fout:
    fout.write(allr) 
