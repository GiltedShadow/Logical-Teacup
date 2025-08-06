"""
Python 3.13
Created by Alex Norment
On 8/1/25

Will be diving into tkinter and creating a psudo version of the greenhouse code
    in order to get the basic functions down and see what i need with what is
    planned
    
this file will be used to dive into functionality before stuffing it
    into tkinter
    
"""

"""
Things that this needs to do:
:outputs needed
- watering
- air circulation
- humidity control
- temp control
- tracking what is planted

:inputs needed
- watering
-- moisture sensor per pot/ avg across pots for large pots
-- time?

- air circulation
-- needs to be controlled by inputs for huidity and temp

- humidity control
-- humidity sensor

- temp control
-- temp sensor

- tracking what is planted
-- user input, .csv file to keep tack

:extra
- some form of updates (email, etc)
"""
#######################
## Second
# Watering

# take into account the plants, basic stats as well as
#   which spots are filled

# Based off of moisture of each sensor, begin watering

# Based off of time and moisture, if watering is not raising moisture
#   throw error

#######################
## Third
# Air Circ

# take into account temp and humidity

# Based off of temp, humidity, and preferences set by user
#   run fan until temp and humidity are within preferences
#   -or- temp or humidity reach low end
#   temp is more important than humidity, eg
#       if temp is at max and humidity is at min, run fan until temp is corrected

#######################
## MOST IMPORTANT, do first
# Plant tracking and user input information

# Take into account user input information

# .csv file to start, possible SQL (is SQL needed at all?)

#######################

import csv
import os
import logging

fileVersion = 0.1

userPresetsFile = "UserPresets.csv"
plantsFile = "plantList.csv"

userFieldnames = ['Name', 'Watering Style', 'Ventilation', 'Panels', 'Frame']
userReseponses = []
plantFieldnames = ['Plant', 'Placement', 'Pot Style', 'Moisture' ,'Temperature', 'Humidity']
plantResponses = []

userPrefList = []
plantListList = []

introText = r"""
   ___       __          _____                     __ __                 
  / _ |__ __/ /____     / ___/______ ___ ___      / // /__  __ _____ ___ 
 / __ / // / __/ _ \   / (_ / __/ -_) -_) _ \    / _  / _ \/ // (_-</ -_)
/_/ |_\_,_/\__/\___/   \___/_/  \__/\__/_//_/   /_//_/\___/\_,_/___/\__/ """

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename="testLogging.log", level=logging.NOTSET, format=FORMAT)


#User interface
def userInterface(userInput):
    match userInput.lower():
        case 'help':
            return help_text()
        case 'version':
            return print(fileVersion)
        case 'file check':
            return file_check()
        case 'settings':
            return user_settings()
        case 'plants':
            return plant_settings()
        # case 'add plant':
        #     return whoops()
        case default:
            return power_down()
        

def help_text():
    print("""
help ------- list commands
version ---- will print out the file version
file check - will search for files and will create them if not found
settings --- checks current user preferences and sets them
plants ----- checks current plant list and allows new/ changed entries
""")

def whoops():
    print("not created yet!")

def power_down():
    prompt = input("Quit?   y/n\n>>")
    if (prompt.lower() == 'y' or prompt.lower() == 'yes'):
        logging.info("user closing program")
        exit()

def file_check():
    for file in (userPresetsFile, plantsFile):
        try:
            open(file, "x")
            logging.warning(file + " created and header added, file not found or first time running software")
            print(file + " created - first time opening software")
            if (file == userPresetsFile):
                with open(file, 'w', newline = '') as csvfile:
                    opener = csv.DictWriter(csvfile, fieldnames=userFieldnames)
                    opener.writeheader()
            elif (file == plantsFile):
                with open(file, 'w', newline = '') as csvfile:
                    opener = csv.DictWriter(csvfile, fieldnames=plantFieldnames)
                    opener.writeheader()
        except:
            logging.info(file + " found")
            print(file + " found")

