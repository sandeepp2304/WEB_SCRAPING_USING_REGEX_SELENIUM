#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
image_url = "background:#fff url('https\\3a //scontent.fhyd2-1.fna.fbcdn.net/v/t1.0-0/cp0/e15/q65/c0.270.360.241a/p640x640/36740353_10157459967347786_3761171945656156160_o.jpg?_nc_cat\\3d 101\\26 _nc_sid\\3d dd9801\\26 efg\\3d eyJpIjoidCJ9\\26 _nc_oc\\3d AQn8gnJgGV8zyhJKgXzNwLgI3mgNhU-d-TJOioqDDfHvsAmOGlGnAEa-Qdn5ayBX2YM\\26 _nc_ht\\3d scontent.fhyd2-1.fna\\26 _nc_tp\\3d 5\\26 oh\\3d 312aaf01cf5e9eca747329b81fe19e41\\26 oe\\3d 5EE8D25B') no-repeat center;background-size: cover;-webkit-background-size: cover;padding-bottom:56.25%;"
string = image_url.replace("\\3a", ":")
string = string.replace("\\3d", "=")
string = string.replace("\\26", "&")
string = string.replace(" ", "")
url = re.findall('\(.*?\)', string)
string = str(url).replace("('", "")
image_url = string.replace("')", "")
print(image_url)


# In[ ]:




