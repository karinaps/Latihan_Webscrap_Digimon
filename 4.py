# Kamis 16 Mei 2019

# LATIHAN IMPORT WEBSCRAP DATA TO MYSQL DATABASE

from bs4 import BeautifulSoup
import requests
import csv
import mysql.connector

url = 'https://wikimon.net/Visual_List_of_Digimon'
web = requests.get(url)
soup = BeautifulSoup(web.content, 'html.parser')
span = soup.find_all('td')
listnama = []
listgambar = []

for a in span:
    nama = a.find('a').text
    if nama == 'Return to Top' or nama == '' or nama == 'List of Digimon (Japanese)' or nama == 'A':
        pass
    else:
        listnama.append(nama)

    for b in a.find_all('img'):
        gambar = b.get('src')
        if gambar == None:
            pass
        else:
            listgambar.append('https://wikimon.net/'+gambar)


# IMPORT TO DICTIONARY=====================================================================================================================

allData = []
digimon_column = ['nama', 'gambar']
for d in range(len(listnama)):
    dataDict = {
        "nama": listnama[d],
        "gambar": listgambar[d]
    }
    allData.append(dataDict)

# import to csv =============================================================================================================================

with open('digimonlist.csv', 'w', newline='', encoding='utf8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=digimon_column)
    writer.writeheader()
    writer.writerows(allData)

#import to mysql=================================================================================================================

mydb= mysql.connector.connect(
    host = 'localhost',
    user = 'karinaps',
    passwd = 'Kimtaehyung1809',
    database ='digimon'
)

hapus = mydb.cursor().execute('delete from digimon')
mulai = mydb.cursor().execute('ALTER TABLE digimon AUTO_INCREMENT = 1')

for c in range(len(listnama)):
    x = mydb.cursor()
    x.execute('insert into digimon (nama, gambar) values (%s, %s)', (listnama[c], listgambar[c])) 
mydb.commit()


