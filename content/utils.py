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
        code = '<p>Xem thêm: <a href="{}">{}</a><p>'.format(*linklist[0])
        code2 = '<p>Xem thêm: <a href="{}">{}</a><p>'.format(*linklist[1])
        html_split.insert(1, code)
        html_split.insert(-3, code2)
        # If document is long >6000 chars, insert one more in the middle
        try:
            index = int(len(html_split)/2)-1
            code3 = '<p>Xem thêm: <a href="{}">{}</a><p>'.format(*linklist[2])
            html_split.insert(index, code3)
        except:
            traceback.print_exc()
            pass
        # Join shit together
        html_new = "".join(html_split)
        return html_new
    except:
        return html

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
            f_l_m = [ptags[0], ptags[int(len(ptags)/2)], ptags[-2]]
        else:
            f_l_m = [ptags[0], ptags[-2]]
        f_l_m = list(set(f_l_m))
        pos = [x.end(0) for x in f_l_m]
        # cut the strings into parts
        parts = [html[i:j] for i, j in zip([None] + pos, pos + [None])]
        # For each position, add the href
        for index in pos:
            # Generate the html manually
            code = f'<p>Xem thêm: <a href="{linklist[0][0]}">{linklist[0][1]}</a><p>'
            # Drop the element we've just inserted
            linklist = linklist[1:]
            html = html[:index] + code + html[index:]
    except:
        pass
    return html