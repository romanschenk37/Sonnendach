# pip install webdriver-manager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from PIL import Image

import time
import os

exit = False
print("Welcome to application Sonnendach")
print("Website is opening")

try:
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.get("https://www.uvek-gis.admin.ch/BFE/sonnendach/")
    driver.implicitly_wait(20)

    print("opening website was done.")
    print("Make your Windows ready to create screenshots.")
    input("Press Enter to start")

except:
    print("opening website failed")
    exit = True

filename_adresslist = input("Please type in Filename to read.")
file_split_char = ","
print("Reading File " + filename_adresslist)

try:
    adress_file = open(filename_adresslist, "r")
    adress_list = adress_file.read().splitlines()
    adress_file.close()

except:
    print("Reading file " + filename_adresslist + " failed.")
    exit = True

if(exit == False):
    for i in range(len(adress_list)):
        line = adress_list[i]
        adress = line.split(file_split_char)
        if((line == adress_list[0]) | ((adress[20][0:11] == "screenshots"))):
            pass
        else:
            search_string = adress[15] + " " + adress[3] + " " + adress[11] + " " + adress[13]
            search_bar = driver.find_element(By.ID, "searchTypeahead1")
            search_bar.clear()
            search_bar.send_keys(search_string)
            driver.implicitly_wait(120)

            found = False
            suggestions = driver.find_elements(By.XPATH, "//div[@class='tt-suggestion tt-selectable']")
            for suggestion in suggestions:
                if(suggestion.text == search_string):
                    found = True
                    suggestion.click()
                    driver.implicitly_wait(120)
                    break

            if(found):

                time.sleep(2)
                url = driver.current_url
                eignung = driver.find_element(By.ID, "eignung")
                image_filename = "screenshots/" + eignung.text + " - " + search_string + ".png"

                adress[18] = url
                adress[19] = eignung.text
                adress[20] = image_filename

                adress_file = open(filename_adresslist, "w")
                new_line_string = ""
                for j in adress:
                    new_line_string = new_line_string + j + file_split_char
                adress_list[i] = new_line_string
                new_adress_list = ""
                for j in adress_list:
                    new_adress_list = new_adress_list + (j) + "\n"
                adress_file.write(new_adress_list)
                adress_file.close()



                #featureElement = driver.find_element(By.XPATH, "// section[contains(string(),’START SCREENSHOT TESTING’)]")
                #location = featureElement.location
                #size = featureElement.size
                driver.save_screenshot(image_filename)
                #x = location["x"]
                #y = location["y"]
                #w = x + size["width"]
                #h = y + size["height"]
                #fullImg = Image.open(image_filename)
                #cropImg = fullImg.crop(x, y, w, h)
                #cropImg.save(image_filename)
                # TODO Screenshot schneiden


                print(image_filename + " was saved.")
            else:
                print("not found: " + search_string)

    input("finished. Press Enter to exit.")