import typer
import mysql.connector


crdChoice = input("Would you like to create, read, or delete")
tableName = "HOBBY"

passwd = input("Please enter your password for 'root': ")
cnn = mysql.connector.connect(
        user='root',
        host='localhost',
        password=passwd,
        database='ProjectPart1')

cursor = cnn.cursor()



def create(cnn, cursor, tableName):
    newId = 0
    if tableName.upper() == "HOBBY":
        cursor.execute("SELECT ID FROM ProjectPart1.HOBBY;")
        for i in cursor:
            newId = i[0] + 2
        newHobby = input("What hobby would you like to add? ")

        cmd = "INSERT INTO ProjectPart1.Hobby VALUES(" + str(newId) + ', "' + newHobby + '");'
        cursor.execute(cmd)
        cnn.commit()
        print("DONE.")
    else:
        print("Table name", tableName.upper(), "does not exist. Please try again.")

def read(cursor, tableName):
    if tableName.upper() == "HOBBY":
        readOpt = input("Do you want to read all entries from the " + tableName.upper() + " table? ")

        if readOpt.lower() == "yes":
            cursor.execute("SELECT * FROM ProjectPart1." + tableName.upper() + ";")
            for i in cursor:
                print(i)

        if readOpt.lower() == "no":
            cmd = "SELECT "
            columns = input("which column(s) would you like to see\n(Use commas to separate): ")
            cmd += columns + " FROM ProjectPart1." + tableName.upper() + " WHERE ID="
            conditional = input("Enter ID #")
            cmd += conditional

            if cmd.endswith(";"):
                cursor.execute(cmd)
                for i in cursor:
                    print(i)
            else:
                cursor.execute(cmd + ";")
                for i in cursor:
                    print(i)

    else:
        print("Table name", tableName.upper(), "does not exist. Please try again.")

def delete(cnn, cursor, tableName):
    if tableName.upper() == "HOBBY":
        delOpt = input("Would you like to delete all records from the " + tableName.upper() + " table? ")

        if delOpt.lower() == "yes":
            try:
                cursor.execute("DELETE FROM ProjectPart1." + tableName.upper() + ";")
                cnn.commit()
                print("DONE.")
            except mysql.connector.errors.IntegrityError:
                print("A foreign key constraint fails. Please fix issue and try again.")
                exit(0)
        if delOpt.lower() == "no":
            cmd = "DELETE FROM ProjectPart1." + tableName.upper() + " WHERE ID= "
            conditional = input("Enter Hobby_name ID's #")

            if conditional.endswith(";"):
                try:
                    cursor.execute(cmd + str(conditional))
                    cnn.commit()
                    print("DONE.")
                except mysql.connector.errors.IntegrityError:
                    print("A foreign key constraint fails. Please fix issue and try again.")
                    exit(0)
            else:
                try:
                    cursor.execute(cmd + conditional + ";")
                    cnn.commit()
                    print("DONE.")
                except mysql.connector.errors.IntegrityError:
                    print("A foreign key constraint fails. Please fix issue and try again.")
                    exit(0)

    else:
        print("Table name", tableName.upper(), "does not exist. Please try again.")


## Calling of functions.

if crdChoice.upper() == "CREATE":
    create(cnn, cursor, tableName)

if crdChoice.upper() == "READ":
    read(cursor, tableName)

if crdChoice.upper() == "DELETE":
    delete(cnn, cursor, tableName)

cursor.close()
cnn.close()

print("it conncets")