#! /usr/bin/env python3
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
#DONE change all csv changes and files to sqlite
import csv
import sqlite3
import os
import logging
import databasePrinter as dbp #EZ DONE either edit this file to pass a table call for print or add that functionality to this file - 
                                # this might be an idea to keep separate but that may be just for the py file
fileVersion = 0.25
# 0.1 addding full functionality of the plant tracking and user information based off of sqlite db
# 0.2 adding watering function based off of information input by the user
# 0.3 adding air control based off of information input by the user and external temperature & humidity readings


######################################################################################
#Stage one - user information storage
######################################################################################
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename="testLogging.log", level=logging.NOTSET, format=FORMAT)

databaseFile = "test.db"

#panels and frame here are kinda useless so far, maybe something about adding it to in a greenhouse or out in the open
# watering style and ventilation will be true/false eg. true turning on automatic logic
userFieldnames = ['Name', 'Spots Available', 'Watering Style: True(1)/False(0)', 'Ventilation: True(1)/False(0)', 'Panels', 'Frame']
userReseponses = []
plantFieldnames = ['Plant Name', 'Placement(int)', 'Placement Modifier(a, b, c, etc)', 'Pot Style', 'Moisture(int)' ,'Temperature(int)', 'Humidity(int)']
plantResponses = []

plantListList = []

# watering style and ventilation will be true(1)/false(0) eg. true turning on automatic logic
appSettings = {'Spots Available':0, 'Watering Style':False, 'Ventilation':False, 'Filled Out':False}

introText = r"""
   ___       __          _____                     __ __                 
  / _ |__ __/ /____     / ___/______ ___ ___      / // /__  __ _____ ___ 
 / __ / // / __/ _ \   / (_ / __/ -_) -_) _ \    / _  / _ \/ // (_-</ -_)
/_/ |_\_,_/\__/\___/   \___/_/  \__/\__/_//_/   /_//_/\___/\_,_/___/\__/ """

#['Plant Name', 'Placement(int)', 'Placement Modifier(a, b, c, etc)', 'Pot Style', 'Moisture(int)' ,'Temperature(int)', 'Humidity(int)']
#                      PK             PK       
sqlStatementCreatePlantTable = """
CREATE TABLE IF NOT EXISTS Plants(
    PlantName VARCHAR NOT NULL,
    Placement INTEGER NOT NULL,
    PlacementModifier VARCHAR NOT NULL,
    PotStyle VARCHAR,
    Moisture INTEGER,
    Temperature INTEGER,
    Humidity INTEGER,
    PRIMARY KEY (Placement, PlacementModifier)
);"""

#['Name', 'Spots Available', 'Watering Style', 'Ventilation', 'Panels', 'Frame']
#  PK
sqlStatementCreateUserTable = """
CREATE TABLE IF NOT EXISTS User_Settings(
    Name VARCHAR NOT NULL,
    SpotsAvailable INTEGER NOT NULL,
    WateringStyle INTEGER CHECK( WateringStyle in ('1', '0')) NOT NULL DEFAULT ('0'),
    Ventilation INTEGER CHECK(Ventilation in ('1', '0')) NOT NULL DEFAULT ('0'),
    Panels VARCAHR,
    Frame VARCHAR,
    PRIMARY KEY (Name)
);"""

# first two columns foreign keys?
# see https://stackoverflow.com/questions/5299267/how-to-create-enum-type-in-sqlite
sqlStatementCreateWorkingPlantTable = """
CREATE TABLE IF NOT EXISTS Plant_Working_Information(
    Placement INTEGER NOT NULL,
    PlacementModifier VARCAHR NOT NULL,
    TimeTaken TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    MoistureReading INTEGER,
    WateringTimer INTEGER,
    PRIMARY KEY (Placement, PlacementModifier, TimeTaken)
);"""

