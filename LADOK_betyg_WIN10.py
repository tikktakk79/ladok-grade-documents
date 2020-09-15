from selenium import webdriver
import time
from time import gmtime, strftime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re
import os
from datetime import datetime

login_name = "xxxxxxx"
passwd = "xxxxxxx"

thisTime = str(datetime.now())
print(thisTime)
thisTime = thisTime.replace(':', '_')
folderName = "Betygslista " + thisTime
folderPath = 'C:\\Users\\msberg\\Downloads\\' + folderName

os.mkdir(folderPath)

def is_text_present(self, text):
    return str(text) in self.driver.page_source



def get_pnr():
    f = open("C:\\Users\\msberg\\Downloads\\pnr.txt", "r")
    pnrArr = []
    for line in f:
        redline = re.sub(r'\s+', '', line)
        redline = redline.replace('-', '')
        for i, ch in enumerate(redline):
            nextNumberDigit = True

            try:
                nextNumberDigit = redline[10].isdigit()
            except:
                nextNumberDigit = False

            evString = (redline[i: i + 10])
            if (evString.isdigit() and not (((redline[i: i + 2] in ("19", "20")) or
                    (redline[i - 1: i + 1]  in ("19", "20"))) and nextNumberDigit) and
                    len(evString) == 10):
                print(redline[i: i + 2])
                print(redline[i - 1: i + 1])
                pnrArr.append(evString)
                print("pers search")
    return pnrArr

def wait_for_correct_current_url(lst_str_url):
    wait.until(
        lambda driver: driver.current_url[-4:] == lst_str_url)

def wait_for_url_change(lst_str_url):
    wait.until(
        lambda driver: driver.current_url[-4:] != lst_str_url)

options = webdriver.ChromeOptions()
options.add_argument('--lang=sv')
options.add_experimental_option('prefs', {
    "download.default_directory": folderPath, #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})

driver=webdriver.Chrome("C:\\Program Files\\chromedriver.exe", options=options)



driver.set_page_load_timeout(30)
driver.get("https://www.start.ladok.se/gui/#/startsida/original")
driver.maximize_window()
driver.implicitly_wait(20)

wait = WebDriverWait(driver, 20)
driver.find_element_by_tag_name("a").click()
driver.find_element_by_css_selector("div[alt='Chalmers']").click()
driver.find_element_by_css_selector("a[id='proceed']").click()

element = driver.find_element_by_css_selector(".username .input input")

element.send_keys(login_name)

element = driver.find_element_by_css_selector(".password .input input")
element.send_keys(passwd)

element = driver.find_element_by_css_selector("input[value='Logga in']")
element.click()

persArr = get_pnr()
outputArr = []
counter = 0

for pers in persArr:
    driver.find_element_by_css_selector("a[href='#/student']").click()
    wait_for_correct_current_url("dent")

    element = driver.find_element_by_css_selector("ladok-sokning-personnummer input")

    element.send_keys(pers)
    element = driver.find_element_by_css_selector("button[type='submit']")
    element.click()

    wait_for_url_change("dent")
    currAddress = driver.current_url
    print(currAddress)

    if currAddress[-8:] == "oversikt":
        outputArr.append(pers + " Betyg hämtat")
        element = driver.find_element_by_css_selector("ladok-students-resultat-intyg button")
        element.click()
        element = driver.find_element_by_css_selector("button[data-e2e='spara']")
        element.click()
        counter+=1
        driver.find_element_by_css_selector("a[href='#/student']").click()
    elif driver.page_source.find("inga träffar"):
        outputArr.append(pers + " Inga träffar")
        print(pers)
        print("Inga träffar")
        driver.elementl = driver.find_element_by_xpath("//*[text()='Rensa']").click()
    else:
        outputArr.append("Okänt fel")



with open(folderPath + '\\pnr_sokning_log.txt', 'w+') as f:
    f.write("Skapad " + datetime.now().isoformat(' ', "seconds") +"\n")
    f.write(str(counter) + " lyckade hämtningar " + str(len(persArr) - counter) + " misslyckanden" +"\n\n")
    for item in outputArr:
        f.write("%s\n" % item)



#driver.quit()