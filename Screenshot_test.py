from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
import os
import qrcode
from selenium.webdriver.common.action_chains import ActionChains

file_split_char = ","
filename_adresslist = "GWR-Daten Schaffhausen.csv"
adress_file = open(filename_adresslist, "r")
adress_list = adress_file.read().splitlines()
adress_file.close()
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.minimize_window()
driver.maximize_window()
driver.get("https://www.uvek-gis.admin.ch/BFE/sonnendach/")
driver.implicitly_wait(20)

try:
    if(not os.path.exists("screenshots")):
        os.makedirs("screenshots", exist_ok=False)
    if (not os.path.exists("qrcodes")):
        os.makedirs("qrcodes", exist_ok=False)
    for i in range(len(adress_list)):
        line = adress_list[i]
        print(line)
        adress = line.split(file_split_char)
        if((line != adress_list[0]) & ((adress[20][0:11] != "screenshots"))):
            print(adress)
            search_string = adress[15] + " " + adress[3] + " " + adress[11] + " " + adress[13]
            print(search_string)
            search_bar = driver.find_element(By.ID, "searchTypeahead1")
            search_bar.send_keys(Keys.CONTROL + "a")
            search_bar.send_keys(Keys.DELETE)
            search_bar.send_keys(search_string)
            driver.implicitly_wait(10)

            found = False
            suggestions = driver.find_elements(By.XPATH, "//div[@class='tt-suggestion tt-selectable']")
            for suggestion in suggestions:
                if(suggestion.text == search_string):
                    found = True
                    suggestion.click()
                    driver.implicitly_wait(120)
                    break

            if(found):
                print("found")
                time.sleep(2)
                url = driver.current_url
                eignung = driver.find_element(By.ID, "eignung")
                image_filename = eignung.text + " - " + search_string

                adress[18] = url
                adress[19] = eignung.text
                adress[20] = image_filename

                #adress_file = open(filename_adresslist, "w")
                new_line_string = ""
                for j in adress:
                    new_line_string = new_line_string + j + file_split_char
                adress_list[i] = new_line_string
                new_adress_list = ""
                for j in adress_list:
                    new_adress_list = new_adress_list + (j) + "\n"
                #adress_file.write(new_adress_list)
                #adress_file.close()

                print("start")

                # Create QR-Code
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(url)
                qr.make(fit=True)
                qr.make_image(fill='black', back_color='white').save(
                    "qrcodes/" + image_filename + "production" + ".png")

                # Create Screenshot
                try:
                    driver.execute_script("""var l = document.getElementsByClassName("ol-zoom ol-unselectable ol-control")[0];
                               l.parentNode.removeChild(l);""")
                except:
                    pass

                mapElement = driver.find_element(By.XPATH,
                                                     "//div[@id='map']//div[@class='ol-viewport']")
                location = mapElement.location
                size = mapElement.size
                x = location["x"]
                y = 43  # location["y"]
                w = x + size["width"]
                h = y + size["height"]
                area = (x, y, w, h)
                time.sleep(1)
                driver.save_screenshot("screenshots/" + image_filename + "map" + ".png")
                time.sleep(0.2)
                Image.open("screenshots/" + image_filename + "map" + ".png").crop(area).save("screenshots/" + image_filename + "map" + ".png")

                #take Screenshot 2
                chartElement = driver.find_element(By.ID, "chart")
                actions = ActionChains(driver)
                actions.move_to_element(chartElement).perform()
                location = chartElement.location
                size = chartElement.size
                x = 920
                y = 1000
                w = 1600
                h = 1300
                area = (x, y, w, h)
                print("X: " + str(x) + "Y: "+ str(y) + "W: "+ str(w) + "H: " + str(h))

                time.sleep(1)
                driver.save_screenshot("screenshots/" + image_filename + "production" + ".png")
                time.sleep(0.2)
                Image.open("screenshots/" + image_filename + "production" + ".png").crop(area).save("screenshots/" + image_filename  + "production" + ".png")


                print("stop")


                print(image_filename + " was saved.")
            else:
                print("not found: " + search_string)
        if(input("Enter zum fortfahren") == "exit"):
            break
except Exception as e:
    print(str(e))
driver.quit()