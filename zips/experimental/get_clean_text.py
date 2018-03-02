import re, string
from bs4 import BeautifulSoup

def extract_text(html):
    soup = BeautifulSoup(html, "lxml")
    for crap in soup(["script", "style", "meta"]):
        crap.extract()
    return soup.get_text()

my_punctuation = ''.join([x for x in string.punctuation if x is not '.']) + string.digits

transdict = {ord(x): " " for x in my_punctuation}

def clean_text(dirty_case):
    depunctuated = dirty_case.translate(transdict)
    desentenced = re.sub('\.\s+', " ", depunctuated) # idea is to try to keep most abbreviation periods (often not followed by spaces, esp. in legal text) and ditch sentence periods
    # I'm also assuming there's no unicode punctuation other than section symbols, paragraph symbols, etc.
    desingled = " ".join([x for x in desentenced.split() if len(x) > 1])
    return re.sub('\s+', " ", desingled).lower()

def get_cleaned_text(opinion_from_courtlistener):
    if opinion_from_courtlistener["plain_text"]:
        text = opinion_from_courtlistener["plain_text"]
    elif opinion_from_courtlistener["html"]:
        text = extract_text(opinion_from_courtlistener["html"])
    elif opinion_from_courtlistener['html_lawbox']:
        text = extract_text(opinion_from_courtlistener["html_lawbox"])
    elif opinion_from_courtlistener['html_columbia']:
        text = extract_text(opinion_from_courtlistener["html_columbia"])
    elif opinion_from_courtlistener['html_with_citations']:
        text = extract_text(opinion_from_courtlistener["html_with_citations"])
    elif opinion_from_courtlistener['extracted_by_ocr']:
        text = opinion_from_courtlistener['extracted_by_ocr']
    else:
        text = ""
    return clean_text(text)