sqlStatementCreateAirconTable = """
CREATE TABLE IF NOT EXISTS Air_Conditioning_Working_Information(
    TimeTaken TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Type VARCHAR CHECK(Type in ("TEMPERATURE","HUMIDITY")) NOT NULL,
    ReadingOrAction VARCHAR CHECK(ReadingOrAction in ("READING","ACTION")) NOT NULL,
    Reading INTEGER,
    Action VARCHAR,
    PRIMARY KEY (TimeTaken, Type, ReadingOrAction)
);"""

sqlStatementSortedPlantsSelect = """
SELECT * FROM Plants
ORDER BY Placement, PlacementModifier"""

plantsTableCheck = 'SELECT * FROM Plants'
userTableCheck = 'SELECT * FROM User_Settings'
workingPlantsTableCheck = 'SELECT * FROM Plant_Working_Information'
airconTableCheck = 'SELECT * FROM Air_Conditioning_Working_Information'

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
            return admin_log_in() #whoops() #DONE log in for admin to cause time to pass and check logic functions
        case 'dbprint'|'db':
            return db_print()
        case 'rt': #TODO move to deleting table or another function
            pass
            # dbConnect("reset table")
            # sqlCursor.execute("DROP TABLE IF EXISTS Plants")
            # sqlCursor.execute(sqlStatementCreatePlantTable)
            # conn.commit()
            # dbDisconnect('reset table')
        case default:
            return power_down()
        
def db_print():
    #DONE change table print to order by specific columns
    # ADDED ability but prints specific table and not the full db
    # either by adding a custom print via databasePrinter.py or by running the select on its own, but then the fancy print would need to be added here
    # add a custom fancy that passes the sql statement
    active=True
    while(active):
        userInput = input("""
1. Full db 
2. plants table
3. user settings table
4. plant backend table
5. aircon backend table 
>>""")
        try:
            int(userInput)
        except:
            print("Please enter a number, quitting to menu")
            return
        match userInput:
            case '1':
                dbp.connect_to_DB(databaseFile)
                dbp.fancy_print_database()
                dbp.disconnect_from_DB()
            case '2':
                dbp.connect_to_DB(databaseFile)
                dbp.fancy_print_custom(sqlStatementSortedPlantsSelect, 'Plants')
                #dbp.fancy_print_table('Plants')
                dbp.disconnect_from_DB()
            case '3':
                dbp.connect_to_DB(databaseFile)
                dbp.fancy_print_table('User_Settings')
                dbp.disconnect_from_DB()
            case '4':
                dbp.connect_to_DB(databaseFile)
                dbp.fancy_print_table('Plant_Working_Information')
                dbp.disconnect_from_DB()
            case '5':
                dbp.connect_to_DB(databaseFile)
                dbp.fancy_print_table('Air_Conditioning_Working_Information')
                dbp.disconnect_from_DB()
            case default:
                active = False
                return

def dbConnect(arg:str):
    global conn
    global sqlCursor
    logging.debug("db connection called - code - " + arg)
    conn = sqlite3.connect(databaseFile)
    if arg=="startup":
        logging.info("db connected to " + databaseFile)
    sqlCursor = conn.cursor()
    
def dbDisconnect(arg:str):
    try:
        logging.debug("db disconnection called - code - " + arg)
        conn.close()
    except:
        logging.warning("db disconnect called when no connection is established - code - " + arg)

def help_text():
    print("""
While in any specific area q or quit should allow you to return to the main menu
help ------- list commands
version ---- will print out the file versionpalce
file check - will search for files and will create them if not found
settings --- checks current user preferences and sets them
plants ----- checks current plant list and allows new/ changed entries
dbprint ---- print out the database or specified table
""")

def whoops():
    print("not created yet!")

def power_down():
    prompt = input("Quit?   y/n\n>>")
    if (prompt.lower() == 'y' or prompt.lower() == 'yes'):
        logging.info("user closing program")
        exit()

def create_all_tables():
    #Am i stupid? these -need- *should be* be run together
    # SQLite is funny where it can only take one statement at a time, so any ; should be followed by the end of the statement and 
    #runs the creation of the table if not found within databaseFile
    sqlCursor.execute(sqlStatementCreatePlantTable)
    logging.debug("plant table created")
    sqlCursor.execute(sqlStatementCreateUserTable)
    logging.debug("user table created")
    sqlCursor.execute(sqlStatementCreateWorkingPlantTable)
    logging.debug("working plant table created")
    sqlCursor.execute(sqlStatementCreateAirconTable)
    logging.debug("aircon table created")

