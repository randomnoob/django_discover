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
    
