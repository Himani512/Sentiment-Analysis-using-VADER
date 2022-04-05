#!/usr/bin/env python
# coding: utf-8

# In[35]:


import requests as r
from bs4 import BeautifulSoup as b
import pandas as p

df = p.DataFrame({'Summary': [],'Review':[],'Author':[],'Rating':[]})

#Scraping data using BeautifulSoup and saving it to a .csv file
for i in range(0,1980,20):
    url = (f'https://www.indeed.com/cmp/Walmart/reviews?fcountry=US&floc=Bentonville%2C+AR&start={i}')
    pages = r.get(url)
    soup = b(pages.content,'lxml')
    results = soup.find('div', attrs = { 'id' : 'cmp-container'})
    elements = results.findAll('div', attrs = {'class':'cmp-Review-container'})
    
    for elem in elements:
        title  = elem.find('div', attrs = {'class':'cmp-Review-title'})
        review = elem.find('div', attrs = {'class': 'cmp-Review-text'})
        author = elem.find('div', attrs = {'class':'cmp-Review-author'})
        rating = elem.find('button',attrs = {'class':'cmp-ReviewRating-text'})
        df = df.append({'Summary': title.text,'Review': review.text,'Author':author.text, 'Rating':rating.text, },
                       ignore_index=True)

author = df['Author'].str.split('-',expand = True)
author = author.rename(index={0:'Job',1:'Location',2:'Time'})
del author[3]
df1 = p.concat([df,author],axis =1)
df1.to_csv('Walmart_Indeed.csv')


# In[ ]:




