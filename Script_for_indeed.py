# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 00:25:17 2018

@author: ikish
"""

#This is a script to scrap the indeed listing and it is written for digital CPR

#importing the required libraries
import requests
import bs4
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import numpy as np
import re
import pygsheets
from time import gmtime, strftime


#Writing the fuctions to scarp the classes from the soup
def get_comp(result):
    try:
        return result.find('span', {'class':'company'}).text
    except:
        return 'NA'
def get_loc(result):
    try:
        return result.find('span', {'class':'location'}).text
    except:
        return 'NA'
    
def get_job(result):
    try:
        return result.find('a', {'data-tn-element':'jobTitle'}).text
    except:
        return 'NA'
    
def get_sal(result):
    try:
        return result.find('td', {'class':'snip'}).find('nobr').text
    except:
        return 'NA'
    
def get_link(result):
    try:
        return result.find("a").attrs['href']
                           
    except:
        return 'NA'
def get_date(result):
    try:
        return result.find('span',{'class':'date'}).text
    except:
        return 'NA'
 
#roles that are required to run in the search bar
indeed_roles = ['Social Media Marketing',"e-commerce","SEO Specialist","Digital marketing",'VP of marketing']


#Running the for loop for a range of 10 job listings per page till 100 pages
results = []

for role in indeed_roles:
  for start in range(0,100,10):
    url = "https://www.indeed.com/jobs?q="+role+"&sort=date&l=United+States&start="+str(start)+""  
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    #url = "https://www.indeed.com/jobs?q="+role+"&l=United+States&rbl=New+York%2C+NY&sort=date&ts=1529120086448&rq=1&fromage=last&start="+str(start)+"&sort=&psf=advsrch"
    html = requests.get(url,headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    for result in soup.find_all('div', {'class':' row result'}):
        results.append(result)
    sleep(1)

#Storing the results in job_list

job_list = pd.DataFrame(columns=['Company_Name','Contact Email','Contact Name','Contact Position','Job_Title','Date 1st Email Sent','Linkedin Sent Date','States','URLs','Date','Posted_date'])
for entry in results:
    company = get_comp(entry)
    Contact_Email = ""
    Contact_Name = ""
    Contact_Position = ""
    title = get_job(entry)
    Date_1st_Email_Sent = ""
    Linkedin_Sent_Date = ""
    States = get_loc(entry)
    URLs = get_link(entry)
    Date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    Posted_date = get_date(entry)
    job_list.loc[len(job_list)] = [company,Contact_Email,Contact_Name,Contact_Position,title,Date_1st_Email_Sent,Linkedin_Sent_Date, States,URLs,Date,Posted_date]
    

#dropping the duplicates with title and company as subsets and adding the .com to the link
final_list = job_list.drop_duplicates(subset=["Job_Title","Company_Name"],keep = False)
final_list['URLs'] = 'www.indeed.com' + final_list['URLs'].astype(str)

List_ready = final_list

#Authorizing the key to access google spreadsheets

google_sheet = pygsheets.authorize(outh_file = ".jsonfilr")

#Open spreadsheet
sheet = google_sheet.open("nameofthesheet")


Staffing_Agencies = sheet.worksheet_by_title("Staffing Agencies - EXCLUSION")
Big_Company = sheet.worksheet_by_title("Big Company - EXCLUSION")
Digital_Marketing_Agencies = sheet.worksheet_by_title("Digital Marketing Agencies - EXCLUSION")
Job_Title = sheet.worksheet_by_title("Job Title - EXCLUSIONS")
Indeed_Database = sheet.worksheet_by_title("Indeed Database")
Glassdoor_Database = sheet.worksheet_by_title("Glassdoor_Database")
Linkedin = sheet.worksheet_by_title("Job Posting-Linkedin")
Angel_List = sheet.worksheet_by_title("Job Posting- Angel List")
Funded_Companies = sheet.worksheet_by_title("Funded Companies")
Glassdoor = sheet.worksheet_by_title("Job Posting-Glassdoor")
Indeed = sheet.worksheet_by_title("Indeed - OLD")
indeed_vp = sheet.worksheet_by_title("VP - Indeed")


#Pulling the sheets as df
Staffing_Agencies_df = Staffing_Agencies.get_as_df()
Big_Company_df= Big_Company.get_as_df()
Digital_Marketing_Agencies_df = Digital_Marketing_Agencies.get_as_df()
Job_Title_df = Job_Title.get_as_df()
Indeed_Database_df = Indeed_Database.get_as_df()
Glassdoor_Database_df = Glassdoor_Database.get_as_df()
Linkedin_df = Linkedin.get_as_df()
Angel_List_df = Angel_List.get_as_df()
Funded_Companies_df = Funded_Companies.get_as_df()
Glassdoor_df = Glassdoor.get_as_df()
Indeed_df = Indeed.get_as_df()
indeed_vp_df = indeed_vp.get_as_df()



#creating a list of companies coloumn for the above data frames
Staffing_Agencies_list = Staffing_Agencies_df.iloc[:,1].tolist()
Big_Company_list = Big_Company_df.iloc[:,0].tolist()
Digital_Marketing_Agencies_list = Digital_Marketing_Agencies_df.iloc[:,1].tolist()
Job_Title_list = Job_Title_df.iloc[:,0].tolist()
Indeed_Database_list = Indeed_Database_df.iloc[:,0].tolist()
Glassdoor_Database_list = Glassdoor_Database_df.iloc[:,0].tolist()
Linkedin_list = Linkedin_df.iloc[:,2].tolist()
Angel_List_list = Angel_List_df.iloc[:,2].tolist()
Funded_Companies_list = Funded_Companies_df.iloc[:,5].tolist()
Glassdoor_list = Glassdoor_df.iloc[:,2].tolist()
indeed_list = Indeed_df.iloc[:,4].tolist()



#removing the empty spaces from the list
Staffing_Agencies_list  = filter(None, Staffing_Agencies_list)
Big_Company_list = filter(None, Big_Company_list)
Digital_Marketing_Agencies_list = filter(None, Digital_Marketing_Agencies_list)
Job_Title_list = filter(None, Job_Title_list)
Indeed_Database_list = filter(None, Indeed_Database_list)
Glassdoor_Database_list = filter(None, Glassdoor_Database_list)
Linkedin_list = filter(None, Linkedin_list)
Angel_List_list = filter(None, Angel_List_list)
Funded_Companies_list= filter(None, Funded_Companies_list)
Glassdoor_list= filter(None, Glassdoor_list)
indeed_list = filter(None, indeed_list)


List_ready["Company_Name"] = [x.replace("\n","") for x in List_ready["Company_Name"]]
List_ready["Company_Name"] = [x.replace("\n\n","") for x in List_ready["Company_Name"]]

#dropping the companies and staffing agencies that have already been scrapped
final1 = List_ready[~List_ready['Job_Title'].str.contains('|'.join(Job_Title_list),flags=re.IGNORECASE)]
final2 = final1[~final1['Company_Name'].str.contains('|'.join(indeed_list),flags=re.IGNORECASE)]
final3 = final2[~final2['Company_Name'].str.contains('|'.join(Staffing_Agencies_list),flags=re.IGNORECASE)]
final4 = final3[~final3['Company_Name'].str.contains('|'.join(Digital_Marketing_Agencies_list),flags=re.IGNORECASE)]
final5 = final4[~final4['Company_Name'].str.contains('|'.join(Big_Company_list),flags=re.IGNORECASE)]
final6 = final5[~final5['Company_Name'].str.contains('|'.join(Linkedin_list),flags=re.IGNORECASE)]
final7 = final6[~final6['Company_Name'].str.contains('|'.join(Angel_List_list),flags=re.IGNORECASE)]
final8 = final7[~final7['Company_Name'].str.contains('|'.join(Funded_Companies_list),flags=re.IGNORECASE)]
final9 = final8[~final8['Company_Name'].str.contains('|'.join(Glassdoor_list),flags=re.IGNORECASE)]
final10 = final9[~final9['Company_Name'].str.contains('|'.join(Glassdoor_Database_list),flags=re.IGNORECASE)]
final11 = final10[~final10['Company_Name'].str.contains('|'.join(Indeed_Database_list),flags=re.IGNORECASE)]
#final12 = final11[~final11['Company_Name'].str.contains('|'.join(indeed_vp_list),flags=re.IGNORECASE)]
print final11

final12_save = sheet.worksheet_by_title("VP - Indeed")

final12_save.set_dataframe(final11,(1,1),copy_head=True)

