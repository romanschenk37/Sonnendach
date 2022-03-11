import tkinter
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
import os
import qrcode
from tkinter import filedialog
import time


DropDownLabels = ["Street: ", "Number: ", "Postal code: ", "City: ", "Sonnendach URL: ", "Eignung", "Image Filename: ", "PV Production 50", "PV Production 75", "PV Production 100", "Value Electricity production"]
file_split_char = ","
OptionList = []
exit = False
stopThread = False
filename_adresslist = ""
adresslist = ""
step = 0
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.minimize_window()
outputtext = "Welcome to application Sonnendach\n"
columnIndexes = []



def search_adresses(adress_list, filename_adresslist, driver):
    global file_split_char
    global stopThread
    global columnIndexes

    if(not os.path.exists("screenshots")):
        os.makedirs("screenshots", exist_ok=False)
    if (not os.path.exists("qrcodes")):
        os.makedirs("qrcodes", exist_ok=False)

    for i in range(len(adress_list)):
        line = adress_list[i]
        adress = line.split(file_split_char)
        if((line != adress_list[0]) & ((adress[20][0:11] != "screenshots"))):
            print(adress)
            search_string = adress[columnIndexes[0]] + " " + adress[columnIndexes[1]] + " " + adress[columnIndexes[2]] + " " + adress[columnIndexes[3]]
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
                    driver.implicitly_wait(10)
                    break

            if(found):
                # TODO: Validation
                url = driver.current_url
                eignung = driver.find_element(By.ID, "eignung")
                pv_Production50 = driver.find_element(By.ID, "pv50")
                pv_Production75 = driver.find_element(By.ID, "pv75")
                pv_Production100 = driver.find_element(By.ID, "pv100")
                value_electricity_production = driver.find_elements(By.XPATH, "//h2[@id='TitelSolarstrom']//strong")[2]

                image_filename = eignung.text + " - " + search_string + ".png"

                adress[columnIndexes[4]] = url
                adress[columnIndexes[5]] = eignung.text
                adress[columnIndexes[6]] = image_filename
                # TODO: 1000er Trennzeichen und " Franken" entfernen
                adress[columnIndexes[7]] = pv_Production50.text.replace("'", "")
                adress[columnIndexes[8]] = pv_Production75.text.replace("'", "")
                adress[columnIndexes[9]] = pv_Production100.text.replace("'", "")
                adress[columnIndexes[10]] = value_electricity_production.text.replace("'", "").replace(" Franken", "")




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

                # Create QR-Code
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(url)
                qr.make(fit=True)
                qr.make_image(fill='black', back_color='white').save("qrcodes/" + image_filename)

                #Create Screenshot
                featureElement = driver.find_element(By.XPATH, "//section[@id='one']//div[@class='container']//div[@class='row 150%']")
                location = featureElement.location
                size = featureElement.size
                x = location["x"]
                y = 0  # location["y"]
                w = x + size["width"]
                h = y + size["height"] - 100
                area = (x, y, w, h)
                time.sleep(2)
                driver.save_screenshot("screenshots/" + image_filename)
                time.sleep(0.2)
                Image.open("screenshots/" + image_filename).crop(area).save("screenshots/" + image_filename)



                print(image_filename + " was saved.")
            else:
                print("not found: " + search_string)
        if(stopThread == True):
            print("closing Thread")
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

def createFrameFileColums(headers):
    global OptionList
    global DropDownLabels
    for header in headers:
        OptionList.append(header)
    desctext = tkinter.Label(frameFileColums, text="Please select Headers of Columns")
    desctext.grid(row=1, column=1, padx=10, pady=3)
    frameFileColums1 = tkinter.Frame(frameFileColums)
    frameFileColums1.grid(row=2, column=1, padx=10, pady=3)

    for i in range(len(DropDownLabels)):
        exec("text" + str(i+1) + " = tkinter.Label(frameFileColums1, text=\"" + DropDownLabels[i] + "\")")
        exec("text" + str(i+1) + ".grid(row=" + str(i+1) + ", column=1, padx=10, pady=3)")
        exec("dropdown" + str(i+1) + " = tkinter.OptionMenu(frameFileColums1, variablesDropdown[" + str(i) + "], *OptionList)")
        exec("dropdown" + str(i+1) + ".grid(row=" + str(i+1) + ", column=2, padx=10, pady=3)")

