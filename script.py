import requests
import os
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup

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

<<<<<<< HEAD
def getlocations(): # x-axis of the graph
    locations = []
    r = requests.get('https://www.formula1.com/en/results.html/2022/drivers/MAXVER01/max-verstappen.html').text
    soup = BeautifulSoup(r, 'html.parser')
    for data in soup.find_all("a", class_="dark ArchiveLink"):
        locations.append(data.get_text())
    return locations

def getpointsanddates(team): # gets all the date points for each race for each driver in a team
=======
proxies = {
    'https': 'http://194.233.77.110:6666',
    'http': 'http://207.180.199.65:3128',
}

def getpointsanddates(team):
>>>>>>> 60588a4dcf9c03ed8f70d832825e8922d64644f5
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

def main(team): # this returns just the points bec thats all we need for the graph
    pointsanddates = getpointsanddates(team)
    squishlist = squishpoints(pointsanddates)
    a = sumpoints(squishlist)
    points = [b['points'] for b in a]
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

if __name__ == "__main__":
<<<<<<< HEAD
    print("-" * 50)
    print("Scraping web for points")
    print("-" * 50)
    updatehtml()
    print("-" * 50)
    print("DONE wanna add how long it took and how many races there have been")
    print("-" * 50)
=======
    updatehtml()
>>>>>>> 60588a4dcf9c03ed8f70d832825e8922d64644f5
