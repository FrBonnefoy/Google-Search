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
keyword=input('Keyword?\n\n')
print('\n\n')
api=input('Insert API\n\n')
keyword=urllib.parse.quote_plus(keyword)
from gpspoints import points
import os.path
from os import path

def nearby(keytup):
    global js
    global next_page_token
    global df
    global df2
    global df3
    time.sleep(random.uniform(2,5))
    print(keytup)
    latitude=keytup[1]
    longitude=keytup[0]
    qpage="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(latitude)+','+str(longitude)+'&radius=5000&'+str(keyword)+'&key='+api
    query=urlreq.urlopen(qpage)
    data=query.read().decode('utf-8').replace('(','[').replace(')',']')
    js=json.loads(data)
    df1=pd.DataFrame(js['results'])
    df2=pd.DataFrame()
    for a in range(len(js['results'])):
        d_temp=js['results'][a]['geometry']['location']
        listy=[d_temp['lng'],d_temp['lat']]
        df3=pd.DataFrame(listy).T
        df2=df2.append(df3,ignore_index=True)
    df2.columns=['Longitude','Latitude']
    df3=pd.concat([df1,df2],axis=1)
    try:
        del df3['permanently_closed']
    except:
        pass
    try:
        del df3['']
    #df3.columns=['Business Status','Geometry','Icon','Name','Open','Photos','Place Id','Plus code','Rating','Reference','Scope','Types','User Ratings','Vicinity','x','y']
    if path.exists("nearby.csv"):
        df3.to_csv('nearby.csv',mode='a',header=False,sep='\t',index=False)
    else:
        df3.to_csv('nearby.csv',sep='\t',index=False)

    #print(js)
    while True:
        try:
            next_page_token=js['next_page_token']
        except:
            break
        if len(js['next_page_token'])>0:
            time.sleep(10)
            print('\n')
            qpage="https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken="+next_page_token+'&key='+api
            query=urlreq.urlopen(qpage)
            data=query.read().decode('utf-8').replace('(','[').replace(')',']')
            js=json.loads(data)
            df1=pd.DataFrame(js['results'])
            df2=pd.DataFrame()
            for a in range(len(js['results'])):
                d_temp=js['results'][a]['geometry']['location']
                listy=[d_temp['lng'],d_temp['lat']]
                df3=pd.DataFrame(listy).T
                df2=df2.append(df3,ignore_index=True)
            df2.columns=['Longitude','Latitude']
            df3=pd.concat([df1,df2],axis=1)
            try:
                del df3['permanently_closed']
            except:
                pass
            '''
            df3.columns=['Business Status','Geometry','Icon','Name','Open','Photos','Place Id','Plus code','Rating','Reference','Scope','Types','User Ratings','Vicinity','x','y']
            '''
            if path.exists("nearby.csv"):
                df3.to_csv('nearby.csv',mode='a',header=False,sep='\t',index=False)
            else:
                df3.to_csv('nearby.csv',sep='\t',index=False)

            #print(js)
        else:
            break


with ProcessPoolExecutor(max_workers=20) as executor:
    future_results = {executor.submit(nearby, keytup): keytup for keytup in (points)}
    results=[]
    for future in concurrent.futures.as_completed(future_results):
        results.append(future.result())
