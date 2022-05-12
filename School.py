# School file
    import mysql.connector

    print("Connecting to db_class database in mySQL.....")
    dbms = mysql.connector.connect(host="localhost",
                                   user="root",
                                   passwd=input("What is your database password?"),
                                   database="db_class")

    myCursor = dbms.cursor()
    Choice = input("create, read, or delete? ")
    table = "school"
    print("Table Name: school with Fields: SchoolID, SchoolName", "SchoolAbbrev", "City", "State", "SchoolDivision")

    # Function that inserts data into table
    def create(dbms, myCursor):
        myCursor.execute("SELECT * FROM db_class.school;")
        for i in myCursor:
            print(i)
        newschoolName = input(" New SchoolName?(within single quotations)#")
        newschoolID = input("New schoolID? That doesn't resemble none of the above")
        SchoolAbbrev = input("School Abbrev #")
        City = input("City")
        State = input("State #")
        SchoolDiv = input("School Division #")
        command = "INSERT INTO db_class.sports(SportsID ,SportsName) VALUES (" + newschoolID + ", " \
                  + newschoolName + ", " + SchoolAbbrev + " , " + City + "," + State + "," + SchoolDiv + ')'
        print(command)
        myCursor.execute(command)
        dbms.commit()
        print("Data Inserted!")

    def read(myCursor, table):
        rOption = input("Read all entries from the " + table + " table? ")
        if rOption == "yes":
            myCursor.execute("SELECT * FROM db_class." + table + ";")
            for i in myCursor:
                print(i)

        if rOption == "no":
            command = "SELECT"
            columns = input("Which columns would you like selected, ()separate with coma")
            command += columns
            additional_cmd = " FROM db_class." + table + " WHERE SchoolID = "
            command += additional_cmd
            conditional = input("Enter ID (Within Single Quotations)#")
            command += conditional
            print(command)
            if command.endswith(";"):
                myCursor.execute(command)
                for i in myCursor:
                    print(i)
            else:
                myCursor.execute(command + ";")
                for i in myCursor:
                    print(i)

    def delete(dbms, myCursor, table):
        del_Option = input("Delete all records from" + table + " table? ")

        if del_Option == "yes":
            myCursor.execute("DELETE FROM db_class." + table + ";")
            dbms.commit()
            print("Deleted")
        else:
            command = "DELETE FROM db_class." + table + " WHERE SchoolID= "
            conditional = input("Enter SchoolID's #(within single Quotations)")
            if conditional.endswith(";"):
                myCursor.execute(command + str(conditional))
                dbms.commit()
                print("Executed")
            else:
                myCursor.execute(command + conditional + ";")
                dbms.commit()
                print("Executed")

    # calling the functions!
    if Choice == "create":
        create(dbms, myCursor)

    if Choice == "read":
        read(myCursor, table)

    if Choice == "delete":
        delete(dbms, myCursor, table)

    myCursor.close()
    dbms.close()
