from bs4 import BeautifulSoup

def generate_excerpt(html):
    try:
        soup = BeautifulSoup(html, 'lxml')
        text = soup.get_text().strip()
        try:
            sentence = text.split(".")[0]
            return sentence
        except:
            return text[:30]
    except:
        return ""
    

def remove_all_links(soup):
    try:
        hrefs = soup.find_all("a")
        for href in hrefs:
            href.replace_with(href.get_text().strip())
    except:
        pass
    return str(soup)