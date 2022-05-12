import PySimpleGUI as sg
import mysql.connector

# connecting to my database with mysql connector
dbms = mysql.connector.connect(host="localhost",
                               user="root",
                               passwd="Dc762019",
                               database="db_class")
myCursor = dbms.cursor()

sg.theme('DarkBlue3')
sg.set_options(font='Courier 16')

StudentsData = []
myCursor.execute("SELECT * FROM db_class.students")
for i in myCursor:
    StudentsData.append(list(i))
headers = ['StudentID', 'FirstName', 'LastName', 'SchoolID', 'PersonalPhone', 'HobbyID', 'SportsID']


# function that updates new data on to the display table on refreshing
def refresh_data():
    dbms2 = mysql.connector.connect(host="localhost",
                                    user="root",
                                    passwd="Dc762019",
                                    database="db_class")
    myCursor2 = dbms2.cursor()
    data = []
    myCursor2.execute("SELECT * FROM db_class.students;")
    for j in myCursor2:
        data.append(list(j))
    window['-table-'].Update(values=data)
    sg.popup("Refreshed")


# clearing form function
def clear_inputs():
    for key in values:
        window['StudentID'].update('')
        window['FirstName'].update('')
        window['LastName'].update('')
        window['SchoolID'].update('')
        window['PersonalPhone'].update('')
        window['HobbyID'].update('')
        window['SportsID'].update('')
    return None


# Submit function
def submit_data():
    StudentID = values['StudentID']
    if StudentID == '':
        sg.popup_error('Missing StudentID')
    FirstName = values['FirstName']
    if FirstName == '':
        sg.popup_error('Missing FirstName')
    LastName = values['LastName']
    if LastName == '':
        sg.popup_error('Missing LastName')
    SchoolID = values['SchoolID']
    if SchoolID == '':
        sg.popup_error('Missing School')
    PersonalPhone = values['PersonalPhone']
    if PersonalPhone == '':
        sg.popup_error('Missing PhoneNumber')
    HobbyID = values['HobbyID']
    if HobbyID == '':
        sg.popup_error('Missing Hobby')
    SportsID = values['SportsID']
    if SportsID == '':
        sg.popup_error('Missing Sports')
    else:
        try:
            command = "INSERT INTO db_class.students(StudentID ,FirstName, LastName, SchoolID, PersonalPhone, HobbyID," \
                      " SportsID) VALUES (" + "'" + values['StudentID'] + "'" + ", " + "'" + values[
                          'FirstName'] + "'" + ", " + "'" \
                      + values['LastName'] + "'" + ", " + "'" + values['SchoolID'] + "'" + ", " + "'" + values[
                          'PersonalPhone'] \
                      + "'" + ", " + "'" + values['HobbyID'] + "'" + ", " + "'" + values['SportsID'] + "'" + ');'
            print(command)
            myCursor.execute(command)
            dbms.commit()
            choice = sg.popup_ok_cancel('Please confirm Entry')
            if choice == 'OK':
                clear_inputs()
                sg.popup_quick('Student Entered')
            else:
                sg.popup_ok('Edit Entry')
        except:
            sg.popup('Kindly Check your Entries')


# deleting selected entry
def delete_data():
    dbms3 = mysql.connector.connect(host="localhost",
                                    user="root",
                                    passwd="Dc762019",
                                    database="db_class")
    myCursor3 = dbms3.cursor()
    data3 = []
    myCursor3.execute("SELECT * FROM db_class.students")
    for i in myCursor3:
        data3.append(list(i))
    print(data3)
    window['-table-'].Update(values=data3)
    table.update(data3)
    indexes = values['-table-']
    StudID_list = []
    if indexes:
        for index in indexes:
            selected_list = data3[index]
            table.update(data3)
            StudID_list.append(selected_list[2])
            for index in sorted(indexes, reverse=True):
                command = "DELETE FROM db_class.students WHERE  StudentID IN (%s)" % ",".join(["%s"] *
                                                                                              len(StudID_list))
                myCursor3.execute(command, StudID_list)
                dbms3.commit()
    sg.popup("Entry Deleted, Refresh!")


# uploading data to database from form

# GUI  layouts
data_layout = [
    [sg.T('Current Students:')],
    [sg.Table(headings=headers, values=StudentsData, display_row_numbers=True, enable_events=True,
              justification='center', key='-table-')]
]

adding_layout = [
    [sg.T(' Students Entry')],
    [sg.T('StudentID'), sg.Push(), sg.I(size=(30, 5), key='StudentID')],
    [sg.T('FirstName'), sg.Push(), sg.I(size=(30, 5), key='FirstName')],
    [sg.T('LastName'), sg.Push(), sg.I(size=(30, 5), key='LastName')],
    [sg.T('SchoolID'), sg.Push(), sg.Combo(size=(30, 5), values=['001', '021', '031'], key='SchoolID')],
    [sg.T('PersonalPhone'), sg.Push(), sg.I(size=(30, 5), key='PersonalPhone')],
    [sg.T('HobbyID'), sg.Push(), sg.Combo(size=(30, 5), values=['101', '102', '103', '104', '105', '106', '107', '108',
                                                                '109', '110'], key='HobbyID')],
    [sg.T('SportsID'), sg.Push(), sg.Combo(size=(30, 5), values=['S00', 'S01', 'S02', 'S03', 'S04',
                                                                 'S05', 'S06', 'S07', 'S08', 'S09', 'S10'],
                                           key='SportsID')],
    [sg.Button('Submit', key='-submit-', expand_x=True), sg.Button('Clear', expand_x=True),
     sg.Button('Exit', expand_x=True)]
]

main_layout = [
    [sg.Column(adding_layout)],
    [sg.Column(data_layout)],
    [sg.Button('Read Data', key='-ref-'), sg.Button('Delete', key='-del-')]
]
window = sg.Window('Students', main_layout)
table = window['-table-']

# -MAIN-
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED or 'Exit'):
        break
    if event == 'Clear':
        clear_inputs()
    if event == '-del-':
        delete_data()
    if event == '-ref-':
        refresh_data()
    if event == '-submit-':
        submit_data()

window.close()
