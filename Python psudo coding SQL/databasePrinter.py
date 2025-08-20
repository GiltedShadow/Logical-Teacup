import sqlite3
#######################################
#                          _             
#__      ____ _ _ __ _ __ (_)_ __   __ _ 
#\ \ /\ / / _` | '__| '_ \| | '_ \ / _` |
# \ V  V / (_| | |  | | | | | | | | (_| |
#  \_/\_/ \__,_|_|  |_| |_|_|_| |_|\__, |
#                                  |___/ 
# WARNING #
#
# This will print the ENTIRE db to the terminal
# This has not been tested on large dbs or tables bigger than 2x10
# This has not been tested an anything but a .db file, and uses sqlite
# 
#######################################

tableList = []
tableColumns = {}


def connectToDB(dbName):
    global sqlCursor
    global conn
    db = dbName
    conn = sqlite3.connect(db)
    sqlCursor = conn.cursor()

def createTablesAndAddInfo():
    sqlCursor.execute("CREATE TABLE test (name TEXT, description TEXT)")
    for item in range(10):
        sqlCursor.execute('INSERT INTO test (name, description) values ("this", "sucks")')

    sqlCursor.execute("CREATE TABLE two (name TEXT, description TEXT)")
    for item in range(10):
        sqlCursor.execute('INSERT INTO two (name, description) values ("second", "sucks")')
    conn.commit()

def processSQLiteTupleToString(arg):
    secondTestString = str(arg)
    secondTestString = secondTestString.translate({ord(i): None for i in "()',"})
    return secondTestString

def printDatabase():
    sqlCursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = sqlCursor.fetchall()

    for item in tables:
        item = processSQLiteTupleToString(item)
        tableList.append(item)

    for table in tableList:
        columnNames=[]
        sqlCursor.execute("SELECT * FROM " + table)
        tabledata = sqlCursor.fetchall()
        sqlDescription = sqlCursor.description

        for column in sqlDescription:
            columnNames.append(column[0])

        print(table)
        print(columnNames)

        for row in tabledata:
            print(row)

        print("\n\n")

def fancyPrintDatabase():
    sqlCursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = sqlCursor.fetchall()

    for item in tables:
        item = processSQLiteTupleToString(item)
        tableList.append(item)

    for table in tableList:
        columnNames='|'
        sqlCursor.execute("SELECT * FROM " + table)
        tabledata = sqlCursor.fetchall()

        sqlDescription = sqlCursor.description
        for column in sqlDescription:
            columnNames = columnNames + (column[0].center(15, ' ') + '|')

        print(str(table).center(20, '-'))
        print('*'*35)
        print(columnNames)
        print('*'*35)

        for row in tabledata:
            rowValues = '|'
            for item in row:
                rowValues = rowValues + str(item).center(15, ' ') + '|'
            print(rowValues)

        print("\n\n")
        

if __name__ == "__main__":
    #I finally have a use for this :3
    # try:
    #     createTablesAndAddInfo()
    # except:
    #     pass
    connectToDB('test.db')
    fancyPrintDatabase()
    conn.close()
    


