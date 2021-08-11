import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from lxml import html
import csv
import time
import random
import json
import re, math

from captcha_solver import CaptchaSolver

def parse_page(htmlstring, driver, driver1, driver2):
    
    solver = CaptchaSolver()
    
    with open("miami_dade_county.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        # print("----------------------------------------------------->", len(csv_reader))
        for row in csv_reader:
            print("000---------------------------------------", line_count)
            
            if line_count == 0:
                print("Read Headers")
                line_count += 1

            
            else:
                
                address         = row[0]

                data = {
                    "address"        : address,
                }

                if "no-address" in address:
                    phone_data ={
                            "phone1" : "",
                            "phone2" : "",
                            "phone3" : "",
                            "phone4" : "",
                            "phone5" : "",
                            "phone6" : "",
                            "phone7" : "",
                            "phone8" : "",
                            "phone9" : "",
                            "phone10" : ""
                    }
                    
                    email_data = {
                        "email1" : "",
                        "email2" : "",
                        "email3" : "",
                        "email4" : "",
                        "email5" : "",
                        "email6" : "",
                        "email7" : "",
                        "email8" : "",
                        "email9" : "",
                        "email10" : "",
                    }
                    with open("miami_dade_county_ppl.csv", "a", newline="", encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow([data["address"], "", phone_data["phone1"], phone_data["phone2"], phone_data["phone3"], phone_data["phone4"], phone_data["phone5"], phone_data["phone6"], phone_data["phone7"], phone_data["phone8"], phone_data["phone9"], phone_data["phone10"], email_data["email1"], email_data["email2"], email_data["email3"], email_data["email4"], email_data["email5"], email_data["email6"], email_data["email7"], email_data["email8"], email_data["email9"], email_data["email10"]])
                    line_count += 1
                else:
                    address_array = address.split(",")
                    addressOnly = address_array[0]
                    city_state = address_array[1] + "," + address_array[2]
                    
                    # state = row[2]
                    # post = row[3]

                    print("Line Count------------------------------", line_count)
                    print("Address------------------> : ", address)
                    print("city_state---------------> : ", city_state)

                    if "#" in addressOnly:
                        addressOnly = addressOnly.replace("#", "%23")
                            
                    default_url = "https://www.truepeoplesearch.com/results?streetaddress={0}&citystatezip={1}"
                    base_url = "https://www.truepeoplesearch.com/results?streetaddress={0}&citystatezip={1}&page={2}"
                    
                    url = default_url.format(addressOnly, city_state)
                    print(url)
                    driver.get(url)
                    
                    try:
                        recaptcha = driver.find_element_by_class_name("g-recaptcha")
                        recaptchaFlag = True
                    except:
                        recaptchaFlag = False
                    if recaptchaFlag == True:
                        print('Stage2')
                        solver.solve_captcha_for_url(driver, driver.current_url)
                        driver.find_element_by_xpath('//button').click()
                        print('Stage2 done')
                    # return
                    # Page_Counts
                
                    try:
                        itemsInfo = driver.find_element_by_xpath("//html/body/div[2]/div/div[2]/div[3]/div[1]").text
                        totals = int((itemsInfo.split(" "))[0])
                        page_counts = math.ceil(totals / 11)
                        print("Total Items Accounts----------------------> : ", totals)
                        try:
                            recaptcha = driver.find_element_by_class_name("g-recaptcha")
                            recaptchaFlag = True
                        except:
                            recaptchaFlag = False
                        
                        if recaptchaFlag == True:
                            print('Stage2')
                            solver.solve_captcha_for_url(driver, driver.current_url)
                            driver.find_element_by_xpath('//button').click()
                            print('Stage2 done') 
                        
                        ownerXpaths = driver.find_elements_by_xpath("//div[contains(@class, 'card-summary')]//div[@class='h4']")
                        viewButtons = driver.find_elements_by_xpath("//div[contains(@class, 'card-summary')]//div[contains(@class, 'align-self-center')]/a")
                        
                        if totals > 3:
                            for item in range(0, 3):
                                ownerName = ownerXpaths[item].text
                                second_url = viewButtons[item].get_attribute('href')
                                print("OwnerName------------------->", ownerName)
                                print("second_url------------------->", second_url)
                                driver1.get(second_url)
                                parse_owner(driver1.page_source, driver1, ownerName, data)
                        else:
                            for item in range(0, totals):
                                ownerName = ownerXpaths[item].text
                                second_url = viewButtons[item].get_attribute('href')
                                print("OwnerName------------------->", ownerName)
                                print("second_url------------------->", second_url)
                                driver1.get(second_url)
                                parse_owner(driver1.page_source, driver1, owerName, data)
                    except:
                        print("No Information")
                        phone_data ={
                            "phone1" : "",
                            "phone2" : "",
                            "phone3" : "",
                            "phone4" : "",
                            "phone5" : "",
                            "phone6" : "",
                            "phone7" : "",
                            "phone8" : "",
                            "phone9" : "",
                            "phone10" : ""
                        }
                        
                        email_data = {
                            "email1" : "",
                            "email2" : "",
                            "email3" : "",
                            "email4" : "",
                            "email5" : "",
                            "email6" : "",
                            "email7" : "",
                            "email8" : "",
                            "email9" : "",
                            "email10" : "",
                        }
                        with open("miami_dade_county_ppl.csv", "a", newline="", encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow([data["address"], "", phone_data["phone1"], phone_data["phone2"], phone_data["phone3"], phone_data["phone4"], phone_data["phone5"], phone_data["phone6"], phone_data["phone7"], phone_data["phone8"], phone_data["phone9"], phone_data["phone10"], email_data["email1"], email_data["email2"], email_data["email3"], email_data["email4"], email_data["email5"], email_data["email6"], email_data["email7"], email_data["email8"], email_data["email9"], email_data["email10"]])
            line_count += 1


def parse_owner(htmlstring, driver1, ownerName, data):
    print("-----------------------------------------------------------------------???")
    solver = CaptchaSolver()
    try:
        recaptcha = driver1.find_element_by_class_name("g-recaptcha")
        recaptchaFlag = True
    except:
        recaptchaFlag = False

    if recaptchaFlag == True:
        print('Stage2')
        solver.solve_captcha_for_url(driver1, driver1.current_url)
        driver1.find_element_by_xpath('//button').click()
        print('Stage2 done')
    phone_data ={
        "phone1" : "",
        "phone2" : "",
        "phone3" : "",
        "phone4" : "",
        "phone5" : "",
        "phone6" : "",
        "phone7" : "",
        "phone8" : "",
        "phone9" : "",
        "phone10" : ""
    }
    
    email_data = {
        "email1" : "",
        "email2" : "",
        "email3" : "",
        "email4" : "",
        "email5" : "",
        "email6" : "",
        "email7" : "",
        "email8" : "",
        "email9" : "",
        "email10" : "",
    }
    with open("miami_dade_county_ppl.csv", "a", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
    
    
        print("Second Parse")
        # time.sleep(4)
        phones = re.findall(r'[(][\d]{3}[)][ ]?[\d]{3}-[\d]{4}', driver1.page_source)
        
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', driver1.page_source)
        
        for phone in range(1, len(phones) + 1):
            phone_data["phone{}".format(phone)] = phones[phone - 1]
            
        for email in range(1, len(emails) + 1):
            if 'truepeople' not in emails[email - 1]:
                email_data["email{}".format(email)] = emails[email - 1]
            
        writer.writerow([data["address"], ownerName, phone_data["phone1"], phone_data["phone2"], phone_data["phone3"], phone_data["phone4"], phone_data["phone5"], phone_data["phone6"], phone_data["phone7"], phone_data["phone8"], phone_data["phone9"], phone_data["phone10"], email_data["email1"], email_data["email2"], email_data["email3"], email_data["email4"], email_data["email5"], email_data["email6"], email_data["email7"], email_data["email8"], email_data["email9"], email_data["email10"]])
        

        

options = webdriver.ChromeOptions()
useragent_argument = "user-agent={}".format("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36")
# options.add_argument('--user-data-dir=C:\\Users\\YJS\\AppData\\Local\\Temp\\scoped_dir675516_23089\\Default')
path = "driver\\chromedriver.exe"

driver = Chrome(executable_path=path, chrome_options=options)
driver1 = Chrome(executable_path=path)
driver2 = Chrome(executable_path=path)

driver.get("https://www.truepeoplesearch.com/")
time.sleep(2)

driver.maximize_window()
driver1.maximize_window()
driver2.maximize_window()
time.sleep(2)

open('miami_dade_county_ppl.csv', 'wb').close()
header = ["Address", "Name", "phone1", "phone2", "phone3", "phone4", "phone5", "phone6", "phone7", "phone8", "phone9", "phone10", "email1", "email2", "email3", "email4", "email5", "email6", "email7", "email8", "email9", "email10"]
with open('miami_dade_county_ppl.csv', "a", newline="") as f:
    csv_writer = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
    csv_writer.writeheader()


parse_page(driver.page_source, driver, driver1, driver2)