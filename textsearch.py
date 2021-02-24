import pandas as pd
with open('items.txt') as f:
    items=f.readlines()
    items=list(map(lambda x: x.strip(),items))
try:
	d_temp=pd.read_csv('textsearch.csv',sep='\t')
	listy=d_temp['Keyword'].tolist()
	items=[item for item in items if item not in listy]
except:
	pass

import json
import urllib.request as urlreq
import urllib.parse
import os.path
from os import path
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

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

import os.path
from os import path
api=input('\nInsert API\n\n')
bias=input('\nInsert Location Bias. Read readme for options. Press Enter to use local IP bias.\n')
if len(bias)>1:
	bias='&locationbias='+bias
else:
	bias=''
def textsearch(keyword):
    global js
    global next_page_token
    global df
    global df2
    global df3
    time.sleep(random.uniform(0.5,1))
    print(keyword)
    #latitude=keytup[1]
    #longitude=keytup[0]
    keyword_url=urllib.parse.quote_plus(keyword)
    qpage="https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+str(keyword_url)+'&inputtype=textquery&fields=name,formatted_address,rating,user_ratings_total,place_id,geometry'+bias+'&key='+api
    query=urlreq.urlopen(qpage)
    data=query.read().decode('utf-8').replace('(','[').replace(')',']')
    js=json.loads(data)
    df1=pd.DataFrame(js['candidates'])
    df2=pd.DataFrame()
    for a in range(len(js['candidates'])):
        d_temp=js['candidates'][a]['geometry']['location']
        listy=[d_temp['lng'],d_temp['lat']]
        df3=pd.DataFrame(listy).T
        df2=df2.append(df3,ignore_index=True)
    df2.columns=['Longitude','Latitude']
    df4=pd.concat([df1,df2],axis=1)
    df4.insert(0,'Keyword',keyword)
    if path.exists("textsearch.csv"):
        df4.to_csv('textsearch.csv',mode='a',header=False,sep='\t',index=False)
    else:
        df4.to_csv('textsearch.csv',sep='\t',index=False)

with ProcessPoolExecutor(max_workers=30) as executor:
    future_results = {executor.submit(textsearch, keyword): keyword for keyword in (items)}
    results=[]
    for future in concurrent.futures.as_completed(future_results):
        results.append(future.result())
