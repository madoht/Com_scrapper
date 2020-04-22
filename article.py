import requests
from bs4 import BeautifulSoup


url = f"https://news.sbs.co.kr/news/newsSection.do?sectionType=02&plink=SNB&cooper=SBSNEWS"

def get_last_page():
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    pages = soup.find('div', {"class": "mdp_inner"}).find_all('a')
    last_page = pages[-8].get_text(strip = True)
    return int(last_page)

def get_arct_title(html):
    title = html.find('strong',{'class': 'sub'})
    if title:
        title_anchor = title.find('a')
        if title_anchor is not None:
            title = str(title_anchor.string)
        else:
            title = str(title.string)
        title = title.strip()
    else:
        title = None
    return{"title": title}

def extract_arct(last_page):
    arcts = []
    for page in range(last_page):
        print(f'Scrapping SBS: Page: {page}')
        result = requests.get(f"{url}&pg={page + 1}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("span", {'class': 'read'})
        for result in results:
            arct = get_arct_title(result)
            arcts.append(arct)
    return arcts

def get_arct():
    last_page = get_last_page()
    arcts = extract_arct(last_page)
    print(arcts)
    return arcts