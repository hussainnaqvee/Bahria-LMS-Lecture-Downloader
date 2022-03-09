from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import time
from datetime import datetime, date, timedelta
import urllib
import requests
import os
import shutil

def initiate(credential,directory_path):
    #Path variable is to locate Chrome Webdrivers
    path=directory_path[0] #example===> "C:\\Users\\Hussa\Desktop\\chromedriver_win32\\chromedriver.exe"
    #dir variable is the path/directory where you want to download lecture slides/notes.
    dir=directory_path[1]  #example===>"C:\\Users\\Hussa\Desktop\\7th Semester\\Lecture_Slides"
    shutil.rmtree(dir)
    os.mkdir(dir)
    #username='username here'
    #password='password here'
    
    todayMessage=''
    subjectName=''
    subjectList=[]
    

    #Setting up selenium webdriver details
    
    
    #driver=webdriver.Chrome("Enter File location for your webdriver")
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('windows-size=1200X600')
    driver = webdriver.Chrome(path,chrome_options=options)
   
    driver.get("https://cms.bahria.edu.pk/Logins/Student/Login.aspx")

    #Finding username,password,institute location and sending username and password
    userTB=driver.find_element_by_name("ctl00$BodyPH$tbEnrollment")
    userTB.send_keys(credential[0])
    passTB=driver.find_element_by_name("ctl00$BodyPH$tbPassword")
    passTB.send_keys(credential[1])
    InsCB=driver.find_element_by_name("ctl00$BodyPH$ddlInstituteID")
    Select(driver.find_element_by_name('ctl00$BodyPH$ddlInstituteID')).select_by_value("1")
    time.sleep(1)
    loginBT=driver.find_element_by_id("BodyPH_btnLogin").click()


    #Navigating to lms by directly inputting the url
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't') 
    driver.get("https://cms.bahria.edu.pk/Sys/Common/GoToLMS.aspx")
    driver.get("https://lms.bahria.edu.pk/Student/LectureNotes.php")
    #checking number of courses
    Couursesdp=Select(driver.find_element_by_id("courseId"))
    count=len(Couursesdp.options)

    #Getting names of the Subjects and putting into a list
    for j in Couursesdp.options:
        subjectName=j.get_attribute('innerHTML')
        subjectName=subjectName.replace('\n                                                      ','')
        subjectName=subjectName.replace('amp;','')
        subjectList.append(subjectName.rstrip('\n                                                      '))
 
    for i in range(1,count):
        #selecting course by index
        Select(driver.find_element_by_id('courseId')).select_by_index(i)
        time.sleep(1)
        #finding rows of the table from table/tbody/tr section
        rows = driver.find_elements_by_xpath("//table/tbody/tr")
        filename=''
        os.mkdir(f"{dir}\\{subjectList[i]}")
        for j in range(1,len(rows)):  
            #extracting number of table-data for each table row by index i.e, rows[i]
            col=rows[j].find_elements_by_tag_name("td")
            
            if(len(col)>2):
                f_name=col[1].get_attribute('innerHTML')
                print(f_name)
                btn=col[2].find_element_by_class_name('label')
                link=btn.get_attribute('href')
                get_list=link.split('/')
                filename=get_list.pop()
                urllib.request.urlretrieve(link,f"{dir}\\{subjectList[i]}\\{filename}" ) 
                time.sleep(1)  
                #print(link)


def main():
    credential=["username/enrollment","password"]
    #example username="01-134181-0xx",password="bahria"
    directory_path=["Chrome Webdriver Path Here","Path to Download your lectures"]
    #example path to download all lectrues="C:\\Users\\Hussa\Desktop\\7th Semester\\Lecture_Slides"
    #example path to chrome webdrivers= "C:\\Users\\Hussa\Desktop\\chromedriver_win32\\chromedriver.exe"
    initiate(credential,directory_path)
    
if __name__ == '__main__':
    main()

