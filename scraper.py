from bs4 import BeautifulSoup
from urllib2 import urlopen
from pprint import pformat, pprint
from random import randint
from functools import wraps
from commons import file_cache


BASE_URL = "http://www.laspilitas.com"


def throttle(func):
    @wraps(func)
    def throttle_func(*args, **kwargs):
        time.sleep(randint(2, 4))
        result = func(*args, **kwargs)
        return result
    return throttle_func


@file_cache('./plant_stubs.json')
def get_plant_stubs():
    print "getting plant stubs"
    url_tmpl = BASE_URL + "/nature-of-california/communities/yellow-pine-forest/plants?community_plants_page={index}"
    i = 1
    stubs = []
    while i < 20:
        url = url_tmpl.format(index=i)
        soup = make_soup(url)

        links = soup.find_all('div', class_="plantresourcelist")
        for link in links:
            link = link.find('p').find('a')
            latin = link.find('span', class_="i").string.strip()
            common = link.contents[-1].strip()
            href = link.attrs.get('href')
            plant = {"latin": latin,
                     "common": common,
                     "url": BASE_URL + href if href else ''}
            stubs.append(plant)
        next = soup.find('div', class_="page_window").find('a', class_="page_next")
        if not next:
            break
        else:
            i += 1
    return stubs


def get_plant_details(url):
    print "getting plant details"
    print url
    soup = make_soup(url)
    for br in soup.findAll('br'):
        br.extract()
    for a in soup.findAll('a'):
        a.extract()
    info = soup.find('div', class_="grid_12 alpha omega")
    ps = info.find_all('p')
    description = []
    short_description = info.find('div', class_="plant-description")

    for c in short_description.children:
        try:
            description.append(c.string.strip())
        except AttributeError:
            continue
    for p in ps:
        for c in p.children:
           try:
               description.append(c.string.strip())
           except AttributeError:
               continue

    description = " ".join(description)
    table = info.find_all('table')[-1]
    headers = [e.string for e in table.find_all('th')]
    data = [e.string for e in table.find_all('td')]
    data = [tuple(text.split(' to ')) for text in data]
    plant = dict(zip(headers, data))

    plant.update({
        "description": description,
    })

    return plant

@file_cache('./plants.json')
def get_all_plants():
    plant_stubs = get_plant_stubs()
    plants = []
    for plant in plant_stubs:
        try:
            details = get_plant_details(plant.get('url'))
            plant.update(details)
            pprint(plant)
            plants.append(plant)
        except Exception as e:
            print e.message
            continue
    return plants


@throttle
def make_soup(url):
    print "making soup (actually hitting URL)"
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")


if __name__ == "__main__":

    get_all_plants()
