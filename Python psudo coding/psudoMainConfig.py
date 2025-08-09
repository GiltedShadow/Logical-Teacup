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
#-SQL- will be easier to reference specific cells and changes (i think, workaround is to recreate the csv file)
#DuckDB, SQLite

#######################

import csv
import sqlite3
import os
import logging

fileVersion = 0.1

userPresetsFile = "UserPresets.csv"
plantsFile = "plantList.csv"
databaseFile = "test.db"

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
        case 'help'|'h':
            return help_text()
        case 'version'|'v':
            return print(fileVersion)
        case 'file check'|'f':
            return file_check()
        case 'settings'|'user'|'s':
            return user_settings()
        case 'plants'|'plant'|'p':
            return plant_settings()
        case 'admin'|'a':
            return whoops()
        # case 'add plant':
        #     return whoops()
        case default:
            return power_down()
        

def help_text():
    print("""
While in any specific area q or quit should allow you to return to the main menu
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
    for file in (userPresetsFile, plantsFile, databaseFile):
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
    if (userPrefList == []):
        print("Empty file! Lets fill that")
    else:
        print(userPrefList)
        prompt = input("do you want to overwrite these values?  y/n\n>>")
        if (prompt != 'y' or prompt != 'yes'):
            return
    for field in userFieldnames:
        userReseponses.append(input(field + "?\n>>"))
    logging.debug("User settings set to " + userReseponses)
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

    pull_plant_list()
    for plant in plantListList:
        print(plant)
    print("Do you want to add, adjust, or delete plants in the list?")
    match input(">>"):
        case 'add':

            active=True
            while active:
                for item in plantFieldnames:
                    userResponse = input(item + "?\n>>")
                    if userResponse == 'q' or userResponse == 'quit':
                        active=False
                        if len(plantResponses)<6:return
                        break
                    plantResponses.append(userResponse)

                with open(plantsFile, 'a', newline='') as csvfile:
                    if len(plantResponses)<6:return
                    plantWriter = csv.DictWriter(csvfile, fieldnames=plantFieldnames)
                    plantWriter.writerow({'Plant':plantResponses[0], 'Placement':plantResponses[1], 
                            'Pot Style':plantResponses[2],'Moisture':plantResponses[3], 
                            'Temperature':plantResponses[4], 'Humidity':plantResponses[5]})
                    print("plant added")
                    logging.debug("Plant added >> " + plantResponses)
                    plantResponses.clear()
            #0'plant', 1'placement', 2'pot style', 3'moisture', 4'temperature', 5'humidity'
    
        case 'adjust'|'adj':
            #TODO add adjuster for specific plants within the plantlistlist so user can pull that plant and add additional/ changed information
            # probably in a while active loop so all changes can be made 
            # TODO make sure everything works here
            #this function is dangerous to time management - this would likely be the sole cause to move to SQL for larger numbers of plants
            active=True
            while active:
                pull_plant_list()
                count=0
                for plant in plantListList:
                    print(str(count) + '--' + str(plant))
                    count+=1
                plantToModify = input("Which plant do you want to adjust?\n>>")
                if plantToModify == 'q' or plantToModify == 'quit':
                        active=False
                        return
                try:
                    len(plantToModify)
                except:
                    logging.warning("Attempted to enter a non int non quit value to adjust plants, entry " + plantToModify + ", continuing")
                    continue

                for item in plantFieldnames:
                    userResponse = input(item + "?\n>>")
                    if userResponse == 'q' or userResponse == 'quit':
                        active=False
                        if len(plantResponses)<6:return
                        break
                    plantResponses.append(userResponse)
                logging.debug(str(plantListList[int(plantToModify)]) + " adjusted to " + str(plantResponses))
                print(plantResponses)
                for plant in plantListList:
                    print(plant)
                input("press any key to continue")
                plantListList[int(plantToModify)] = plantResponses
                for plant in plantListList:
                    print(plant)
                with open(plantsFile, 'w', newline='') as csvfile:
                        plantOverwriter = csv.DictWriter(csvfile, fieldnames=plantFieldnames)
                        plantOverwriter.writeheader
                for row in plantListList:
                        with open(plantsFile, 'a', newline='') as csvfile:
                            plantWriter = csv.DictWriter(csvfile, fieldnames=plantFieldnames)
                            plantWriter.writerow({'Plant':row[0], 'Placement':row[1], 
                            'Pot Style':row[2],'Moisture':row[3], 
                            'Temperature':row[4], 'Humidity':row[5]})
                        # print({'Plant':row[0], 'Placement':row[1], 
                        #     'Pot Style':row[2],'Moisture':row[3], 
                        #     'Temperature':row[4], 'Humidity':row[5]})
            #0'plant', 1'placement', 2'pot style', 3'moisture', 4'temperature', 5'humidity'
                        print("Plants adjusted")
                        plantResponses.clear()
            
            return print("plants adjusted") #overwrite whole file with adjusted information
        
        case 'delete'|'del'|'d':
            #TODO confirm functionality of delete and active loop
            active=True
            while active:
                pull_plant_list()
                count=0
                for plant in plantListList:
                    print(str(count) + '--' + str(plant))
                    count+=1
                plantToModify = input("Which plant do you want to delete?\n>>")
                if plantToModify == 'q' or plantToModify == 'quit':
                        active=False
                        return
                try:
                    len(plantToModify)
                except:
                    logging.warning("Attempted to enter a non int non quit value to delete plants, entry " + plantToModify + ", continuing")
                    continue
                logging.debug(str(plantListList[int(plantToModify)]) + " deleted")
                plantListList.pop(int(plantToModify))
                with open(plantsFile, 'w', newline='') as csvfile:
                        plantOverwriter = csv.DictWriter(csvfile, fieldnames=plantFieldnames)
                        plantOverwriter.writeheader
                for row in plantListList:
                        with open(plantsFile, 'a', newline='') as csvfile:
                            plantWriter = csv.DictWriter(csvfile, fieldnames=plantFieldnames)
                            plantWriter.writerow({'Plant':row[0], 'Placement':row[1], 
                            'Pot Style':row[2],'Moisture':row[3], 
                            'Temperature':row[4], 'Humidity':row[5]})
                plantResponses.clear()

        case default:
            return
    

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