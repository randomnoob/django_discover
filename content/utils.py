from bs4 import BeautifulSoup
import re

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



def insert_internal_links(html, linklist):
    """
    Insert internal links to html
    Preferably after the first paragraph, before the last one
    and somewhere in between
    linklist should be a NESTED LIST which follows this format : 
    [
        ['/abcxyz1', 'Title1'],
        ['/abcxyz2', 'Title2'],
    ]
    """
    try:
        # Find all the </p> tags
        ptags = [x for x in re.finditer("</p>", html)]
        # Get the first, last and middle positions
        # If the document is long, choose 3 positions, otherwise only 2
        if len(html) >= 6000:
            flm = [ptags[0], ptags[int(len(ptags)/2)], ptags[-2]]
        else:
            flm = [ptags[0], ptags[-2]]
        flm = list(set(flm))
        pos = [x.end(0) for x in flm]
        # For each position, add the href
        for index in pos:
            # Generate the html manually
            code = f'Xem thêm: <a href="{linklist[0][0]}">{linklist[0][1]}</a>'
            # Drop the element we've just inserted
            linklist = linklist[1:]
            html = html[:index] + code + html[index:]
    except:
        pass
    return html