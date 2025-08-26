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


def connect_to_DB(dbName:str):
    global sqlCursor
    global conn
    db = dbName
    conn = sqlite3.connect(db)
    sqlCursor = conn.cursor()

def disconnect_from_DB():
    try:
        conn.close()
    except:
        pass

def create_tables_and_add_info():
    sqlCursor.execute("CREATE TABLE test (name TEXT, description TEXT)")
    for item in range(10):
        sqlCursor.execute('INSERT INTO test (name, description) values ("this", "sucks")')

    sqlCursor.execute("CREATE TABLE two (name TEXT, description TEXT)")
    for item in range(10):
        sqlCursor.execute('INSERT INTO two (name, description) values ("second", "sucks")')
    conn.commit()

def process_SQLite_tuple_to_string(arg):
    secondTestString = str(arg)
    secondTestString = secondTestString.translate({ord(i): None for i in "()',"})
    return secondTestString

def print_database():
    sqlCursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = sqlCursor.fetchall()

    for item in tables:
        item = process_SQLite_tuple_to_string(item)
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

def fancy_print_database():
    sqlCursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = sqlCursor.fetchall()

    for item in tables:
        item = process_SQLite_tuple_to_string(item)
        tableList.append(item)
    #TODO? maybe add sort by pk here
    for table in tableList:
        sqlCursor.execute("SELECT * FROM " + table) #crazy idea to sort by pk, but would need to pull pk in above statement
        tabledata = sqlCursor.fetchall()
        sqlDescription = sqlCursor.description

        fancy_format([tabledata, sqlDescription, table])

        
def fancy_print_table(table:str):
    sqlCursor.execute("SELECT * FROM " + table)
    tabledata = sqlCursor.fetchall()
    sqlDescription = sqlCursor.description

    fancy_format([tabledata, sqlDescription, table])

def fancy_print_custom(sqlStatement:str, table:str):
    sqlCursor.execute(sqlStatement) 
    tabledata = sqlCursor.fetchall()
    sqlDescription = sqlCursor.description

    fancy_format([tabledata, sqlDescription, table])

def fancy_format(tabeDataList:list):
    numColumns = 1
    columnNames='|'
    for column in tabeDataList[1]:
        columnNames = columnNames + (column[0].center(16, ' ') + '|')
        numColumns += 1

    print(str(tabeDataList[2]).center(numColumns*5, '-'))
    print(('*'*15) * numColumns)
    print(columnNames)
    print(('*'*15) * numColumns)

    for row in tabeDataList[0]:
        rowValues = '|'
        for item in row:
            rowValues = rowValues + str(item).center(16, ' ') + '|'
        print(rowValues)
        
    print("\n\n")

if __name__ == "__main__":
    #I finally have a use for this :3
    # try:
    #     createTablesAndAddInfo()
    # except:
    #     pass
    connect_to_DB('test.db')
    fancy_print_database()
    conn.close()
    


