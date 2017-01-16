# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


from bs4 import BeautifulSoup, Comment
import os
import urllib.request
import socket
from datetime import datetime


class dataGrab():
    def basicTableStore(self,soup,basicScoreTableID,HomeOrAway,matchdate,team,opponent):
        table=soup.find('table', id=basicScoreTableID)
        table_Head=table.thead
        tableBody=table.find('tbody')
        rowsData=""
        for rows in tableBody.findAll('tr'):
            if len(rows)!=43 and len(rows)!=2:                                
                
                cellData = matchdate+","+team+","+opponent#+","+HomeOrAway                
                for playerName in rows.findAll('th'):
                    cellData = cellData+","+playerName.find('a').text
                    
                for cells in rows.findAll('td'):
                    if(cells.text!=""):                        
                        cellData=cellData+","+str(cells.text)
                    else:
                        cellData = cellData+","+"0"                        
                rowsData=rowsData+"\n"+cellData                
        print(rowsData)
        
        file.write(bytes(rowsData, encoding="ascii", errors="ignore"))
        
    def seriesStats(self, url,teamOneID, teamTwoID,location,winLoss):
        print(url)
        page=urllib.request.urlopen(url)
        soup = BeautifulSoup(page,"html.parser")
        divs=soup.find('div', class_='scorebox_meta')        
        date = divs.find('div').text
        newDateFormat = datetime.strptime(date, '%I:%M %p, %B %d, %Y')
        newDateString = str(newDateFormat.strftime('%m/%d/%Y'))
        
        HomeOrAway = "1" if teamOneID in location.lower() else "0"
        
        self.teamScoreSheet(newDateString,teamOneID,teamTwoID,HomeOrAway,winLoss)
        teams= ['box_'+teamOneID+'_basic','box_'+teamTwoID+'_basic']
        for teamID in teams:
            self.basicTableStore(soup,teamID,location,newDateString,teamOneID,teamTwoID)
            
    def teamScoreSheet(self,date,team,opponent,HomeOrAway,winOrLoss):
        teamDataRow=date+","+team+","+opponent+","+HomeOrAway+","+winOrLoss+"\n"        
        fileTeam.write(bytes(teamDataRow, encoding="ascii", errors="ignore"))
    
    def playOffSeriesSets(self, url):
        page=urllib.request.urlopen(url)
        
        soup = BeautifulSoup(page,"html.parser")
        table=soup.find('table', id='all_playoffs')    
        tableBody=table.find('tbody')
        for rows in tableBody.findAll('tr'):
            cellData = ""
            teamName = rows.find('td').text                
            for row in rows.findAll('td'):            
                links = row.findAll('a')
                for link in links:
                    if link.text =="Series Stats":
                        print(link.get('href'))
                        newLink = "http://www.basketball-reference.com" + link.get('href')
                        self.getTeamList(url)
                        
                        
    def getTeamList(self,url):
        url = "http://www.basketball-reference.com/playoffs/2016-nba-western-conference-first-round-grizzlies-vs-spurs.html"
        page=urllib.request.urlopen(url)
        soup = BeautifulSoup(page,"html.parser")                
        div=soup.find('div', id='div_other_scores')        
        tables = div.findAll("table", class_="teams poptip")

        team1 = ""
        team2 = ""
        teamGroup = []
        scoreGroup = []
        for table in tables:
           for rows in table.findAll('tr'):
               for row in rows.findAll('td'):
                   
                   if("Game" not in row.text and row.text.isdigit()):
                       scoreGroup.append(row.text)
                       
                   links = row.findAll('a')
                   for link in links:
                       if(links[0].text != 'Final' and links[0].text != ''):
                           teamGroup.append(links[0].text)
        groupNum = 0
        
        for table in tables:
            location = table.get('data-tip')
            location = location[location.find('at ')+3:]            
            for rows in table.findAll('tr'):
                for row in rows.findAll('td'):
                    links = row.findAll('a')
                    for link in links:
                        if link.text == 'Final':
                               newLink = "http://www.basketball-reference.com" + link.get('href')
#                               print(newLink,teamGroup[groupNum],teamGroup[groupNum+1])
                               team1 = teamGroup[groupNum].lower()
                               team2 = teamGroup[groupNum+1].lower()
                               
                               score1 = scoreGroup[groupNum]
                               score2 = scoreGroup[groupNum+1]
                               
                               winLoss = '1' if int(score1)>int(score2) else '0'
                               self.seriesStats(newLink,team1,team2,location,winLoss)
                               groupNum = groupNum + 2
                               print(newLink)
    
                
        
file=open(os.path.expanduser("PlayerData.csv"),"wb")
fileTeam=open(os.path.expanduser("TeamData.csv"),"wb")
#Header of the table
#tabel_header_main = "MatchDate,team,opponent,HomeOrAway,PlayerName,MP,FG,FGA,FGPerc,ThreeP,ThreePA,ThreePPerc,FT,FTA,FTPerc,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,PlusOrMinus"
tabel_header_main = "MatchDate,team,opponent,PlayerName,MP,FG,FGA,FGPerc,ThreeP,ThreePA,ThreePPerc,FT,FTA,FTPerc,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,PlusOrMinus"
file.write(bytes(tabel_header_main,encoding="ascii", errors="ignore"))

tabel_header_main_team = "MatchDate,team,opponent,HomeOrAway,WinOrLoss"
fileTeam.write(bytes(tabel_header_main_team,encoding="ascii", errors="ignore"))

                        
scrapThePage = dataGrab()


#URL for main website
url = "http://www.basketball-reference.com/playoffs/"
page=urllib.request.urlopen(url)
soup = BeautifulSoup(page,"html.parser")
table=soup.find('table', id='champions_index')
storeYears = []
tableBody=table.find('tbody')
for rows in tableBody.findAll('tr'):
    cellData = ""
    for year in rows.findAll('th'):
        #Store all the years available
        storeYears.append(year.text)
        
#Iterate available years in web page
for year in storeYears:    
    yearWiseUrl = "http://www.basketball-reference.com/playoffs/NBA_"+year+".html"
    scrapThePage.playOffSeriesSets(yearWiseUrl)
    

__author__ = "S524960"
__date__ = "$Nov 15, 2016 12:28:12 PM$"

if __name__ == "__main__":
    print("***********************")