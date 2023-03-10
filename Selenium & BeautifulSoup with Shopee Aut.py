#!/usr/bin/env python
# coding: utf-8

# In[128]:


from selenium import webdriver
import bs4
import re
import pandas as pd
import time
from IPython.core.display import HTML


# In[129]:


#open chrome driver
path=r'C:\Users\atphor\Downloads\chromedriver'
driver = webdriver.Chrome(executable_path=path)

driver.get('https://shopee.co.th/')


# In[130]:


#input data
i=input ('input 1-12 :')
name='00'+i
print('name excel :',name)
head =round(int(i)/2)
if int(i) <= 1:
    head = 1
index = i

if int(index) % 2 == 0:
    index = 2
else:
    index = 1

#input number page
current_url=driver.current_url  
number_page = input('How much data do you want? (1 page = 60 data) :')
number_page = int(number_page)


# In[131]:


#close popup
thai_button = driver.find_element("xpath",'/html/body/div[2]/div[1]/div[1]/div/div[3]/div[1]/button')
thai_button.click()


# In[132]:


close_button = driver.execute_script('return document.querySelector("shopee-banner-popup-stateful").shadowRoot.querySelector("div.shopee-popup__close-btn")')
close_button.click()

type_url='/html/body/div[1]/div/div[2]/div/div/div[3]/div[2]/div[1]/div/div/div[2]/div/div[1]/ul/li['+str(head)+']/div/a['+str(index)+']/div/div[1]/div'

Types_button = driver.find_element("xpath",type_url)
#Types_button = driver.find_element("class",'n-CE6j _8YHYKq')
Types_button.click()
time.sleep(5)

Best_sales = driver.find_element("xpath",'/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div[2]/div/div[1]/div[1]/div[3]')
Best_sales.click()


# In[133]:


#zoom out and scraping data
driver.execute_script('document.body.style.zoom="10%"')
time.sleep(10)
data = driver.page_source

soup = bs4.BeautifulSoup(data)

#list all product data
all_product =soup.find_all('div',{'class':"_1yN94N WoKSjC _2KkMCe"})

all_product_list = []
for product in all_product:
    all_product_list.append(product.text)

all_price =soup.find_all('div',{'class':"cbl0HO MUmBjS"})

all_price_list = []
for product in all_price:
    all_price_list.append(product.text)

all_sell =soup.find_all('div',{'class':'x+3B8m wOebCz'})

all_sell_list = []
for product in all_sell:
    all_sell_list.append(product.text)


#removing symbol
all_sell_list =re.findall(r'[\d\.\d]+',str(all_sell_list))#ทำให้ลิสไม่มีตัวหนังสือหรือสัญลักษณ์

#make product dataframe
all_data = pd.DataFrame({
    'Product Name': all_product_list,
    'Price': all_price_list,
    'sold(kpcs./Mouth)': all_sell_list
})

#list url
all_pic =soup.find_all('div',{'class':'usRW1x S8FTqJ'})

all_pic = soup.find_all('img',src=True)
all_pic=all_pic
print('Number of Images: ', len(all_pic))

# select src tag
image_src = [x['src'] for x in all_pic]

#sel only pic
image_src = [x for x in image_src if 61 < len(x)]

#make dataframe
df =pd.DataFrame(image_src,columns=['img'])[0:60]

#sel product
img = image_src[0:60]

df['img'] = img
df = pd.concat([df,all_data],axis=1)

# Converting links to html tags
def path_to_image_html(path):
    return '<img src="'+ path + '" width="60" >'

# Rendering the dataframe as HTML table
df.to_html(escape=False, formatters=dict(img=path_to_image_html))

# Rendering the images in the dataframe using the HTML method.
HTML(df.to_html(escape=False,formatters=dict(img=path_to_image_html)))


# In[140]:


#name excel
def hi_var(var_name):
    globals()[var_name]=df  
hi_var(name)
df.to_excel(name+'.xlsx')