def file_check():
    try:
        open(databaseFile, 'x')
        logging.warning(databaseFile + " created and tables created, db file not found or first time running software")
        print(databaseFile + " created - first time openeing software")
    except:
        logging.info(databaseFile + " found")
        print(databaseFile + "found")

    logging.debug("checking for tables")
    try:
        dbConnect("checking for tables")
        for statement in [plantsTableCheck, userTableCheck, workingPlantsTableCheck, airconTableCheck]:
            logging.debug("Checking " + statement)
            sqlCursor.execute(statement)
        logging.debug("All tables accounted for")
        dbDisconnect("checking for tables")
    except sqlite3.OperationalError:
        logging.debug("creating tables after failed check for tables existing")
        dbConnect("creating tables after failed check")
        create_all_tables()
        dbDisconnect("creating tables after failed check")
    except:
        logging.error("issue happened when attempting to check for tables")
        print("Tables not confirmed")

def user_settings():
    if (appSettings['Filled Out'] == False): #checked without pulling the whole table, not stressing the db even though its quick to access
        print("Empty file! Lets fill that")
    else:
        print(appSettings)
        prompt = input("do you want to overwrite these values?  y/n\n>>")
        if (prompt != 'y' and prompt != 'yes'):
            return
    x=0
    while(x<len(userFieldnames)):
        response = input(userFieldnames[x] + "?\n>>")
        if(x<=3 and response == ''):
            print("Please enter a value, this is a non null entry")
            continue
        if(1<=x<=3):
            try:
                int(response)
            except:
                print("Please enter an integer for this value")
                continue
        userReseponses.append(response)
        x+=1
            
    logging.debug("User settings set to " + str(userReseponses))
    sqlStatementDeleteUserTableInformation = """DELETE FROM User_Settings"""
    sqlStatement = f"""
INSERT INTO User_Settings (Name, SpotsAvailable, WateringStyle, Ventilation, Panels, Frame)
VALUES('{userReseponses[0]}', {userReseponses[1]}, {userReseponses[2]}, {userReseponses[3]}, '{userReseponses[4]}', '{userReseponses[5]}')"""
    dbConnect("inputting information")

    sqlCursor.execute(sqlStatementDeleteUserTableInformation)
    sqlCursor.execute(sqlStatement)
    conn.commit()
    dbDisconnect("inputting information")

        #['Name', 'Spots Available', 'Watering Style', 'Ventilation', 'Panels', 'Frame']
    userReseponses.clear()
    pull_user_prefrences()

def get_plant_input(addOrAdj:str):
    plantResponses.clear()
    x=0
    print("enter q to quit at any time")
    while(x<len(plantFieldnames)):# lol while(while)? maybe a better way here, a goto command would be great
        response = input(plantFieldnames[x] + "?\n>>")
        if (addOrAdj.lower() == 'adj' and 1 == x == 2):
            plantResponses.append(' ')
            x+=1
            continue
        if response.lower() == 'q' or response.lower() == 'quit':
            x=99
            active=False
            if len(plantResponses)<6:return [False]#this should also quit out of the main calling function, used to be achieved by the active=False above
            continue
        #0-2 non null, 1 4 5 6 int, 2 single VARCHAR, 1 not more than the number of spots
        if (x<=2 and response==''):
            print("Please enter a value, this is a non null entry")
            continue
        if (x==1 or 4<=x<=6 and response != ''):
            try:
                int(response)
            except:
                print("Please enter an integer for this value")
                continue
        if (x==1 and int(response)>int(appSettings['Spots Available'])):
            print("Plant placement over number of available spots, please add more spots or addjust")
            continue
        if (x==2):
            try:
                int(response)
                print("Please enter an alphabetic character for the modifier")
                continue
            except:
                pass
            finally:
                if(len(response)>1):
                    print("This value should only be one letter long")
                    continue
            
        plantResponses.append(response)
        x+=1
    #print(plantResponses)
    return plantResponses