def getColumnIndex():
    global OptionList
    global columnIndexes
    for j in range(len(DropDownLabels)):
        for i in range(len(OptionList)):
            if(OptionList[i] == variablesDropdown[j].get()):
                columnIndexes.append(i)

def command():
    global exit
    global stopThread
    global adresslist
    global step
    global driver
    global filename_adresslist
    global outputtext
    global thread_search_adresses
    global file_split_char
    if(exit):
        print("Command Exit received")
        stopThread = True
        try:
            thread_search_adresses.join()
        except:
            pass
        print("Thread is closed")
        root.quit()
        print("Application is closed")
        driver.quit()
        print("Webdriver is closed")
    elif(step == 0):
        #Schritt 1
        filename_adresslist = filedialog.askopenfilename()
        outputtext = outputtext + "Searching File " + filename_adresslist + "\n"
        mainText.config(text=outputtext)
        adress_list_result = read_adresslist(filename_adresslist)
        if(adress_list_result):
            adresslist = adress_list_result[1]
            outputtext = outputtext + "File " + filename_adresslist + " found." + "\n"
            mainText.config(text=outputtext)
            button1.config(text="read file")
            createFrameFileColums(adresslist[0].split(file_split_char))
            frameFileColums.grid(row=2, column=1)
            step += 1
        else:
            outputtext = outputtext + "File " + filename_adresslist + " not found." + "\n"
            mainText.config(text=outputtext)
            exit = True
            button1.grid_remove()
    elif (step == 1):
        # TODO: check if dropdowns are selected
        getColumnIndex()
        outputtext = outputtext + "Reading File " + filename_adresslist + " done." + "\n"
        mainText.config(text=outputtext)
        frameFileColums.grid_remove()
        button1.config(text="open Webbrowser")
        step += 1
    elif(step == 2):
        # Schritt 2
        outputtext = outputtext + "Website is opening" + "\n"
        mainText.config(text=outputtext)
        try:
            driver.maximize_window()
            driver.get("https://www.uvek-gis.admin.ch/BFE/sonnendach/")
            driver.implicitly_wait(20)
            outputtext = outputtext + "opening website was done.\nPrepare the browser window to create screenshots." + "\n"
            mainText.config(text=outputtext)
            button1.config(text="start process")
            step += 1
        except:
            outputtext = outputtext + "opening website failed" + "\n"
            mainText.config(text=outputtext)
            exit = True
            button1.grid_remove()
    elif(step == 3):
        thread_search_adresses = threading.Thread(target=search_adresses, args=(adresslist, filename_adresslist, driver))
        thread_search_adresses.start()
        print("Thread started")
        outputtext = outputtext + "process running." + "\n"
        mainText.config(text=outputtext)
        button1.grid_remove()
        exit = True

def command_exit():
    global exit
    exit = True
    command()




root = tkinter.Tk()
root.wm_title("Sonnendach")
mainText = tkinter.Label(root, text=outputtext, width=80)
mainText.grid(row=1, column=1, padx=10, pady=3)

frameFileColums = tkinter.Frame(root)
variablesDropdown = []
for i in range(len(DropDownLabels)):
    variablesDropdown.append(tkinter.StringVar(root))


frameButtons = tkinter.Frame(root)
frameButtons.grid(row=3, column=1)
button1 = tkinter.Button(frameButtons, text="Select Adresslist file", command=command, width=20, height=2, bg="#FCCA03")
button1.grid(row=3, column=1, padx=10, pady=3)
button2 = tkinter.Button(frameButtons, text="EXIT", command=command_exit, width=20, height=2, bg="#FCCA03")
button2.grid(row=3, column=2, padx=10, pady=3)
root.mainloop()


