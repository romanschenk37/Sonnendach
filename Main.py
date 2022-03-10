import tkinter
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image

from tkinter import filedialog
import time




exit = False
stopThread = False
filename_adresslist = ""
adresslist = ""
step = 0
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.minimize_window()
outputtext = "Welcome to application Sonnendach\n"

def search_adresses(adress_list, filename_adresslist, driver):
    file_split_char = ","
    global exit
    for i in range(len(adress_list)):
        line = adress_list[i]
        adress = line.split(file_split_char)
        if((line != adress_list[0]) & ((adress[20][0:11] != "screenshots"))):
            print(adress)
            search_string = adress[15] + " " + adress[3] + " " + adress[11] + " " + adress[13]
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

        if(stopThread == True):
            print("Exit")
            break


def read_adresslist(filename_adresslist):
    returnvalues = []
    try:
        adress_file = open(filename_adresslist, "r")
        adress_list = adress_file.read().splitlines()
        adress_file.close()
        returnvalues.append(True)
        returnvalues.append(adress_list)
    except:
        returnvalues.append(False)
    return returnvalues

def command():
    global exit
    global stopThread
    global adresslist
    global step
    global driver
    global filename_adresslist
    global outputtext
    global thread_search_adresses
    if(exit):
        stopThread = True
        outputtext = outputtext + "Application will stop" + "\n"
        text1.config(text=outputtext)
        thread_search_adresses.join()
        root.quit()
        driver.quit()
    elif(step == 0):
        #Schritt 1
        filename_adresslist = filedialog.askopenfilename()
        outputtext = outputtext + "Reading File " + filename_adresslist + "\n"
        text1.config(text=outputtext)
        adress_list_result = read_adresslist(filename_adresslist)
        if(adress_list_result):
            adresslist = adress_list_result[1]
            outputtext = outputtext + "Reading file " + filename_adresslist + " done." + "\n"
            text1.config(text=outputtext)
            button1.config(text="open Webbrowser")
            step += 1
        else:
            outputtext = outputtext + "Reading file " + filename_adresslist + " failed." + "\n"
            text1.config(text=outputtext)
            exit = True
            button1.grid_remove()
    elif(step == 1):
        # Schritt 2
        outputtext = outputtext + "Website is opening" + "\n"
        text1.config(text=outputtext)
        try:
            driver.maximize_window()
            driver.get("https://www.uvek-gis.admin.ch/BFE/sonnendach/")
            driver.implicitly_wait(20)
            outputtext = outputtext + "opening website was done.\nPrepare the browser window to create screenshots." + "\n"
            text1.config(text=outputtext)
            button1.config(text="start process")
            step += 1
        except:
            outputtext = outputtext + "opening website failed" + "\n"
            text1.config(text=outputtext)
            exit = True
            button1.grid_remove()
    elif(step == 2):
        thread_search_adresses = threading.Thread(target=search_adresses, args=(adresslist, filename_adresslist, driver))
        thread_search_adresses.start()
        #search_adresses(adresslist, filename_adresslist, driver)
        outputtext = outputtext + "process running." + "\n"
        text1.config(text=outputtext)
        button1.grid_remove()
        exit = True

def command_exit():
    exit = True
    command()




root = tkinter.Tk()
root.wm_title("Sonnendach")
text1 = tkinter.Label(root, text=outputtext, width=80, height=30)
text1.grid(row=1, column=1, padx=10, pady=3)
button1 = tkinter.Button(root, text="Select Adresslist file", command=command, width=20, height=2, bg="#FCCA03")
button1.grid(row=2, column=1, padx=10, pady=3)
button2 = tkinter.Button(root, text="EXIT", command=command_exit, width=20, height=2, bg="#FCCA03")
button2.grid(row=2, column=2, padx=10, pady=3)
root.mainloop()


