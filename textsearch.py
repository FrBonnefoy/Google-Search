with open('items.txt') as f:
    parc_accor=f.readlines()
    parc_accor=list(map(lambda x: x.strip(),parc_accor))
import json
import urllib.request as urlreq
import urllib.parse
import os.path
from os import path
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import pandas as pd
'''
if path.exists("geocode_simple.csv"):
    pass
else:
    headers=("line\tcheck\tplace_id\tlong\tlat\n")
    fhandle2=open('geocode_simple.csv','w')
    fhandle2.write(headers)
    fhandle2.close()
'''
import time
import random
#keyword=input('Keyword?')
#keyword=urllib.parse.quote_plus(keyword)
from pointsmrs import points
import os.path
from os import path
api=input('\nInsert API\n\n')
def textsearch(keyword):
    global js
    global next_page_token
    global df
    global df2
    global df3
    time.sleep(random.uniform(2,3))
    print(keyword)
    #latitude=keytup[1]
    #longitude=keytup[0]
    keyword_url=urllib.parse.quote_plus(keyword)
    qpage="https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+str(keyword_url)+'&inputtype=textquery&fields=name,formatted_address,rating,user_ratings_total,place_id&key='+api
    query=urlreq.urlopen(qpage)
    data=query.read().decode('utf-8').replace('(','[').replace(')',']')
    js=json.loads(data)
    df=pd.DataFrame(js['candidates'])
    df.insert(0,'Keyword',keyword)
    if path.exists("textsearch.csv"):
        df.to_csv('textsearch.csv',mode='a',header=False,sep='\t',index=False)
    else:
        df.to_csv('textsearch.csv',sep='\t',index=False)

with ProcessPoolExecutor(max_workers=10) as executor:
    future_results = {executor.submit(textsearch, keyword): keyword for keyword in (parc_accor)}
    results=[]
    for future in concurrent.futures.as_completed(future_results):
        results.append(future.result())
