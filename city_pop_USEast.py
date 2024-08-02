import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter
import requests


# Read the CSV file from the URL into a DataFrame
url = 'https://gist.githubusercontent.com/mattkram/d3880a3a23ca36ccf10f22c1f49adb29/raw/f4602d2b9a17eb0d17355897264f4bad80c5528f/NST-EST2022-POPCHG2020_2022.csv'
df = pd.read_csv(url)

# Display the first 10 rows of the DataFrame
print(df.head(10))
pop_est_reg=(df[(df['REGION']=='1') & (df['SUMLEV']==40)])
pop_est=pop_est_reg[["NAME","POPESTIMATE2020","POPESTIMATE2021", "POPESTIMATE2022"]]
pop_est.index=pop_est['NAME']
print(pop_est)
#pop_est.plot(kind='bar')

plt.rc('font', family='Open Sans')
plt.figure(figsize=(10, 6))
fig , ax = plt.subplots()
bars = ax.bar(
     x=np.arange(pop_est.index.size),
     height=pop_est.POPESTIMATE2020,
     tick_label=pop_est.index,
     
        
 )
ax.spines['top'].set_color('#DDDDDD')
ax.spines['right'].set_color('#DDDDDD')
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(bottom=False, left=False)
ax.set_axisbelow(True)
ax.yaxis.grid(True, color='#EEEEEE')
ax.xaxis.grid(False)


bar_color = bars[0].get_facecolor()
for bar in bars:
  ax.text(
      bar.get_x() + bar.get_width() / 2,
      bar.get_height() + 0.3,
      round(bar.get_height()/1e6, 1), 
      horizontalalignment='center',
      color=bar_color,
      weight='bold'
      
  )

def millions_formatter(x, pos):
    return f'{x / 1000000}'
    
     
ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))    
ax.set_xlabel('Region', labelpad=15, color='#333333')
ax.set_ylabel('Population 2020 (in Millions)', labelpad=15, color='#333333')
ax.set_title('Population of Major Cities on East Coast')

fig.tight_layout()
plt.xticks(rotation=90)
plt.show()
     
