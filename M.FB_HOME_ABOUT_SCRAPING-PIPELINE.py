#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import web driver
from selenium import webdriver
import re
import json
import difflib
from time import sleep
import math
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import word_tokenize
import json
class HomeAboutData:
    def __init__(self):
#         options = webdriver.ChromeOptions()
#         options.add_argument("--start-maximized")
#         # options.add_argument("--headless")
#         # options.add_experimental_option("")
#         options.add_argument("--disable-infobars")
#         options.add_argument("--disable-notifications")
#         options.add_argument("--disable-extension")
        path = 'C://Users//USER//Desktop//chromedriver.exe'
#         self.driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        self.driver = webdriver.Chrome(executable_path=path)
        self.driver.get('https://m.facebook.com/')
        self.driver.find_element_by_xpath('//*[@id="m_login_email"]').send_keys('johnsonMLAI2304@gmail.com')
        self.driver.find_element_by_xpath('//*[@id="m_login_password"]').send_keys('johnsonMLAI2304@007')
        self.driver.find_element_by_xpath('//*[@id="u_0_4"]/button').click()
        sleep(5)
        self.driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div/div[3]/div[1]/div/div/a').click()
        sleep(5)
    def result(self, query):
        if query.isdigit()== True:
            if len(query)>=10:
                url = "https://m.facebook.com/profile.php?id="+query
        else:
            url = "https://m.facebook.com/"+query
        self.driver.get(url)
        Personal_Info = dict()
        Profile_Name = self.driver.title
        Personal_Info['Profile_Name'] = Profile_Name
        Personal_Info['USer_Name/ID'] = query
        string = self.driver.page_source
        string = string.replace("\\3a",":")
        string = string.replace("\\3d","=")
        string = string.replace("\\26","&")
        string =string.replace(" ","")
        urls = re.findall('\(.*?\)',string)
        Profile_Photo_urls = []
        Cover_Photo_urls = []
        for url in urls:
            if 'https://scontent.fhyd2-1.fna.fbcdn.net/v' in url:
                if '/p200x200/' in url:
                    Profile_Photo_urls.append(url)
                    Profile_Photo = Profile_Photo_urls[0]
                    if len(Profile_Photo)>=200:
                        Profile_Photo = Profile_Photo.replace("('","")
                        Profile_Photo1 = Profile_Photo.replace("')","")
                        Personal_Info['Profile_Photo']= Profile_Photo1
                        Cover_Photo_urls.append(urls[urls.index(url)-1])
                        if len(Cover_Photo_urls[0])>=200:
                            Cover_Photo = Cover_Photo_urls[0]
                            Cover_Photo = Cover_Photo.replace("('","")
                            Cover_Photo1 = Cover_Photo.replace("')","")
                            Personal_Info['Cover_Photo']= Cover_Photo1
                        else:
                            Personal_Info['Cover_Photo']= "No_Cover_Photo"
                    else:
                        Personal_Info['Profile_Photo']= "No_Profile_Photo"
        user_ids = []
        for url in urls:
            if '"USER_ID"' in url:
                user_ids.append(url)
                User_Id = user_ids[0]
        start_index = string.index('"USER_ID"')
        start = string[start_index:]
        end_index = start.index(',"NAME":') 
        end = start[:end_index]
        ua = end.split(',')
        User_ID = ua[0]
        User_id = User_ID.split(':')
        User_id = User_id[1]
        User_id = User_id.replace('"',"")
        Account_ID = ua[1]
        Account_iD = Account_ID.split(':')
        Account_iD = Account_iD[1]
        Account_iD = Account_iD.replace('"',"")
        Personal_Info['User_ID']= User_id
        Personal_Info['Account_ID']= Account_iD
        test_list = re.findall(r'">(.*?)<',self.driver.page_source)
        without_empty_strings = [string for string in test_list if string != ""]
        Info6 = []
        if 'Events' in without_empty_strings:
            target_ibdex3 = without_empty_strings.index('Events')
            info1 =without_empty_strings[target_ibdex3+1:]
            list = ['Friends','Photos','Life events','Did You Know','Videos','Check_ins','Sports','Music','Films','Keyboard shortcut help']
            index1 = []
            for i in list:
            #     print(i)
                for j in info1:
            #         if i in info:
                    if i == j:
                        index = info1.index(i)
            #             print(index)
                        index1.append(index)
                    else:
                        pass
            if len(index1)>0:
                Info1 =info1[:min(index1)]
                stopwords =['Details']
                [Info6.append(e) for e in Info1 if e not in stopwords]
                INFO = []
            #     stopwords =['Follow','Details'] 
            # #     [Info6.append(e) for e in Info5 if e not in Family_Member_Relation]
                for id,line in enumerate(Info6):
                    if 'at' in line:
                        line1 = Info6[id]+Info6[id+1]
                        INFO.append(line1)
                        Info6.pop(id+1)
                    elif 'From' in line:
                        line1 = Info6[id]+Info6[id+1]
                        INFO.append(line1)
                        Info6.pop(id+1)
                    elif 'Joined on ' in line:
                        INFO.append(line)
            #         elif 'by' in line:
            #             line1 = Info6[id]+Info6[id+1]
            #             INFO.append(line1)
            #             Info6.pop(id+1)
                    elif 'Married to ' in line:
                        line1 = Info6[id]+Info6[id+1]
                        INFO.append(line1)
                        Info6.pop(id+1)
                #     elif 'single' in line:
                #         print(line)
                    elif 'Went to' in line:
                        line1 = Info6[id]+Info6[id+1]
                        INFO.append(line1)
                        Info6.pop(id+1)
                    elif 'Single'== line:
                        INFO.append(line)
                    elif 'Maried'==  line:
                        INFO.append(line)
                    elif 'Engaged'==  line:
                        INFO.append(line)   
                    elif 'Live' in line:      
                        line1 = Info6[id]+Info6[id+1]
                        INFO.append(line1)
                        Info6.pop(id+1)
                    elif 'of' in line:
                        line1 = Info6[id]+Info6[id+1]
                        INFO.append(line1)
                        Info6.pop(id+1)
                    else:
                #         Info1.pop(id)
                        INFO.append(line)
                Personal_Info['Overview']= INFO
                if query.isdigit()== True:
                    if len(query)>=10:
                        url = "https://m.facebook.com/profile.php?id="+query+"&v=info"
                else:
                    url = "https://m.facebook.com/"+query+"/about"
                self.driver.get(url)
                Info = self.About_data()
                if 'Work' in Info:
                    target_ibdex4 = Info.index('Work')
                    if 'Education' in Info:
                        target_ibdex6= Info.index('Education')
                    elif "Places he's lived" in Info:
                        target_ibdex6= Info.index("Places he's lived")
                    elif "Places She's lived" in Info:
                        target_ibdex6= Info.index("Places She's Lived")
                    elif "Contact Info" in Info:
                        target_ibdex6= Info.index("Contact Info")
                    else:
                        target_ibdex6= Info.index("Basic info")
                    Info5 =Info[target_ibdex4+1:target_ibdex6]
                    Personal_Info['Work']= Info5
                else:
                    Personal_Info['Work']= None
                if 'Education' in Info:
                    target_ibdex5 = Info.index('Education')
                    if "Places he's lived" in Info:
                        target_ibdex6= Info.index("Places he's lived")
                        Info5 =Info[target_ibdex5+1:target_ibdex6]
                    elif "Places She's Lived" in Info:
                        target_ibdex6= Info.index("Places She's Lived")
                        Info5 =Info[target_ibdex5+1:target_ibdex6]
                    elif "Contact Info" in Info:
                        target_ibdex6= Info.index("Contact Info")
                        Info5 =Info[target_ibdex5+1:target_ibdex6]
                    else:
                        target_ibdex6= Info.index("Basic info")
                        Info5 =Info[target_ibdex5+1:target_ibdex6]
                    Personal_Info['Education']= Info5
                else:
                    Personal_Info['Education']= None
                if "Places he's lived" in Info:
                    target_ibdex6= Info.index("Places he's lived")
                    if 'Current City' in Info:
                        target_ibdex7= Info.index('Current City')
                        Info5 = Info[target_ibdex6+1:target_ibdex7]
                        Personal_Info['Current city']= Info5
                    else:
                        Personal_Info['Current city']= None

                elif "Places She's Lived" in Info:
                    target_ibdex6= Info.index("Places She's Lived")
                    if 'Current City' in Info:
                        target_ibdex7= Info.index('Current City')
                        Info5 = Info[target_ibdex6+1:target_ibdex7]
                        Personal_Info['Current city']= Info5
                    else:
                        Personal_Info['Current city']= None
                if "Places he's lived" in Info:
                    if "Home Town" in Info:
                        target_ibdex8 = Info.index('Home Town')
         
                        if 'Current City' in Info:
                            target_ibdex9 = Info.index('Current City')
                            target_ibdex8 = Info.index('Home Town')
                            Info5 = Info[target_ibdex9+1:target_ibdex8]
                            Personal_Info['Home Town']= Info5
                        else:
                            target_ibdex8 = Info.index('Home Town')
                            target_ibdex6= Info.index("Places he's lived")
                            Info5 = Info[target_ibdex6+1:target_ibdex8]
                            Personal_Info['Home Town']= Info5
                    else:
                        Personal_Info['Home Town']= None
                if "Places She's Lived" in Info:
                    if "Home Town" in Info:
                        target_ibdex8 = Info.index('Home Town')
            
                        if 'Current City' in Info:
                            target_ibdex9 = Info.index('Current City')
                            target_ibdex8 = Info.index('Home Town')
                            Info5 = Info[target_ibdex9+1:target_ibdex8]
                            Personal_Info['Home Town']= Info5
                        else:
                            target_ibdex8 = Info.index('Home Town')
                            target_ibdex6= Info.index("Places She's Lived")
                            Info5 = Info[target_ibdex6+1:target_ibdex8]
                            Personal_Info['Home Town']= Info5
                    else:
                        Personal_Info['Home Town']= None
                if "Other Places Lived" in Info:
                    target_ibdex9 = Info.index('Other Places Lived')
                    if 'Contact Info' in Info:
                        target_ibdex10 = Info.index('Contact Info')
                    elif 'Basic info' in Info:
                        target_ibdex10 = Info.index('Basic info')
                    Info5 = Info[target_ibdex9+1:target_ibdex10]
                    Personal_Info['Other Places Lived']= Info5
                else:
                    Personal_Info['Other Places Lived']= None
                Full_Name = self.driver.title
                About = 'About'+' '+Full_Name.split()[0]
                About1 = '>'+About+'<'
                if About in Info:
                    target_ibdex17 = Info.index(About)
                    if 'Life events' in Info:
                        target_ibdex18 = Info.index('Life events')
                        Info5 = Info[target_ibdex17+1:target_ibdex18] 
                        Personal_Info['About'] = Info5
                    elif 'Favourite Quotes' in Info:
                        target_ibdex18 = Info.index('Favourite Quotes')
                        Info5 = Info[target_ibdex17+1:target_ibdex18] 
                        Personal_Info['About'] = Info5
                    else:
                        Info5 = Info[target_ibdex17+1:] 
                        Personal_Info['About'] = Info5
                else:
                    Personal_Info['About']= None
                if 'Contact Info' in Info:
                    target_ibdex10 = Info.index('Contact Info')
                    if 'Basic info' in Info:
                        target_ibdex11 = Info.index('Basic info')
                        Info5 = Info[target_ibdex10+1:target_ibdex11] 
                        Personal_Info['Contact Information'] = Info5
                    elif 'Other Names' in Info:
                        target_ibdex11 = Info.index('Other Names')
                        Info5 = Info[target_ibdex10+1:target_ibdex11] 
                        Personal_Info['Contact Information'] = Info5
                    elif 'Relationship' in Info:
                        target_ibdex11 = Info.index('Relationship')
                        Info5 = Info[target_ibdex10+1:target_ibdex11] 
                        Personal_Info['Contact Information'] = Info5
                    elif 'Family Members' in Info:
                        target_ibdex11 = Info.index('Family Members')
                        Info5 = Info[target_ibdex10+1:target_ibdex11] 
                        Personal_Info['Contact Information'] = Info5
                    elif About in Info:
                        target_ibdex11 = Info.index(About)
                        Info5 = Info[target_ibdex10+1:target_ibdex11] 
                        Personal_Info['Contact Information'] = Info5
                    elif 'Life events' in Info:
                        target_ibdex11 = Info.index('Life events')
                        Info5 = Info[target_ibdex10+1:target_ibdex11] 
                        Personal_Info['Contact Information'] = Info5
                    elif 'Favourite Quotes' in Info:
                        target_ibdex11 = Info.index('Favourite Quotes')
                        Info5 = Info[target_ibdex10+1:target_ibdex11] 
                        Personal_Info['Contact Information'] = Info5
                else:
                    Personal_Info['Contact Information']= None
                if 'Basic info' in Info:
                    target_ibdex11 = Info.index('Basic info')
                    if 'Other Names' in Info:
                        target_ibdex12 = Info.index('Other Names')
                        Info5 = Info[target_ibdex11+1:target_ibdex12]
               
                    elif 'Relationship' in Info:
                        target_ibdex12 = Info.index('Relationship')
                        Info5 = Info[target_ibdex11+1:target_ibdex12]
               
                    elif 'Family Members' in Info:
                        target_ibdex12 = Info.index('Family Members')
                        Info5 = Info[target_ibdex11+1:target_ibdex12]
               
                    elif About in Info:
                        target_ibdex12 = Info.index(About)
                        Info5 = Info[target_ibdex11+1:target_ibdex12]
        
                    elif 'Life events' in Info:
                        target_ibdex12 = Info.index('Life events')
                        Info5 = Info[target_ibdex11+1:target_ibdex12]
        
                    elif 'Favourite Quotes' in Info:
                        target_ibdex12 = Info.index('Favourite Quotes')
                        Info5 = Info[target_ibdex11+1:target_ibdex12]
        
                    INFO = [] 
                    for id,line in enumerate(Info5):
                        if 'Birthday' in line:
                            line1 = 'Birthday :'+Info5[id-1]
                            INFO.append(line1)
                            Personal_Info['Basic Information'] = INFO
                        elif 'Birth Year' in line:
                            line1 = 'Gender :'+Info5[id-1]
                            INFO.append(line1)
                            Personal_Info['Basic Information'] = INFO
                        elif 'Gender' in line:
                            line1 = 'Gender :'+Info5[id-1]
                            INFO.append(line1)
                            Personal_Info['Basic Information'] = INFO
                        elif 'Interested in' in line:
                            line1 = 'Interested in :'+Info5[id-1]
                            INFO.append(line1)
                            Personal_Info['Basic Information'] = INFO
                        elif 'Languages' in line:
                            line1 = 'Languages :'+Info5[id-1]
                            INFO.append(line1)
                            Personal_Info['Basic Information'] = INFO
                        elif 'Religious views' in line:
                            line1 = 'Religious views :'+Info5[id-1]
                            INFO.append(line1)
                            Personal_Info['Basic Information'] = INFO
                        elif 'Political views' in line:
                            line1 = 'Political views :'+Info5[id-1]
                            INFO.append(line1)
                            Personal_Info['Basic Information'] = INFO
                        else:
                            pass
                else:
                    Personal_Info['Basic Information'] = None
                if 'Other Names' in Info:
                    target_ibdex1 = Info.index('Other Names')
                    if 'Relationship' in Info:
                        target_ibdex12 = Info.index('Relationship')
                        Info5 = Info[target_ibdex1+1:target_ibdex12]
                        Personal_Info['Other Names'] = Info5
                    elif 'Family Members' in Info:
                        target_ibdex12 = Info.index('Family Members')
                        Info5 = Info[target_ibdex1+1:target_ibdex12]
                        Personal_Info['Other Names'] = Info5
                    elif About in Info:
                        target_ibdex12 = Info.index(About)
                        Info5 = Info[target_ibdex1+1:target_ibdex12]
                        Personal_Info['Other Names'] = Info5
                    elif 'Life events' in Info:
                        target_ibdex12 = Info.index('Life events')
                        Info5 = Info[target_ibdex1+1:target_ibdex12]
                        Personal_Info['Other Names'] = Info5
                    elif 'Favourite Quotes' in Info:
                        target_ibdex12 = Info.index('Favourite Quotes')
                        Info5 = Info[target_ibdex1+1:target_ibdex12]
                        Personal_Info['Other Names'] = Info5
                else:
                    Personal_Info['Other Names'] = None
                if 'Favourite Quotes' in Info:
                    target_ibdex20 = Info.index('Favourite Quotes')
                    Info5 = Info[target_ibdex20+1:]
                    Personal_Info['Favourite Quotes'] = Info5
                else:
                    Personal_Info['Favourite Quotes'] = None
                years = []
                if 'Life events' in Info:
                    if 'Favourite Quotes' in Info:
                        target_ibdex19 = Info.index('Life events')
                        target_ibdex20 = Info.index('Favourite Quotes')
                        Info5 = Info[target_ibdex19+1:target_ibdex20]
                        for i in Info5:
                            i1 = i.isdigit()
                            if i1 == True:
                                year_Index = Info5.index(i)
                                years.append(year_Index)
                    else:
                        target_ibdex19 = Info.index('Life events')
                        Info5 = Info[target_ibdex19:]
                        for i in Info5:
                            i1 = i.isdigit()
                            if i1 == True:
                                year_Index = Info5.index(i)
                                years.append(year_Index)
                output = []
                prev = 0
                for index in years:
                    output.append(Info5[prev:index])
                    prev = index
                if len(output)>0:
                    output.append(Info5[years[-1]:])
                    Personal_Info["Life events"]=output[1:]
                else:
                    Personal_Info["Life events"]= None 
                if "Relationship" in Info:
                    target_ibdex4 = Info.index('Relationship')
                    if 'Family Members' in Info:
                        target_ibdex5 = Info.index('Family Members')
                    elif 'Life events' in Info:
                        target_ibdex5 = Info.index('Life events')
                    elif 'Favourite Quotes' in Info:
                        target_ibdex5 = Info.index('Favourite Quotes')
                    elif 'Friends' in Info:
                        target_ibdex5 = Info.index('Friends')
                    elif 'Photos' in Info:
                        target_ibdex5 = Info.index('Photos')
                    elif 'Videos' in Info:
                        target_ibdex5 = Info.index('Videos')
                    else:
                        target_ibdex5 = Info.index('Check_ins')
                    Info5 = Info[target_ibdex4+1:target_ibdex5]
                    f1_index = self.driver.page_source.index('>Relationship<')
                    f1_text = self.driver.page_source[f1_index:]
                    if '>Family Members<' in f1_text: 
                        f2_index = f1_text.index('>Family Members<')
                        f2_text = f1_text[1:f2_index]
                    elif About1 in f1_text:
                        f2_index = f1_text.index(About1)
                        f2_text = f1_text[:f2_index]
                    elif 'Life events' in f1_text:
                        f2_index = f1_text.index('Life events')
                        f2_text = f1_text[:f2_index]
                    elif 'Favourite Quotes' in f1_text:
                        f2_index = f1_text.index('Favourite Quotes')
                        f2_text = f1_text[:f2_index]
                    elif 'Friends' in f1_text:
                        f2_index = f1_text.index('Friends')
                        f2_text = f1_text[:f2_index]
                    elif 'Photos' in f1_text:
                        f2_index = f1_text.index('Photos')
                        f2_text = f1_text[:f2_index]
                    elif 'Videos' in f1_text:
                        f2_index = f1_text.index('Videos')
                        f2_text = f1_text[:f2_index]
                    elif 'Check_ins' in f1_text:
                        f2_index = f1_text.index('Check_ins')
                        f2_text = f1_text[:f2_index]

                    else:
                        pass
                    Relation_ships = []
                    Relation_ship = []
                    for i,name in enumerate(Info5):
                        f = f2_text.count(name)
                        if f==2:
                            Relation_ships.append(name)
                        elif f==1:
                            Relation_ship.append(name)
                        else:
                            pass
                    Relation_Ships_data = []
                    if len(Relation_ships)>=1:
                        for a in Relation_ships:
                            Relation_Ships_data.append(a)
                            f = f2_text.rindex(a)
                            f_index = f
                            Ainfo6 =f2_text[:f_index]
                            g = Ainfo6.rindex(a)
                            g_index = g
                            Ainfo7 =Ainfo6[g_index:]
                            user_name = re.findall(r'href=[\'"]?([^\'" >]+)', Ainfo7)
                            user_name = str(user_name)
                            user_name1 = user_name.split('?')
                            if "['/profile.php" in  user_name1:
                                user_name1 = user_name1[1]
                                list2 = user_name1.split('&')
                                list2 = list2[0]
                                list2 = list2.split('=')
                                user_name1 = list2[1]
                                Relation_Ships_data .append(user_name1)
                                Full_Url = "https://m.facebook.com/"+user_name1
                                Relation_Ships_data.append(Full_Url)
                            else:
                                user_name1 = user_name1[0]
                                user_name1 = user_name1.split('/')
                                if "scrapbooks" not in user_name1:
                                    user_name1 = user_name1[1]
                                    Relation_Ships_data .append(user_name1)
                                    Full_Url = "https://m.facebook.com/"+user_name1
                                    Relation_Ships_data.append(Full_Url)
                                else:
                                    user_name1 = "No_Username"
                                    Relation_Ships_data.append(user_name1)
                                    Full_Url = "No_Url"
                                    Relation_Ships_data.append(Full_Url)
                        Relation_Ships_data1 = [Relation_Ships_data[3*i:3*i+3] for i in range(0,math.ceil(len(Relation_Ships_data)/3))]
                    else:
                        Personal_Info['Relationship_Data'] = None

                    if len(Relation_ship)>=1:
                        Personal_Info['Relationship_Data'] = Relation_ship
                    else:
                        Personal_Info['Relationship_Data'] = None
                    if len(Relation_ships)>=1:
                        Personal_Info['Relationship_Data_w'] = Relation_Ships_data1
                    else:
                        Personal_Info['Relationship_Data_w'] = None
                else:
                    Personal_Info['Relationship_Data'] = None
                Info6 = []
                Family_Member_Relation = []
                Family_Member_Relation_stopwords =['Cousin','Aunt','Friend','Father','Mother','Brother','Sister','Son', 'Niece','Daughter','Auntie','Uncle','Nephew','Cousin(female)','Cousin(male)','Grandfather','Grandmother','Granddaughter','Grandson','Srepsister','Stepbrother','Stepfather','Stepmother','Stepson','Stepdaughter','Sister-in-law','Brother-in-law','Mother-in-law','Father-in-law','Son-in-law','Daughter-in-law'] 
                if "Family Members" in Info:
                    target_ibdex15 = Info.index('Family Members')
                    if About in Info:
                        target_ibdex16 = Info.index(About)
                    elif 'Life events' in Info:
                        target_ibdex16 = Info.index('Life events')
                    elif 'Favourite Quotes' in Info:
                        target_ibdex16 = Info.index('Favourite Quotes')
                    else:
                        Info5 = Info[target_ibdex15+1:]
                    Info5 = Info[target_ibdex15+1:target_ibdex16]
                    Family_Member_Relati = [Family_Member_Relation.append(e) for e in Info5 if e in Family_Member_Relation_stopwords]
                    Personal_Info['Family_Member_Relation']= Family_Member_Relation
                    Family_Member_Rela = [Info6.append(e) for e in Info5 if e not in Family_Member_Relation]
                    f1_index = self.driver.page_source.index('>Family Members<')
                    f1_text = self.driver.page_source[f1_index:]
                    if About1 in f1_text:
                        f2_index = f1_text.index(About1)
                        f2_text = f1_text[:f2_index]
                    elif 'Life events' in f1_text:
                        f2_index = f1_text.index('Life events')
                        f2_text = f1_text[:f2_index]
                    elif 'Favourite Quotes' in f1_text:
                        f2_index = f1_text.index('Favourite Quotes')
                        f2_text = f1_text[:f2_index]
                    elif 'Friends' in f1_text:
                        f2_index = f1_text.index('Friends')
                        f2_text = f1_text[:f2_index]
                    elif 'Photos' in f1_text:
                        f2_index = f1_text.index('Photos')
                        f2_text = f1_text[:f2_index]
                    elif 'Videos' in f1_text:
                        f2_index = f1_text.index('Videos')
                        f2_text = f1_text[:f2_index]
                    elif 'Check_ins' in f1_text:
                        f2_index = f1_text.index('Check_ins')
                        f2_text = f1_text[:f2_index]

                    else:
                        pass
                    Family_Members = []
                    Family_Member = []
                    for i,name in enumerate(Info6):
                        f = f2_text.count(name)
                        if f==2:
                            Family_Members.append(name)
                        elif f==1:
                            Family_Member.append(name)
                        else:
                            pass 
                    Family_Members_data = []
                    if len(Family_Members)>=1:
                        for a in Family_Members:
                            Family_Members_data.append(a)
                            f = f2_text.rindex(a)
                            f_index = f
                            Ainfo6 =f2_text[:f_index]
                            g = Ainfo6.rindex(a)
                            g_index = g
                            Ainfo7 =Ainfo6[g_index:]
                            user_name = re.findall(r'href=[\'"]?([^\'" >]+)', Ainfo7)
                    #         print(user_name)
                            user_name = str(user_name)
                            user_name1 = user_name.split('?')
                            if "['/profile.php" in  user_name1:
                                user_name1 = user_name1[1]
                                list2 = user_name1.split('&')
                                list2 = list2[0]
                                list2 = list2.split('=')
                                user_name1 = list2[1]
                                Family_Members_data.append(user_name1)
                                Full_Url = "https://m.facebook.com/"+user_name1
                                Family_Members_data.append(Full_Url)
                            else:
                                user_name1 = user_name1[0]
                                user_name1 = user_name1.split('/')
                                if "scrapbooks" not in user_name1:
                                    user_name1 = user_name1[1]
                                    Family_Members_data.append(user_name1)
                                    Full_Url = "https://m.facebook.com/"+user_name1
                                    Family_Members_data.append(Full_Url)
                                else:
                                    user_name1 = "No_Username"
                                    Family_Members_data.append(user_name1)
                                    Full_Url = "No_Url"
                                    Family_Members_data.append(Full_Url)
                        Family_Members_data1 = [Family_Members_data[3*i:3*i+3] for i in range(0,math.ceil(len(Family_Members_data)/3))]
                    else:
                        Personal_Info['Family_memeber_Data_W'] = None
                    if len(Family_Member)>0:
                        Personal_Info['Family_memeber_Data/About']= Family_Member
                    else:
                        Personal_Info['Family_memeber_Data/About']= None
                    if len(Family_Members)>0:
                        Personal_Info['Family_memeber_Data_W'] = Family_Members_data1
                    else:
                        Personal_Info['Family_memeber_Data_W'] = None

                else:
                    Personal_Info['Family_memeber_Data/About']= None
        #         print(Personal_Info)
                result = json.dumps(Personal_Info)
                print(result)
                return result

            else:
#                 pass
                result = "No_Profile_with_that_User_Name:"+" "+query
                print(result)
                return result
            
    def About_data(self):
        list = ['Friends','Photos','Videos','Check_ins','Sports','Music','Films','Keyboard shortcut help']
        index1 = []
        test_list = re.findall(r'>(.*?)<',self.driver.page_source)
        without_empty_strings = [string for string in test_list if string != ""]
        target_ibdex = without_empty_strings.index('Events')
        info =without_empty_strings[target_ibdex:]
        index1 = []
        for i in list:
            for j in info:
                if i == j:
                    index = info.index(i)
                    index1.append(index)
                else:
                    pass
        if len(index1)>1:
            Info =info[1:min(index1)]
            return Info
        else:
            pass


if __name__ == '__main__':
    obj = HomeAboutData()
    result = obj.result(query='priscilla')
    

    

