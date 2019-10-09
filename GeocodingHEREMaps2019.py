#!/usr/bin/env python
# coding: utf-8

# In[133]:


import herepy
from herepy.models import HEREModel
import pandas as pd
import os
import re
import json
###https://pypi.org/project/herepy/


# In[134]:


###Make a relative path to read and save files
script_path = os.path.abspath('__file__') 
path_list = script_path.split(os.sep)
script_directory = path_list[0:len(path_list)-1]
rel_path = "/PL_GLP_GNC_colonia.xlsx"
path = "/".join(script_directory) + "/" + rel_path


# In[136]:


###Read excel file
df = pd.read_excel(path)
print(df[:3])


# In[137]:


###Insert the API and test the code with one record and test the API
geocoderApi = herepy.GeocoderApi('XXXXXXXXXXXX', 'XXXXXXXXXXXX')
response = HEREModel.as_dict(geocoderApi.free_form('200 S Mathilda Sunnyvale CA'))
print(response)
type (response)


# In[139]:


### Test Subset of data from dictionary
df1 = [response['Response']['View'][0]['Result'][0]['Relevance'],response['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude'],response['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Longitude']]
print(df1)


# In[140]:


###regex cleanning the vector for geocoding
df['regexCODING'] = df['CODING'].map(lambda x: re.sub(r'[^.,a-zA-Z0-9 áéíóúÁÉÍÓÚñ]', '', x))
# print(df[:3])
df1 = df[['Permiso', 'regexCODING']].copy()
# print(df1)

###Create the loop for geocoding the complete database (less than 2500 records)
###For more records is necessary a Cron Job
df2 = []
for index, row in df1.iterrows():
#     print(row['regexCODING'])
    geocoding = HEREModel.as_dict(geocoderApi.free_form(row['regexCODING']))
    extract = [geocoding['Response']['View']]
    if len(extract[0])== 0:
        print('I Cant find the location, Sorry')
        pass
    else:
        data = [row['Permiso'],geocoding['Response']['View'][0]['Result'][0]['Relevance'],geocoding['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude'],geocoding['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Longitude']]  
#         print(data)
    df2.append(data)
# print(df2)  

    
###Add data to json
###data[0]['f'] = var


# In[141]:


### Create a dataframe and create a csv file
df3 = pd.DataFrame(df2,columns = ['Permiso' , 'Precision', 'Latitud','Longitud']) 
# print(df3)
df3.to_csv(r'GeocodingHEREMaps_UGI.csv')

