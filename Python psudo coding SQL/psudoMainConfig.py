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
a#TODO change all csv changes and files to sqlite
import csv
import sqlite3
import os
import logging

fileVersion = 0.2
# 0.1 added full functionality of the plant tracking and user information based off of .csv files
# 0.2 adding watering function based off of information input by the user
# 0.3 adding air control based off of information input by the user and external temperature & humidity readings


######################################################################################
#Stage one - user information storage
######################################################################################
userPresetsFile = "UserPresets.csv" #FIXME
plantsFile = "plantList.csv" #FIXME
databaseFile = "test.db"

userFieldnames = ['Name', 'Spots Available', 'Watering Style', 'Ventilation', 'Panels', 'Frame']
userReseponses = []
plantFieldnames = ['Plant', 'Placement', 'Pot Style', 'Moisture' ,'Temperature', 'Humidity']
plantResponses = []

userPrefList = []
plantListList = []

appSettings = {'Spots Available':0, 'Watering Style':'', 'Ventilation':''}

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

def file_check(): #FIXME
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

def user_settings(): #FIXME
    if (userPrefList == []):
        print("Empty file! Lets fill that")
    else:
        print(userPrefList)
        prompt = input("do you want to overwrite these values?  y/n\n>>")
        if (prompt != 'y' and prompt != 'yes'):
            return
    for field in userFieldnames:
        userReseponses.append(input(field + "?\n>>"))
    logging.debug("User settings set to " + str(userReseponses))
    with open(userPresetsFile, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=userFieldnames)
        writer.writeheader()
        writer.writerow({'Name':userReseponses[0], 'Spots Available':userReseponses[1],
                         'Watering Style':userReseponses[2], 'Ventilation':userReseponses[3],
                         'Panels':userReseponses[4], 'Frame':userReseponses[5]})

        #['Name', 'Spots Available', 'Watering Style', 'Ventilation', 'Panels', 'Frame']
    userReseponses.clear()
    pull_user_prefrences()

def plant_settings(): #FIXME
#TODO add a check to make sure that plants are not added to spots above "spots avaialable" found in the user presets file
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

                with open(plantsFile, 'a', newline='') as csvfile: #FIXME
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
                if plantToModify == 0:print("please do not attempt to adjust the column names");continue
                for item in plantFieldnames:
                    userResponse = input(item + "?\n>>")
                    if userResponse == 'q' or userResponse == 'quit':
                        active=False
                        if len(plantResponses)<6:return
                        break
                    plantResponses.append(userResponse)
                logging.debug(str(plantListList[int(plantToModify)]) + " adjusted to " + str(plantResponses))
                print(plantResponses)
                # input("press any key to continue")
                # for plant in plantListList:
                #     print(plant)
                # input("press any key to continue")
                plantListList[int(plantToModify)] = plantResponses
                # for plant in plantListList:
                #     print(plant)
                with open(plantsFile, 'w', newline='') as csvfile: #FIXME
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
                if plantToModify == 0:print("please do not attempt to remove the column names");continue
                logging.debug(str(plantListList[int(plantToModify)]) + " deleted")
                plantListList.pop(int(plantToModify))
                with open(plantsFile, 'w', newline='') as csvfile: #FIXME
                        plantOverwriter = csv.DictWriter(csvfile, fieldnames=plantFieldnames)
                        plantOverwriter.writeheader
                for row in plantListList:
                        with open(plantsFile, 'a', newline='') as csvfile: #FIXME
                            plantWriter = csv.DictWriter(csvfile, fieldnames=plantFieldnames)
                            plantWriter.writerow({'Plant':row[0], 'Placement':row[1], 
                            'Pot Style':row[2],'Moisture':row[3], 
                            'Temperature':row[4], 'Humidity':row[5]})
                plantResponses.clear()

        case default:
            return
    

def pull_plant_list(): #FIXME
    plantListList.clear()
    with open(plantsFile, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            plantListList.append(row)

def pull_user_prefrences(): #FIXME
    userPrefList.clear()
    appSettings['Spots Available'] = 0
    with open(userPresetsFile, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row)
            userPrefList.append(row)
            appSettings['Spots Available'] = int(row['Spots Available'])
            appSettings['Ventilation'] = row['Ventilation']
            appSettings['Watering Style'] = row['Watering Style']
        
######################################################################################
#Stage one - user information storage
######################################################################################

######################################################################################
#Stage two - watering logic
######################################################################################
#arggghhh what do i even do here
#how often should the watering be run?
#   maybe check with user, should be an overall setting or perhaps a per plant setting rather than keeping the plants at a specific moisture
#   to start, plants should be watered once a day
#how will the logic know how much to water
#   there should be a feedback loop here - first is a guess say 30 seconds of watering to start
#   based on the next days reading for the moisture, the water should be adjusted
#   once the moisture reading can be steady at the setting set by the plant list entry, level off
#moisture measurements should be taken hourly? quarterly? user set measurement
#   there should be a way to not have the moisture measurements, like users taking manual measurements
#how will long pots be categorized? should they be 1a, 1b, etc or be classified as separate spots 1, 2, etc
#   these spts should have some form of averaged moisture content 
#TODO take measurements with moisture sensor, water based on a table, log based on plant spot vs moisture at time of watering
#TODO take measurements with moisture sendor, off of the watering schedule to check against drainage, if moisture reads around the requested amount it gets a carrot
#   this should be in between the waterings and should assist with the watering schedule and amount
plantSpotsTurnedOn = []

def turn_on_off_spots():
    #TODO pull plant spots from plant CSV
    pass

def take_moisture():
    #TODO function to take moisture measurements
    # This needs to search for moisture sensors, or for lack of sensors (mostly for this code or for when users do not have them) assume a specific loss based on plant spots
    # this needs to average long pots to one value over multiple sensors with error checing and checks to see if one spot's watering spout is encountering an issue
    for plant in plantSpotsTurnedOn:
        print("moisture collected for " + plant)
    pass



def water_plants():
    #TODO function to use moisture to water
    # this will pull the moisture based on each plant placement (see moisture function) potentially based on history and previous moisture measurements and will water based on time
    pass



def adjust_water():
    #TODO function to use moisture to check water
    # this will pull moisture (see moisture function) and the previous water amount (see water function) to adjust if the time needs to be increased or decreased
    pass


#TODO function to adjust water values based off of first 3
# this may be integrated into the watering functionv
#remember, it is ok to overwater --- but only a little bit, dont kill plants

######################################################################################
#Stage two - watering logic
######################################################################################


######################################################################################
#Stage three - air control logic
######################################################################################
#   
######################################################################################
#Stage three - air control logic
######################################################################################

print(introText)
logging.info("starting program")
file_check()
pull_plant_list()
pull_user_prefrences()
#print(appSettings)
# print(userPrefList)
# for row in plantListList:
#     print(row)
while(True):
    # main menu!
    #should add the user settings and plant list when user logs in, this should make the try catch loops much easier

    print("\nreturning to start, type help for command list")
    userInterface(input(">>"))