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
from selenium.webdriver.common.action_chains import ActionChains

DropDownLabels = ["Street: ", "Number: ", "Postal code: ", "City: ", "Sonnendach URL: ", "Eignung", "Image Filename Map: ", "Image Filename Production: ", "Image Filename qrcode: ", "PV Production 50", "PV Production 75", "PV Production 100", "Value Electricity production"]
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
        if((line != adress_list[0]) & ((adress[columnIndexes[4]] == ""))):
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
                time.sleep(2)
                # TODO: Validation
                url = driver.current_url
                eignung = driver.find_element(By.ID, "eignung").text
                pv_Production50 = driver.find_element(By.ID, "pv50").text.replace("'", "")
                pv_Production75 = driver.find_element(By.ID, "pv75").text.replace("'", "")
                pv_Production100 = driver.find_element(By.ID, "pv100").text.replace("'", "")
                value_electricity_production = driver.find_elements(By.XPATH, "//h2[@id='TitelSolarstrom']//strong")[2].text.replace("'", "").replace(" Franken", "")


                image_filename = eignung + " - " + search_string
                image_folder_map = "screenshots/"
                image_filename_map = image_filename + " map" + ".png"
                image_folder_production = "screenshots/"
                image_filename_production = image_filename + " production" + ".png"
                image_folder_qrcode = "qrcodes/"
                image_filename_qrcode = image_filename + " qrcode" + ".png"

                # Create QR-Code
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(url)
                qr.make(fit=True)
                qr.make_image(fill='black', back_color='white').save(image_folder_qrcode + image_filename_qrcode)

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
                driver.save_screenshot(image_folder_map + image_filename_map)
                time.sleep(0.2)
                Image.open(image_folder_map + image_filename_map).crop(area).save(
                    image_folder_map + image_filename_map)

                # take Screenshot 2
                try:
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
                    print("X: " + str(x) + "Y: " + str(y) + "W: " + str(w) + "H: " + str(h))

                    time.sleep(1)
                    driver.save_screenshot(image_folder_production + image_filename_production)
                    time.sleep(0.2)
                    Image.open(image_folder_production + image_filename_production).crop(area).save(
                        image_folder_production + image_filename_production)
                except:
                    image_filename_production = "not-found"

                print(image_filename_map + " was saved.")
            else:
                url = "not-found"
                eignung = "not-found"
                image_filename_map = "not-found"
                image_filename_production = "not-found"
                image_filename_qrcode = "not-found"
                pv_Production50 = "not-found"
                pv_Production75 = "not-found"
                pv_Production100 = "not-found"
                value_electricity_production = "not-found"


                print("not found: " + search_string)


            #Write back into file
            adress[columnIndexes[4]] = url
            adress[columnIndexes[5]] = eignung
            adress[columnIndexes[6]] = image_filename_map
            adress[columnIndexes[7]] = image_filename_production
            adress[columnIndexes[8]] = image_filename_qrcode
            adress[columnIndexes[9]] = pv_Production50
            adress[columnIndexes[10]] = pv_Production75
            adress[columnIndexes[11]] = pv_Production100
            adress[columnIndexes[12]] = value_electricity_production
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
root.protocol("WM_DELETE_WINDOW", command_exit)
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


