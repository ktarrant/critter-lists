from bs4 import BeautifulSoup
import requests
import datetime

wiki_base_url = "https://animalcrossing.fandom.com"

fish_url = "/".join([wiki_base_url,
                     "wiki/Fish_(New_Horizons)"])

months_choices = []
for i in range(1,13):
    months_choices.append(datetime.date(2020, i, 1).strftime('%B'))


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

def generate_critter_rows(tab):
    for tr in tab.find_all("tr")[1:]:
        row = format_critter_row(tr)
        if row:
            yield row

def get_critter_list():
    print(fish_url)
    page = requests.get(fish_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.find("div", id="mw-content-text")
    return {tab['title']: list(generate_critter_rows(tab))
            for tab in content.find_all("div", {"class": "tabbertab"})}



if __name__ == "__main__":
    import pprint
    import json

    url_dicts = get_critter_list()
    pprint.pprint(url_dicts)
    with open("wiki_data.json", "w") as fobj:
        json.dump(url_dicts, fobj)
