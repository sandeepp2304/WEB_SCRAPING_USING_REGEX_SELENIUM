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
import time
class LinkedInData:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36')
        path = 'C://Users//USER//Desktop//chromedriver.exe'
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        self.driver.get('https://www.linkedin.com/')
        self.driver.find_element_by_xpath('/html/body/nav/a[3]').click()
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys('AIMLjohnson@outlook.com')
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys('2304johnson@007MLAI')
        sleep(1)
#         self.driver.find_element_by_link_text('Sign in').click()
        self.driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[4]/button').click()
        sleep(5)
    def result(self, query):
        if query.isdigit()== True:
            if len(query)>=10:
                url = "https://www.linkedin.com/in/"+query
        else:
            url = "https://www.linkedin.com/in/"+query
        self.driver.get(url)
        Profile_Info = dict()
        Profile_Info['Profile_url'] = url
        stopwords =['(1)','(2)','(3)','(4)','(5)','(6)','(7)','(8)','(9)','(10)']
        title = self.driver.title
        Profile_name = title.split('|')[0]
        Profile_name = Profile_name.strip()
        Profile_name = Profile_name.split(' ')
        sentence = [e for e in Profile_name if e not in stopwords]
        Profile_Name = ' '.join(sentence)
        if '-' in Profile_Name:
            Profile_Name = Profile_Name.split('-')
            Profile_Name = Profile_Name[0]
            Profile_Info['Profile_Name'] = Profile_Name
        else:
            Profile_Info['Profile_Name'] = Profile_Name
        Profile_Info['User_Name'] = query
        if 'Contact info' in self.driver.page_source:
            self.driver.find_element_by_link_text('Contact info').click()
        else:
            print('No_Contact info')
        test_list = re.findall(r'">(.*?)<',self.driver.page_source)
        without_empty_strings = [string for string in test_list if string != ""]
        if 'Dialog content start.' in without_empty_strings:
            index1 = without_empty_strings.index('Dialog content start.')
            if 'Dialog content end.' in without_empty_strings:
                index2 = without_empty_strings.index('Dialog content end.')
                contact_info = without_empty_strings[index1+1:index2]
                Contact_info = []
                for info in contact_info:
                    info = re.sub(' +', '',info)
                    if len(info)>2:
                        Contact_info.append(info)
                        if len(Contact_info)>0:
                            Contact_Info = []
                            for info in Contact_info:
                                index3 = self.driver.page_source.index('">'+info+'<')
                                text = self.driver.page_source[index3:index3+300]
                                urls = re.findall(r'href=[\'"]?([^\'" >]+)', text)
                                urls = ', '.join(urls)
                                Info_Url = info+":-"+" "+urls
                                Contact_Info.append(Info_Url)
                            Profile_Info['Contact info'] = Contact_Info
        else:
            pass
        self.driver.get(url)
        sleep(2)
        self.driver.minimize_window()
        urls = re.findall(r'(https?://\S+)', self.driver.page_source)
        Cover_Photo_Urls = []
        Profile_Photo_Urls = []
        for url in urls:
            if "https://media-exp1.licdn.com/dms/image" in url:
                if "200_800"  not in url:
                    if "200_200" in url:
                        Profile_Photo1 = url.replace("amp;", "")
                        Profile_Photo1 = Profile_Photo1[:-1]
                        if len(Profile_Photo1)<200:
                            Profile_Photo_Urls.append(Profile_Photo1)
                            if len(Profile_Photo_Urls)==1:
                                Profile_Info['Profile_Photo'] = Profile_Photo_Urls[0]
                    elif "400_400" in url:
                        Profile_Photo1 = url.replace("amp;", "")
                        Profile_Photo1 = Profile_Photo1[:-1]
                        if len(Profile_Photo1)<200:
                            Profile_Photo_Urls.append(Profile_Photo1)
                            if len(Profile_Photo_Urls)==1:
                                Profile_Info['Profile_Photo'] = Profile_Photo_Urls[0]

                else:
                    Cover_Photo1 = url.replace("amp;", "")
                    Cover_Photo1 = Cover_Photo1[:-1]
                    if len(Cover_Photo1)<200:
                        Cover_Photo_Urls.append(Cover_Photo1)
                        Profile_Info['Cover_Photo'] = Cover_Photo_Urls[0]
                    else:
                        pass
        View = []
        if 'Contact info\n' in self.driver.page_source:
            index4 = self.driver.page_source.index('Contact info\n')
            text = self.driver.page_source[:index4]
            index5 = text.rindex(Profile_Name)
            view = text[index5-15:] 
            view = re.sub(' +', ' ',view)
            view = view.split('">\n')
            for v in view:
                if len(v)>2:
                    if '\n' in  v:
                        v = v.split('\n')[0]
                        if '<' not in v:
                            if '>' not in v:
                                View.append(v)
            Profile_Info['Basic_Info'] = View
        else:
            pass