def clear_table(tableToClear:str):
    dbConnect("reset table")
    sqlCursor.execute("DELETE FROM " + tableToClear)
    conn.commit()
    dbDisconnect('reset table')

def get_and_check_plant_pk(): #get this integrated into adjust and delete
    response = input("Which plant to modify (select using spot+modifier like 1a or 12b)\n>>")
    if (response.lower()=='q' or response.lower()=='quit'):return [False]
    plantPlacement = [response[:-1], response[-1]]
    # placementModifier = response[-1]
    # placement = response[:-1]
    dbConnect("Adjusting plant + check -- " + plantPlacement[0] + plantPlacement[1])
    sqlCursor.execute(f"SELECT * FROM Plants WHERE Placement={plantPlacement[0]} AND PlacementModifier='{plantPlacement[1]}'")
    values = sqlCursor.fetchall()
    if values == []:
        print("Please enter a real placement + modifier")
        dbDisconnect("wrong adjustment request--" + plantPlacement[0] + plantPlacement[1])
        return ['noListing']
    return plantPlacement

def plant_settings(): #DONE add sql calls to plant settings
#DONE add a check to make sure that plants are not added to spots above "spots avaialable" found in the user presets file
    for plant in plantListList:
        print(plant)
    print("Do you want to add, adjust, or delete plants in the list?")
    match input(">>"):

        case 'add': 
            active=True
            while(active):
                dbp.connect_to_DB(databaseFile)
                dbp.fancy_print_custom(sqlStatementSortedPlantsSelect, 'Plants')
                #dbp.fancy_print_table('Plants')
                dbp.disconnect_from_DB()

                plantResponses = get_plant_input('add')
                if plantResponses == [False]:
                    active = False
                    return
                dbConnect("Adding a plant")
                statement = f"""
INSERT INTO Plants (PlantName, Placement, PlacementModifier, PotStyle, Moisture, Temperature, Humidity)
VALUES('{plantResponses[0]}', {plantResponses[1]}, '{plantResponses[2]}', '{plantResponses[3]}', '{plantResponses[4]}', '{plantResponses[5]}', '{plantResponses[6]}')"""
                try:
                    sqlCursor.execute(statement)
                    conn.commit()
                    dbDisconnect("Adding a plant")
                    print("Add more?")
                    response = input(">>").lower()
                    if(response !='y' and response !='yes'):
                        active=False
                except sqlite3.IntegrityError:
                    print("That unique key (spot, modifier) already exists. These values together must be unique")
                    dbDisconnect("Failed at adding a plant")
            #0'Plant Name', 1'Placement(int)', 2'Placement Modifier(a, b, c, etc)', 3'Pot Style', 4'Moisture(int)', 5'Temperature(int)', 6'Humidity(int)'
    
        case 'adjust'|'adj': 
            #this function is dangerous to time management - this would likely be the sole cause to move to SQL for larger numbers of plants
            active=True
            while active:
                dbp.connect_to_DB(databaseFile)
                dbp.fancy_print_custom(sqlStatementSortedPlantsSelect, 'Plants')
                #dbp.fancy_print_table('Plants')
                dbp.disconnect_from_DB()
                plantPlacement = get_and_check_plant_pk()
                if plantPlacement == [False]:return
                elif plantPlacement == ['noListing']:continue
                # dbp.connect_to_DB(databaseFile)
                # dbp.fancy_print_table('Plants')
                # dbp.connect_to_DB()
                
                # response = input("Which plant to modify (select using spot+modifier like 1a or 12b)\n>>")
                # if (response.lower()=='q' or response.lower()=='quit'):return
                # placementModifier = response[-1]
                # placement = response[:-1]
                # dbConnect("Adjusting plant + check -- " + placement + placementModifier)
                # sqlCursor.execute(f"SELECT * FROM Plants WHERE Placement={placement} AND PlacementModifier='{placementModifier}'")
                # values = sqlCursor.fetchall()
                # if values == []:
                #     print("Please enter a real placement + modifier")
                #     dbDisconnect("wrong adjustment request--" + placement + placementModifier)
                #     continue
                print("What do you want this plant changed to?")
                plantResponses = get_plant_input('adj')
                if plantResponses == [False]:
                    active = False
                    dbDisconnect("requesting to quit plant adjust")
                    return
                
                sqlAdjustStatement = f"""
UPDATE Plants
SET PlantName='{plantResponses[0]}', PotStyle='{plantResponses[3]}', Moisture='{plantResponses[4]}', Temperature='{plantResponses[5]}', Humidity='{plantResponses[6]}'
WHERE Placement={plantPlacement[0]} AND PlacementModifier='{plantPlacement[1]}'
"""
                try: #Keeping this try block in for now, the earlier try block shoiuld catch all incorrect inputs but just in case
                    sqlCursor.execute(sqlAdjustStatement)
                    conn.commit()
                    dbDisconnect("Adjusting plant" + plantPlacement[0] + plantPlacement[1])
                except sqlite3.OperationalError:
                    print("Please enter a real placement + modifier")
                    dbDisconnect("wrong adjustment request" + plantPlacement[0] + plantPlacement[1])

            #0'Plant Name', 1'Placement(int)', 2'Placement Modifier(a, b, c, etc)', 3'Pot Style', 4'Moisture(int)', 5'Temperature(int)', 6'Humidity(int)'
            return print("plants adjusted") 
        
        case 'delete'|'del'|'d':
            active=True
            while active:
                dbp.connect_to_DB(databaseFile)
                dbp.fancy_print_custom(sqlStatementSortedPlantsSelect, 'Plants')
                #dbp.fancy_print_table('Plants')
                dbp.disconnect_from_DB()

                print("Delete the whole list or individual plants?")
                response = input(">>").lower() # trying out a freeform answer here
                if (response.lower()=='q' or response.lower()=='quit'):return
                if ('list' in response or 'all' in response):
                    print("list found, confirm delete whole list")
                    response = input(">>").lower()
                    if (response=='y' or response=='yes' or 'firm' in response):
                        clear_table('Plants')
                elif('indiv' in response or 'plant' in response):
                    print("individual plants found")

                    plantPlacement = get_and_check_plant_pk()
                    if plantPlacement == [False]:return
                    elif plantPlacement == ['noListing']:continue
                    # response = input("Which plant to modify (select using spot+modifier like 1a or 12b)\n>>")
                    # if (response.lower()=='q' or response.lower()=='quit'):return
                    # placementModifier = response[-1]
                    # placement = response[:-1]
                    # dbConnect("Deleting plant + check -- " + placement + placementModifier)
                    # sqlCursor.execute(f"SELECT * FROM Plants WHERE Placement={placement} AND PlacementModifier='{placementModifier}'") #This is not returning an error value here - duh cause will return empty list, issue is present in adjust as well
                    # values = sqlCursor.fetchall()
                    # if values == []:
                    #     print("Please enter a real placement + modifier")
                    #     dbDisconnect("wrong adjustment request--" + placement + placementModifier)
                    #     continue
                    sqlDeleteStatement = f"""
DELETE FROM Plants
WHERE Placement={plantPlacement[0]} AND PlacementModifier='{plantPlacement[1]}'
"""
                    #dbConnect("Deleting item from plants -- " + placement + placementModifier)
                    sqlCursor.execute(sqlDeleteStatement)
                    conn.commit()
                    dbDisconnect("Deleted item -- " + plantPlacement[0] + plantPlacement[1])   

                else:
                    return                 

        case default:
            return
    

