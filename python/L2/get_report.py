from msedge.selenium_tools import Edge, EdgeOptions
from datetime import date
from datetime import timedelta
from datetime import datetime
from datetime import time
import time
import os

def get_prev_date():
    today = date.today()
    prev_date = today.strftime("%Y-%m-%d")
    return prev_date

def download_report(URL, gecko):
    assert(os.path.exists(gecko))
    options=EdgeOptions()
    options.use_chromium = True
    options.add_argument("user-data-dir=C:\\Users\\atanas.janeshliev\\AppData\\Local\\Microsoft\\Edge\\User Data")
    options.add_argument("profile-directory=selenium_profil_2")

    driver = Edge(executable_path=gecko, options=options)
    driver.get(URL)
    time.sleep(2)
    el = driver.find_elements_by_class_name("resultfile")

    today = get_prev_date()

    cor_el = None
    for x in el:
        if today in x.text:
            print("Found today's report!")
            cor_el = x

    if cor_el != None:
        print (cor_el.text)

    fileToDownload = cor_el.text

    parent = cor_el.find_element_by_xpath("../..")
    print(parent.text)

    parent.click()
    print("Downloading file!")
    time.sleep(7)

    driver.close()

    fileToDownload = r"C:\Users\atanas.janeshliev\Downloads\edge_downloads/" + fileToDownload
    return fileToDownload

#MTD_closed = 'https://vmdwhwp001.austria.local/ReportPortal/frmreport.aspx?reportid=8234'
#yes(MTD_closed)
