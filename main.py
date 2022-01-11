import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from settings import creds
from settings import daylist

browser = webdriver.Chrome()

# Login to Mainestreet and navigate to the class search page, wait is time in seconds to give the form to load properly
def Navigating(wait):
    # Load data from settings.py for login
    for data in creds:
        if data == 'username':
            username = creds[data]
        else:
            password = creds[data]
    # Login to UMS portal from the creds in settings
    browser.get('https://umaine.edu/portal/')
    inputSearch = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/p[1]/a/span')
    inputSearch.click()
    sleep(3)
    browser.find_element(By.XPATH, '//*[@id="username"]').send_keys(username)
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
    browser.find_element(By.XPATH, '//*[@id="fm1"]/button').click()
    sleep(3)

    # Switch to Mainestreet Tab
    browser.find_element(By.XPATH, '//*[@id="_categorylinks_WAR_categorylinksportlet_collapse0"]/div/a[2]/div/img').click()
    sleep(1)
    browser.switch_to.window(browser.window_handles[1])
    sleep(3)

    # Switch to Class Search Tab
    browser.find_element(By.XPATH, '//*[@id="ADMN_SC_PGT_QUICK_LINKS_Data"]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a').click()
    browser.switch_to.window(browser.window_handles[2])
    sleep(3)
    # Switch to iframe form
    browser.switch_to.frame('ptifrmtgtframe')
    sleep(2)

    # Select School
    browser.find_element(By.XPATH, '//*[@id="CLASS_SRCH_WRK2_INSTITUTION$31$"]/option[3]').click()
    sleep(1)


    # Check off the days to click from settings
    for day in daylist:
        if day == 'monday':
            if daylist[day] == 'yes':
                browser.find_element(By.XPATH, '//*[@id="SSR_CLSRCH_WRK_MON$5"]').click()
                print(daylist[day])
        if day == 'tuesday':
            if daylist[day] == 'yes':
                print(daylist[day])
                browser.find_element(By.XPATH, '//*[@id="SSR_CLSRCH_WRK_TUES$5"]').click()
        if day == 'wednesday':
            if daylist[day] == 'yes':
                print(daylist[day])
                browser.find_element(By.XPATH, '//*[@id="SSR_CLSRCH_WRK_WED$5"]').click()
        if day == 'thursday':
            if daylist[day] == 'yes':
                print(daylist[day])
                browser.find_element(By.XPATH, '//*[@id="SSR_CLSRCH_WRK_THURS$5"]').click()
        if day == 'friday':
            if daylist[day] == 'yes':
                print(daylist[day])
                browser.find_element(By.XPATH, '//*[@id="SSR_CLSRCH_WRK_FRI$5"]').click()

    # Search
    browser.find_element(By.XPATH, '//*[@id="CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"]').click()
    sleep(2)
    # Confirm search for over 50
    browser.find_element(By.XPATH, '//*[@id="#ICSave"]').click()
    #Wait time in seconds
    sleep(wait)

def Scraping():
    print("Scrape")
    total = int(browser.find_element(By.XPATH, '//*[@id="win0divSSR_CLSRSLT_WRK_GROUPBOX1"]/table/tbody/tr[1]/td').text.split()[0])
    print ('Range: ' + str(total) + '\n Beginning...\n')
    for i in range(total):
        location = browser.find_element(By.XPATH, '//*[@id="MTG_ROOM$' + str(i) + '"]').text
        days = browser.find_element(By.XPATH, '//*[@id="MTG_DAYTIME$' + str(i) + '"]').text.split()[0]
        time = browser.find_element(By.XPATH, '//*[@id="MTG_DAYTIME$' + str(i) + '"]').text.split()[1]
        professor = browser.find_element(By.XPATH, '//*[@id="MTG_INSTR$' + str(i) + '"]').text

        print('Result: ' + str(i) + ' of ' + str(total))
        print(professor)
        print(location)
        print(days)
        print(time + '\n')
        Export(location,days,time,professor)

# CSV Stuff    
def Export(location,days,time,professor):
    header = ['Class','Days','Time','Location','Professor']
    data = ['',days,time,location,professor]
    with open('MoWeFri_Classes_S2022.csv','a',newline='',encoding='UTF8') as file:
        writer = csv.writer(file)
        # Write in Header
        #writer.writerow(header)

        # Write in Data
        writer.writerow(data)


def NewScrape():
    totalSections = int(browser.find_element(By.XPATH, '//*[@id="win0divSSR_CLSRSLT_WRK_GROUPBOX1"]/table/tbody/tr[1]/td').text.split()[0])
    for classnum in range(1000):
        try:
            className = browser.find_element(By.XPATH, '//*[@id="win0divSSR_CLSRSLT_WRK_GROUPBOX2GP$' + str(classnum) + '"]')
            print('Element ' + str(classnum) + ': ' + browser.find_element(By.XPATH, '//*[@id="win0divSSR_CLSRSLT_WRK_GROUPBOX2GP$' + str(classnum) + '"]').text)
            try:
                for i in range(totalSections):
                    try:
                        data = className.find_elements(By.XPATH, '.child::*').text
                        #data = browser.find_elements(By.XPATH, '//*[@id="MTG_ROOM$' + str(i) + '"]').text
                        print('Data ' + str(i) + ': ' + str(data))
                        pass
                    except NoSuchElementException:
                        pass
            except NoSuchElementException:
                pass
        except NoSuchElementException:
            print('No Such element - ' + str(classnum))
            return



        

Navigating(90)
browser.close()