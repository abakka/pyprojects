import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter
import requests
import json
import seaborn as sns 
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas.core.common import flatten

#create list of most recent 6 qtrs
two_yrs_ago = (datetime.now() - relativedelta(years=2)).strftime('%d/%m/%Y')
qs=(pd.date_range(two_yrs_ago,freq="Q",periods=6).to_period('Q'))
qlist=[]
for qt in qs.to_numpy():
    index = str(qt).find('Q')
    out_q = str(qt)[:index] + '-' + str(qt)[index:]
    #print(out_q)
    qlist.append(out_q)
      
# Request Data from data.gov.sg
base_url = "https://data.gov.sg/api/action/datastore_search?"
url = base_url + "resource_id=d_23000a00c52996c55106084ed0339566&limit=15000"
response = requests.get(url)

#extract data from json object
json_resp=(response.json())['result']
fields=json_resp['fields']
records=json_resp['records']

#create dataframe object from json data object 
df= pd.json_normalize(records)

#select latest quarters
df=df[(df['quarter'] == qlist[0]) | (df['quarter'] == qlist[1]) | (df['quarter'] == qlist[2]) | (df['quarter'] == qlist[3]) | (df['quarter'] == qlist[4]) | (df['quarter'] == qlist[5])]

#filter dataframe for flat_type 3-RM 
ddf=df[(df['flat_type'] == '3-RM')]

#convert median_rent column to numeric from object 
ddf['median_rent']=pd.to_numeric(ddf['median_rent'], errors='coerce')
       
#extract quarters & town areas to create ndarray rent [] for heatmap
quarters=ddf[(ddf['flat_type']=='3-RM')]['quarter'].unique()
town=ddf[(ddf['flat_type']=='3-RM')]['town'].unique()

#ndarray for heatmap
rent = []
for t in town :
    l = list()
    for q in quarters :
       l.append(ddf[(ddf['quarter']==q) & (ddf['town']==t)]['median_rent'].to_list()[0])
    rent.append(l)    
#print(rent)

#plot heatmap using seaborn
plt.rc('font', family = 'Open Sans')
plt.figure(figsize=(12,9))
fig , ax = plt.subplots()
figsize = fig.get_size_inches()
fig.set_size_inches(figsize * 1.5)
g = sns.heatmap(rent, cmap="crest")

#axis labels & titles
g.set_xticklabels(labels=quarters.tolist(), va="center")
g.set_yticklabels(labels=town, va="center")
plt.setp(ax.get_yticklabels(), rotation=0, ha="center")
plt.setp(ax.get_xticklabels(), rotation=0, ha="center",rotation_mode="anchor")
plt.title('Heatmap of 3-Room HDB Rent By Location', fontsize = 20) 
plt.xlabel('Quarters', fontsize = 15) 
plt.ylabel('Town Locations', fontsize = 15) 

plt.show()
