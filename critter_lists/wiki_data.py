from bs4 import BeautifulSoup
import requests
import datetime
from urllib.request import urljoin

wiki_base_url = "https://animalcrossing.fandom.com"

critter_list_urls_source = "/".join(
    [wiki_base_url, "wiki/Guide:Monthly_critter_lists_(New_Horizons)"])

fish_url = "/".join([wiki_base_url,
                     "wiki/Fish_(New_Horizons)"])

months_choices = []
for i in range(1,13):
    months_choices.append(datetime.date(2020, i, 1).strftime('%B'))


def get_critter_list_urls():
    print(critter_list_urls_source)
    page = requests.get(critter_list_urls_source)
    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.find("div", id="mw-content-text")
    headers = [header.text.strip() for header in content.find_all("h2")]
    url_lists = [url_list for url_list in content.find_all("ul")]
    url_dicts = {header: {a['title']: a['href'] for a in url_list.find_all("a")}
                 for header, url_list in zip(headers, url_lists)}
    return url_dicts


def format_critter_row(row):
    d = dict()
    elements = row.find_all("td")
    if not elements:
        return None
    link = elements[0].find("a")
    d["name"] = link.text.strip()
    try:
        d["page"] = link['href']
    except KeyError:
        d["page"] = ""
    d["image"] = elements[1].find("a")['href']
    d["price"] = elements[2].text.strip()
    d["location"] = elements[3].text.strip()
    d["shadow_size"] = elements[4].text.strip()
    d["time"] = elements[5].text.strip()
    d["months"] = [month for month, td in zip(months_choices, elements[6:18])
                   if td.text.strip() != "-"]

    return d

def get_critter_list():
    print(fish_url)
    page = requests.get(fish_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.find("div", id="mw-content-text")
    return {tab['title']: [format_critter_row(tr) for tr in tab.find_all("tr")]
            for tab in content.find_all("div", {"class": "tabbertab"})}



if __name__ == "__main__":
    import pprint
    import json

    url_dicts = get_critter_list()
    pprint.pprint(url_dicts)
    with open("wiki_data.json", "w") as fobj:
        json.dump(url_dicts, fobj)