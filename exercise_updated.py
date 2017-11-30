"""
Your task is to write a python program to do the following:
    1) For each inspection for each facility on a single page of results from the Napa county health
       department website (url given below), scrape the following information:
       - Facility name
       - Address (just street info, not city, state, or zip)
       - City
       - State
       - Zipcode
       - Inspection date
       - Inspection type
       - For each out-of-compliance violation type, scrape the violation type number and corresponding description.
         For example, an inspection might contain violation type numbers 6 and 7, and descriptions
         "Adequate handwashing facilities supplied & accessible" and "Proper hot and cold holding temperatures"
    2) Place this information in a database of some sort. You can use whatever you want; sqlite, postgres, mongodb, etc.
       Organize the data in a fashion which seems the most logical and useful to you. Include in your result the
       necessary instructions to set up this database, such as create table statements.
    3) Fetch this information from the database, and print it to the console in some fashion which clearly
       and easily displays the data you scraped.

We have provided a little bit of code using the lxml and sqlite to get you started,
but feel free to use whatever method you would like.
"""

from lxml import html
from lxml.html import tostring
import sqlite3
import urllib.request
import requests
import pandas

page_url = (
    "http://ca.healthinspections.us/napa/search.cfm?start=1&1=1&sd=01/01/1970&ed=03/01/2017&kw1=&kw2=&kw3="
    "&rel1=N.permitName&rel2=N.permitName&rel3=N.permitName&zc=&dtRng=YES&pre=similar"
)

'''Convert data to string'''
def cleanData(data):
    byteText = data.encode('utf-8').strip()# convert to byte from <class 'lxml.etree._ElementUnicodeResult'>
    byteConvertToString = str(byteText, encoding = "utf-8")  #convert to String
    dataInString = byteConvertToString.replace("\t",'').replace('\r','').replace('\n','')
    return dataInString

'''Get the postcode from the postcode and city string'''
def getPostCode(postCodeAndCity):
    postCodeString = postCodeAndCity[-5:]
    return postCodeString


'''Get the string of city data from the postcode and city string'''
def getCity(postCodeAndCity):
    cityString = postCodeAndCity[:-10]
    return cityString


'''Get the state data from the postcode and city string'''
def getState(postCodeAndCity):
    stateString = postCodeAndCity[-8:-6]
    return stateString


'''Get information from the above url, return data as a list, with each 
item in the list represents one facility's data '''
def scrape():
    page = requests.get(page_url)
    tree = html.fromstring(page.content)
    allFacilityInfo = []
    for index in range(1,11):
        '''get xpath for each item'''
        xpath = '//tr/td/div[' + str(index) + ']'
        nameXpath = xpath + '/a/b/text()'
        streetNameXpath = xpath + '/div[2]/text()[1]'
        cityAndPostCodeXpath = xpath + '/div[2]/text()[2]'
        inspectionDateXpath = xpath + '/div[2]/div/a/text()'
        inspectionGradeXpath = xpath + '/div[2]/div/text()[2]'
        '''get data from xpath'''
        name = tree.xpath(nameXpath)    
        streetName = tree.xpath(streetNameXpath)
        cityAndPostCode = tree.xpath(cityAndPostCodeXpath)
        inspectionDate = tree.xpath(inspectionDateXpath)
        inspectionGrade = tree.xpath(inspectionGradeXpath)
        '''process data '''
        nameProcessed = cleanData(name[0])
        streetNameProcessed = cleanData(streetName[0])
        cityAndPostCodeProcessed = cleanData(cityAndPostCode[0])
        cityProcessed = getCity(cityAndPostCodeProcessed)
        postCodeProcessed = getPostCode(cityAndPostCodeProcessed)
        stateProcessed = getState(cityAndPostCodeProcessed)
        inspectionDateProcessed = cleanData(inspectionDate[0])
        inspectionGradeProcessed = cleanData(inspectionGrade[0])
        indexNumber = index
        '''add all data for one facility into a tuple'''
        facilityInfo = (indexNumber, nameProcessed, streetNameProcessed, 
        cityProcessed, stateProcessed, postCodeProcessed, inspectionDateProcessed, 
        inspectionGradeProcessed)
        '''add all data into one list and return the list as the result'''
        allFacilityInfo.append(facilityInfo)
    return allFacilityInfo


'''insert data into a database, data should be a list, 
each item will be inserted into the database as one row of information'''
def setup_db(data):
    conn = sqlite3.connect("C:/Users/Su Wang/facility.db")
    c = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS facility (
                Id integer NOT NULL, 
                'Facility name' text, 
                Address text,
                City text, 
                State text, 
                Zipcode text, 
                'Inspection date' text, 
                'Inspection type' text
            ); """
    c.execute(sql)
    conn.commit()
    for item in data:
        c.execute('INSERT INTO facility VALUES (?,?,?,?,?,?,?,?)', item) 
    conn.commit()
    sqlPrintStatement = 'SELECT * FROM facility;'
    df = pandas.read_sql_query(sqlPrintStatement, conn)
    print(df)
    c.close()

'''scrape the data from above url, store them in a sqlite database and 
print all data to console in a table format'''
def main():
    dataList = scrape()
    setup_db(dataList)


if __name__ == '__main__':
    main()