def pull_plant_list(): #DONE sql call to pull plant list
    #Do we need this anymore? everyting can be directly modified with a sql statement
    #No this is not needed
    pass


def pull_user_prefrences(): #DONE sql call to pull user settings
    #   only pull pertanent information like the appSettings dict, maybe the name
    appSettings['Spots Available'] = 0
    appSettings['Ventilation'] = False
    appSettings['Watering Style'] = False

    dbConnect("pulling app settings")

    sqlCursor.execute("SELECT * FROM User_Settings")
    settingsPull = sqlCursor.fetchall() 
    if settingsPull == []:appSettings['Filled Out'] = False
    else:appSettings['Filled Out'] = True;print("user settings loaded")
    appSettings['Spots Available'] = settingsPull[0][1]
    if settingsPull[0][2] == 1:appSettings['Watering Style']=True
    else: appSettings['Watering Style']=False
    if settingsPull[0][3] == 1:appSettings['Ventilation']=True
    else: appSettings['Ventilation']=False
    #print(settingsPull)
    #print(appSettings['Filled Out'])
    dbDisconnect("Pulling app settings")
        
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
# When watering long pots, the controls should be connected, eg 1a and 2a should get the same amount of water - this can be changed later but will allow a much easier build when put along side the averaging of the long pots
import random as random

