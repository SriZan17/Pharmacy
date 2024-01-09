from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time
import regex as re


suburbs = []
with open("error.txt", "r") as f:
    for line in f:
        suburbs.append(line.strip())

options = Options()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
for suburb in suburbs:
    pharmacies = {}
    link = (
        "https://www.findapharmacy.com.au/location-search?loc=" + suburb + "&service="
    )
    driver.get(link)
    time.sleep(1)
    driver.fullscreen_window()
    wait = WebDriverWait(driver, 10)

    try:
        no_of_pharmacies = wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "s-filtered-search__results__item")
            )
        )
    except:
        continue

    if len(no_of_pharmacies) == 0:
        continue

    for i in range(len(no_of_pharmacies)):
        driver.get(link)
        driver.fullscreen_window()
        # Relocate elements after navigating back
        no_of_pharmacies = wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "s-filtered-search__results__item")
            )
        )
        a_pharmacy = no_of_pharmacies[i]
        # for a_pharmacy in no_of_pharmacies:
        wait = WebDriverWait(a_pharmacy, 10)
        see_details = wait.until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "See details"))
        )
        # see_details = a_pharmacy.find_element(By.PARTIAL_LINK_TEXT, "See details")
        see_details.click()
        time.sleep(1)
        wait = WebDriverWait(driver, 10)
        details = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "s-filtered-search__details-section")
            )
        )
        details = details.text
        details = details.split("\n")
        print(details)
        pharmacy_name = details[0]
        pharmacy_address = details[1]
        pharmacy_address = pharmacy_address[9:]
        pharmacy_phone = details[3]
        pharmacy_phone = pharmacy_phone[7:]
        pharmacy_fax = details[4]
        pharmacy_fax = pharmacy_fax[5:]
        pharmacy_email = details[5]
        pharmacy_email = pharmacy_email[7:]
        print(pharmacy_name)
        if len(details) > 6:
            pharmacy_website = details[6]
        pharmacy_website = pharmacy_website[9:]
        if re.match(r"http?", pharmacy_website):
            pass
        else:
            pharmacy_website = "NA"
        pharmacies[pharmacy_name] = {
            "address": pharmacy_address,
            "phone": pharmacy_phone,
            "fax": pharmacy_fax,
            "email": pharmacy_email,
            "website": pharmacy_website,
        }
        back_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app-search"]/div/div[1]/div/div[2]/div/button')
            )
        )
        back_button.click()
        time.sleep(1)

        # save to json
        file_name = "data/" + suburb + ".json"
        with open(file_name, "w") as json_file:
            json.dump(pharmacies, json_file)