def user_settings():
    # commented out as program will read the file at start and fill out a list
    ########################################################
    # try:
    #     with open(userPresetsFile, 'r', newline='') as csvfile:
    #         print("csv opened")
    #         logging.info("user preferences successfully read")
    #         numRows = 0
    #         reader = csv.DictReader(csvfile)
    #         for row in reader:
    #             print(row)
    #             if (row==['Name', 'Watering Style', 'Ventilation', 'Panels', 'Frame']):
    #                 print("Empty file! Lets fill that")
    #                 #interesting here, this does not pull at all with just the header
    #                 #not even if the user deletes their settings manually
    #                 logging.warning("empty file found with just a header for user preferences")
    #             numRows +=1
    #         if (numRows == 0):
    #             print("Empty file! Lets fill that")
    #             logging.warning("completely empty file found for user preferences")
    #         else:
    #             prompt = input("do you want to overwrite these values?  y/n\n>>")
    #             if (prompt == "n" or prompt =="no"):
    #                 return
    # except FileNotFoundError:
    #     logging.warning("user preferences file not found, attempting to create/ find both files")
    #     file_check()
    #     print("Empty file! Lets fill that")
    # except:
    #     logging.error(str(Exception) + " found when attempting to read user presets file")
    #     print(str(Exception) + " found, check log files")
    #     return
    ########################################################
    if (userPrefList == []):
        print("Empty file! Lets fill that")
    else:
        print(userPrefList)
        prompt = input("do you want to overwrite these values?  y/n\n>>")
        if (prompt != 'y' or prompt != 'yes'):
            return
    for field in userFieldnames:
        userReseponses.append(input(field + "?\n>>"))
    logging.debug(userReseponses)
    with open(userPresetsFile, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=userFieldnames)
        writer.writeheader()
        writer.writerow({'Name':userReseponses[0], 'Watering Style':userReseponses[1], 
                         'Ventilation':userReseponses[2],'Panels':userReseponses[3], 
                         'Frame':userReseponses[4]})

        #['Name', 'Watering Style', 'Ventilation', 'Panels', 'Frame']
    userReseponses.clear()
    pull_user_prefrences()

def plant_settings():
    #might want to have the original creation of the file autoamtically call the user settings input
    #---creation of the file will now add the column names, 

    #TODO rewrite this and the user section to adjust
    # or something that will force at least one line to be printed so the try catch below to be simpler
    # try:
    #     with open(plantsFile, 'r', newline='') as csvfile:
    #         print("csv opened")
    #         logging.info("user preferences successfully read")
    #         numRows = 0
    #         reader = csv.DictReader(csvfile)
    #         for row in reader:
    #             print(row)
    #             if (row==[]):
    #                 print("Empty file! Lets fill that")
    #                 logging.warning("empty file found for plants list")
    #             numRows +=1
    #         if (numRows == 0):
    #             print("Empty file! Lets fill that")
    #             logging.warning("empty file found for plants list")
    # except FileNotFoundError:
    #     logging.warning("user preferences file not found, attempting to create/ find both files")
    #     file_check()
    #     print("Empty file! Lets fill that")
    # except:
    #     logging.error(str(Exception) + " found when attempting to read user presets file")
    #     print(str(Exception) + " found, check log files")
    #     return
    for plant in plantListList:
        print(plant)
    print("Do you want to add or adjust the list?")
    match input(">>"):
        case 'add':
            for item in plantFieldnames:
                plantResponses.append(input(item + "?\n>>"))
            with open(plantsFile, 'a', newline='') as csvfile:
                plantWriter = csv.DictWriter(csvfile, fieldnames=plantFieldnames)
                plantWriter.writerow({'Plant':plantResponses[0], 'Placement':plantResponses[1], 
                         'Pot Style':plantResponses[2],'Moisture':plantResponses[3], 
                         'Temperature':plantResponses[4], 'Humidity':plantResponses[5]})

            plantResponses.clear()
            pull_plant_list()
            return print("plant added") #append
            #should this just be within this definition? like the only way to interact with the plants is within the plants command
        case 'adjust':
            plantResponses.clear()
            return print("plants adjusted") #overwrite whole file with adjusted information
        case default:
            return
    #0'plant', 1'placement', 2'pot style', 3'moisture', 4'temperature', 5'humidity'

def pull_plant_list():
    plantListList.clear()
    with open(plantsFile, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            plantListList.append(row)

def pull_user_prefrences():
    userPrefList.clear()
    with open(userPresetsFile, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            userPrefList.append(row)

print(introText)
logging.info("starting program")
file_check()
pull_plant_list()
pull_user_prefrences()
print(userPrefList)
for row in plantListList:
    print(row)
while(True):
    # main menu!
    #should add the user settings and plant list when user logs in, this should make the try catch loops much easier

    print("\nreturning to start, type help for command list")
    userInterface(input(">>"))