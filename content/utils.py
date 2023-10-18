from bs4 import BeautifulSoup
import re
import itertools
import traceback
from unidecode import unidecode
from django.template import defaultfilters

def slugify(text):
    # works wit  unicode
    return defaultfilters.slugify(unidecode(text))

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
    Insert internal links to html - BETTER VERSION
    Preferably after the first paragraph, before the last one
    and somewhere in between
    linklist should be a NESTED LIST which follows this format : 
    [
        ['/abcxyz1', 'Title1'],
        ['/abcxyz2', 'Title2'],
    ]
    """
    try:
        # Split the string by all the </p> tags
        # then add the </p> tags back
        html_split = [x+"</p>" for x in re.split("</p>", html)]
        # Insert after first paragraph and before last one
        try:
            _build_internal_links(linklist[0], html_split, 1)
            if len(html) <= 6000:
                _build_internal_links(linklist[1], html_split, -3)
            else:
                _build_internal_links(linklist[2], html_split, int(len(html_split)/2)-1)
        except:
            traceback.print_exc()
            pass
        # Join shit together
        html_new = "".join(html_split)
        return html_new
    except:
        return html

def _build_internal_links(linklist_element, html_split, index):
    """
    Build the internal link code
    insert it at index position
    in html_split list
    returns nothing
    """
    code = '<p>Xem thêm: <a href="{}">{}</a><p>'.format(*linklist_element)
    html_split.insert(index, code)

