import requests
from bs4 import BeautifulSoup
import datetime
URL = 'https://www.statecollege.com/penn-state-football-schedules/'

def remove_tag(stuff):
    output = ""
    adding = True
    stuff = str(stuff)
    for char in stuff:
        if char == '<':
            adding = False
        if adding:
            output += char
        if char == '>':
            adding = True
    return output

        

def parse_table(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.table
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = {}
    column_list = []
    for row in rows:
        columns = row.find_all('td')
        data[row] = columns
        column_list.append(columns)
    
    for i in range(len(column_list)):
        for j in range(len(column_list[i])):
            column_list[i][j] = remove_tag(column_list[i][j])
    return column_list

def check_game(table):
    today = datetime.date.today()
    day = today.strftime("%B %d, %Y")
    writing = True
    parsed_day = ''
    for i in range(len(day)):
        if day[i] == ',':
            writing = False
        if writing:
            parsed_day += day[i]
            
    print("today is " + parsed_day)
    today_index = 0
    today_is_game = False
    for i in range(len(table)):
        if parsed_day in table[i]:
            today_is_game = True
            today_index = i
            print("Today is a game day")
    if not today_is_game:
        print("No game today lol")

    #Check the time of the game
    game_time = ''
    if today_is_game:
        game_time = table[today_index][2]
    gametime = ''
    writing = True
    for i in range(len(game_time)):
        if game_time[i] == '|':
            writing = False
        if writing:
            gametime += game_time[i]
        
    print("The game time is " + gametime)

    if gametime[0] == 'NOON':
        print("It's noon, safe to brunch")
        return True
    if int(gametime[0]) >= 9:
        print("Safe to brunch")
        return True
    else:
        print("NOT SAFE TO BRUNCH, Gametime in afternoon")
        return False

    
    
            


            


#print(*parse_table(URL))
check_game(parse_table(URL))