#         Scroll_down()
        self.driver.execute_script("window.scrollBy(0, 500);")
        if '">see more</a>\n' in self.driver.page_source:
            self.driver.find_element_by_link_text('see more').click()
            sleep(2)
            if '\n    About\n ' in self.driver.page_source:
                index5 = self.driver.page_source.index('\n    About\n ')
                text = self.driver.page_source[index5:]
                if '">see more<' in text:
                    index6 = text.index('</span>')
                    About = text[:index6]
                    About =About.split('">')
                    About_ = []
                    for a in About:
                        if '\n    About\n' not in a:
                            if 'class="' not in a:
                                About_.append(a)
                                Profile_Info['Profile_Summary'] = About_
        else:
            if '\n    About\n ' in self.driver.page_source:
                index5 = self.driver.page_source.index('\n    About\n ')
                text = self.driver.page_source[index5:]
                if '">see more<' in text:
                    index6 = text.index('</span>')
                    About = text[:index6]
                    About =About.split('">')
                    About_ = []
                    for a in About:
                        if '\n    About\n' not in a:
                            if 'class="' not in a:
                                About_.append(a)
                                Profile_Info['Profile_Summary'] = About_ 
            
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep(3)
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep(3)
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep(3)
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep(3)
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep(3)
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep(3)
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep(3)
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep(3)
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep(3)
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep(3)
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep(3)
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep(3)
        # if 'About\n' in driver.page_source:
#     index7 = driver.page_source.index('About\n')
        text = self.driver.page_source
        if '</main>\n' in text:
            index8 = text.index('</main>\n')
            corpus_list = text[:index8]
        elif '>People Also Viewed<' in text:
            index8 = text.index('>People Also Viewed<')
            corpus_list = text[:index8]
        elif '>Interests<' in text:
            index8 = text.index('>Interests<')
            corpus_list = text[:index8]
        elif '>Accomplishments<' in text:
            index8 = text.index('>Accomplishments<')
            corpus_list = text[:index8]
        elif '>Recommendations<' in text:
            index8 = text.index('>Recommendations<')
            corpus_list = text[:index8]
        elif 'Skills &amp; Endorsements\n' in text:
            index8 = text.index('Skills &amp; Endorsements\n')
            corpus_list = text[:index8]
        elif 'Licenses &amp; Certifications\n' in text:
            index8 = text.index('Licenses &amp; Certifications\n')
            corpus_list = text[:index8]
        elif 'Volunteer Experience\n' in text:
            index8 = text.index('Volunteer Experience\n')
            corpus_list = text[:index8]
        elif 'Education\n' in text:
            index8 = text.index('Education\n')
            corpus_list = text[:index8]
        elif 'Experience\n' in text:
            index8 = text.index('Experience\n')
            corpus_list = text[:index8]
        else:
            pass
        test_list = re.findall(r'">(.*?)\n',corpus_list)
        without_empty_strings = [string for string in test_list if string != ""]
        corpus_list = corpus_list.split('>')
        Corpus_list = []
        for e in corpus_list:
            e = e.split('<')[0]
            e = e.split() 
            e=" ".join(e)
            if len(e)>2:
                Corpus_list.append(e)
        if 'Experience' in Corpus_list:
            Experience_index = Corpus_list.index('Experience')
            Experience_list = Corpus_list[Experience_index:]
            if 'Education' in Experience_list:
                Education_index = Experience_list.index('Education')
                Experience = Experience_list[1:Education_index]
            elif 'Volunteer Experience' in Experience_list:
                Volunteer_Experience_index = Experience_list.index('Volunteer Experience')
                Experience = Experience_list[1:Volunteer_Experience_index]
            elif 'Licenses &amp; Certifications' in Experience_list:
                Licenses_Certifications_index = Experience_list.index('Licenses &amp; Certifications')
                Experience = Experience_list[1:Licenses_Certifications_index]
            elif 'Skills &amp; Endorsements' in Experience_list:
                Skills_Endorsements_index = Experience_list.index('Skills &amp; Endorsements')
                Experience = Experience_list[1:Skills_Endorsements_index]
            elif 'Recommendations' in Experience_list:
                Recommendations_index = Experience_list.index('Recommendations')
                Experience = Experience_list[1:Recommendations_index]
            elif 'Accomplishments' in Experience_list:
                Accomplishments_index = Experience_list.index('Accomplishments')
                Experience = Experience_list[1:Accomplishments_index]
            elif 'Interests' in Experience_list:
                Interests_index = Experience_list.index('Interests')
                Experience = Experience_list[1:Interests_index]
            if 'Company Name' in Experience:
                index = []
                for idx, val in enumerate(Experience):
                    if val == 'Company Name':
                        index.append(idx-1)
                Experience1 = [Experience[i : j] for i, j in zip([0] + index, index + [None])] 
                Experience1 = Experience1[1:]
                Profile_Info['Profile_Experience'] = Experience1
            else:
                Profile_Info['Profile_Experience'] = "No_Company_Details"
        else:
            Profile_Info['Profile_Experience'] = "No_Experience_Details"

        if 'Education' in Corpus_list:
            Education_index = Corpus_list.index('Education')
            Education_list = Corpus_list[Education_index:]
            if 'Volunteer Experience' in Education_list:
                Volunteer_Experience_index = Education_list.index('Volunteer Experience')
                Education = Education_list[1:Volunteer_Experience_index]
            elif 'Licenses &amp; Certifications' in Education_list:
                Licenses_Certifications_index = Education_list.index('Licenses &amp; Certifications')
                Education = Education_list[1:Licenses_Certifications_index]
            elif 'Skills &amp; Endorsements' in Education_list:
                Skills_Endorsements_index = Education.index('Skills &amp; Endorsements')
                Education = Education_list[1:Skills_Endorsements_index]
            elif 'Recommendations' in Education_list:
                Recommendations_index = Education_list.index('Recommendations')
                Education = Education_list[1:Recommendations_index]
            elif 'Accomplishments' in Education_list:
                Accomplishments_index = Education_list.index('Accomplishments')
                Education = Education_list[1:Accomplishments_index]
            elif 'Interests' in Education_list:
                Interests_index = Education_list.index('Interests')
                Education = Education_list[1:Interests_index]
            if 'Degree Name' in Education:
                    index1 = []
                    for idx, val in enumerate(Education):
                        if val == 'Degree Name':
                            index1.append(idx-1)
                    Education1 = [Education[i : j] for i, j in zip([0] + index1, index1 + [None])] 
                    Education1 = Education1[1:]
                    Profile_Info['Profile_Education'] = Education1
            else:
                Profile_Info['Profile_Education'] = "No_Degree Name_Details"
        else:
            Profile_Info['Profile_Education'] = "No_Educatione_Details"         
        if 'Volunteer Experience' in Corpus_list:
            Volunteer_Experience_index = Corpus_list.index('Volunteer Experience')
            Volunteer_Experience_list = Corpus_list[Volunteer_Experience_index:]
            if 'Licenses &amp; Certifications' in Volunteer_Experience_list:
                Licenses_Certifications_index = Volunteer_Experience_list.index('Licenses &amp; Certifications')
                Volunteer_Experience = Volunteer_Experience_list[1:Licenses_Certifications_index]
            elif 'Skills &amp; Endorsements' in Volunteer_Experience_list:
                Skills_Endorsements_index = Volunteer_Experience_list.index('Skills &amp; Endorsements')
                Volunteer_Experience = Volunteer_Experience_list[1:Skills_Endorsements_index]
            elif 'Recommendations' in Volunteer_Experience_list:
                Recommendations_index = Volunteer_Experience_list.index('Recommendations')
                Volunteer_Experience = Volunteer_Experience_list[1:Recommendations_index]
            elif 'Accomplishments' in Education_list:
                Accomplishments_index = Volunteer_Experience_list.index('Accomplishments')
                Volunteer_Experience = Volunteer_Experience_list[1:Accomplishments_index]
            elif 'Interests' in Volunteer_Experience_list:
                Interests_index = Volunteer_Experience_list.index('Interests')
                Volunteer_Experience = Volunteer_Experience_list[1:Interests_index]
            if 'Company Name' in Volunteer_Experience:
                    index2 = []
                    for idx, val in enumerate(Volunteer_Experience):
                        if val == 'Company Name':
                            index2.append(idx-1)
                    Volunteer_Experience1 = [Volunteer_Experience[i : j] for i, j in zip([0] + index2, index2 + [None])]
                    Volunteer_Experience1 = Volunteer_Experience1[1:]
                    Profile_Info['Volunteer Experience'] = Volunteer_Experience1
            else:
                Profile_Info['Volunteer Experience'] = "No_Company_Details"
        else:
            Profile_Info['Volunteer Experience'] = "No_Volunteer Experience_Details"
        if 'Licenses &amp; Certifications' in Corpus_list:
            Licenses_Certifications_index = Corpus_list.index('Licenses &amp; Certifications')
            Licenses_Certifications_list = Corpus_list[Licenses_Certifications_index:]
            if 'Skills &amp; Endorsements' in Licenses_Certifications_list:
                Skills_Endorsements_index = Licenses_Certifications_list.index('Skills &amp; Endorsements')
                Licenses_Certifications = Licenses_Certifications_list[1:Skills_Endorsements_index]
            elif 'Recommendations' in Licenses_Certifications_list:
                Recommendations_index = Licenses_Certifications_list.index('Recommendations')
                Licenses_Certifications = Licenses_Certifications_list[1:Recommendations_index]
            elif 'Accomplishments' in Licenses_Certifications_list:
                Accomplishments_index = Licenses_Certifications_list.index('Accomplishments')
                Licenses_Certifications = Licenses_Certifications_list[1:Accomplishments_index]
            elif 'Interests' in Licenses_Certifications_list:
                Interests_index = Licenses_Certifications_list.index('Interests')
                Licenses_Certifications = Licenses_Certifications_list[1:Interests_index]
            Profile_Info['Licenses_Certifications'] = Licenses_Certifications
        else:
             Profile_Info['Licenses_Certifications'] = 'No_Licenses_Certifications_Details'
        if 'Skills &amp; Endorsements' in Corpus_list:
            Skills_Endorsements_index = Corpus_list.index('Skills &amp; Endorsements')
            Skills_Endorsements_list = Corpus_list[Skills_Endorsements_index:]
            if 'Recommendations' in Skills_Endorsements_list:
                Recommendations_index = Skills_Endorsements_list.index('Recommendations')
                Skills_Endorsements = Skills_Endorsements_list[1:Recommendations_index]
            elif 'Accomplishments' in Skills_Endorsements_list:
                Accomplishments_index = Skills_Endorsements_list.index('Accomplishments')
                Skills_Endorsements = Skills_Endorsements_list[1:Accomplishments_index]
            elif 'Interests' in Skills_Endorsements_list:
                Interests_index = Skills_Endorsements_list.index('Interests')
                Skills_Endorsements = Skills_Endorsements_list[1:Interests_index]
            Profile_Info['Skills_Endorsements'] = Skills_Endorsements
        else:
            Profile_Info['Skills_Endorsements'] =  'No_Skills_Endorsements_Details'
        if 'Accomplishments' in Corpus_list:
            Accomplishments_index = Corpus_list.index('Accomplishments')
            Accomplishments_list = Corpus_list[Accomplishments_index:]
            if 'Interests' in Accomplishments_list:
                Interests_index = Accomplishments_list.index('Interests')
                Accomplishments = Accomplishments_list[1:Interests_index]
            else:
                Accomplishments = Accomplishments_list
            Profile_Info['Accomplishments'] = Accomplishments
        else:
            Profile_Info['Accomplishments'] =  'No_Accomplishments_Details'
        if 'Interests' in Corpus_list:
            Interests_index = Corpus_list.index('Interests')
            Interests_list = Corpus_list[Interests_index:]
            Profile_Info['Interests'] = Interests_list
        else:
            Profile_Info['Interests'] =  'No_Interests_Details'
#         print(Profile_Info)
        result = json.dumps(Profile_Info)
        print(result)
        return result
#                 return result
#     def Scroll_down(self):
#         self.driver.execute_script("window.scrollBy(0, 500);")

if __name__ == '__main__':
    obj = LinkedInData()
    result = obj.result(query='reidhoffman')


# In[ ]:




