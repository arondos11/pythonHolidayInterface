from ast import And
import json
import gc
from config import websiteLink2020
from config import websiteLink2021
from config import websiteLink2022
from config import websiteLink2023
from config import websiteLink2024
from config import apiLink
from datetime import date, datetime
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import csv
from flask import Flask, render_template, request

class Holiday:
    def __init__(self, name, date):
        self.name = name
        self.date = date
    def __str__ (self):
        return self.name + ' ('+ self.date +')'

class HolidayEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
    

class HolidayList:
   def __init__(self):
       self.holidayList = []

def getHTML(url):
    response = requests.get(url)
    return response.text

    
def initialJSON():    
    #opens json file 
    f = open('holidays.json')
    # returns JSON object as 
    # a dictionary
    data = json.loads(f.read())
  
    # Iterating through the json
    # list
    global holidayList
    holidayList = []
    for i in data['holidays']:
        holidays = Holiday(i['name'], i['date'])
        holidayList.append(holidays)

    # Closing file
    f.close()

def fromJSON():    
    #opens json file 
    f = open('holidayFiles.json')
    # returns JSON object as 
    # a dictionary
    data = json.loads(f.read())
  
    # Iterating through the json
    # list
    global holidayList
    holidayList = []
    for i in data:
        holidays = Holiday(i['name'], i['date'])
        holidayList.append(holidays)

    # Closing file
    f.close()

def writeJSON():
    #open('holidayFiles.json', 'w').close()
    with open('holidayFiles.json', 'w', encoding='utf-8') as f:
        json.dump(holidayList, f, ensure_ascii=False, indent=4, cls=HolidayEncoder)

def webScrape(link, year):

    url = getHTML(link)
    soup = BeautifulSoup(url, 'html.parser')

    out = [[td.text.strip() for td in tr.select('th, td')] for tr in soup.select('tr[data-mask]')]

    with open('file.csv', 'w', newline='') as f_out:
        writer=csv.writer(f_out)
        writer.writerows(out)

    with open('file.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            csvDate = year + ' ' + row[0]
            date = str(datetime.strptime(csvDate , '%Y %b %d').date())
            holidayCSV = Holiday(row[2], date)
            holidayList.append(holidayCSV)
        
   
        
def removeDuplicates():
    global holidayList
    holidayList = [*set(holidayList)]

def findHoliday(HolidayName, Date):
    sameNameList = [x for x in holidayList if x.name == HolidayName]
    sameBothList = [y for y in sameNameList if y.date == Date]
    i = 0
    while i != len(sameBothList):
        return sameBothList[i]
        # Find Holiday in holidayList
        # Return Holiday

def addHoliday():
    print("Add a Holiday")
    holidayInput = input("Holiday:")
    dateInput = input("Date (YYYY-MM-DD):")
    try:
        dateTest = datetime.strptime(dateInput, '%Y-%m-%d')
    except ValueError:
        print("Incorrect Date Format Try Again")
        return addHoliday()
    holidayUser = Holiday(holidayInput, dateInput)
    holidayList.append(holidayUser)
    print("Added " + holidayInput)

def removeHoliday():
    print("Remove a Holiday")
    holidayInput = input("Holiday:")
    dateInput = input("Date (YYYY-MM-DD):")
    try:
        dateTest = datetime.strptime(dateInput, '%Y-%m-%d')
    except ValueError:
        print("Incorrect Date Format Try Again")
        return removeHoliday()
    try:
        holidayList.remove(findHoliday(holidayInput, dateInput))
    except ValueError:
        print("Incorrect Holiday Name")
        return removeHoliday()
    print(holidayInput + " Removed")

def viewHoliday(yearUser, weekNumUser):
    if weekNumUser == '':
        todayDate = date.today()
        weekNumUser = str(todayDate.isocalendar().week)
        print(weekNumUser)
    
    viewHolidayList = []
    for x in holidayList:
        if yearUser == str(datetime.strptime(x.date, '%Y-%m-%d').date().isocalendar().year):
            if weekNumUser == str(datetime.strptime(x.date, '%Y-%m-%d').date().isocalendar().week):
                viewHolidayList.append(x.name + ' (' + x.date + ')')
    print(*viewHolidayList, sep = "\n")
    return viewHolidayList      


 
    

initialJSON()
writeJSON()

webScrape(websiteLink2020, str(2020))
webScrape(websiteLink2021, str(2021))
webScrape(websiteLink2022, str(2022))
webScrape(websiteLink2023, str(2023))
webScrape(websiteLink2024, str(2024))
writeJSON()
removeDuplicates()

exitCount = 0
saveCount = 0
while exitCount == 0:
    print("Holiday Management")
    print("There are " + str(len(holidayList)) + " holidays stored in the system")
    print("--------------------")
    print("Holiday Menu")
    print("1. Add a Holiday")
    print("2. Remove a Holiday")
    print("3. View Holidays")
    print("4. Save Changes")
    print("5. Exit")
    selection = input("Enter you choice:")
    if selection == '1':
        addHoliday()
    if selection == '2':
        removeHoliday()
    if selection == '3':
        print("View Holidays")
        yearUser = input("Which Year:")
        weekNumUser = input("Which Week? (#1-52, leave blank for current week):")
        viewHoliday(yearUser, weekNumUser)
    if selection == '4':
        saveChoice = input('Are you sure you want to save your changes? y or n')
        saveCount = 1
        if saveChoice == 'y':
            print("Changes Saved")
            saveCount = 1
            open('holidayFiles.json', 'w').close()
            writeJSON()
        if saveChoice == 'm':
            print("Changes Not Saved")
            
    if selection == '5':
        if saveCount == 1:
            exitChoice = input("Are you sure you want to exit? y or n")
            if exitChoice == 'y':
                    exitCount = 1
                    print("Goodbye")
        else:
            exitChoice = input("Changes are unsaved and will be lost. Want to exit?  y or n")
            if exitChoice == 'y':
                exitCount = 1
                print("Goodbye")






 
   
    

