import requests
import os
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup

TeamM = [
    'https://www.formula1.com/en/results.html/2022/drivers/MAXVER01/max-verstappen.html',
    'https://www.formula1.com/en/results.html/2022/drivers/LEWHAM01/lewis-hamilton.html',
    'https://www.formula1.com/en/results.html/2022/drivers/KEVMAG01/kevin-magnussen.html',
    'https://www.formula1.com/en/results.html/2022/drivers/DANRIC01/daniel-ricciardo.html',
    'https://www.formula1.com/en/results.html/2022/drivers/YUKTSU01/yuki-tsunoda.html'
    ]

TeamC = [
    'https://www.formula1.com/en/results.html/2022/drivers/CARSAI01/carlos-sainz.html',
    'https://www.formula1.com/en/results.html/2022/drivers/GEORUS01/george-russell.html',
    'https://www.formula1.com/en/results.html/2022/drivers/ESTOCO01/esteban-ocon.html',
    'https://www.formula1.com/en/results.html/2022/drivers/LANNOR01/lando-norris.html',
    'https://www.formula1.com/en/results.html/2022/drivers/MICSCH02/mick-schumacher.html'
    ]

TeamZ = [
    'https://www.formula1.com/en/results.html/2022/drivers/CHALEC01/charles-leclerc.html',
    'https://www.formula1.com/en/results.html/2022/drivers/VALBOT01/valtteri-bottas.html',
    'https://www.formula1.com/en/results.html/2022/drivers/SERPER01/sergio-perez.html',
    'https://www.formula1.com/en/results.html/2022/drivers/PIEGAS01/pierre-gasly.html',
    'https://www.formula1.com/en/results.html/2022/drivers/FERALO01/fernando-alonso.html'
    ]

# for the love of god make this shit auto and it should be the race locatio in order
dates = ['20 Mar 2022', '27 Mar 2022', '10 Apr 2022', '24 Apr 2022', '08 May 2022', '22 May 2022', '29 May 2022', '12 Jun 2022',
         '19 Jun 2022', '03 Jul 2022', '10 Jul 2022', '24 Jul 2022', '31 Jul 2022', '28 Aug 2022', '04 Sep 2022', '11 Sep 2022',
         '02 Oct 2022', '09 Oct 2022', '23 Oct 2022', '30 Oct 2022', '13 Nov 2022', '20 Nov 2022',] 
racenames = ['Bahrain GP', 'Saudi Arabian GP', 'Australian GP', 'Emilia Romagna GP', 'Miami GP', 'Spanish GP', 'Monaco GP',
             'Azerbaijan GP', 'Canadian GP', 'British GP', 'Austrian GP', 'French GP', 'Hungarian GP', 'Belgian GP', 'Dutch GP',
             'Italian GP', 'Singapore GP', 'Japanese GP', 'United States GP', 'Mexican GP', 'Brazilian GP', 'Abu Dhabi GP',]
points = []

def getpointsanddates(team):
    points.clear()
    for drivers in team:
        r = requests.get(drivers).text
        soup = BeautifulSoup(r, 'html.parser')
        for data in soup.find_all("td", class_="dark bold"):
            points.append(data.get_text())
    return points

def getpoints(pointslist, date):
    lst = []
    indices = [i for i, x in enumerate(pointslist) if x == date]
    # print(indices)
    for indexs in indices:
        # print(pointslist[indexs])
        lst.append(pointslist[indexs+1])
    lst = [int(i) for i in lst]
    return(sum(lst))

def getracenames():
    numraces = (len(getpointsanddates(TeamM))/5)/2
    d = racenames[0:int(numraces)]
    return d

def cleanpoints(team):
    # while date is in the index range keep pluging it into getpoints()
    # data = [sum(1st race), sum(1st race plus 2nd race)]
    # take last value and add new value to get 
    getpointsanddates(team) 
    race1 = getpoints(points, '20 Mar 2022')
    race2 = getpoints(points, '27 Mar 2022')
    race3 = getpoints(points, '10 Apr 2022')
    race4 = getpoints(points, '24 Apr 2022')
    race5 = getpoints(points, '08 May 2022')
    race6 = getpoints(points, '22 May 2022')
    data = [race1, race1 + race2,
            race1 + race2 + race3,
            race1 + race2 + race3 + race4,
            race1 + race2 + race3 + race4 + race5,
            race1 + race2 + race3 + race4 + race5 + race6,
            ]
    return data

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment( loader = FileSystemLoader(templates_dir) )
    template = env.get_template('index.html')
    filename = os.path.join(root, 'html', 'index.html')
    with open(filename, 'w') as fh:
        fh.write(template.render(
            racenames = getracenames(),
            datam = cleanpoints(TeamM),
            datac = cleanpoints(TeamC),
            dataz = cleanpoints(TeamZ),
            ))

if __name__ == "__main__":
    main()

# list of possible dates then we have it divide the races by five to find x many races then it runs
# all the dates up to that index