plantSpotsTurnedOn = []

sensorsConnected = False

sqlStatementPullPlantPlacements = "SELECT Placement, PlacementModifier FROM Plants"

adminHelp = """
"""

def admin_log_in():
    passResponse = input("Enter Password\n>>")
    if passResponse != 'pass':return #TODO add a real password/ security service here
    
    while True:
        adminResponse = input("Admin menu\n>>")
        match adminResponse:
            case 's'|'spot'|'spots':
                turn_on_off_spots()
            case 'm'|'moisture'|'tm':
                take_moisture()
            case 'w'|'water':
                water_plants()
            case 'a'|'adjust':
                adjust_water()
            case default:
                print("Exit admin?")
                eResponse = input(">>").lower()
                if ('y' in eResponse):
                    break
        

def turn_on_off_spots():
    #DONE pull plant spots from plant -CSV- SQL
    dbConnect("Pulling plant spots")
    sqlCursor.execute(sqlStatementPullPlantPlacements)
    placementData = sqlCursor.fetchall()
    for place, modifier in placementData:
        plantSpotsTurnedOn.append(str(place) + modifier)
        #print(str(place) + modifier)
    print("Spots detected -- " + str(plantSpotsTurnedOn))
    dbDisconnect("Pulling plant spots")
    pass

def take_moisture(functionCall:int=1):
    #functionCall will be what process this function will take #This might only be a thing for the testing and building of the logic
    #   0 will be no time passed, and will only pass the dict
    #   1 will be a standard time pass and should reduce water
    #TODO function to take moisture measurements
    # This needs to search for moisture sensors, or for lack of sensors (mostly for this code or for when users do not have them) assume a specific loss based on plant spots
    # this needs to average long pots to one value over multiple sensors with error checing and checks to see if one spot's watering spout is encountering an issue
    previousMoistureReadings = []
    previousMoistureReadingsDict = {}

    wateringReadingDict = {}
    
    if not sensorsConnected:
        #testing code, assume sensors will be connected later
        #assume moisture will measure 0-100, this is very much in a sterile environment and will #TODO need another look after physical trials
        #assume the same amount of time and random moisture loss each time the take_moisture function is ran
        #if previous moisture measurement is not available, set to 0 #DONE ONE
        #each run assume ~8 hours past, random moisture loss of 5-25 #TODO TWO kinda need watering working to test next 2
        #if after a watering, add (random moiture 5-10) times however long the watering cycle is per 10 sec #TODO THREE
        #   so if watering for 30 secongs, (random5-10)x3
        #DONE !!MAJOR!! figure out a way to pass the dict for immediate moisture readings while keeping the functionality of reducint moisture when run on its own 
        # To save space, if the place is removed from the turned on spots, it will be deleted from the db #TODO revist after physical trails
        dbConnect("take moisture") 
        for plant in plantSpotsTurnedOn:
            #print("running for "+ str(plant))
            sqlCursor.execute(f"SELECT MoistureReading FROM Plant_Working_Information WHERE Placement={plant[:-1]} and PlacementModifier='{plant[-1]}' ORDER BY TimeTaken DESC") #TODO test this specific statement intensively, need to afirm that it is taking the most recent measurement
            #DONE WORKING add a watering reading like below to pull watering times in seconds (this will be used to bypass the moisture ticking down and instead add moisture as listed above)
            moistureData = sqlCursor.fetchone()

            sqlCursor.execute(f"SELECT WateringTimer FROM Plant_Working_Information WHERE Placement={plant[:-1]} and PlacementModifier='{plant[-1]}' ORDER BY TimeTaken DESC") # it may be a good idea to figure out how to add both of these sql statements together to reduce db strain, probably by splitting the data below into separate dicts once functionality is confirmed
            #splitting them will allow only one pass through each data item, combining them well put 2 numbers each [plant] pass so the for block post 
            wateringData = sqlCursor.fetchone()

            if moistureData != None:
                for item in moistureData:
                    #print(str(item))
                    previousMoistureReadings.append([plant, item]) #might be an idea to keep it like this for quick reference, maybe a dict
                    previousMoistureReadingsDict[plant] = item

                #previousMoistureReadings.append(moistureData)
            #print(moistureData)
            if wateringData != None:
                for item in wateringData:
                    wateringReadingDict[plant] = item

            # do the watering thing here
            # TODO working adjust the moisture for watering based off of watering dict
            

        print("Moisture readings" + str(previousMoistureReadings))
        print("Moisture readings dics" + str(previousMoistureReadingsDict))
        if previousMoistureReadings == []:
            print("new places all around")
            for plant in plantSpotsTurnedOn:
                sqlStatementMoistureNull = f"""
INSERT INTO Plant_Working_Information (Placement, PlacementModifier, MoistureReading, WateringTimer)
VALUES ({plant[:-1]}, '{plant[-1]}', 0, 0)
"""

