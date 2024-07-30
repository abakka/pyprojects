import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter
import requests
import json

# Request Data from data.gov.sg
base_url = "https://data.gov.sg/api/action/datastore_search?"
url = base_url + "resource_id=d_23000a00c52996c55106084ed0339566&limit=1000&q={\"town\":\"Bedok\"}"
response = requests.get(url)

#extract data from json object
json_resp=(response.json())['result']
fields=json_resp['fields']
records=json_resp['records']

#create dataframe object from json data object
df= pd.json_normalize(records)

#filter dataframe for flat_type 3-RM & 4-RM
ddf=df[(df['flat_type'] == '3-RM') | (df['flat_type'] == '4-RM')]
#print((ddf['median_rent']).dtype)
#convert median_rent column to numeric from object 
ddf['median_rent']=pd.to_numeric(ddf['median_rent'], errors='coerce')
#ddf=ddf.fillna(0.0)
#print(ddf)

#extract columns for x axis & 2 columns for 3-RM & 4-RM rent
quarters=ddf[(ddf['flat_type']=='3-RM')]['quarter']
median_rent_3RM=ddf[(ddf['flat_type']=='3-RM')]['median_rent']
median_rent_4RM=ddf[(ddf['flat_type']=='4-RM')]['median_rent']

#format plt for prettier chart
plt.rc('font', family='Open Sans')
plt.figure(figsize=(10, 6))
fig , ax = plt.subplots()

#plot 3-RM median rent & 4-RM mdeian rent
plt.plot(quarters,median_rent_3RM, marker='o', color='#005b96', label='3-RM')
plt.plot(quarters,median_rent_4RM, marker='*', color='#6497b1', label='4-RM')

#format axes
ax.spines['top'].set_color('#DDDDDD')
ax.spines['right'].set_color('#DDDDDD')
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(bottom=False, left=False)
ax.set_axisbelow(True)
ax.yaxis.grid(True, color='#EEEEEE')
ax.xaxis.grid(False)

#reduce the number of xticks & yticks on the axes
ax.xaxis.set_major_locator(plt.MaxNLocator(20))
ax.yaxis.set_major_locator(plt.MaxNLocator(20))
     
#axes labels & title   
ax.set_xlabel('Quarters', labelpad=15, color='#333333')
ax.set_ylabel('Monthly Rent (in SGD)', labelpad=15, color='#333333')
ax.set_title('Monthly Rent of HDBs in Bedok Town Region Since 2005')

fig.tight_layout()

#rotate x axis label 90 degrees & add legend
plt.xticks(rotation=90)
plt.legend()
plt.show()
     
