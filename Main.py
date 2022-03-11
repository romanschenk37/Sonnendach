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
file_split_char = ","


def search_adresses(adress_list, filename_adresslist, driver):
    global file_split_char
    global stopThread
    columnIndex1 = getColumnIndex(variabledropdown1.get())
    columnIndex2 = getColumnIndex(variabledropdown2.get())
    columnIndex3 = getColumnIndex(variabledropdown3.get())
    columnIndex4 = getColumnIndex(variabledropdown4.get())
    columnIndex5 = getColumnIndex(variabledropdown5.get())
    columnIndex6 = getColumnIndex(variabledropdown6.get())
    columnIndex7 = getColumnIndex(variabledropdown7.get())
    columnIndex8 = getColumnIndex(variabledropdown8.get())
    columnIndex9 = getColumnIndex(variabledropdown9.get())
    columnIndex10 = getColumnIndex(variabledropdown10.get())
    columnIndex11 = getColumnIndex(variabledropdown11.get())

    for i in range(len(adress_list)):
        line = adress_list[i]
        adress = line.split(file_split_char)
        if((line != adress_list[0]) & ((adress[20][0:11] != "screenshots"))):
            print(adress)
            search_string = adress[columnIndex1] + " " + adress[columnIndex2] + " " + adress[columnIndex3] + " " + adress[columnIndex4]
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

                adress[columnIndex5] = url
                adress[columnIndex6] = eignung.text
                adress[columnIndex7] = image_filename

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
    for header in headers:
        OptionList.append(header)
    desctext = tkinter.Label(frameFileColums, text="Please type in Header of Columns")
    desctext.grid(row=1, column=1, padx=10, pady=3)
    frameFileColums1 = tkinter.Frame(frameFileColums)
    frameFileColums1.grid(row=2, column=1, padx=10, pady=3)

    text1 = tkinter.Label(frameFileColums1, text="Street: ")
    text1.grid(row=1, column=1, padx=10, pady=3)
    dropdown1 = tkinter.OptionMenu(frameFileColums1, variabledropdown1, *OptionList)
    dropdown1.grid(row=1, column=2, padx=10, pady=3)

    text2 = tkinter.Label(frameFileColums1, text="Number: ")
    text2.grid(row=2, column=1, padx=10, pady=3)
    dropdown2 = tkinter.OptionMenu(frameFileColums1, variabledropdown2, *OptionList)
    dropdown2.grid(row=2, column=2, padx=10, pady=3)

    text3 = tkinter.Label(frameFileColums1, text="Postal code: ")
    text3.grid(row=3, column=1, padx=10, pady=3)
    dropdown3 = tkinter.OptionMenu(frameFileColums1, variabledropdown3, *OptionList)
    dropdown3.grid(row=3, column=2, padx=10, pady=3)

    text4 = tkinter.Label(frameFileColums1, text="City: ")
    text4.grid(row=4, column=1, padx=10, pady=3)
    dropdown4 = tkinter.OptionMenu(frameFileColums1, variabledropdown4, *OptionList)
    dropdown4.grid(row=4, column=2, padx=10, pady=3)

    text5 = tkinter.Label(frameFileColums1, text="Sonnendach URL: ")
    text5.grid(row=5, column=1, padx=10, pady=3)
    dropdown5 = tkinter.OptionMenu(frameFileColums1, variabledropdown5, *OptionList)
    dropdown5.grid(row=5, column=2, padx=10, pady=3)

    text6 = tkinter.Label(frameFileColums1, text="Eignung")
    text6.grid(row=6, column=1, padx=10, pady=3)
    dropdown6 = tkinter.OptionMenu(frameFileColums1, variabledropdown6, *OptionList)
    dropdown6.grid(row=6, column=2, padx=10, pady=3)

    text7 = tkinter.Label(frameFileColums1, text="Screenshot Filename: ")
    text7.grid(row=7, column=1, padx=10, pady=3)
    dropdown7 = tkinter.OptionMenu(frameFileColums1, variabledropdown7, *OptionList)
    dropdown7.grid(row=7, column=2, padx=10, pady=3)


def getColumnIndex(header):
    global OptionList
    for i in range(len(OptionList)):
        if(OptionList[i] == header):
            return i

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
variabledropdown1 = tkinter.StringVar(root)
variabledropdown2 = tkinter.StringVar(root)
variabledropdown3 = tkinter.StringVar(root)
variabledropdown4 = tkinter.StringVar(root)
variabledropdown5 = tkinter.StringVar(root)
variabledropdown6 = tkinter.StringVar(root)
variabledropdown7 = tkinter.StringVar(root)
variabledropdown8 = tkinter.StringVar(root)
variabledropdown9 = tkinter.StringVar(root)
variabledropdown10 = tkinter.StringVar(root)
variabledropdown11 = tkinter.StringVar(root)

frameButtons = tkinter.Frame(root)
frameButtons.grid(row=3, column=1)
button1 = tkinter.Button(frameButtons, text="Select Adresslist file", command=command, width=20, height=2, bg="#FCCA03")
button1.grid(row=3, column=1, padx=10, pady=3)
button2 = tkinter.Button(frameButtons, text="EXIT", command=command_exit, width=20, height=2, bg="#FCCA03")
button2.grid(row=3, column=2, padx=10, pady=3)
root.mainloop()