# Placement INTEGER NOT NULL,
# PlacementModifier VARCAHR NOT NULL,
# TimeTaken TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
# MoistureReading INTEGER,
# WateringTimer INTEGER,
                sqlCursor.execute(sqlStatementMoistureNull)
                conn.commit()
                print("moisture collected for " + plant + "--0")

        if functionCall==0:return previousMoistureReadingsDict #wateringReadingDict # wait no dont pass this, just adjust the moisture reading
        dbDisconnect("take moisture")
        return
    for plant in plantSpotsTurnedOn:
        print("moisture collected for " + plant)
    pass



def water_plants():
    moistureReadings = {}
    moistureReadings = take_moisture(0)
    print(moistureReadings)
    #TODO function to use moisture to water
    # this will pull the moisture based on each plant placement (see moisture function) potentially based on history and previous moisture measurements and will water based on time
    if not sensorsConnected:
        dbConnect("Watering plants")
        #testing code, assume sensors will be connected later
        #if no moisture reading, run watering for 60 sec (for this dryrun water 6 units) #DONE ONE 
        for plant in plantSpotsTurnedOn:
            if moistureReadings.get(plant) == 0:
                
                sqlStatementWateringFromZero = f"""
INSERT INTO Plant_Working_Information (Placement, PlacementModifier, MoistureReading, WateringTimer)
VALUES ({plant[:-1]}, '{plant[-1]}', 0, 60)"""
                #print(sqlStatementWateringFromZero)
                sqlCursor.execute(sqlStatementWateringFromZero)
                conn.commit()
            else:
                print(plant + ' is moist')    
        dbDisconnect("Watering plants")
        return
    print("Plants watered")
    pass



def adjust_water():
    #TODO function to use moisture to check water
    # this will pull moisture (see moisture function) and the previous water amount (see water function) to adjust if the time needs to be increased or decreased
    print("Water adjusted")
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
dbConnect("startup")
dbDisconnect("startup")
file_check()
pull_user_prefrences()
turn_on_off_spots()
#print(appSettings)
# for row in plantListList:
#     print(row)
while(True):
    # main menu!
    #should add the user settings and plant list when user logs in, this should make the try catch loops much easier

    print("\nreturning to start, type help for command list")
    userInterface(input(">>"))