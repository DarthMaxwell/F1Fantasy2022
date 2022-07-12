import requests
import os
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup
import datetime

TeamM = [
    'https://www.formula1.com/en/results.html/2022/drivers/MAXVER01/max-verstappen.html',
    'https://www.formula1.com/en/results.html/2022/drivers/LEWHAM01/lewis-hamilton.html',
    'https://www.formula1.com/en/results.html/2022/drivers/KEVMAG01/kevin-magnussen.html',
    'https://www.formula1.com/en/results.html/2022/drivers/DANRIC01/daniel-ricciardo.html',
    'https://www.formula1.com/en/results.html/2022/drivers/YUKTSU01/yuki-tsunoda.html',
    ]

TeamC = [
    'https://www.formula1.com/en/results.html/2022/drivers/CARSAI01/carlos-sainz.html',
    'https://www.formula1.com/en/results.html/2022/drivers/GEORUS01/george-russell.html',
    'https://www.formula1.com/en/results.html/2022/drivers/ESTOCO01/esteban-ocon.html',
    'https://www.formula1.com/en/results.html/2022/drivers/LANNOR01/lando-norris.html',
    'https://www.formula1.com/en/results.html/2022/drivers/MICSCH02/mick-schumacher.html',
    ]

TeamZ = [
    'https://www.formula1.com/en/results.html/2022/drivers/CHALEC01/charles-leclerc.html',
    'https://www.formula1.com/en/results.html/2022/drivers/VALBOT01/valtteri-bottas.html',
    'https://www.formula1.com/en/results.html/2022/drivers/SERPER01/sergio-perez.html',
    'https://www.formula1.com/en/results.html/2022/drivers/PIEGAS01/pierre-gasly.html',
    'https://www.formula1.com/en/results.html/2022/drivers/FERALO01/fernando-alonso.html',
    ]

def getlocations():
    locations = []
    r = requests.get('https://www.formula1.com/en/results.html/2022/drivers/MAXVER01/max-verstappen.html').text
    soup = BeautifulSoup(r, 'html.parser')
    for data in soup.find_all("a", class_="dark ArchiveLink"):
        locations.append(data.get_text())
    return locations

def getpointsanddates(team):
    pointsanddates = []
    for drivers in team:
        r = requests.get(drivers).text # This is where you would add the proxies
        soup = BeautifulSoup(r, 'html.parser')
        race = {}
        for index, data in enumerate(soup.find_all("td", class_="dark bold")):
            if index % 2 == 0:
                race['date'] = data.get_text()
            else:
                race['points'] = int(data.get_text())
                pointsanddates.append(race)
                race = {}
    return pointsanddates

def squishpoints(pointsanddates): # addes the points for the same date
    squishlist = []
    for race in pointsanddates:
        if race['date'] in [d['date'] for d in squishlist]:
            existingrace = [item for item in squishlist if item['date'] == race['date']][0]
            existingrace['points'] += race['points']
        else:
            squishlist.append(race)
    return squishlist

def sumpoints(squishlist): # this makes it so points of the second race is first race points + second race points
    total = 0
    for race in squishlist:
        total += race['points']
        race['points'] = total
    return squishlist

def getteamname(team):
    if team[0] == 'https://www.formula1.com/en/results.html/2022/drivers/MAXVER01/max-verstappen.html':
        return("Maxwell's team")
    elif team[0] == 'https://www.formula1.com/en/results.html/2022/drivers/CARSAI01/carlos-sainz.html':
        return("Cara's team")
    elif team[0] == 'https://www.formula1.com/en/results.html/2022/drivers/CHALEC01/charles-leclerc.html':
        return("Zara's team")

def main(team): # this returns just the points bec thats all we need for the graph
    pointsanddates = getpointsanddates(team)
    squishlist = squishpoints(pointsanddates)
    a = sumpoints(squishlist)
    points = [b['points'] for b in a]
    teamname = getteamname(team)
    print("Finished scraping points for " + str(teamname))
    return points

def updatehtml(): # This uses the /templates/index.html template to update the /docs/index.html
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment( loader = FileSystemLoader(templates_dir) )
    template = env.get_template('index.html')
    filename = os.path.join(root, 'docs', 'index.html')
    with open(filename, 'w') as fh:
        fh.write(template.render(
            locations = getlocations(),
            datam = main(TeamM),
            datac = main(TeamC),
            dataz = main(TeamZ),
            ))

def prettytop():
    print("-" * 55)
    print("Scrapping the web for points")
    print("Starting time " + str(start))
    print("-" * 55)

def prettybottom():
    races = len(getlocations())
    end = datetime.datetime.now()
    timedelta = end - start
    print("-" * 55)
    print("Updated html all good to go. There have been " + str(races) + " races")
    print("Time elapsed " + str(timedelta.total_seconds()) + " seconds")
    print("-" * 55)

if __name__ == "__main__":
    start = datetime.datetime.now()
    prettytop()
    updatehtml()
    prettybottom()
