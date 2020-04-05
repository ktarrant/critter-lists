from bs4 import BeautifulSoup
import requests
from urllib.request import urljoin

wiki_base_url = "https://animalcrossing.fandom.com"

critter_list_urls_source = "/".join(
    [wiki_base_url, "wiki/Guide:Monthly_critter_lists_(New_Horizons)"])


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

if __name__ == "__main__":
    import pprint

    url_dicts = get_critter_list_urls()
    pprint.pprint(url_dicts)