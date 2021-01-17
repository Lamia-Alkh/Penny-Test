import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")
import pandas as pd # to read excel sheet
import requests # to load url
from bs4 import BeautifulSoup # to scrape content
import urllib.request
from urllib.parse import urlparse
import os
from requests.utils import requote_uri
from lxml import html

# the script scrapes the contents from astro and knipex, the both sites contains different structure, therefore,
# seperate codes have writte. first it loads the given url and finds the relvant information from the html and store them into dataframe/


# In[82]:


# set directory to save image files
directory = "D:/"
# this function download image from the url and save it into directory
def downloadImage(link,index,site):
    filename = directory+site+str(index)+".jpg"# create filename
    link = requote_uri(link)# strip link
    req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})# get file
    with open(filename, "wb") as f:# write file
        with urllib.request.urlopen(req) as r:
            f.write(r.read())
    return filename


# # Scrape Contents from Astro

# In[83]:


astrodf = pd.read_excel (r'Dataset.xlsx', sheet_name='Astro')# read astro excel sheet
astrodf = pd.DataFrame(astrodf)
astrodf.head()


# In[79]:


headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
}
print("Scraping Task: Astro")
for index,row in astrodf.iterrows():# iterate over all urls
    URL = row['Identifier']# get url
    link = row['Image']
    page = requests.get(URL,headers = headers, verify=False)# load url
    soup = BeautifulSoup(page.content, 'html.parser')# get html content from url
    results = soup.find_all("div",attrs={'class': 'value'})# get div
    if len(results) > 0:# if there is div
        sku = results[0].decode_contents()# get sku
        description = results[1].decode_contents()# get description
        specification = results[2].decode_contents()# get specifications
        # append contents into dataframe
        # remove html tags from contents
        description = str(html.fromstring(description).text_content())
        specification = str(html.fromstring(specification).text_content())
        
        # put extract contents into pandas df
        astrodf["SKU.1"][index] = sku
        astrodf["Description"][index] = description
        astrodf["Specification"][index] = specification
           # get image
        filename = downloadImage(link,index,"astro")
        astrodf["Pointer"][index] = "file:\\\\"+filename


# In[80]:


# save results as output excel file
file_name = 'astrodf.xlsx'
astrodf.to_excel(file_name) 


# # Scrape Contents from Knipex

# In[55]:


knipexdf = pd.read_excel (r'Dataset.xlsx', sheet_name='Knipex')# read knipex excel sheet
kinpexdf = pd.DataFrame(knipexdf)
kinpexdf.head()


# In[56]:


headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
}
print("Scraping Task: Knipex")
for index,row in knipexdf.iterrows():# iterate over all urls
    URL = row['URL']# get url
    link = row['Image']
    description = ""
    details = ""
    if URL != "None":
        page = requests.get(URL,headers = headers, verify=False)# load url
        soup = BeautifulSoup(page.content, 'html.parser')# get html content from url
        # scrape table 1
        results = soup.find("div",attrs={'id': 'fragment-1'})# get div
        table = results.find('table')
        rows = table.find_all("tr")
        for row in rows:
            head = row.find("th")
            header = head.decode_contents()
            td = row.find_all("td")[1]
            value= td.decode_contents()
            #print(header,",",value)
            details = details + header+": "+ value + "\n"

        # scrape table 2
        results = soup.find("div",attrs={'id': 'fragment-2'})# get div
        li = results.find_all('li')
        for row in li:
            text = row.decode_contents()
            description = description + text + "\n"
        
        knipexdf["Description"][index] = description
        knipexdf["Details"][index] = details
        
        # get image
        filename = downloadImage(link,index,"knipex")
        knipexdf["Pointer"][index] = "file:\\\\"+filename


# In[57]:


# save results as output excel file
file_name = 'knipexdf.xlsx'
knipexdf.to_excel(file_name) 


# In[ ]:




