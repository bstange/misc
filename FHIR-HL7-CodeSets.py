# -*- coding: utf-8 -*-
   
import requests, zipfile, csv, json, os.path
from io import BytesIO

def extract_terms(url='http://hl7.org/fhir/validation.json.zip', path='./Data/validation.json'):
    """
    Parameters
    ----------
    url : FHIR validation url ('http://hl7.org/fhir/validation.json.zip')
    path: Filesystem path to extract json files, can be relative to wd/script location
    
    Returns
    ----------
    None, extracts files to disk
    """
    r = requests.get(url, stream=True)
    z = zipfile.ZipFile(BytesIO(r.content))   
    z.extractall(path=path,members=['v2-tables.json','v3-codesystems.json','valuesets.json'])

def valuesets_to_csv(infile, outfile):
    """
    Parameters
    ----------
    infile : json file of FHIR terminology table
    outfile : csv output file
    
    Returns
    ----------
    None, csv on disk
    """
    with open(infile,encoding='utf8') as data_file:
        data = json.load(data_file)
    with open(outfile, 'w',newline='\n') as writefile:
        wr = csv.writer(writefile)
        wr.writerow(['id','name','publisher','url','system','filter'])
        for i in data['entry']:
            wr.writerow([
            i['resource']['id'], 
            i['resource']['name'], 
            i['resource'].get('publisher',''), 
            i['resource']['url'],
            i['resource'].get('codeSystem',{}).get('system','') or 
            i['resource'].get('compose',{}).get('include',[{}])[0].get('system',''),
            json.dumps(i['resource'].get('compose',{}).get('include',[{}])[0].get('filter',''))
            ])

def get_concepts(infile, outfile):
    """
    Parameters
    ----------
    infile : json file of FHIR terminology table
    outfile : csv output file
    
    Returns
    ----------
    None, csv on disk
    """
    with open(infile,encoding='utf8') as data_file:
        data = json.load(data_file)
    with open(outfile, 'w',newline='\n',encoding = 'utf8') as writefile:
        wr = csv.writer(writefile)
        wr.writerow(['id','code','display','definition'])        
        for i in data['entry']:
          id = i['resource']['id']
          for concept in i['resource'].get('codeSystem',{}).get('concept',[]):
              wr.writerow([id,
              concept.get('code',''),
              concept.get('display',''),
                concept.get('definition','')])
          for concept in i['resource'].get('compose',{}).get('include',[{}])[0].get('concept',[]):
              wr.writerow([id,
              concept.get('code',''),
              concept.get('display',''),
                concept.get('definition','') or concept.get('extension',[{}])[0].get('valueString','')])

#   data['entry']['fullUrl']
#
#   [sets['fullUrl'] for sets in data['entry']]
#   [sets['fullUrl'] for sets in data['entry']].index('http://hl7.org/fhir/ValueSet/cpt-all')
#   data['entry'][27]


if __name__ == "__main__":
    url = 'http://hl7.org/fhir/validation.json.zip'
    path = './Data/validation.json'
    extract_terms(url)
    valuesets_to_csv(os.path.join(path,'valuesets.json'), 'valuesets.csv')
    valuesets_to_csv(os.path.join(path,'v2-tables.json'), 'v2-tables.csv')
    valuesets_to_csv(os.path.join(path,'v3-codesystems.json'), 'v3-codesystems.csv')
    get_concepts(os.path.join(path,'valuesets.json'), 'valueset_concepts.csv')
    get_concepts(os.path.join(path,'v2-tables.json'), 'v2-tables_concepts.csv')
    get_concepts(os.path.join(path,'v3-codesystems.json'), 'v3-codesystems_concepts.csv')
    